import type { ReactNode } from "react";

type Props = {
  title: string;
  subtitle?: string;
  rightSlot?: ReactNode;
};

export function PageHeader({ title, subtitle, rightSlot }: Props) {
  return (
    <div className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
      <div>
        <div className="tiny-label">AI-Based Early Warning System</div>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-white md:text-4xl">{title}</h1>
        {subtitle ? <p className="mt-2 max-w-3xl text-sm leading-6 text-cyan-50/65">{subtitle}</p> : null}
      </div>
      {rightSlot ? <div>{rightSlot}</div> : null}
    </div>
  );
}
