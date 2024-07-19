import "@/styles/globals.css";
import "@/styles/carbon.scss";
import type { AppProps } from "next/app";
import { Theme } from "@carbon/react";
import { ReactElement, ReactNode } from "react";
import { NextPage } from "next";
import WatsonAssistantProvider from "@/context/WatsonAssistant";

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode;
};

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
};

export default function App({ Component, pageProps }: AppPropsWithLayout) {
  const getLayout = Component.getLayout || ((page) => page);

  return (
    <>
      <Theme theme="g10">
        <WatsonAssistantProvider
          customResponses={[
            {
              id: "example",
              render: ({ instance }) => <div>This is a custom component!</div>,
            },
          ]}
        >
          {getLayout(<Component {...pageProps} />)}
        </WatsonAssistantProvider>
      </Theme>
    </>
  );
}
