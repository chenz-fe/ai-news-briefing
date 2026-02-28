import Link from "next/link";
import { getAllReports } from "@/lib/reports";

export default function Home() {
  const reports = getAllReports();
  const latest = reports[0];
  const earlier = reports.slice(1);

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-3xl px-4 pb-20 pt-8 sm:px-6 sm:pt-12">
        {/* Hero：最新一期，大标题 + 元信息 + CTA，参考 The Verge / Substack */}
        {latest && (
          <article className="mb-16 sm:mb-20">
            <Link
              href={`/reports/${latest.slug}`}
              className="group block outline-none"
            >
              <p className="mb-2 text-[11px] font-medium uppercase tracking-[0.2em] text-muted">
                Latest · {latest.date}
              </p>
              <h1 className="mb-3 text-3xl font-bold leading-tight tracking-tight text-foreground transition-colors group-hover:text-accent sm:text-4xl sm:leading-[1.15]">
                {latest.title}
              </h1>
              <p className="max-w-xl text-[15px] leading-relaxed text-muted">
                {latest.description}
              </p>
              <p className="mt-4 inline-flex items-center gap-1.5 text-[13px] font-medium text-accent">
                Read the briefing
                <span className="transition-transform group-hover:translate-x-0.5" aria-hidden>→</span>
              </p>
            </Link>
          </article>
        )}

        {/* 归档：简洁列表，标题 + 日期，行 hover */}
        <section>
          <h2 className="mb-4 text-[11px] font-medium uppercase tracking-[0.2em] text-muted">
            Earlier briefings
          </h2>
          <ul className="border-t border-border">
            {earlier.length === 0 && !latest && (
              <li className="border-b border-border py-6 text-sm text-muted">
                No briefings yet.
              </li>
            )}
            {earlier.map((report) => (
              <li key={report.slug} className="border-b border-border">
                <Link
                  href={`/reports/${report.slug}`}
                  className="article-list-item flex items-baseline justify-between gap-4 py-4 text-left outline-none hover:bg-surface/80 sm:py-5"
                >
                  <span className="min-w-0 flex-1 text-[15px] font-semibold text-foreground sm:text-base">
                    {report.title}
                  </span>
                  <time className="shrink-0 text-[12px] text-muted" dateTime={report.date}>
                    {report.date}
                  </time>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  );
}
