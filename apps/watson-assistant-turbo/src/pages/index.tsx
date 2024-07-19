import { Inter } from "next/font/google";
import { NextPageWithLayout } from "./_app";
import WatsonAssistantActionsPanel from "@/components/WastonAssistantActionsPanel";

const inter = Inter({ subsets: ["latin"] });

const Page: NextPageWithLayout = () => {
  return (
    <div className="font-sans bg-[url('/Vodafone-Background.png')] h-screen bg-cover text-white">
      <WatsonAssistantActionsPanel />
    </div>
  );
};

export default Page;
