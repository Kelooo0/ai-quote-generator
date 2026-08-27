import type { Proposal } from "../types/types";
import "./ProposalCard.css";

type ProposalCardProps = {
  proposal: Proposal;
  proposalRef: React.RefObject<HTMLElement | null>;
};

export default function ProposalCard({
  proposal,
  proposalRef,
}: ProposalCardProps) {
  async function handleCopy() {
    const textPlain = `Title: ${proposal.title}\n\nIntroduction:\n${proposal.introduction}\n\nScope:\n${proposal.scope.map((item) => `• ${item}`).join("\n")}\n\nTimeline: ${proposal.timeline}\n\nPrice: ${proposal.price} ${proposal.currency}`;

    const textHtml = `
            <div>
            <p><strong>Title:</strong> ${proposal.title}</p>
            <p><strong>Introduction:</strong><br>${proposal.introduction}</p>
            <p><strong>Scope:</strong></p>
            <ul>
                ${proposal.scope.map((item) => `<li>${item}</li>`).join("")}
            </ul>
            <p><strong>Timeline:</strong> ${proposal.timeline}</p>
            <p><strong>Price:</strong> ${proposal.price} ${proposal.currency}</p>
            </div>
        `.trim();
    try {
      const blobText = new Blob([textPlain], { type: "text/plain" });
      const blobHtml = new Blob([textHtml], { type: "text/html" });

      await navigator.clipboard.write([
        new ClipboardItem({
          "text/plain": blobText,
          "text/html": blobHtml,
        }),
      ]);
      window.alert("Proposal copied to clipboard.");
    } catch {
      window.alert("Failed to copy proposal to clipboard.");
    }
  }
  return (
    <section ref={proposalRef} className="proposal-card-container">
      <section className="proposal-data-container">
        <p className="proposal-header">PROPOSAL</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Title:</p>
        <p className="proposal-data-content">{proposal.title}</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Introduction:</p>
        <p className="proposal-data-content">{proposal.introduction}</p>
      </section>
      <section className="proposal-data-container proposal-scope-container">
        <p className="proposal-data-header">Scope:</p>
        {proposal.scope.length === 0
          ? "None"
          : proposal.scope.map((s) => (
              <p key={s} className="proposal-data-content">
                &bull; {s}
              </p>
            ))}
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Timeline:</p>
        <p className="proposal-data-content">
          {proposal.timeline ? proposal.timeline : "Not specified"}
        </p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Price:</p>
        <p className="proposal-data-content">
          {proposal.price} {proposal.currency}
        </p>
      </section>
      <section className="proposal-data-container">
        <button
          type="button"
          className="action-button"
          onClick={() => handleCopy()}
        >
          Copy
        </button>
        <button type="button" className="action-button">
          Download PDF
        </button>
      </section>
    </section>
  );
}
