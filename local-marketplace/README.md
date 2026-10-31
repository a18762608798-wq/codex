# 全局 Codex 公式插件

本 marketplace 名称为 `dell-local`，现在只维护全局 `formula-style` 插件。

## 生效

```bash
codex plugin marketplace add ~/.codex/local-marketplace
codex plugin add formula-style@dell-local
```

重新打开 Codex，在 `/hooks` 中审核信任该插件的三个 hooks。安装或 enabled=true 不等于
已授予信任；未审核时 hooks 会被跳过。不使用危险的 hook-trust bypass 代替审核。

公式规则通过 SessionStart（包括 resume/compact/fork）、UserPromptSubmit 和
SubagentStart 注入，覆盖回复和写入 Markdown。与原 Pi 扩展一样，这是提示词注入，
不是事后公式校验或自动改写器。脚本只使用 Python 标准库，不访问网络或文献库。

## 测试

```bash
node --test ~/.codex/local-marketplace/tests/formula.test.mjs
python3 ~/.codex/local-marketplace/tests/validate_installed.py
```

原生发现检查不发送模型 turn、不授予 hook 信任。脚本使用的 Codex app-server 日志若
报告 Linux user namespace 权限受限，应单独处理沙箱环境，不以关闭沙箱绕过。

## Spec Kit 返工插件已迁出

三种宿主的返工插件统一存放在：

`~/.agents/sdd/specify/plugins/speckit-rework/`

请按该目录 README 在 Spec Kit 初始化后手动安装到项目。旧的
`speckit-rework@dell-local` 已从此 marketplace 和全局安装中移除。
Codex 新 catalog 名为 `sdd-local`：包可以使用共享缓存，但用户级关闭、项目级开启；
不要再次把返工插件加入这个全局公式 marketplace。
