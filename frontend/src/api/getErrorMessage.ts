export function getErrorMessage(message: string, fallback: string): string {
  let parsedMessage = fallback;
  if (message) {
    try {
      const parsed = JSON.parse(message);
      const detail = parsed.detail;

      if (typeof detail === "string") {
        parsedMessage = detail;
      }
      if (Array.isArray(detail)) {
        const msg = detail[0].msg;

        if (typeof msg === "string") {
          parsedMessage = msg;
        }
      }
    } catch {
      parsedMessage = fallback;
    }
  }
  switch (parsedMessage) {
    case "Value error, Client message can not be empty or just whitespaces":
      return "Client message can not be empty or just whitespaces.";
    case "String should have at least 50 characters":
      return "Client message must be at least 50 characters long.";
    case "String should have at most 5000 characters":
      return "Client message can not be longer than 5000 characters.";
    default:
      return parsedMessage;
  }
}
