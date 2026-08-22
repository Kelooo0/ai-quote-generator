import { getErrorMessage } from "./getErrorMessage";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    const message = await response.text();
    const fallback = `A request error occured: ${response.status}`;

    const final_message = getErrorMessage(message, fallback);
    throw new Error(final_message);
  }
  return response.json() as Promise<T>;
}
