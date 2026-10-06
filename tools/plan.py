#!/usr/bin/env python3
"""Read-only validator and task selector. Standard library; never executes tasks."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

ROLES = {'designer', 'engineer', 'reviewer', 'product'}
STATUSES = {'planned', 'in_progress', 'needs_review', 'done', 'blocked', 'deferred'}
ACTIVE = {'in_progress', 'needs_review', 'done'}
TASK_LISTS = {'depends_on': 0, 'gates': 0, 'requirements': 1, 'inputs': 1,
              'allowed_paths': 1, 'steps': 3, 'outputs': 1, 'checks': 2, 'stop_if': 1}


@dataclass
class Plan:
    root: Path
    tasks: list[dict[str, Any]] = field(default_factory=list)
    states: dict[str, Any] = field(default_factory=dict)
    gates: list[dict[str, Any]] = field(default_factory=list)
    requirements: list[dict[str, Any]] = field(default_factory=list)
    components: list[dict[str, Any]] = field(default_factory=list)
    screens: list[dict[str, Any]] = field(default_factory=list)
    tokens: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def local_path(root: Path, value: str) -> Path | None:
    """Reject absolute paths, parent traversal and symlink escapes."""
    if not value or Path(value).is_absolute() or '..' in Path(value).parts:
        return None
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def read_object(plan: Plan, path: str) -> dict[str, Any]:
    target = local_path(plan.root, path)
    if target is None or not target.is_file():
        plan.errors.append(f'missing/unsafe file: {path}')
        return {}
    try:
        data = json.loads(target.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        plan.errors.append(f'invalid JSON {path}: {exc}')
        return {}
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        plan.errors.append(f'object/schema_version=1 required: {path}')
        return {}
    return data


def records(plan: Plan, data: dict[str, Any], key: str, path: str) -> list[dict[str, Any]]:
    value = data.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(x, dict) for x in value):
        plan.errors.append(f'nonempty object list {key} required: {path}')
        return []
    return value


def load(root: Path) -> Plan:
    plan = Plan(root.resolve())
    manifest = read_object(plan, 'docs/tasks/queue.json')
    paths = manifest.get('task_files', [])
    if not isinstance(paths, list) or not paths or not all(isinstance(x, str) for x in paths):
        plan.errors.append('task_files must be a nonempty string list')
        paths = []
    if len(paths) != len(set(paths)):
        plan.errors.append('duplicate task_files')
    for path in paths:
        plan.tasks.extend(records(plan, read_object(plan, path), 'tasks', path))
    states = manifest.get('states')
    if not isinstance(states, dict):
        plan.errors.append('states must be an object')
    else:
        plan.states = states
    for attr, path, key in [
        ('gates', 'docs/gates.json', 'gates'),
        ('requirements', 'docs/requirements.json', 'requirements'),
        ('components', 'docs/design/components.json', 'components'),
        ('screens', 'docs/design/screens.json', 'screens'),
    ]:
        setattr(plan, attr, records(plan, read_object(plan, path), key, path))
    plan.tokens = read_object(plan, 'docs/design/tokens.json')
    return plan


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: Any, minimum: int = 0) -> bool:
    return isinstance(value, list) and len(value) >= minimum and all(text(v) for v in value)


def index_records(rows: list[dict[str, Any]], pattern: str, label: str,
                  errors: list[str]) -> dict[str, dict[str, Any]]:
    result = {}
    for row in rows:
        identifier = row.get('id')
        if not isinstance(identifier, str) or not re.fullmatch(pattern, identifier):
            errors.append(f'invalid {label} id: {identifier!r}')
            continue
        if identifier in result:
            errors.append(f'duplicate {label} id: {identifier}')
        result[identifier] = row
    return result


def valid_evidence(root: Path, value: Any) -> bool:
    if not text(value):
        return False
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if parsed.scheme in {'https', 'http'}:
        return bool(parsed.netloc) and not parsed.username and not parsed.password
    if parsed.scheme:
        return False
    path = local_path(root, unquote(parsed.path))
    return path is not None and path.is_file()


def evidence_errors(root: Path, evidence: Any, label: str, errors: list[str]) -> None:
    if not strings(evidence, 1):
        errors.append(f'{label}: nonempty evidence required')
    else:
        for item in evidence:
            if not valid_evidence(root, item):
                errors.append(f'{label}: missing/invalid evidence: {item}')


def state_of(plan: Plan, identifier: str) -> dict[str, Any]:
    value = plan.states.get(identifier, {})
    return value if isinstance(value, dict) else {}


def eligible(plan: Plan, task: dict[str, Any]) -> bool:
    gates = {g.get('id'): g for g in plan.gates}
    return (state_of(plan, task['id']).get('status') == 'planned'
            and all(state_of(plan, d).get('status') == 'done' for d in task['depends_on'])
            and all(gates[g].get('status') == 'passed' for g in task['gates']))


def find_cycle(tasks: dict[str, dict[str, Any]]) -> str | None:
    # Iterative DFS: malformed/deep user-edited queues cannot overflow recursion.
    color: dict[str, int] = {}
    for start in tasks:
        if color.get(start):
            continue
        stack = [(start, False)]
        while stack:
            node, exiting = stack.pop()
            if exiting:
                color[node] = 2
                continue
            if color.get(node) == 1:
                return node
            if color.get(node) == 2:
                continue
            color[node] = 1
            stack.append((node, True))
            deps = tasks[node].get('depends_on', [])
            if strings(deps):
                stack.extend((d, False) for d in reversed(deps) if d in tasks)
    return None


def contrast(a: str, b: str) -> float:
    def luminance(color: str) -> float:
        rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
        return sum(c * w for c, w in zip(lin, (0.2126, 0.7152, 0.0722)))
    x, y = sorted((luminance(a), luminance(b)))
    return (y + 0.05) / (x + 0.05)


def validate(plan: Plan) -> list[str]:
    errors = list(plan.errors)
    tasks = index_records(plan.tasks, r'KF-\d{3}', 'task', errors)
    gates = index_records(plan.gates, r'G-[A-Z][A-Z0-9-]*', 'gate', errors)
    reqs = index_records(plan.requirements, r'R\d{2}', 'requirement', errors)
    comps = index_records(plan.components, r'C\d{2}', 'component', errors)
    screens = index_records(plan.screens, r'S\d{2}', 'screen', errors)
    covered: set[str] = set()
    for rid, req in reqs.items():
        if not text(req.get('text')):
            errors.append(f'{rid}: requirement text missing')
    if set(plan.states) != set(tasks):
        errors.append('state/task IDs mismatch')
    for tid, task in tasks.items():
        for key in ('title', 'goal', 'phase'):
            if not text(task.get(key)):
                errors.append(f'{tid}: missing {key}')
        if not isinstance(task.get('role'), str) or task['role'] not in ROLES:
            errors.append(f'{tid}: unknown role')
        for key, count in TASK_LISTS.items():
            if not strings(task.get(key), count):
                errors.append(f'{tid}: invalid {key} list (minimum {count})')
        for key, registry in (('depends_on', tasks), ('gates', gates), ('requirements', reqs)):
            if strings(task.get(key)):
                if len(task[key]) != len(set(task[key])):
                    errors.append(f'{tid}: duplicate {key}')
                for ref in task[key]:
                    if ref not in registry:
                        errors.append(f'{tid}: unknown {key} reference {ref}')
        if strings(task.get('requirements')):
            covered.update(task['requirements'])
        if strings(task.get('inputs')):
            for value in task['inputs']:
                path = local_path(plan.root, value)
                if path is None or not path.is_file():
                    errors.append(f'{tid}: missing/unsafe input {value}')
        if strings(task.get('allowed_paths')):
            for value in task['allowed_paths']:
                if local_path(plan.root, value) is None:
                    errors.append(f'{tid}: unsafe allowed path {value}')
        if 'figma_pages' in task and not strings(task['figma_pages'], 1):
            errors.append(f'{tid}: invalid figma_pages')
        state = state_of(plan, tid)
        status = state.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'{tid}: unknown/missing status')
        if not isinstance(state.get('evidence'), list):
            errors.append(f'{tid}: evidence must be a list')
        if status == 'blocked' and not text(state.get('reason')):
            errors.append(f'{tid}: blocked needs reason')
        if isinstance(status, str) and status in ACTIVE:
            for dep in task.get('depends_on', []) if strings(task.get('depends_on')) else []:
                if state_of(plan, dep).get('status') != 'done':
                    errors.append(f'{tid}: dependency not done: {dep}')
            for gate in task.get('gates', []) if strings(task.get('gates')) else []:
                if gates.get(gate, {}).get('status') != 'passed':
                    errors.append(f'{tid}: gate not passed: {gate}')
        if isinstance(status, str) and status in {'needs_review', 'done'}:
            evidence_errors(plan.root, state.get('evidence'), tid, errors)
        if status == 'done' and not text(state.get('reviewed_by')):
            errors.append(f'{tid}: done needs independent reviewed_by')
    missing = set(reqs) - covered
    if missing:
        errors.append('uncovered requirements: ' + ', '.join(sorted(missing)))
    cycle = find_cycle(tasks)
    if cycle:
        errors.append(f'dependency cycle at {cycle}')
    for gid, gate in gates.items():
        if not isinstance(gate.get('status'), str) or gate['status'] not in {'pending', 'passed', 'revoked'}:
            errors.append(f'{gid}: invalid gate status')
        for key in ('owner', 'condition'):
            if not text(gate.get(key)):
                errors.append(f'{gid}: missing {key}')
        if gate.get('status') == 'passed':
            if not text(gate.get('approved_by')):
                errors.append(f'{gid}: passed gate needs approved_by')
            try:
                dt.datetime.fromisoformat(str(gate.get('approved_at')).replace('Z', '+00:00'))
            except ValueError:
                errors.append(f'{gid}: passed gate needs ISO approved_at')
            evidence_errors(plan.root, gate.get('evidence'), gid, errors)
    for cid, comp in comps.items():
        if not text(comp.get('name')):
            errors.append(f'{cid}: missing component name')
        for key in ('props', 'states', 'rules'):
            if not strings(comp.get(key), 1):
                errors.append(f'{cid}: invalid {key}')
    for sid, screen in screens.items():
        for key in ('name', 'route', 'goal', 'primary', 'data', 'acceptance'):
            if not text(screen.get(key)):
                errors.append(f'{sid}: missing {key}')
        for key in ('components', 'states', 'actions'):
            if not strings(screen.get(key), 1):
                errors.append(f'{sid}: invalid {key}')
        if strings(screen.get('components')):
            for cid in screen['components']:
                if cid not in comps:
                    errors.append(f'{sid}: unknown component {cid}')
    themes = plan.tokens.get('themes', {})
    if not isinstance(themes, dict) or not {'light', 'dark'} <= set(themes):
        errors.append('tokens: light/dark themes required')
    elif not all(isinstance(themes[x], dict) for x in ('light', 'dark')):
        errors.append('tokens: theme must be an object')
    elif set(themes['light']) != set(themes['dark']):
        errors.append('tokens: theme keys mismatch')
    else:
        for theme in ('light', 'dark'):
            colors = themes[theme]
            for key, value in colors.items():
                if not isinstance(value, str) or not re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
                    errors.append(f'tokens: invalid color {theme}/{key}')
            for fg, bg in [('text.primary', 'surface.canvas'), ('text.secondary', 'surface.canvas'),
                           ('action.onPrimary', 'action.primary')]:
                if fg not in colors or bg not in colors:
                    errors.append(f'tokens: missing contrast pair {theme}/{fg}/{bg}')
                elif all(isinstance(colors[k], str) and re.fullmatch(r'#[0-9A-Fa-f]{6}', colors[k]) for k in (fg, bg)):
                    if contrast(colors[fg], colors[bg]) < 4.5:
                        errors.append(f'tokens: contrast below 4.5 {theme}/{fg}/{bg}')
    return errors


def markdown_errors(root: Path) -> list[str]:
    errors = []
    paths = list(root.glob('*.md')) + list((root / 'docs').rglob('*.md'))
    for path in paths:
        try:
            source = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'unreadable markdown {path}: {exc}')
            continue
        source = re.sub(r'```.*?```', '', source, flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', source):
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f'markdown link escapes repository: {path.name} -> {target}')
                continue
            if not resolved.exists():
                errors.append(f'broken markdown link: {path.name} -> {target}')
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('validate')
    next_cmd = sub.add_parser('next')
    next_cmd.add_argument('--role', choices=sorted(ROLES))
    show_cmd = sub.add_parser('show')
    show_cmd.add_argument('task_id')
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    plan = load(root)
    errors = validate(plan) + markdown_errors(root)
    if errors:
        print(json.dumps({'ok': False, 'errors': errors}, ensure_ascii=False, indent=2))
        return 1
    if args.command == 'validate':
        print(json.dumps({'ok': True, 'tasks': len(plan.tasks), 'requirements': len(plan.requirements),
                          'screens': len(plan.screens), 'components': len(plan.components),
                          'gates': len(plan.gates), 'eligible': [t['id'] for t in plan.tasks if eligible(plan, t)],
                          'note': 'Structural checks only; not application, music, visual or approval verification.'},
                         ensure_ascii=False, indent=2))
        return 0
    if args.command == 'show':
        task = next((t for t in plan.tasks if t['id'] == args.task_id), None)
        if task is None:
            print(f'Unknown task: {args.task_id}', file=sys.stderr)
            return 2
        print(json.dumps({**task, 'execution_state': state_of(plan, task['id']),
                          'eligible': eligible(plan, task)}, ensure_ascii=False, indent=2))
        return 0
    active = [tid for tid, value in plan.states.items()
              if isinstance(value, dict) and value.get('status') in {'in_progress', 'needs_review'}]
    if active:
        print('Finish/review active work before selecting another task: ' + ', '.join(active))
        return 0
    task = next((t for t in plan.tasks if eligible(plan, t)
                 and (args.role is None or t['role'] == args.role)), None)
    if task is None:
        print('No eligible task. Inspect dependencies, review status and pending gates; do not bypass them.')
        return 0
    print(json.dumps({**task, 'execution_state': state_of(plan, task['id']),
                      'instruction': 'Read the inputs, execute one task, verify, hand off for independent review. Selection is read-only.'},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
