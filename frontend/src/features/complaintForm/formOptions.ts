export const complaintSourceOptions = [
  "Email",
  "Phone Call",
  "Customer Portal",
  "Regulatory Authority",
  "Sales Representative",
  "Distributor",
  "Letter",
  "Other",
].map((v) => ({ value: v, label: v }));

export const complaintTypeOptions = [
  "Foreign Particulate/Contamination",
  "Potency/Efficacy Issue",
  "Packaging Defect",
  "Labeling Error",
  "Physical/Appearance Defect",
  "Adverse Event",
  "Delayed Onset of Action",
  "Counterfeit Suspicion",
  "Other",
].map((v) => ({ value: v, label: v }));

export const severityOptions = ["Critical", "Major", "Minor"].map((v) => ({ value: v, label: v }));
export const priorityOptions = ["High", "Medium", "Low"].map((v) => ({ value: v, label: v }));
export const quantityUnitOptions = ["kg", "units", "tablets", "capsules", "vials", "boxes"].map((v) => ({
  value: v,
  label: v,
}));
