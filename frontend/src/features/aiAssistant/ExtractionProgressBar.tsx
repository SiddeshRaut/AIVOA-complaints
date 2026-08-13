import { useAppSelector } from "../../app/hooks";

export default function ExtractionProgressBar() {
  const { extractionStatus, progressPercent, progressMessage, error } = useAppSelector((s) => s.aiAssistant);

  if (extractionStatus === "idle") return null;

  return (
    <div className="mt-4">
      <div className="mb-1 flex items-center justify-between text-xs font-medium uppercase tracking-wide text-slate-500">
        <span>Extraction Progress</span>
        <span>{progressPercent}%</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-brand-500 transition-all duration-300 ease-out"
          style={{ width: `${progressPercent}%` }}
        />
      </div>
      <p className={`mt-2 text-xs ${extractionStatus === "error" ? "text-red-600" : "text-slate-500"}`}>
        {extractionStatus === "error" ? error : progressMessage}
      </p>
    </div>
  );
}
