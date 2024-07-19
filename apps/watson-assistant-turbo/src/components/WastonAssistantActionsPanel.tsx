import { useAssistant } from "@/context/WatsonAssistant";

const WatsonAssistantActionsPanel = () => {
  const { assistant } = useAssistant();

  if (assistant)
    return (
      <div className="fixed bottom-8 left-8">
        <div className="flex gap-4">
          <button
            className="bg-[#d30000] px-5 py-2 text-[0.9rem] text-white rounded-full hover:bg-[#8c0000]"
            onClick={() => assistant.current.openWindow()}
          >
            Open window
          </button>
          <button
            className="bg-[#d30000] px-5 py-2 text-[0.9rem] text-white rounded-full hover:bg-[#8c0000]"
            onClick={() => assistant.current.closeWindow()}
          >
            Close window
          </button>
          <button
            className="bg-[#d30000] px-5 py-2 text-[0.9rem] text-white rounded-full hover:bg-[#8c0000]"
            onClick={() => assistant.current.restartConversation()}
          >
            Restart conversation
          </button>
        </div>
      </div>
    );

  return <></>;
};

export default WatsonAssistantActionsPanel;
