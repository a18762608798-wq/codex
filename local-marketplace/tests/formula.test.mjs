import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const script = fileURLToPath(new URL('../plugins/formula-style/scripts/formula_style.py', import.meta.url));
for (const event of ['SessionStart', 'UserPromptSubmit', 'SubagentStart']) {
  test('formula hook injects developer context for ' + event, () => {
    const result = spawnSync('/usr/bin/python3', [script], {
      input: JSON.stringify({ hook_event_name: event, source: 'compact', prompt: 'test' }),
      encoding: 'utf8',
    });
    assert.equal(result.status, 0, result.stderr);
    const output = JSON.parse(result.stdout).hookSpecificOutput;
    assert.equal(output.hookEventName, event);
    assert.ok(output.additionalContext.includes('<formula-style>'));
    assert.ok(output.additionalContext.includes('写入 Markdown 文件'));
    assert.ok(output.additionalContext.includes('各自单独成行'));
  });
}

test('formula hook does not rewrite tool input or assistant output', () => {
  const result = spawnSync('/usr/bin/python3', [script], {
    input: JSON.stringify({ hook_event_name: 'PreToolUse', tool_input: { command: 'unchanged' } }),
    encoding: 'utf8',
  });
  assert.equal(result.status, 0);
  assert.deepEqual(JSON.parse(result.stdout), {});
});
