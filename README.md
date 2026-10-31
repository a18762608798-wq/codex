# Codex 配置

本仓库保存 `~/.codex/` 中可复用的配置与自维护插件源码：

- `AGENTS.md`：全局工作规则，与 Pi 基本对齐。
- `config.toml`：Codex、MCP 与插件配置；凭证通过环境变量或本机登录提供。
- `local-marketplace/`：全局公式插件及测试，安装说明见其 README。
- `skills/`、`rules/`、`prompts/`、`hooks/`：按需维护的自定义资源。

`.gitignore` 使用顶层白名单；登录凭证、会话记录、数据库、日志、缓存、下载包、
系统内置 skills 和 CCGUI 自动生成的 skill 均不入库。

换机器时需重新登录 Codex、提供 MCP 所需环境变量，并检查配置中的绝对路径。
插件 hooks 的信任应在本机 `/hooks` 中审核，不以仓库中的配置替代审核。

Spec Kit 返工插件源码位于 `~/.agents/sdd/specify/plugins/speckit-rework/`，
按项目手动安装，不作为本仓库的全局插件维护。
