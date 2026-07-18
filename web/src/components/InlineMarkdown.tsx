"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Render a short markdown fragment inline (no wrapping <p>), so *italics*
 * and **bold** work inside resonance cards, key terms, etc.
 */
export function InlineMarkdown({
  children,
  className,
}: {
  children: string;
  className?: string;
}) {
  if (!children) return null;
  return (
    <span className={`inline-markdown ${className || ""}`.trim()}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children: c }) => <>{c}</>,
          // Avoid block elements leaking into titles / one-liners.
          ul: ({ children: c }) => <span className="block pl-4">{c}</span>,
          ol: ({ children: c }) => <span className="block pl-4">{c}</span>,
          li: ({ children: c }) => <span className="block">{c}</span>,
          a: ({ href, children: c }) => (
            <a href={href} className="underline decoration-amber-200/40 underline-offset-2">
              {c}
            </a>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </span>
  );
}
