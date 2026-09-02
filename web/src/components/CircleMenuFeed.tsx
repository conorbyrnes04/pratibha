"use client";

import Link from "next/link";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { SanghaBoundary } from "@/components/SanghaBoundary";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { CIRCLE_OPENINGS } from "@/lib/circleOpenings";
import { excerptReading } from "@/lib/circleVerses";
import { useT } from "@/components/LocaleProvider";

export function CircleMenuFeed({ active }: { active: boolean }) {
  if (!CONVEX_ENABLED) return null;
  return (
    <SanghaBoundary>
      <CircleMenuFeedInner active={active} />
    </SanghaBoundary>
  );
}

function CircleMenuFeedInner({ active }: { active: boolean }) {
  const t = useT();
  const recent = useQuery(api.studentCommentaries.listRecent, active ? { limit: 3 } : "skip");
  const rows = recent && recent.length > 0 ? recent.slice(0, 2) : null;
  const opening = !rows ? CIRCLE_OPENINGS[0] : null;

  return (
    <div className="nav-more__circle">
      <p className="nav-more__label">{t("circle.title")}</p>
      {rows
        ? rows.map((reading) => (
            <Link key={reading._id} href={`/circle/${reading._id}`} role="menuitem" className="nav-more__post">
              <span className="nav-more__post-title">{reading.verseTitle}</span>
              <span className="nav-more__post-body">{excerptReading(reading.body, 90)}</span>
              <span className="nav-more__post-meta">
                {reading.replyCount === 1
                  ? t("circle.replyOne")
                  : reading.replyCount > 0
                    ? t("circle.replies", { count: reading.replyCount })
                    : t("circle.noReplies")}
              </span>
            </Link>
          ))
        : opening ? (
            <Link href={`/read/${encodeURIComponent(opening.id)}#circle`} role="menuitem" className="nav-more__post">
              <span className="nav-more__post-title">{opening.label}</span>
              <span className="nav-more__post-body">{excerptReading(opening.body, 90)}</span>
              <span className="nav-more__post-meta">{t("circle.houseOpening")}</span>
            </Link>
          ) : (
            <p className="nav-more__post-body">{t("circle.emptyFeed")}</p>
          )}
      <Link href="/circle" role="menuitem" className="nav-more__item">
        {t("circle.backToCircle")}
      </Link>
    </div>
  );
}
