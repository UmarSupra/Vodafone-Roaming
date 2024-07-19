# Watson Assistant Turbo

- [Watson Assistant Turbo](#watson-assistant-turbo)
  - [Getting started](#getting-started)
    - [Running the application](#running-the-application)
    - [Creating a custom response](#creating-a-custom-response)
    - [Creating an API route](#creating-an-api-route)

Created to accelerate the speed engineers can bootstrap and watson assistant applications.

:star: **Custom responses**

Quickly create custom reponses using the built in `customResponses` property.

:star: **useAssistant hook**

Send messages (and more!) from anywhere in your application using the built in `useAssistant` hook.

:star: **Tailwind + Carbon**

Supports Tailwind styling configured to used native Carbon colours and spacing out of the box. Quickly create custom components that look like native Carbon components.

:star: **VSCode plugins**

Supports automatic installation of recommended VSCode plugins during setup.

:star: **Shared Prettier config**

Supports shared prettier config tied to the workspace. No more massive commit changes due to conflicting styling rules.

:star: **Pre-commit linting**

Supports pre-commit linting with automatic configuration of Husky during setup. Avoid unnecessary bugs reaching your repo and deployment pipeline.

## Getting started

### Running the application

1. Install the required packages

```bash
npm install
```

2. Provide environment variables

```env
NEXT_PUBLIC_WA_INTEGRATION_ID=
NEXT_PUBLIC_WA_REGION=
NEXT_PUBLIC_WA_SERVICE_INSTANCE_ID=
```

3. Run the development server:

```bash
npm run dev
```

### Creating a custom response

Quickly create custom reponses using the built in `customResponses` property.

1. Add a `customResponses` property to the `WatsonAssistantProvider` in the `_app.tx` file.

```js
// src/pages/_app.tsx

<WatsonAssistantProvider
  customResponses={[
    {
      id: "example123",
      render: ({ instance }) => <div>This is a custom component!</div>,
    },
  ]}
>
```

1. Update the JSON for your Watson Assistant action to send a custom response.**The ID in your JSON must match the ID in your application e.g. `example123`**

```json
{
  "generic": [
    {
      "user_defined": {
        "id": "example123"
      },
      "response_type": "user_defined"
    }
  ]
}
```

### Creating an API route

1. Create an API route within the `/pages/api/` directory that you Watson Assistant will call. You can find more information about creating API routes in NextJS [here](https://nextjs.org/docs/pages/building-your-application/routing/api-routes).

```js
// src/pages/api/example.ts

import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  message: string,
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const text = req.body.text;
  res.status(200).json({ message: `The text sent was: ${text}` });
}
```

2. You will then need to host the application to generate an external endpoint that Watson Assistant will call. For development purposes, you can alternatively [expose your localhost using ngrok](https://ngrok.com/docs/getting-started/) to get an external endpoint Watson Assistant can use you call the API route.

```bash
ngrok http 3000
```

3. You will then need to create an integration in Watson Assistant that defines how your API will be called. This will require the creation of an OpenAPI schema. An example is below:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "Example OpenAPI schema",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "<endpoint>/api"
    }
  ],
  "paths": {
    "/example": {
      "get": {
        "summary": "Example summary",
        "operationId": "handler",
        "parameters": [
          {
            "name": "text",
            "in": "query",
            "description": "Example description",
            "required": true,
            "explode": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful operation",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Response"
                }
              }
            }
          },
          "400": {
            "description": "Failed operation"
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Response": {
        "type": "object",
        "properties": {
          "data": {
            "type": "object",
            "properties": {
              "message": {
                "type": "string"
              }
            }
          }
        }
      }
    }
  }
}
```
