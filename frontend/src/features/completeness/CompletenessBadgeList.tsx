import { useAppSelector } from "../../app/hooks";
import { Badge } from "../../components/ui/Badge";

const FIELD_LABELS: Record<string, string> = {
  customer_name: "Customer Name",
  product_name: "Product Name",
  batch_number: "Batch/Lot Number",
  complaint_type: "Complaint Type",
  complaint_date: "Complaint Date",
  description: "Description",
  complaint_source: "Complaint Source",
  product_strength: "Product Strength",
  manufacturing_date: "Manufacturing Date",
  expiry_date: "Expiry Date",
  quantity_affected: "Quantity Affected",
};

export default function CompletenessBadgeList() {
  const completeness = useAppSelector((s) => s.aiAssistant.completeness);
  const warnings = useAppSelector((s) => s.aiAssistant.warnings);

  if (!completeness && warnings.length === 0) return null;

  const missingRequired = completeness?.missingRequired ?? [];
  const lowConfidence = completeness?.lowConfidence ?? [];

  if (missingRequired.length === 0 && lowConfidence.length === 0 && warnings.length === 0) {
    return (
      <div className="mt-3 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs text-emerald-700">
        ✓ All required fields extracted with good confidence.
      </div>
    );
  }

  return (
    <div className="mt-3 space-y-2">
      {missingRequired.length > 0 && (
        <div>
          <p className="mb-1 text-xs font-medium text-red-600">Missing required fields — please fill in manually:</p>
          <div className="flex flex-wrap gap-1">
            {missingRequired.map((f) => (
              <Badge key={f} tone="red">
                {FIELD_LABELS[f] ?? f}
              </Badge>
            ))}
          </div>
        </div>
      )}
      {lowConfidence.length > 0 && (
        <div>
          <p className="mb-1 text-xs font-medium text-amber-600">Low-confidence — please verify:</p>
          <div className="flex flex-wrap gap-1">
            {lowConfidence.map((f) => (
              <Badge key={f} tone="amber">
                {FIELD_LABELS[f] ?? f}
              </Badge>
            ))}
          </div>
        </div>
      )}
      {warnings.map((w, i) => (
        <p key={i} className="text-xs text-slate-400">
          {w}
        </p>
      ))}
    </div>
  );
}
