export function WaterBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.08),transparent_30%),linear-gradient(180deg,#020617_0%,#071220_45%,#061019_100%)]" />
      <div className="absolute left-[-10%] top-[-14%] h-[420px] w-[420px] animate-pulse rounded-full bg-cyan-300/10 blur-3xl" />
      <div className="absolute bottom-[-12%] right-[-8%] h-[460px] w-[460px] animate-pulse rounded-full bg-blue-500/10 blur-3xl [animation-delay:900ms]" />
      <div className="absolute left-1/4 top-1/2 h-[280px] w-[280px] rounded-full bg-sky-300/5 blur-3xl" />
      <div className="absolute inset-x-0 top-[12%] h-px bg-gradient-to-r from-transparent via-cyan-200/10 to-transparent" />
      <div className="absolute inset-x-0 top-[34%] h-px bg-gradient-to-r from-transparent via-cyan-200/5 to-transparent" />
      <div className="absolute inset-x-0 top-[62%] h-px bg-gradient-to-r from-transparent via-cyan-200/6 to-transparent" />
    </div>
  );
}
