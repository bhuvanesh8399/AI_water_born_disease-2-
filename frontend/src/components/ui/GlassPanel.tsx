import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

type Props = {
  title?: string;
  subtitle?: string;
  rightSlot?: ReactNode;
  className?: string;
  children: ReactNode;
};

export function GlassPanel({ title, subtitle, rightSlot, className, children }: Props) {
  return (
    <section className={cn("group relative overflow-hidden rounded-3xl surface-dark ring-water hover-lift", className)}>
      <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-white/8 to-transparent" />
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(34,211,238,0.08),transparent_28%),radial-gradient(circle_at_bottom_left,rgba(59,130,246,0.07),transparent_30%)]" />
      <div className="relative z-10 p-5 md:p-6">
        {(title || subtitle || rightSlot) && (
          <div className="mb-4 flex items-start justify-between gap-4">
            <div>
              {title ? <h3 className="panel-title">{title}</h3> : null}
              {subtitle ? <p className="mt-1 text-sm text-cyan-50/65">{subtitle}</p> : null}
            </div>
            {rightSlot ? <div>{rightSlot}</div> : null}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}
