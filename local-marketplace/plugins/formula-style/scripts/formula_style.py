#!/usr/bin/env python3
"""Codex command hook: inject formula guidance, without rewriting output."""
import json
import sys

FORMULA_RULE = (
    "数学公式（含对话回复与写入 Markdown 文件）必须统一使用 LaTeX $ 格式，"
    "禁止用纯文本或 Unicode 字符代替公式。行内公式使用 $...$；"
    "定界符与外侧文字间保留空格，与内部公式之间不加空格。"
    "独立成段公式使用 $$，开头定界符、公式内容、结尾定界符各自单独成行。"
    "禁止使用 \\(...\\) 或 \\[...\\] 格式。"
)


def hook_result(event):
    name = event.get("hook_event_name")
    if name not in {"SessionStart", "UserPromptSubmit", "SubagentStart"}:
        return {}
    return {
        "hookSpecificOutput": {
            "hookEventName": name,
            "additionalContext": "<formula-style>\n" + FORMULA_RULE + "\n</formula-style>",
        }
    }


if __name__ == "__main__":
    try:
        result = hook_result(json.load(sys.stdin))
    except (ValueError, TypeError) as exc:
        print(json.dumps({"systemMessage": "formula-style hook input error: " + str(exc)}))
        raise SystemExit(1)
    print(json.dumps(result, ensure_ascii=False))
