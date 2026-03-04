# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Installed Skills

### summarize 🧾
- **路径**: `~/.local/bin/summarize`
- **版本**: 0.11.1
- **用途**: 总结网页、PDF、YouTube 视频
- **用法**:
  ```bash
  summarize "https://example.com"
  summarize "/path/to/file.pdf"
  summarize "https://youtu.be/xxx" --youtube auto
  ```

### GitHub 🐙
- **状态**: 内置技能
- **所需**: `gh` CLI (GitHub CLI)
- **手动安装**:
  ```bash
  # 方法1: Homebrew (推荐)
  brew install gh
  # 方法2: 官网下载 https://github.com/cli/cli/releases
  ```
- **认证**: `gh auth login`
- **用途**: 查 Issue、提 PR、代码审计

### Notion 📝
- **状态**: 内置技能
- **所需**: Notion API Key
- **配置步骤**:
  1. 访问 https://notion.so/my-integrations 创建集成
  2. 复制 API key (以 `ntn_` 或 `secret_` 开头)
  3. 存储 key: `mkdir -p ~/.config/notion && echo "ntn_your_key" > ~/.config/notion/api_key`
  4. 在 Notion 中分享页面给集成
- **用途**: 自动整理笔记，同步数据库

### Obsidian 💎
- **状态**: 内置技能
- **所需**: `obsidian-cli`
- **手动安装**:
  ```bash
  # 方法1: Homebrew
  brew install yakitrak/yakitrak/obsidian-cli
  # 方法2: 官网下载 https://github.com/yakitrak/obsidian-cli/releases
  ```
- **用途**: 读写本地库，构建第二大脑

### Gmail 📧
- **状态**: ✅ 已安装
- **路径**: `~/.local/lib/node_modules/@mcinteerj/openclaw-gmail`
- **所需**: Gmail OAuth 认证
- **配置**: 运行 `gh auth login` 并配置 Google API 凭据
- **用途**: 自动写邮件、归档、总结收件箱

### Calendar 📅
- **状态**: ✅ 已安装 (Apple Calendar)
- **路径**: `~/.local/lib/node_modules/openclaw-apple-calendar`
- **所需**: macOS Calendar 权限
- **用途**: 读取和管理日历事件

### Obsidian 💎
- **状态**: ✅ 已安装
- **路径**: `~/.local/bin/obsidian-cli`
- **版本**: v0.3.1
- **用途**: 读写本地库，构建第二大脑
- **用法**:
  ```bash
  obsidian-cli print-default --path-only  # 查看默认 Vault
  obsidian-cli list-notes                 # 列出笔记
  obsidian-cli create-note "标题"          # 创建笔记
  ```

---

## 配置指南

### GitHub 认证
```bash
gh auth login
# 按提示完成浏览器认证
```

### Gmail 认证
需配置 Google OAuth 2.0:
1. 访问 https://console.cloud.google.com
2. 创建项目并启用 Gmail API
3. 创建 OAuth 2.0 凭据
4. 下载 `credentials.json`

### Apple Calendar 权限
首次使用时会自动请求日历访问权限，请点击"允许"。

---

Add whatever helps you do your job. This is your cheat sheet。
