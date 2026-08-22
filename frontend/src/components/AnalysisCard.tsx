import type { Analysis } from "../types/types";

type AnalysisCardProps = {
  analysis: Analysis;
};

export default function AnalysisCard({ analysis }: AnalysisCardProps) {
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
      <section className="analysis-data-container">
        <p className="analysis-data-header">Requirements:</p>
        {analysis.requirements.map((requirement) => (
          <section className="req-container">
            <p className="req-header">{requirement.service}</p>
            {requirement.details.map((det) => (
              <p key={det} className="req-detail">
                {det}
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
      <section className="analysis-data-container">
        <p className="analysis-data-header">Missing information:</p>
        {analysis.missing_information.map((missing) => (
          <p key={missing} className="analysis-data-content">
            {missing}
          </p>
        ))}
      </section>
      <section className="analysis-data-container">
        <p className="analysis-data-header">Assumptions:</p>
        <p className="analysis-data-content">analysis.assumptions</p>
        {analysis.assumptions.map((assum) => (
          <p key={assum} className="analysis-data-content">
            {assum}
          </p>
        ))}
      </section>
    </section>
  );
}
