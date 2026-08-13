import { useState } from "react";
import { Card } from "../../components/ui/Card";
import { Badge } from "../../components/ui/Badge";
import { Button } from "../../components/ui/Button";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { resetForm, markSaved } from "./complaintFormSlice";
import { resetAssistant } from "../aiAssistant/aiAssistantSlice";
import { resetChat } from "../aiAssistant/chatSlice";
import { clearDuplicates, checkFinished, openModal } from "../duplicates/duplicatesSlice";
import { useCreateComplaintMutation, useCheckDuplicatesMutation } from "../../api/apiSlice";
import type { ComplaintCreatePayload, DuplicateConflictDetail } from "../../api/types";
import OriginCustomerSection from "./sections/OriginCustomerSection";
import ProductBatchSection from "./sections/ProductBatchSection";
import ComplaintDetailsSection from "./sections/ComplaintDetailsSection";
import AssessmentPrioritySection from "./sections/AssessmentPrioritySection";
import DuplicateWarningModal from "../duplicates/DuplicateWarningModal";

const statusTone = (status: string) => {
  if (status === "Resolved") return "green" as const;
  if (status === "Under Investigation") return "blue" as const;
  return "amber" as const;
};

export default function ComplaintFormPanel() {
  const dispatch = useAppDispatch();
  const { fields, status, savedComplaintNumber } = useAppSelector((s) => s.complaintForm);
  const documentId = useAppSelector((s) => s.aiAssistant.documentId);
  const [createComplaint, { isLoading: isSaving }] = useCreateComplaintMutation();
  const [checkDuplicates] = useCheckDuplicatesMutation();
  const [saveError, setSaveError] = useState<string | null>(null);

  const buildPayload = (acknowledge: boolean): ComplaintCreatePayload => ({
    complaint_source: fields.complaint_source || null,
    customer_name: fields.customer_name,
    product_name: fields.product_name,
    product_strength: fields.product_strength || null,
    batch_number: fields.batch_number,
    manufacturing_date: fields.manufacturing_date || null,
    expiry_date: fields.expiry_date || null,
    quantity_affected: fields.quantity_affected ? Number(fields.quantity_affected) : null,
    quantity_unit: fields.quantity_unit || "kg",
    complaint_type: fields.complaint_type,
    complaint_date: fields.complaint_date,
    description: fields.description,
    initial_severity: fields.initial_severity || null,
    priority: fields.priority || null,
    source_document_id: documentId,
    acknowledge_duplicates: acknowledge,
  });

  const handleReset = () => {
    dispatch(resetForm());
    dispatch(resetAssistant());
    dispatch(resetChat());
    dispatch(clearDuplicates());
    setSaveError(null);
  };

  const handleSave = async (acknowledge = false) => {
    setSaveError(null);
    try {
      const result = await createComplaint(buildPayload(acknowledge)).unwrap();
      dispatch(markSaved({ complaintNumber: result.complaint_number, status: result.status }));
      dispatch(clearDuplicates());
    } catch (err: unknown) {
      const detail = (err as { data?: { detail?: DuplicateConflictDetail } })?.data?.detail;
      if (detail?.duplicates?.length) {
        dispatch(checkFinished(detail.duplicates));
        dispatch(openModal());
        return;
      }
      setSaveError("Failed to save complaint. Check required fields and try again.");
    }
  };

  const handlePreflightSave = async () => {
    if (fields.product_name || fields.batch_number || fields.description) {
      const candidates = await checkDuplicates({
        product_name: fields.product_name,
        batch_number: fields.batch_number,
        complaint_type: fields.complaint_type,
        description: fields.description,
      }).unwrap();
      if (candidates.length) {
        dispatch(checkFinished(candidates));
        dispatch(openModal());
        return;
      }
    }
    handleSave(false);
  };

  return (
    <div>
      <div className="mb-4 flex items-start justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">Log Customer Complaint</h1>
          <p className="text-sm text-slate-500">API &amp; FDF Quality Assurance Module</p>
        </div>
        <Badge tone={statusTone(status)}>{status}</Badge>
      </div>

      {savedComplaintNumber && (
        <div className="mb-4 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm text-emerald-700">
          Saved as <span className="font-semibold">{savedComplaintNumber}</span>.
        </div>
      )}
      {saveError && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-700">
          {saveError}
        </div>
      )}

      <Card className="space-y-6 p-6">
        <OriginCustomerSection />
        <hr className="border-slate-200" />
        <ProductBatchSection />
        <hr className="border-slate-200" />
        <ComplaintDetailsSection />
        <hr className="border-slate-200" />
        <AssessmentPrioritySection />
      </Card>

      <div className="mt-4 flex justify-between">
        <Button variant="secondary" onClick={handleReset} type="button">
          Reset Form
        </Button>
        <Button variant="primary" onClick={handlePreflightSave} disabled={isSaving} type="button">
          {isSaving ? "Saving..." : "Save Complaint"}
        </Button>
      </div>

      <DuplicateWarningModal onConfirmSaveAnyway={() => handleSave(true)} />
    </div>
  );
}
