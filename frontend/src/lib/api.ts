import type {
  CampaignScenariosResponse,
  OsintEnrichmentResponse,
  RiskInput,
  RiskScoreReport,
} from "./types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// ─── Generic fetch wrapper ────────────────────────────────────────────────────
async function apiFetch<T>(
  path: string,
  init?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`[${res.status}] ${detail}`);
  }

  return res.json() as Promise<T>;
}

// ─── Risk ─────────────────────────────────────────────────────────────────────
export async function computeRiskScore(
  payload: RiskInput
): Promise<RiskScoreReport> {
  return apiFetch<RiskScoreReport>("/risk/score", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function computeRiskScoreBatch(
  payloads: RiskInput[]
): Promise<RiskScoreReport[]> {
  return apiFetch<RiskScoreReport[]>("/risk/score/batch", {
    method: "POST",
    body: JSON.stringify(payloads),
  });
}

// ─── OSINT ────────────────────────────────────────────────────────────────────
export async function lookupOsintProfile(
  email: string,
  persist = false
): Promise<OsintEnrichmentResponse> {
  return apiFetch<OsintEnrichmentResponse>(
    `/osint/lookup?persist=${persist}`,
    {
      method: "POST",
      body: JSON.stringify({ email }),
    }
  );
}

export async function getOsintProfile(
  profileId: string
): Promise<OsintEnrichmentResponse["profile"]> {
  return apiFetch(`/osint/profiles/${profileId}`);
}

// ─── Campaigns ────────────────────────────────────────────────────────────────
export async function getCampaignScenarios(
  campaignId: string
): Promise<CampaignScenariosResponse> {
  return apiFetch<CampaignScenariosResponse>(
    `/campaigns/${campaignId}/scenarios`
  );
}

export async function generateCampaignScenario(
  campaignId: string,
  payload: {
    campaign_id: string;
    osint_profile_id: string;
    target_email: string;
    attack_vector?: string;
    tone?: string;
  }
) {
  return apiFetch(`/campaigns/${campaignId}/scenarios/generate`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
