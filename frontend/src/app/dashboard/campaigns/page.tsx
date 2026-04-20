"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { generateCampaignScenario, getCampaignScenarios } from "@/lib/api";
import type { SpearPhishingScenario } from "@/lib/types";

const CAMPAIGN_IDS = [
  { id: "campaign-q2-finance", label: "Q2 Payroll Spoofing — Finance" },
  { id: "campaign-ceo-fraud", label: "CEO Fraud — COMEX" },
  { id: "campaign-sso-reset", label: "SSO Reset — All staff" },
];

export default function CampaignsPage() {
  const [selectedCampaign, setSelectedCampaign] = useState(CAMPAIGN_IDS[0].id);
  const [scenarios, setScenarios] = useState<SpearPhishingScenario[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState<string | null>(null);

  useEffect(() => {
    async function fetchScenarios() {
      setLoading(true);
      setError(null);
      try {
        const res = await getCampaignScenarios(selectedCampaign);
        setScenarios(res.scenarios);
        setNote(res.note ?? null);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
        setScenarios([]);
      } finally {
        setLoading(false);
      }
    }
    fetchScenarios();
  }, [selectedCampaign]);

  async function handleGenerate() {
    setGenerating(true);
    setError(null);
    try {
      await generateCampaignScenario(selectedCampaign, {
        campaign_id: selectedCampaign,
        osint_profile_id: "00000000-0000-0000-0000-000000000001",
        target_email: "demo@corp.local",
        attack_vector: "email",
        tone: "urgent",
      });
      // Re-fetch scenarios after generation
      const res = await getCampaignScenarios(selectedCampaign);
      setScenarios(res.scenarios);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />

        <Card className="mb-6">
          <div className="flex flex-wrap items-center gap-3">
            {CAMPAIGN_IDS.map((c) => (
              <button
                key={c.id}
                onClick={() => setSelectedCampaign(c.id)}
                className={`rounded-xl border px-4 py-2 text-sm transition ${
                  selectedCampaign === c.id
                    ? "border-cyan-500 bg-cyan-500/10 text-cyan-300"
                    : "border-white/10 bg-slate-900 text-slate-300 hover:bg-slate-800"
                }`}
              >
                {c.label}
              </button>
            ))}
            <Button onClick={handleGenerate} disabled={generating} className="ml-auto">
              {generating ? "Génération…" : "Générer un scénario"}
            </Button>
          </div>
        </Card>

        <Card>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white">Scénarios de la campagne</h3>
              <p className="text-sm text-slate-400">
                Données via <code className="text-cyan-300">GET /campaigns/{selectedCampaign}/scenarios</code>
              </p>
            </div>
            <Badge variant={scenarios.length > 0 ? "success" : "default"}>
              {scenarios.length} scénario{scenarios.length > 1 ? "s" : ""}
            </Badge>
          </div>

          {error && <p className="mb-4 text-sm text-rose-300">{error}</p>}
          {note && <p className="mb-4 text-sm text-amber-300">{note}</p>}

          {loading ? (
            <p className="text-sm text-slate-400">Chargement…</p>
          ) : scenarios.length === 0 ? (
            <p className="text-sm text-slate-400">
              Aucun scénario persisté — cliquez sur "Générer un scénario" pour en créer un.
            </p>
          ) : (
            <div className="space-y-3">
              {scenarios.map((s) => (
                <div
                  key={s.scenario_id}
                  className="rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-4"
                >
                  <div className="mb-2 flex items-center justify-between">
                    <p className="font-medium text-white">{s.subject}</p>
                    <Badge variant="warning">{s.attack_vector}</Badge>
                  </div>
                  <p className="text-sm text-slate-300">{s.body}</p>
                  <p className="mt-2 text-xs text-slate-500">Cible : {s.target_email} · Ton : {s.tone}</p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </section>
    </main>
  );
}
