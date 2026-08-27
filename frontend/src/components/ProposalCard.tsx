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
    </section>
  );
}
