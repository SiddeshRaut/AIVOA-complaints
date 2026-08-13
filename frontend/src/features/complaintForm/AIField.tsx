import { useEffect } from "react";
import clsx from "clsx";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { setField, clearFieldFlash, type ComplaintFormFields } from "./complaintFormSlice";

type FieldType = "text" | "date" | "number" | "select" | "textarea";

interface Option {
  value: string;
  label: string;
}

interface AIFieldProps {
  name: keyof ComplaintFormFields;
  label: string;
  type?: FieldType;
  options?: Option[];
  placeholder?: string;
  suffix?: string;
  required?: boolean;
  fullWidth?: boolean;
}

export default function AIField({
  name,
  label,
  type = "text",
  options,
  placeholder,
  suffix,
  required,
  fullWidth,
}: AIFieldProps) {
  const dispatch = useAppDispatch();
  const value = useAppSelector((s) => s.complaintForm.fields[name]);
  const meta = useAppSelector((s) => s.complaintForm.meta[name]);

  useEffect(() => {
    if (meta?.justUpdated) {
      const t = setTimeout(() => dispatch(clearFieldFlash(name)), 1200);
      return () => clearTimeout(t);
    }
  }, [meta?.justUpdated, name, dispatch]);

  const handleChange = (v: string) => dispatch(setField({ name, value: v }));

  const isAI = meta?.source === "ai";
  const lowConfidence = isAI && (meta?.confidence ?? 1) < 0.6;
  const effectivePlaceholder = placeholder ?? "Awaiting AI extraction...";

  const baseInputClasses = clsx(
    "w-full rounded-lg border px-3 py-2 text-sm text-slate-800 placeholder:text-slate-400 transition-colors",
    "focus:outline-none focus:ring-2 focus:ring-brand-500/30 focus:border-brand-400",
    lowConfidence ? "border-amber-300 bg-amber-50/60" : "border-slate-300 bg-slate-50",
    meta?.justUpdated && "animate-field-flash"
  );

  return (
    <div className={fullWidth ? "sm:col-span-2" : undefined}>
      <div className="mb-1 flex items-center justify-between">
        <label className="text-sm font-medium text-slate-700">
          {label} {required && <span className="text-red-400">*</span>}
        </label>
        {isAI && (
          <span
            className={clsx(
              "text-[10px] font-semibold uppercase tracking-wide",
              lowConfidence ? "text-amber-600" : "text-brand-600"
            )}
            title={meta?.confidence != null ? `AI confidence: ${Math.round(meta.confidence * 100)}%` : undefined}
          >
            {lowConfidence ? "verify" : "AI filled"}
          </span>
        )}
      </div>

      {type === "select" ? (
        <select className={baseInputClasses} value={value} onChange={(e) => handleChange(e.target.value)}>
          <option value="">Select...</option>
          {options?.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      ) : type === "textarea" ? (
        <textarea
          className={clsx(baseInputClasses, "min-h-[92px] resize-y")}
          value={value}
          placeholder={effectivePlaceholder}
          onChange={(e) => handleChange(e.target.value)}
        />
      ) : (
        <div className="relative">
          <input
            type={type}
            className={baseInputClasses}
            value={value}
            placeholder={effectivePlaceholder}
            onChange={(e) => handleChange(e.target.value)}
          />
          {suffix && (
            <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              {suffix}
            </span>
          )}
        </div>
      )}
    </div>
  );
}
