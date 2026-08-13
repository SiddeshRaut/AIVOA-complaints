import { useAppSelector } from "../../../app/hooks";
import { SectionHeading } from "../../../components/ui/Card";
import AIField from "../AIField";
import { priorityOptions, severityOptions } from "../formOptions";

export default function AssessmentPrioritySection() {
  const rationale = useAppSelector((s) => s.complaintForm.aiRiskRationale);

  return (
    <div>
      <SectionHeading>4. Initial Assessment &amp; Priority</SectionHeading>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <AIField name="initial_severity" label="Initial Severity" type="select" options={severityOptions} />
        <AIField name="priority" label="Priority" type="select" options={priorityOptions} />
      </div>
      {rationale && (
        <p className="mt-3 rounded-lg bg-brand-50 px-3 py-2 text-xs text-brand-700">
          <span className="font-semibold">AI rationale: </span>
          {rationale}
        </p>
      )}
    </div>
  );
}
