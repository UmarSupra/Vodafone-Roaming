import type { NextApiRequest, NextApiResponse } from "next";

type Data = {
  data: {
    message: string;
  };
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const text = req.body.text;
  res.status(200).json({ data: { message: `The text sent was: ${text}` } });
}
