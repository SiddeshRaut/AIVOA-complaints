import type { PropsWithChildren } from "react";
import clsx from "clsx";

type Tone = "amber" | "green" | "blue" | "red" | "slate";

const toneClasses: Record<Tone, string> = {
  amber: "bg-amber-50 text-amber-700 border-amber-200",
  green: "bg-emerald-50 text-emerald-700 border-emerald-200",
  blue: "bg-brand-50 text-brand-700 border-blue-200",
  red: "bg-red-50 text-red-700 border-red-200",
  slate: "bg-slate-100 text-slate-600 border-slate-200",
};

export function Badge({ children, tone = "slate" }: PropsWithChildren<{ tone?: Tone }>) {
  return (
    <span
      className={clsx(
        "inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        toneClasses[tone]
      )}
    >
      {children}
    </span>
  );
}
