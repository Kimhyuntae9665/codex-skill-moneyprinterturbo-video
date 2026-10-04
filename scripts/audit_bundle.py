"""Audit the distributable package without network access or engine installation."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from install_bundle import ROOT, verify_bundle


def audit(root: Path = ROOT) -> dict:
    errors = []
    count = verify_bundle(root)
    inventory = json.loads((root / 'distribution/source-inventory.json').read_text(encoding='utf-8'))
    all_names = {s['name'] for s in inventory['skills']}
    bundled = [s for s in inventory['skills'] if s['distribution'] == 'bundled']
    external = [s for s in inventory['skills'] if s['distribution'] == 'external']
    for skill in inventory['skills']:
        for dep in skill['dependencies']:
            if dep not in all_names:
                errors.append(f'Unresolved companion: {skill["name"]} -> {dep}')
        if skill['distribution'] == 'external':
            if not re.fullmatch('[0-9a-f]{40}', skill['commit']):
                errors.append('Unpinned external skill: ' + skill['name'])
            continue
        directory = root / skill['path']
        if not (directory / 'SKILL.md').is_file() or not (directory / 'LICENSE').is_file():
            errors.append('Missing entrypoint/license: ' + skill['name'])
        for source in skill['files']:
            if not (directory / source['path']).is_file():
                errors.append('Missing source file: ' + skill['name'] + '/' + source['path'])
    manifest = json.loads((root / 'distribution/file-manifest.json').read_text(encoding='utf-8'))
    paths = {f['path'] for f in manifest['files']}
    python_count = 0
    markdown_links = 0
    for rel in sorted(paths):
        file = root / rel
        if file.name in {'.env', 'config.toml'} or any(p in file.parts for p in ['.venv', '__pycache__', 'node_modules']) or file.suffix in {'.pyc', '.log', '.pem', '.key'}:
            errors.append('Private/runtime file in release: ' + rel)
        if file.suffix.lower() not in {'.md', '.py', '.ps1', '.yaml', '.yml', '.json', '.toml', '.txt', '.ts', '.js', '.html', '.svg', '.csv', '.srt', '.sh', '.jsx', '.ass', '.css', '.tsx', '.glsl', '.obj'}:
            continue
        text = file.read_text(encoding='utf-8')
        if re.search(r'C:[/\\]Users[/\\]user[/\\]|10[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', text, re.I):
            errors.append('Author-specific path/connection in release: ' + rel)
        if re.search(r'(?:ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}|sk-proj-[A-Za-z0-9_-]{40,}|hf_[A-Za-z0-9]{34,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)', text):
            errors.append('Possible credential in release: ' + rel)
        if file.suffix == '.py':
            try:
                ast.parse(text, filename=rel)
                python_count += 1
            except SyntaxError as error:
                errors.append(f'Python syntax: {rel}: {error}')
        if file.suffix == '.md':
            for raw in re.findall(r'\]\(([^\n)]+)\)', text):
                dest = raw.split(' "')[0].strip('<>')
                if re.match(r'^[a-z][a-z+.-]*:', dest, re.I) or dest.startswith('#'):
                    continue
                dest = unquote(dest.split('#')[0])
                if not dest:
                    continue
                markdown_links += 1
                if not (file.parent / dest).exists():
                    errors.append(f'Broken local Markdown link: {rel} -> {dest}')
    return {'status': 'pass' if not errors else 'fail', 'verified_files': count,
            'bundled_skills': len(bundled), 'external_skills': len(external),
            'python_sources_parsed': python_count, 'local_markdown_links_checked': markdown_links,
            'errors': errors}


if __name__ == '__main__':
    try:
        report = audit()
    except (ValueError, FileNotFoundError) as error:
        report = {'status': 'fail', 'errors': [str(error)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['status'] == 'pass' else 1)
