# Transitions.dev

- 来源：Jakub Antalik
- 网站：https://transitions.dev/
- Skill 安装页：https://transitions.dev/skill.html
- GitHub：https://github.com/Jakubantalik/transitions.dev
- 记录时间：2026-07-26

## 来源事实

- 站点定位是 web 应用常用 UI transition 的可交互菜谱集合（modal、dropdown、badge、tabs、skeleton 等）。
- 同一内容也打包成 agent skill（`npx skills add Jakubantalik/transitions.dev`），可装到 Claude Code / Codex / Cursor 等。
- 菜谱以 portable CSS 为主：`t-*` 命名空间、CSS custom properties，并带 `prefers-reduced-motion` 处理。
- 站点主价值是演示观感 + 复制 snippet；skill 只是把同一套内容塞进 agent，方便不打开浏览器时照抄。

## 本库判断（2026-07-26）

- 更适合当作「写动画时打开的参考站」，而不是全局常驻 agent skill。
- 不写入 dotfiles 的 public skill manifest；不需要跨机同步安装。
- 需要时直接打开官网；临时给 agent 用可 `npx skills add`，用完不必长期保留。
- 布局动画心智与性能模型见 wiki 内 FLIP 综合页，不在本站覆盖范围内。
