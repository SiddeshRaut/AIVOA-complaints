import { Card } from "../../components/ui/Card";
import CompletenessBadgeList from "../completeness/CompletenessBadgeList";
import ChatPanel from "./ChatPanel";
import DocumentDropzone from "./DocumentDropzone";
import ExtractionProgressBar from "./ExtractionProgressBar";
import { useExtractionStream } from "./useExtractionStream";

export default function AIAssistantPanel() {
  const { start } = useExtractionStream();

  return (
    <div>
      <div className="mb-4 flex items-center gap-2">
        <h2 className="flex items-center gap-2 text-lg font-semibold text-slate-900">
          <span className="text-brand-500">✦</span> AI Complaint Intake Assistant
        </h2>
        <span className="rounded-full bg-brand-100 px-2 py-0.5 text-[10px] font-semibold text-brand-700">
          BETA
        </span>
      </div>

      <Card className="p-5">
        <DocumentDropzone onUploaded={(documentId) => start(documentId)} />
        <ExtractionProgressBar />
        <CompletenessBadgeList />
      </Card>

      <ChatPanel />
    </div>
  );
}
