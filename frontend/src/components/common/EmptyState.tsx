import type { ReactNode } from "react";

export function EmptyState({ title, description, action }: { title: string; description?: string; action?: ReactNode }) {
  return (
    <div className="rounded-3xl border border-dashed border-cyan-300/15 bg-slate-950/35 p-8 text-center">
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      {description ? <p className="mx-auto mt-2 max-w-lg text-sm text-cyan-50/60">{description}</p> : null}
      {action ? <div className="mt-4">{action}</div> : null}
    </div>
  );
}
