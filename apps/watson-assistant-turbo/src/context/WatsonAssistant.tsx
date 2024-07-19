import React, {
  createContext,
  MutableRefObject,
  ReactElement,
  ReactNode,
  useContext,
  useRef,
} from "react";
import {
  setEnableDebug,
  WebChatConfig,
  WebChatContainer,
  WebChatInstance,
} from "@ibm-watson/assistant-web-chat-react";
import { CustomResponseEvent } from "@ibm-watson/assistant-web-chat-react/dist/types/CustomResponseEvent";

setEnableDebug(true);

const WatsonAssistantContext = createContext<{
  assistant: WebChatInstance | null;
}>({
  assistant: null,
});

const WatsonAssistantProvider = ({
  children,
  customResponses,
}: {
  children: ReactNode;
  customResponses?: {
    id: string;
    render: (instance: WebChatInstance) => ReactElement;
  }[];
}) => {
  const assistant = useRef<WebChatInstance>(null);

  return (
    <WatsonAssistantContext.Provider value={{ assistant }}>
      <WebChatContainer
        instanceRef={assistant as MutableRefObject<WebChatInstance>}
        config={
          {
            integrationID: process.env.NEXT_PUBLIC_WA_INTEGRATION_ID || "",
            region: process.env.NEXT_PUBLIC_WA_REGION || "eu-gb",
            serviceInstanceID:
              process.env.NEXT_PUBLIC_WA_SERVICE_INSTANCE_ID || "",
          } as WebChatConfig
        }
        renderCustomResponse={(event, instance) => {
          if (customResponses)
            return renderCustomResponses({
              event,
              instance,
              responses: customResponses,
            });
          return <></>;
        }}
        onBeforeRender={(instance) => {
          instance.on({
            type: "receive",
            handler: (event: any) => console.log(event),
          });
          instance.on({
            type: "send",
            handler: (event: any) => console.log(event),
          });
          return Promise.resolve();
        }}
      />
      {children}
    </WatsonAssistantContext.Provider>
  );
};

const renderCustomResponses = ({
  event,
  instance,
  responses,
}: {
  event: CustomResponseEvent;
  instance: WebChatInstance;
  responses: {
    id: string;
    render: ({
      instance,
      event,
    }: {
      instance: WebChatInstance;
      event: CustomResponseEvent;
    }) => ReactElement;
  }[];
}) => {
  const response = responses.filter(
    (response) =>
      response.id ===
      (event.data.message as { user_defined: { id: string } }).user_defined.id
  )[0];
  if (!response) {
    return <></>;
  }
  return response.render({ instance, event });
};

export const useAssistant = () => useContext(WatsonAssistantContext);

export default WatsonAssistantProvider;
