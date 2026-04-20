// ─── Risk ────────────────────────────────────────────────────────────────────
export type RiskGrade = "A" | "B" | "C" | "D" | "E" | "F";

export interface PhishingOutcome {
  scenario_id: string;
  clicked_link: boolean;
  submitted_credentials: boolean;
}

export interface RiskInput {
  target_email: string;
  osint_profile_id: string;
  seniority?: string;
  exposed_on_linkedin?: boolean;
  company_employee_count?: number;
  breached?: boolean;
  breach_count?: number;
  breach_includes_passwords?: boolean;
  phishing_outcomes?: PhishingOutcome[];
  completed_training_modules?: number;
  total_training_modules?: number;
}

export interface RiskFactor {
  name: string;
  description: string;
  weight: number;
  raw_value: number;
  weighted_contribution: number;
}

export interface RiskScoreReport {
  report_id: string;
  target_email: string;
  osint_profile_id: string;
  score: number;
  grade: RiskGrade;
  factors: RiskFactor[];
  recommendations: string[];
  computed_at: string;
  tags: string[];
}

// ─── OSINT ───────────────────────────────────────────────────────────────────
export interface OsintProfile {
  id: string;
  email: string;
  full_name?: string;
  company?: string;
  job_title?: string;
  seniority?: string;
  exposed_on_linkedin?: boolean;
  breach_count?: number;
  breached?: boolean;
  breach_includes_passwords?: boolean;
}

export interface OsintEnrichmentResponse {
  profile: OsintProfile;
  persisted: boolean;
}

// ─── Campaigns ───────────────────────────────────────────────────────────────
export interface SpearPhishingScenario {
  scenario_id: string;
  campaign_id: string;
  target_email: string;
  subject: string;
  body: string;
  attack_vector: string;
  tone: string;
  generated_at: string;
}

export interface CampaignScenariosResponse {
  campaign_id: string;
  scenarios: SpearPhishingScenario[];
  note?: string;
}
