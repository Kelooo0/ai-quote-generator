import AnalysisForm from "../components/AnalysisForm";
import { useState } from "react";
import type { Analysis, Proposal } from "../types/types";
import AnalysisCard from "../components/AnalysisCard";
import ProposalCard from "../components/ProposalCard";

export default function MainPage() {
  const [analysis, setAnalysis] = useState<Analysis | null>();
  const [proposal, setProposal] = useState<Proposal | null>();
  const [error, setError] = useState("");

  function clearAll() {
    setAnalysis(null);
    setProposal(null);
    setError("");
  }

  return (
    <section className="main-page">
      <section className="main-header-container">
        <h1 className="main-header">QuoteAI</h1>
      </section>
      <section className="message-container">
        {error && <p role="alert">{error}</p>}
      </section>
      <AnalysisForm
        onSuccess={setAnalysis}
        onError={setError}
        onStart={() => clearAll()}
      />
      {analysis && (
        <AnalysisCard
          analysis={analysis}
          onError={setError}
          onSuccess={setProposal}
        />
      )}
      {proposal && <ProposalCard proposal={proposal} />}
    </section>
  );
}
