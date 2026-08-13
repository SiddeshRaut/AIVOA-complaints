import type { ReactNode } from "react";

export default function TwoPaneLayout({ left, right }: { left: ReactNode; right: ReactNode }) {
  return (
    <div className="mx-auto grid max-w-[1400px] grid-cols-1 gap-6 px-4 lg:grid-cols-[1.3fr_1fr]">
      <div>{left}</div>
      <div>{right}</div>
    </div>
  );
}
