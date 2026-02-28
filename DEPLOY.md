# 今日 AI 简报 - 部署说明

## 架构概览

- **前端**：Next.js（ai-news-web），部署到 Vercel，从 `ai-news-web/content/reports` 读取 Markdown 简报（SSG）。
- **数据**：Python Agent（ai-news-agent）生成简报到 `daily_reports/`，由 GitHub Actions 同步到 `ai-news-web/content/reports` 并提交。
- **自动化**：GitHub Actions 每日定时运行 Agent → 同步 MD → 推送 → Vercel 自动重新构建发布。

---

## 一、部署前端到 Vercel

### 1. 连接仓库

1. 打开 [vercel.com](https://vercel.com)，用 GitHub 登录。
2. 点击 **Add New → Project**，选择本项目的 **Git 仓库**（需先推送到 GitHub）。

### 2. 配置项目

- **Framework Preset**：Next.js（自动识别）
- **Root Directory**：点击 **Edit**，填 `ai-news-web`（只部署前端目录）
- **Build Command**：`npm run build`（默认）
- **Output Directory**：默认（.next）
- **Install Command**：`npm install`（默认）

### 3. 部署

点击 **Deploy**。构建完成后会得到一个 `*.vercel.app` 的地址。

### 4. 自定义域名（可选）

在 Vercel 项目 **Settings → Domains** 里添加自己的域名并按提示解析。

---

## 二、配置 GitHub Actions（每日自动生成简报）

### 1. 添加仓库 Secrets

在 GitHub 仓库页面：**Settings → Secrets and variables → Actions**，新增：

| Name           | 说明           | 示例 |
|----------------|----------------|------|
| `LLM_API_KEY`  | 大模型 API Key | 你的 DeepSeek/OpenAI Key |
| `LLM_BASE_URL` | API 地址（可选） | `https://api.deepseek.com` |
| `LLM_MODEL`    | 模型名（可选）   | `deepseek-chat` |

若使用 DeepSeek，一般只需填 `LLM_API_KEY`，其余有默认值。

### 2. 确认工作流文件

仓库根目录下应有 `.github/workflows/ai-news-daily.yml`，内容为：

- 定时：每天 UTC 0 点（约北京时间 8 点）运行。
- 手动：在 **Actions** 页选择 “Daily AI News Briefing” → **Run workflow**。

### 3. 运行一次

在 **Actions** 里手动跑一次 “Daily AI News Briefing”，确认：

- 能成功拉取新闻并调用大模型；
- 会生成/更新 `ai-news-agent/daily_reports/*.md`；
- 会同步到 `ai-news-web/content/reports/` 并 **commit + push**。

推送后 Vercel 会自动用最新内容重新构建、发布网站。

---

## 三、本地与线上数据说明

- **本地开发**：若未建 `ai-news-web/content/reports` 或目录为空，前端会回退到读取 `../ai-news-agent/daily_reports`，方便本地跑 Agent 后直接看效果。
- **线上（Vercel）**：只读 `ai-news-web/content/reports`。该目录下的 `.md` 由 GitHub Actions 从 `ai-news-agent/daily_reports` 同步并提交，无需在 Vercel 里配置 Python 或 Agent。

---

## 四、常见问题

**Q：首次部署后首页没有简报？**  
A：确保 `ai-news-web/content/reports` 下已有至少一个 `.md` 文件并已提交。仓库里已带一份示例，若没有可先手动复制：  
`cp ai-news-agent/daily_reports/*.md ai-news-web/content/reports/` 再提交。

**Q：Actions 报错 “LLM_API_KEY” 相关？**  
A：在仓库 Settings → Secrets and variables → Actions 中检查是否已添加 `LLM_API_KEY` 等并保存。

**Q：想改每天跑的时间？**  
A：编辑 `.github/workflows/ai-news-daily.yml` 里的 `cron`。例如北京时间早上 9 点：`cron: "0 1 * * *"`（UTC 1:00）。

**Q：Vercel 构建失败？**  
A：确认 Root Directory 为 `ai-news-web`，且该目录下有 `package.json` 和 `content/reports`（可先只有 `.gitkeep` 或若干 `.md`）。
