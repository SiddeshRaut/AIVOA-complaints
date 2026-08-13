import { useAppDispatch, useAppSelector } from "../../../app/hooks";
import { SectionHeading } from "../../../components/ui/Card";
import AIField from "../AIField";
import { setField } from "../complaintFormSlice";
import { quantityUnitOptions } from "../formOptions";

function AffectedQuantityField() {
  const dispatch = useAppDispatch();
  const quantityUnit = useAppSelector((s) => s.complaintForm.fields.quantity_unit);
  const quantityAffected = useAppSelector((s) => s.complaintForm.fields.quantity_affected);
  const meta = useAppSelector((s) => s.complaintForm.meta.quantity_affected);
  const isAI = meta?.source === "ai";

  return (
    <div>
      <div className="mb-1 flex items-center justify-between">
        <label className="text-sm font-medium text-slate-700">Affected Quantity</label>
        {isAI && <span className="text-[10px] font-semibold uppercase tracking-wide text-brand-600">AI filled</span>}
      </div>
      <div className="flex overflow-hidden rounded-lg border border-slate-300 bg-slate-50 focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-500/30">
        <input
          type="number"
          className="w-full border-none bg-transparent px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none"
          placeholder="Awaiting AI extraction..."
          value={quantityAffected}
          onChange={(e) => dispatch(setField({ name: "quantity_affected", value: e.target.value }))}
        />
        <select
          className="border-l border-slate-300 bg-white px-2 text-sm text-slate-600 focus:outline-none"
          value={quantityUnit}
          onChange={(e) => dispatch(setField({ name: "quantity_unit", value: e.target.value }))}
        >
          {quantityUnitOptions.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default function ProductBatchSection() {
  return (
    <div>
      <SectionHeading>2. Product &amp; Batch Identification</SectionHeading>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <AIField name="product_name" label="Product Name" required />
        <AIField name="product_strength" label="Product Strength/Grade" placeholder="e.g. 500mg" />

        <AIField name="batch_number" label="Batch/Lot Number" required />
        <AffectedQuantityField />

        <AIField name="manufacturing_date" label="Manufacturing Date" type="date" />
        <AIField name="expiry_date" label="Expiry Date" type="date" />
      </div>
    </div>
  );
}
