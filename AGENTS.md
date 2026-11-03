# 全局工作规则

## 语言

* 默认使用中文进行分析、说明和回答。除非用户明确要求，不要切换为其他语言。
* 代码、命令、变量名、函数名、库名和专业术语可保留英文。

## 命令与工具缺失

* 系统级工具缺失（如需 `sudo` / `apt` 安装的 Bash 命令或工具）：优先告知并请用户下载安装，给出完整安装命令供用户执行，不要擅自通过 Python 等其他工具强行绕过。
* 项目级 / 非 `sudo` 环境可自行安装（如 `pip`、`uv`、`conda`、`julia Pkg`、`npm`、`cargo` 等用户空间包管理）：可在项目环境内自行安装，无需等待用户操作。

## Bash 命令组织

* 只读检查与文件修改、Git 暂存、清理操作分开调用；不要把无关步骤拼成长命令。临时文件同样遵循回收站规则，不得为减少确认而绕过审批。

## 技能调用

* 需要找论文、补参考文献、给任务配文献时，使用 `zotero-paper-hunter` skill（websearch 发现候选，arXiv/出版商页核实元数据，全经 Zotero MCP 去重入库到主题 `paper/inbox`）。
* 需要找书、教材、讲义入库时，使用 `zotero-book-hunter` skill（先查 ISBN 再入库）。
* 只在库内检索已有文献时，用 Zotero 语义搜索，不走 hunter。

## MCP 工具调用

* 已加载的 MCP 工具直接调用；未暴露的先通过 Codex 提供的工具发现机制查找。不改配置、不杀进程、不绕过 MCP 直读库。

## 文件删除与移动

* 删除文件或目录一律用 `mv` 移到回收站，不论是否由 Git 管理，临时文件也不例外；禁止直接使用 `rm` 或 `git rm`，并避免覆盖回收站中的同名内容。
* 非删除用途的项目内移动、重命名仍优先用 `git mv`。

## 长任务工具绕行（T3 harness 已知问题，未修复前有效）

* 单次 `exec_command` 约 10 秒即返回并清理原进程组，前台长任务活不到结束；`sleep` 也会受影响，与 CPU 无关。
* `exec_command` 超时后返回 `session_id`（如 `83987`）属正常 `Unified Exec` 行为，但 `write_stdin` 把整数传成浮点（如 `83987.0`），报 `expected i32`，会话不可续接。`yield_time_ms` 只是让出控制权，不是最大执行时间，不与 `timeout_ms` 混用。
* 未修复前，超 10 秒任务一律用 `setsid nohup … &` 落盘后台跑，每轮只做小于 10 秒的 `tail/ps` 轮询；同时落盘退出码。示例：`setsid nohup python -u scripts/verify_exp06.py > /tmp/verify_fix.log 2>&1 < /dev/null &`，之后 `tail -n 20 /tmp/verify_fix.log` 轮询。
* 上游修复整数续接后取消本绕行，不把 `setsid` 当通用最终方案。
