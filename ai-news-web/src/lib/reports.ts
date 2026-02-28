import fs from "fs";
import path from "path";
import matter from "gray-matter";

export type ReportMeta = {
  slug: string;
  title: string;
  date: string;
  description: string;
};

/** gray-matter 可能把 date 解析成 Date 对象，统一转为 YYYY-MM-DD 字符串 */
function normalizeDate(value: unknown): string {
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  if (typeof value === "string") return value;
  return "";
}

export type Report = ReportMeta & {
  content: string;
};

/** 去掉详情正文里的冗余标题行（旧版 prompt 生成的重复文案） */
export function cleanReportContent(content: string): string {
  if (!content || typeof content !== "string") return content;
  const lines = content.split("\n");
  const out: string[] = [];
  for (const line of lines) {
    const t = line.trim();
    if (
      /^(\*\*)?AI\s*简报[：:].*最值得关注的进展\s*(\*\*)?$/i.test(t) ||
      /^(\*\*)?今日\s*AI\s*简报\s*[（(][^）)]+[）)]\s*(\*\*)?$/i.test(t)
    ) {
      continue;
    }
    out.push(line);
  }
  return out.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

// 部署时（如 Vercel）从 ai-news-web/content/reports 读取；本地可回退到 ../ai-news-agent/daily_reports
function getReportsDir(): string {
  const inApp = path.join(process.cwd(), "content", "reports");
  const agentDir = path.join(process.cwd(), "..", "ai-news-agent", "daily_reports");
  if (fs.existsSync(inApp)) return inApp;
  return agentDir;
}

function readAllMarkdownFiles() {
  const dir = getReportsDir();
  if (!fs.existsSync(dir)) {
    return [];
  }

  const files = fs
    .readdirSync(dir)
    .filter((file) => file.toLowerCase().endsWith(".md"));

  return files.map((filename) => {
    const fullPath = path.join(dir, filename);
    const fileContents = fs.readFileSync(fullPath, "utf8");
    const parsed = matter(fileContents);
    return {
      filename,
      ...parsed,
    };
  });
}

export function getAllReports(): ReportMeta[] {
  const items = readAllMarkdownFiles();

  const reports: ReportMeta[] = items.map(({ filename, data }) => {
    const frontmatter = data as Partial<ReportMeta>;
    const fallbackSlug = filename.replace(/_AINews\.md$/i, "").trim();

    return {
      slug: frontmatter.slug || fallbackSlug,
      title: frontmatter.title || fallbackSlug,
      date: normalizeDate(frontmatter.date) || fallbackSlug,
      description:
        frontmatter.description ||
        "今日 AI 领域的最新产品、模型进展与大事件简报。",
    };
  });

  // 按日期倒序排序（最新在前）；如果没有合法日期，就保持原顺序
  return reports.sort((a, b) => {
    if (!a.date || !b.date) return 0;
    return a.date > b.date ? -1 : 1;
  });
}

export function getReportBySlug(slug: string): Report | null {
  const items = readAllMarkdownFiles();
  const match = items.find(({ filename, data }) => {
    const fm = data as Partial<ReportMeta>;
    if (fm.slug === slug) return true;

    const fromName = filename.replace(/_AINews\.md$/i, "").trim();
    return fromName === slug;
  });

  if (!match) return null;

  const fm = match.data as Partial<ReportMeta>;

  return {
    slug: fm.slug || slug,
    title: fm.title || slug,
    date: normalizeDate(fm.date) || slug,
    description:
      fm.description ||
      "今日 AI 领域的最新产品、模型进展与大事件简报。",
    content: cleanReportContent(match.content),
  };
}

