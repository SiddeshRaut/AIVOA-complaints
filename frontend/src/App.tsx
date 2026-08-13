import TwoPaneLayout from "./components/layout/TwoPaneLayout";
import ComplaintFormPanel from "./features/complaintForm/ComplaintFormPanel";
import AIAssistantPanel from "./features/aiAssistant/AIAssistantPanel";

export default function App() {
  return (
    <div className="min-h-screen py-6">
      <TwoPaneLayout left={<ComplaintFormPanel />} right={<AIAssistantPanel />} />
    </div>
  );
}
