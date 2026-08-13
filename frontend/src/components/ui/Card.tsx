import type { PropsWithChildren, ReactNode } from "react";
import clsx from "clsx";

export function Card({ children, className }: PropsWithChildren<{ className?: string }>) {
  return (
    <div className={clsx("rounded-xl border border-slate-200 bg-white shadow-sm", className)}>
      {children}
    </div>
  );
}

export function SectionHeading({ children, icon }: PropsWithChildren<{ icon?: ReactNode }>) {
  return (
    <h3 className="mb-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
      {icon}
      {children}
    </h3>
  );
}
