export interface Message {
  content: string;
}

export interface Requirement {
  service: string;
  details: string[];
}
export interface Analysis {
  service_type: string;
  client_summary: string;
  requirements: Requirement[];
  scope: string;
  timeline: string | null;
  budget: string | null;
  missing_information: string[];
  assumptions: string[];
}
