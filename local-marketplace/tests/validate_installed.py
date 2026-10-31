"""Check the remaining global formula plugin; no model turn or trust bypass."""
from pathlib import Path

from codex_rpc import CodexRPC

marketplace = str(Path.home() / ".codex/local-marketplace/.agents/plugins/marketplace.json")
with CodexRPC() as rpc:
    plugin = rpc.request("plugin/read", {"marketplacePath": marketplace, "pluginName": "formula-style"})["plugin"]
    assert plugin["summary"]["installed"] and plugin["summary"]["enabled"]
    assert len(plugin["hooks"]) == 3
    thread = rpc.request("thread/start", {"cwd": "/tmp", "ephemeral": True})["thread"]
    entries = rpc.request("hooks/list", {"threadId": thread["id"]})["data"]
    hooks = [hook for entry in entries for hook in entry["hooks"]]
    formula = [hook for hook in hooks if hook.get("pluginId") == "formula-style@dell-local"]
    assert len(formula) == 3
    assert not any("speckit-rework" in (hook.get("pluginId") or "") for hook in hooks)
    servers = rpc.request("mcpServerStatus/list", {"threadId": thread["id"], "limit": 30, "detail": "toolsAndAuthOnly"})["data"]
    assert not any(server["name"] == "speckit_rework" for server in servers)
    print("PASS: global formula plugin present; no global rework hooks or MCP")
    for hook in formula:
        print("Formula hook:", hook["eventName"], "trust=" + hook["trustStatus"])
    print("No model turn, hook trust grant, project write or Zotero write performed.")
