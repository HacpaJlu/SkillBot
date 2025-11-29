#!/usr/bin/env python3
"""Build a code index (JSON + Markdown) for the repository.

Usage:
  python scripts/build_index.py [--root PATH] [--out-json PATH] [--out-md PATH]

Produces `code_index.json` and `CODE_INDEX.md` by default.
The index includes: module docstring, imports, top-level classes and functions
(with line numbers and docstrings), and top-level assignments (simple variables).
"""
import ast
import json
import os
import sys
from argparse import ArgumentParser


def is_simple_value(node):
    return isinstance(node, (ast.Constant, ast.List, ast.Tuple, ast.Dict, ast.Set))


def short(s, n=200):
    if not s:
        return None
    s = s.strip()
    # Ensure proper handling of Unicode characters (including Cyrillic)
    return s if len(s) <= n else s[: n - 1] + "…"


def get_params(func_node):
    """Return a list of parameter descriptors for a FunctionDef node."""
    params = []
    args = func_node.args
    # positional args
    for a in getattr(args, 'args', []):
        name = a.arg
        ann = None
        if hasattr(a, 'annotation') and a.annotation is not None:
            try:
                ann = ast.unparse(a.annotation)
            except Exception:
                ann = None
        params.append({'name': name, 'kind': 'arg', 'annotation': ann})
    # vararg
    if getattr(args, 'vararg', None):
        params.append({'name': args.vararg.arg, 'kind': 'vararg', 'annotation': None})
    # kwonly args
    for a in getattr(args, 'kwonlyargs', []):
        params.append({'name': a.arg, 'kind': 'kwonly', 'annotation': None})
    # kwarg
    if getattr(args, 'kwarg', None):
        params.append({'name': args.kwarg.arg, 'kind': 'kwarg', 'annotation': None})
    return params


def parse_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    try:
        tree = ast.parse(src, filename=path)
    except SyntaxError:
        return None

    module_doc = ast.get_docstring(tree)

    imports = []
    classes = []
    functions = []
    variables = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for n in node.names:
                imports.append(f"{mod}.{n.name}" if mod else n.name)
        elif isinstance(node, ast.ClassDef):
            # collect methods inside class
            methods = []
            for cnode in node.body:
                if isinstance(cnode, ast.FunctionDef):
                    methods.append({
                        'name': cnode.name,
                        'lineno': cnode.lineno,
                        'doc': short(ast.get_docstring(cnode)),
                        'params': get_params(cnode),
                    })
            classes.append({
                "name": node.name,
                "lineno": node.lineno,
                "doc": short(ast.get_docstring(node)),
                "methods": methods,
            })
        elif isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "doc": short(ast.get_docstring(node)),
                "params": get_params(node),
            })
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and is_simple_value(node.value):
                    variables.append({
                        "name": t.id,
                        "lineno": t.lineno if hasattr(t, 'lineno') else node.lineno,
                        "repr": type(node.value).__name__,
                    })

    return {
        "module_doc": short(module_doc),
        "imports": sorted(set(imports)),
        "classes": classes,
        "functions": functions,
        "variables": variables,
    }


def build_index(root):
    index = {"files": {}}
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root):
        # skip __pycache__ and .git and hidden folders
        dirnames[:] = [d for d in dirnames if d != '__pycache__' and not d.startswith('.')]
        for fname in filenames:
            if not fname.endswith('.py'):
                continue
            path = os.path.join(dirpath, fname)
            rel = os.path.relpath(path, root).replace('\\', '/')
            parsed = parse_file(path)
            if parsed is None:
                continue
            index['files'][rel] = {
                'relative_path': rel,
                'absolute_path': path,
                'module_doc': parsed['module_doc'],
                'imports': parsed['imports'],
                'classes': parsed['classes'],
                'functions': parsed['functions'],
                'variables': parsed['variables'],
            }
    return index


def make_markdown(index, root):
    lines = ["# Code Index", "", f"Repository root: `{os.path.abspath(root)}`", ""]
    lines.append("_Automatically generated. Click file links to open in VSCode._")
    lines.append("")
    for rel, info in sorted(index['files'].items()):
        lines.append(f"## `{rel}`")
        abs_path = info['absolute_path']
        # create a link to the top-most symbol (first class or function) if present
        anchor_line = None
        if info['classes']:
            anchor_line = info['classes'][0]['lineno']
        elif info['functions']:
            anchor_line = info['functions'][0]['lineno']
        else:
            anchor_line = 1
        uri = f"vscode://file/{abs_path}:{anchor_line}"
        lines.append(f"- Path: [{rel}]({uri})")
        if info['module_doc']:
            lines.append(f"- Doc: {info['module_doc']}")
        if info['imports']:
            lines.append(f"- Imports: `{', '.join(info['imports'])}`")
        if info['variables']:
            vars_str = ', '.join([f"{v['name']} (L{v['lineno']})" for v in info['variables']])
            lines.append(f"- Variables: {vars_str}")
        if info['classes']:
            lines.append(f"- Classes:")
            for c in info['classes']:
                uri_c = f"vscode://file/{abs_path}:{c['lineno']}"
                doc = f": {c['doc']}" if c.get('doc') else ""
                lines.append(f"  - [{c['name']} (L{c['lineno']})]({uri_c}){doc}")
        if info['functions']:
            lines.append(f"- Functions:")
            for f in info['functions']:
                uri_f = f"vscode://file/{abs_path}:{f['lineno']}"
                doc = f": {f['doc']}" if f.get('doc') else ""
                lines.append(f"  - [{f['name']} (L{f['lineno']})]({uri_f}){doc}")
        lines.append("")
    lines.append("---")
    lines.append("Generated by `scripts/build_index.py`.")
    return '\n'.join(lines)


def main(argv):
    p = ArgumentParser()
    p.add_argument('--root', default='.', help='Repository root to index')
    p.add_argument('--out-json', default='code_index.json')
    p.add_argument('--out-md', default='CODE_INDEX.md')
    args = p.parse_args(argv)

    idx = build_index(args.root)
    with open(args.out_json, 'w', encoding='utf-8') as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)

    md = make_markdown(idx, args.root)
    with open(args.out_md, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"Wrote {args.out_json} and {args.out_md}")


if __name__ == '__main__':
    main(sys.argv[1:])
