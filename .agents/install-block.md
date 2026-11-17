# Install block

`INSTALL.md` is the canonical installation guide. Keep this compact copy aligned
with it for agents inspecting `.agents/`.

Install every skill globally into Codex and Claude Code:

```bash
npx skills@latest add sakohovaguimian/skillet --global --agent codex claude-code --skill '*' --yes
```

Update installed skills:

```bash
npx skills@latest update --global --yes
```
