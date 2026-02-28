import Link from "next/link";
import { notFound } from "next/navigation";
import { getAllReports, getReportBySlug } from "@/lib/reports";
import { MarkdownContent } from "@/components/MarkdownContent";

type Params = {
  slug: string;
};

export function generateStaticParams() {
  const reports = getAllReports();
  return reports.map((report) => ({ slug: report.slug }));
}

export default async function ReportPage({ params }: { params: Promise<Params> }) {
  const resolvedParams = await params;
  const report = getReportBySlug(resolvedParams.slug);

  if (!report) {
    return notFound();
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <article className="mx-auto max-w-3xl px-4 pb-20 pt-8 sm:px-6 sm:pt-12">
        {/* 面包屑 + 返回 */}
        <nav className="mb-6">
          <Link
            href="/"
            className="text-[13px] font-medium text-muted transition-colors hover:text-accent"
          >
            ← All briefings
          </Link>
        </nav>

        {/* 文章头部：大标题 + 元信息，参考主流博客/新闻 */}
        <header className="mb-10 border-b border-border pb-8 sm:mb-12 sm:pb-10">
          <p className="mb-2 text-[11px] font-medium uppercase tracking-[0.2em] text-muted">
            {report.date}
          </p>
          <h1 className="text-3xl font-bold leading-tight tracking-tight text-foreground sm:text-4xl sm:leading-[1.15]">
            {report.title}
          </h1>
          <p className="mt-4 text-[15px] leading-relaxed text-muted">
            {report.description}
          </p>
        </header>

        {/* 正文 */}
        <div className="min-w-0">
          <MarkdownContent content={report.content} />
        </div>
      </article>
    </main>
  );
}
