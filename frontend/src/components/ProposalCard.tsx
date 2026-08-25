import type { Proposal } from "../types/types";

type ProposalCardProps = {
  proposal: Proposal;
};

export default function ProposalCard({ proposal }: ProposalCardProps) {
  return (
    <section className="proposal-card-container">
      <section className="proposal-data-container">
        <p className="proposal-data-header">Title:</p>
        <p className="proposal-data-content">{proposal.title}</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Introduction</p>
        <p className="proposal-data-content">{proposal.introduction}</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Scope</p>
        <p className="proposal-data-content"></p>
        {proposal.scope.map((s) => (
          <p key={s} className="proposal-data-content">
            {s}
          </p>
        ))}
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Timeline:</p>
        <p className="proposal-data-content">{proposal.timeline}</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Price:</p>
        <p className="proposal-data-content">{proposal.price}</p>
      </section>
      <section className="proposal-data-container">
        <p className="proposal-data-header">Currency:</p>
        <p className="proposal-data-content">{proposal.currency}</p>
      </section>
    </section>
  );
}
