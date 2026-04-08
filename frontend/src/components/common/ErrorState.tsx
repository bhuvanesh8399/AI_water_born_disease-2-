export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div className="rounded-3xl border border-red-400/15 bg-red-500/10 p-6">
      <h3 className="text-lg font-semibold text-red-100">Could not load data</h3>
      <p className="mt-2 text-sm text-red-100/70">{message}</p>
      {onRetry ? (
        <button onClick={onRetry} className="mt-4 rounded-2xl border border-red-300/20 bg-white/5 px-4 py-2 text-sm text-white">
          Retry
        </button>
      ) : null}
    </div>
  );
}
