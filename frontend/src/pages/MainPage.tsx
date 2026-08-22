import AnalysisForm from "../components/AnalysisForm";
import { useState } from "react";
import type { Analysis } from "../types/types";
import AnalysisCard from "../components/AnalysisCard";

export default function MainPage() {
  const [analysis, setAnalysis] = useState<Analysis | null>();
  const [error, setError] = useState("");
  return (
    <section className="main-page">
      <section className="main-header-container">
        <h1 className="main-header">QuoteAI</h1>
      </section>
      <section className="message-container">
        {error && <p role="alert">{error}</p>}
      </section>
      <AnalysisForm onSuccess={setAnalysis} onError={setError} />
      {analysis && <AnalysisCard analysis={analysis} />}
    </section>
  );
}
