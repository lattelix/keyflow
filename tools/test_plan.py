"""Negative/positive tests of planning controls, NOT application tests."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import plan


class PlanningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'docs').mkdir()
        (self.root / 'docs/input.md').write_text('# Input\n', encoding='utf-8')
        (self.root / 'README.md').write_text('[Input](docs/input.md)\n', encoding='utf-8')
        tasks = []
        for num in range(1, 4):
            tasks.append({'id': f'KF-{num:03d}', 'title': f'Task {num}', 'goal': 'Bounded result',
                          'role': ('designer', 'engineer', 'reviewer')[num-1], 'phase': 'test',
                          'depends_on': [] if num == 1 else [f'KF-{num-1:03d}'],
                          'gates': [] if num == 1 else ['G-IMPLEMENT'],
                          'requirements': ['R01' if num == 1 else 'R02'], 'inputs': ['docs/input.md'],
                          'allowed_paths': ['docs/reports/**'], 'steps': ['Read', 'Change', 'Check'],
                          'outputs': ['Report'], 'checks': ['Output exists', 'Output matches'],
                          'stop_if': ['Approval missing']})
        self.write('docs/tasks/queue.json', {'schema_version': 1, 'task_files': ['docs/tasks/test.json'],
                   'states': {t['id']: {'status': 'planned', 'evidence': [], 'reviewed_by': None} for t in tasks}})
        self.write('docs/tasks/test.json', {'schema_version': 1, 'tasks': tasks})
        self.write('docs/gates.json', {'schema_version': 1, 'gates': [
            {'id': 'G-IMPLEMENT', 'status': 'pending', 'owner': 'product-owner', 'condition': 'Accept design',
             'approved_by': None, 'approved_at': None, 'evidence': []}]})
        self.write('docs/requirements.json', {'schema_version': 1, 'requirements': [
            {'id': 'R01', 'text': 'Start'}, {'id': 'R02', 'text': 'Learn'}]})
        self.write('docs/design/components.json', {'schema_version': 1, 'components': [
            {'id': 'C01', 'name': 'Button', 'props': ['label'], 'states': ['ready'], 'rules': ['Accessible']} ]})
        self.write('docs/design/screens.json', {'schema_version': 1, 'screens': [
            {'id': 'S01', 'name': 'Home', 'route': '/', 'goal': 'Start', 'primary': 'Learn', 'data': 'Local',
             'acceptance': 'No login', 'components': ['C01'], 'states': ['ready'], 'actions': ['Open']} ]})
        self.write('docs/design/tokens.json', {'schema_version': 1, 'themes': {
            'light': {'surface.canvas': '#FFFFFF', 'text.primary': '#000000', 'text.secondary': '#333333',
                      'action.primary': '#000000', 'action.onPrimary': '#FFFFFF'},
            'dark': {'surface.canvas': '#000000', 'text.primary': '#FFFFFF', 'text.secondary': '#DDDDDD',
                     'action.primary': '#FFFFFF', 'action.onPrimary': '#000000'}}})
        self.model = plan.load(self.root)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding='utf-8')

    def errors(self, expected):
        self.assertTrue(any(expected in e for e in plan.validate(self.model)), expected)

    def run_cli(self, args):
        out, err = io.StringIO(), io.StringIO()
        with patch.object(plan, '__file__', str(self.root / 'tools/plan.py')):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                status = plan.main(args)
        return status, out.getvalue(), err.getvalue()

    def test_valid_plan_and_first_eligible(self):
        self.assertEqual(plan.validate(self.model), [])
        self.assertEqual([t['id'] for t in self.model.tasks if plan.eligible(self.model, t)], ['KF-001'])

    def test_duplicate_task_id_rejected(self):
        self.model.tasks.append(copy.deepcopy(self.model.tasks[0]))
        self.errors('duplicate task id')

    def test_unknown_dependency_rejected(self):
        self.model.tasks[1]['depends_on'] = ['KF-999']
        self.errors('unknown depends_on')

    def test_cycle_rejected(self):
        self.model.tasks[0]['depends_on'] = ['KF-003']
        self.errors('dependency cycle')

    def test_self_cycle_rejected(self):
        self.model.tasks[0]['depends_on'] = ['KF-001']
        self.errors('dependency cycle')

    def test_missing_input_rejected(self):
        self.model.tasks[0]['inputs'] = ['docs/missing.md']
        self.errors('missing/unsafe input')

    def test_path_traversal_rejected(self):
        self.model.tasks[0]['allowed_paths'] = ['../../outside']
        self.errors('unsafe allowed path')

    def test_uncovered_requirement_rejected(self):
        self.model.requirements.append({'id': 'R03', 'text': 'Forgotten obligation'})
        self.errors('uncovered requirements')

    def test_unknown_requirement_rejected(self):
        self.model.tasks[0]['requirements'].append('R99')
        self.errors('unknown requirements')

    def test_unknown_gate_rejected(self):
        self.model.tasks[0]['gates'] = ['G-NOT-REAL']
        self.errors('unknown gates')

    def test_cannot_start_before_dependency_and_gate(self):
        self.model.states['KF-002']['status'] = 'in_progress'
        self.errors('dependency not done')
        self.errors('gate not passed')

    def test_done_requires_review_and_evidence(self):
        self.model.states['KF-001']['status'] = 'done'
        self.errors('nonempty evidence required')
        self.errors('done needs independent reviewed_by')

    def test_needs_review_requires_evidence(self):
        self.model.states['KF-001']['status'] = 'needs_review'
        self.errors('nonempty evidence required')

    def test_missing_evidence_file_rejected(self):
        self.model.states['KF-001'].update(status='done', reviewed_by='reviewer', evidence=['docs/no-file.md'])
        self.errors('missing/invalid evidence')

    def test_gate_cannot_be_passed_without_approval(self):
        self.model.gates[0]['status'] = 'passed'
        self.errors('needs approved_by')
        self.errors('needs ISO approved_at')
        self.errors('nonempty evidence required')

    def test_valid_review_and_gate_unlock_next(self):
        self.model.states['KF-001'].update(status='done', reviewed_by='reviewer', evidence=['docs/input.md'])
        self.model.gates[0].update(status='passed', approved_by='owner', approved_at='2026-10-06',
                                   evidence=['docs/input.md'])
        self.assertEqual(plan.validate(self.model), [])
        self.assertTrue(plan.eligible(self.model, self.model.tasks[1]))

    def test_blocked_needs_reason(self):
        self.model.states['KF-001']['status'] = 'blocked'
        self.errors('blocked needs reason')

    def test_state_registry_mismatch(self):
        self.model.states.pop('KF-003')
        self.errors('state/task IDs mismatch')

    def test_unknown_screen_component(self):
        self.model.screens[0]['components'] = ['C99']
        self.errors('unknown component')

    def test_theme_contract_mismatch(self):
        self.model.tokens['themes']['dark'].pop('text.primary')
        self.errors('theme keys mismatch')

    def test_invalid_color(self):
        self.model.tokens['themes']['light']['text.primary'] = 'purple-ish'
        self.errors('invalid color')

    def test_low_contrast(self):
        self.model.tokens['themes']['light']['text.primary'] = '#FFFFFF'
        self.errors('contrast below 4.5')

    def test_malformed_json_is_error_not_pass(self):
        (self.root / 'docs/tasks/queue.json').write_text('{', encoding='utf-8')
        self.assertTrue(plan.validate(plan.load(self.root)))
        self.assertEqual(self.run_cli(['validate'])[0], 1)

    def test_malformed_field_types_are_errors(self):
        self.model.tasks[0]['role'] = []
        self.model.states['KF-001']['status'] = []
        self.model.gates[0]['status'] = []
        self.errors('unknown role')
        self.errors('unknown/missing status')
        self.errors('invalid gate status')

    def test_markdown_link_checker(self):
        self.assertEqual(plan.markdown_errors(self.root), [])
        (self.root / 'README.md').write_text('[Missing](docs/missing.md)\n', encoding='utf-8')
        self.assertTrue(plan.markdown_errors(self.root))

    def test_evidence_protocol_safety(self):
        self.assertFalse(plan.valid_evidence(self.root, 'javascript:alert(1)'))
        self.assertFalse(plan.valid_evidence(self.root, 'https://user:secret@example.com'))
        self.assertFalse(plan.valid_evidence(self.root, 'http://[invalid'))
        self.assertTrue(plan.valid_evidence(self.root, 'https://example.com/review'))

    def test_cli_validate_and_show(self):
        status, output, _ = self.run_cli(['validate'])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output)['tasks'], 3)
        status, output, _ = self.run_cli(['show', 'KF-002'])
        self.assertEqual(status, 0)
        self.assertFalse(json.loads(output)['eligible'])
        self.assertEqual(self.run_cli(['show', 'KF-999'])[0], 2)

    def test_cli_next_role_and_read_only(self):
        def digest():
            return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        before = digest()
        status, output, _ = self.run_cli(['next'])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output)['id'], 'KF-001')
        self.assertIn('No eligible task', self.run_cli(['next', '--role', 'engineer'])[1])
        self.assertEqual(digest(), before)

    def test_active_task_prevents_selecting_new_work(self):
        path = self.root / 'docs/tasks/queue.json'
        data = json.loads(path.read_text())
        data['states']['KF-001']['status'] = 'in_progress'
        self.write('docs/tasks/queue.json', data)
        self.assertIn('Finish/review active work', self.run_cli(['next'])[1])


if __name__ == '__main__':
    unittest.main()
