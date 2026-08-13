import { SectionHeading } from "../../../components/ui/Card";
import AIField from "../AIField";
import { complaintTypeOptions } from "../formOptions";

export default function ComplaintDetailsSection() {
  return (
    <div>
      <SectionHeading>3. Complaint Details</SectionHeading>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <AIField name="complaint_type" label="Complaint Type" type="select" options={complaintTypeOptions} required />
        <AIField name="complaint_date" label="Complaint Date" type="date" required />
        <AIField
          name="description"
          label="Detailed Complaint Description"
          type="textarea"
          required
          fullWidth
        />
      </div>
    </div>
  );
}
