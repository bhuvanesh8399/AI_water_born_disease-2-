export function LoadingPanel() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
      <div className="animate-pulse space-y-4">
        <div className="h-6 w-40 rounded bg-white/10" />
        <div className="h-24 rounded-2xl bg-white/10" />
        <div className="h-24 rounded-2xl bg-white/10" />
      </div>
    </div>
  );
}
