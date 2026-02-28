'use client';

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Props = {
  content: string;
};

type LinkProps = {
  href?: string;
  children?: React.ReactNode;
};

function getLinkText(children: React.ReactNode): string {
  if (typeof children === "string") return children.trim();
  if (Array.isArray(children)) return children.map(getLinkText).join("").trim();
  return "";
}

const ExternalLinkIcon = () => (
  <svg
    className="inline-block h-4 w-4 shrink-0 align-middle text-accent"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden
  >
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);

function MarkdownLink({ href, children }: LinkProps) {
  const [copied, setCopied] = useState(false);
  const isSourceLink = getLinkText(children) === "原文链接";

  if (!href) {
    return <span>{children}</span>;
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.open(href, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <span className="inline-flex flex-wrap items-center gap-1 break-all">
      {/* 桌面端：原文链接只显示图标，其他链接显示文字 */}
      <a
        href={href}
        target="_blank"
        rel="noreferrer"
        className="hidden md:inline-flex items-center gap-1 text-accent hover:opacity-90"
        title={href}
      >
        {isSourceLink ? <ExternalLinkIcon /> : children}
      </a>

      {/* 移动端：原文链接为图标+复制，其他为复制按钮 */}
      {isSourceLink ? (
        <button
          type="button"
          className="inline-flex items-center gap-1 rounded border border-border px-2 py-0.5 text-accent md:hidden"
          onClick={handleCopy}
          title="复制链接"
        >
          <ExternalLinkIcon />
          <span className="text-[12px]">{copied ? "已复制" : "复制"}</span>
        </button>
      ) : (
        <a
          href={href}
          target="_blank"
          rel="noreferrer"
          className="md:hidden text-accent text-[12px]"
        >
          {children}
        </a>
      )}
    </span>
  );
}

export function MarkdownContent({ content }: Props) {
  return (
    <article className="prose mx-auto max-w-3xl">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ node, ...props }) => (
            <MarkdownLink href={props.href}>{props.children}</MarkdownLink>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </article>
  );
}

