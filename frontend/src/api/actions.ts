import { apiRequest } from "./client";
import type { Message, Analysis, Proposal } from "../types/types";

export async function generateAnalysis(
  client_message: Message,
): Promise<Analysis> {
  return apiRequest<Analysis>("/analyse", {
    method: "POST",
    body: JSON.stringify(client_message),
  });
}
export async function generateProposal(analysis: Analysis): Promise<Proposal> {
  return apiRequest<Proposal>("/proposal", {
    method: "POST",
    body: JSON.stringify(analysis),
  });
}
