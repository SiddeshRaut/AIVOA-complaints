import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { Button } from "../../components/ui/Button";
import { Badge } from "../../components/ui/Badge";
import { closeModal } from "./duplicatesSlice";

export default function DuplicateWarningModal({ onConfirmSaveAnyway }: { onConfirmSaveAnyway: () => void }) {
  const dispatch = useAppDispatch();
  const { modalOpen, candidates } = useAppSelector((s) => s.duplicates);

  if (!modalOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4">
      <div className="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">
        <div className="mb-3 flex items-center gap-2">
          <span className="text-lg">⚠️</span>
          <h2 className="text-base font-semibold text-slate-900">Possible duplicate complaint(s) found</h2>
        </div>
        <p className="mb-4 text-sm text-slate-600">
          This complaint looks similar to {candidates.length} existing record
          {candidates.length === 1 ? "" : "s"}. Review before saving a new entry.
        </p>

        <div className="mb-5 max-h-64 space-y-2 overflow-y-auto">
          {candidates.map((c) => (
            <div key={c.complaint_id} className="rounded-lg border border-slate-200 p-3">
              <div className="mb-1 flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-800">{c.complaint_number}</span>
                <Badge tone={c.similarity_score >= 70 ? "red" : "amber"}>
                  {Math.round(c.similarity_score)}% match
                </Badge>
              </div>
              <p className="text-xs text-slate-500">
                {c.product_name} · Batch {c.batch_number} · {c.complaint_type}
              </p>
              <p className="text-xs text-slate-400">
                Matched on: {c.matched_fields.join(", ") || "description similarity"}
              </p>
            </div>
          ))}
        </div>

        <div className="flex justify-end gap-2">
          <Button variant="secondary" onClick={() => dispatch(closeModal())}>
            Go back &amp; review
          </Button>
          <Button
            variant="primary"
            onClick={() => {
              dispatch(closeModal());
              onConfirmSaveAnyway();
            }}
          >
            Save anyway
          </Button>
        </div>
      </div>
    </div>
  );
}
