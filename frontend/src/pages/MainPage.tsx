import AnalysisForm from "../components/AnalysisForm";
import { useState } from "react";
import type { Analysis, Proposal } from "../types/types";
import AnalysisCard from "../components/AnalysisCard";
import ProposalCard from "../components/ProposalCard";
import "./MainPage.css";
import { useRef } from "react";
import { useEffect } from "react";

export default function MainPage() {
  const [analysis, setAnalysis] = useState<Analysis | null>();
  const [proposal, setProposal] = useState<Proposal | null>();
  const [analysisError, setAnalysisError] = useState("");
  const [proposalError, setProposalError] = useState("");
  const analysisRef = useRef<HTMLElement>(null);

  function clearAll() {
    setAnalysis(null);
    setProposal(null);
    setAnalysisError("");
    setProposalError("");
  }

  useEffect(() => {
    if (analysis) {
      analysisRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [analysis]);

  return (
    <section className="main-page">
      <section className="main-header-container">
        <h1 className="main-header">QuoteAI</h1>
      </section>
      <AnalysisForm
        onSuccess={setAnalysis}
        onError={setAnalysisError}
        onStart={() => clearAll()}
      />
      <section className="analysis-message-container">
        {analysisError && (
          <p role="alert" className="message">
            {analysisError}
          </p>
        )}
      </section>
      {analysis && (
        <AnalysisCard
          analysis={analysis}
          onError={setAnalysisError}
          onSuccess={setProposal}
          analysisRef={analysisRef}
        />
      )}
      <section className="proposal-message-container">
        {proposalError && (
          <p role="alert" className="message">
            {proposalError}
          </p>
        )}
      </section>
      {proposal && <ProposalCard proposal={proposal} />}
    </section>
  );
}
