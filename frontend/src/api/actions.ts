import { apiRequest } from "./client";
import type { Message, Analysis } from "../types/types";

export async function analyse(client_message: Message): Promise<Analysis> {
  return apiRequest<Analysis>("/analyse", {
    method: "POST",
    body: JSON.stringify(client_message),
  });
}
