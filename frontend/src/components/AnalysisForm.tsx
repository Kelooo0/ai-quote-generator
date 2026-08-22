import { useState } from "react";
import { analyse } from "../api/actions";
import type { Analysis } from "../types/types";

type AnalysisFormProps = {
  onSuccess: (data: Analysis) => void;
  onError: (message: string) => void;
};

export default function AnalysisForm({
  onSuccess,
  onError,
}: AnalysisFormProps) {
  const [content, setContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
    try {
      event.preventDefault();
      setIsLoading(true);
      onError("");

      const analysis = await analyse({ content });
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
          ></textarea>
        </section>
        <section className="form-submit-container">
          <button className="form-submit" type="submit" disabled={isLoading}>
            {isLoading ? "Generating..." : "Generate Analysis"}
          </button>
        </section>
      </form>
    </section>
  );
}
