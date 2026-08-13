import { SectionHeading } from "../../../components/ui/Card";
import AIField from "../AIField";
import { complaintSourceOptions } from "../formOptions";

export default function OriginCustomerSection() {
  return (
    <div>
      <SectionHeading>1. Origin &amp; Customer Details</SectionHeading>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <AIField name="complaint_source" label="Complaint Source" type="select" options={complaintSourceOptions} required />
        <AIField name="customer_name" label="Customer Name" required />
      </div>
    </div>
  );
}
