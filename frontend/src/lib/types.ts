export type RiskGrade = "A" | "B" | "C" | "D" | "E" | "F";

export interface RiskTrendPoint {
  month: string;
  score: number;
}

export interface CampaignPoint {
  name: string;
  sent: number;
  clicked: number;
  reported: number;
}

export interface DashboardMetric {
  label: string;
  value: string;
  delta: string;
}

export interface OsintProfile {
  id: string;
  fullName: string;
  role: string;
  department: string;
  breachCount: number;
  riskGrade: RiskGrade;
}
