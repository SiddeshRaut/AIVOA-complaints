import { useCallback, useState } from "react";
import { useDropzone, type FileRejection } from "react-dropzone";
import { useAppDispatch } from "../../app/hooks";
import { Button } from "../../components/ui/Button";
import { usePasteDocumentMutation, useUploadDocumentMutation } from "../../api/apiSlice";
import { uploadFailed, uploadStarted, uploadSucceeded } from "./aiAssistantSlice";

const ACCEPTED = {
  "application/pdf": [".pdf"],
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
  "text/plain": [".txt"],
  "message/rfc822": [".eml"],
};
const MAX_SIZE = 10 * 1024 * 1024;

export default function DocumentDropzone({ onUploaded }: { onUploaded: (documentId: number) => void }) {
  const dispatch = useAppDispatch();
  const [uploadDocument] = useUploadDocumentMutation();
  const [pasteDocument] = usePasteDocumentMutation();
  const [pasteText, setPasteText] = useState("");
  const [fileError, setFileError] = useState<string | null>(null);

  const onDrop = useCallback(
    async (acceptedFiles: File[], rejections: FileRejection[]) => {
      setFileError(null);
      if (rejections.length) {
        setFileError(rejections[0]?.errors?.[0]?.message ?? "File rejected");
        return;
      }
      const file = acceptedFiles[0];
      if (!file) return;

      dispatch(uploadStarted());
      const formData = new FormData();
      formData.append("file", file);
      try {
        const result = await uploadDocument(formData).unwrap();
        dispatch(uploadSucceeded({ documentId: result.document_id, documentName: result.original_filename }));
        onUploaded(result.document_id);
      } catch (err) {
        const detail = (err as { data?: { detail?: string } })?.data?.detail;
        dispatch(uploadFailed(detail ?? "Upload failed"));
      }
    },
    [dispatch, uploadDocument, onUploaded]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED,
    maxSize: MAX_SIZE,
    multiple: false,
  });

  const handlePasteSubmit = async () => {
    if (!pasteText.trim()) return;
    dispatch(uploadStarted());
    try {
      const result = await pasteDocument({ text: pasteText }).unwrap();
      dispatch(uploadSucceeded({ documentId: result.document_id, documentName: "Pasted text" }));
      onUploaded(result.document_id);
      setPasteText("");
    } catch {
      dispatch(uploadFailed("Failed to submit pasted text"));
    }
  };

  return (
    <div>
      <div
        {...getRootProps()}
        className={`cursor-pointer rounded-xl border-2 border-dashed px-4 py-8 text-center transition-colors ${
          isDragActive ? "border-brand-400 bg-brand-50" : "border-slate-300 bg-slate-50 hover:bg-slate-100"
        }`}
      >
        <input {...getInputProps()} />
        <div className="mb-2 text-2xl">📤</div>
        <p className="text-sm text-slate-600">
          Drag &amp; drop complaint document here
          <br />
          or <span className="font-medium text-brand-600">click to browse</span>
        </p>
      </div>
      {fileError && <p className="mt-2 text-xs text-red-600">{fileError}</p>}

      <div className="my-4 flex items-center gap-3 text-xs text-slate-400">
        <div className="h-px flex-1 bg-slate-200" />
        OR
        <div className="h-px flex-1 bg-slate-200" />
      </div>

      <div className="space-y-2">
        <p className="text-sm font-medium text-slate-700">📄 Paste Complaint Text / Email</p>
        <textarea
          className="min-h-[110px] w-full rounded-lg border border-slate-300 bg-white p-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/30"
          placeholder="Paste the complaint email or text here..."
          value={pasteText}
          onChange={(e) => setPasteText(e.target.value)}
        />
        <div className="flex justify-end gap-2">
          {pasteText && (
            <Button variant="ghost" onClick={() => setPasteText("")} type="button">
              Clear
            </Button>
          )}
          <Button variant="primary" onClick={handlePasteSubmit} disabled={!pasteText.trim()} type="button">
            Analyze Text
          </Button>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs text-emerald-700">
        ℹ️ Supported formats: PDF, DOCX, TXT, EML · Max file size: 10MB
      </div>
    </div>
  );
}
