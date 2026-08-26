import type { Analysis, Proposal } from "../types/types";
import { useState } from "react";
import { generateProposal } from "../api/actions";
import "./AnalysisCard.css";

type AnalysisCardProps = {
  analysis: Analysis;
  onError: (message: string) => void;
  onSuccess: (data: Proposal) => void;
};

export default function AnalysisCard({
  analysis,
  onError,
  onSuccess,
}: AnalysisCardProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [isProposalGenerated, setIsProposalGenerated] = useState(false);

  async function handleGenerateProposal(analysis: Analysis) {
    try {
      setIsLoading(true);
      onError("");

      const proposal = await generateProposal(analysis);
      onSuccess(proposal);
      setIsProposalGenerated(true);
    } catch (error) {
      onError(
        error instanceof Error ? error.message : "Failed to generate proposal.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="analysis-card-container">
      <section className="analysis-data-container">
        <p className="analysis-data-header">Service type:</p>
        <p className="analysis-data-content">{analysis.service_type}</p>
      </section>
      <section className="analysis-data-container">
        <p className="analysis-data-header">Client summary:</p>
        <p className="analysis-data-content">{analysis.client_summary}</p>
      </section>
      <section className="analysis-data-container reqs-container">
        <p className="analysis-data-header reqs-header">Requirements:</p>
        {analysis.requirements.map((requirement) => (
          <section className="req-container">
            <p className="req-header">{requirement.service}</p>
            {requirement.details.map((det) => (
              <p key={det} className="req-detail">
                &bull; {det}
              </p>
            ))}
          </section>
        ))}
      </section>
      <section className="analysis-data-container">
        <p className="analysis-data-header">Scope:</p>
        <p className="analysis-data-content">{analysis.scope}</p>
      </section>
      <section className="analysis-data-container">
        <p className="analysis-data-header">Timeline:</p>
        <p className="analysis-data-content">{analysis.timeline}</p>
      </section>
      <section className="analysis-data-container">
        <p className="analysis-data-header">Budget:</p>
        <p className="analysis-data-content">{analysis.budget}</p>
      </section>
      <section className="analysis-data-container miss-info-container">
        <p className="analysis-data-header">Missing information:</p>
        {analysis.missing_information.map((missing) => (
          <p key={missing} className="analysis-data-content miss-info-content">
            &bull; {missing}
          </p>
        ))}
      </section>
      <section className="analysis-data-container assumptions-container">
        <p className="analysis-data-header">Assumptions:</p>
        {analysis.assumptions.map((assum) => (
          <p key={assum} className="analysis-data-content assumptions-content">
            &bull; {assum}
          </p>
        ))}
      </section>
      <section className="analysis-data-container generate-proposal-container">
        {!isProposalGenerated && (
          <button
            type="button"
            disabled={isLoading}
            onClick={() => handleGenerateProposal(analysis)}
            className="generate-proposal-button"
          >
            {isLoading ? "Generating Proposal..." : "Generate Proposal"}
          </button>
        )}
      </section>
    </section>
  );
}
