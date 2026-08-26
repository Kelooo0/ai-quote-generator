import { useState } from "react";
import { generateAnalysis } from "../api/actions";
import type { Analysis } from "../types/types";
import "./AnalysisForm.css";
type AnalysisFormProps = {
  onSuccess: (data: Analysis) => void;
  onError: (message: string) => void;
  onStart: () => void;
};

export default function AnalysisForm({
  onSuccess,
  onError,
  onStart,
}: AnalysisFormProps) {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    try {
      event.preventDefault();
      setIsLoading(true);
      onStart();

      const analysis = await generateAnalysis({ content });
      onSuccess(analysis);
    } catch (error) {
      onError(
        error instanceof Error ? error.message : "Failed to generate analysis.",
      );
    } finally {
      setIsLoading(false);
    }
  }
  return (
    <section className="analysis-form-container">
      <form onSubmit={handleSubmit} className="analysis-form">
        <section className="form-text-container">
          <textarea
            className="form-text"
            disabled={isLoading}
            onChange={(event) => setContent(event.target.value)}
            placeholder="Enter client's message content..."
          ></textarea>
        </section>
        <section className="form-submit-container">
          <button
            className="form-submit action-button"
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? "Generating Analysis..." : "Generate Analysis"}
          </button>
        </section>
      </form>
    </section>
  );
}
