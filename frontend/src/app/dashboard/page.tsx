import { CampaignChart } from "@/components/charts/CampaignChart";
import { RiskScoreChart } from "@/components/charts/RiskScoreChart";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";
import { computeRiskScoreBatch } from "@/lib/api";
import type { RiskInput, RiskScoreReport } from "@/lib/types";

// Mock dataset — replace with DB query when persistence layer is ready
const MOCK_TARGETS: RiskInput[] = [
  {
    target_email: "camille.r@corp.local",
    osint_profile_id: "00000000-0000-0000-0000-000000000001",
    seniority: "director",
    exposed_on_linkedin: true,
    breached: true,
    breach_count: 5,
    breach_includes_passwords: true,
    completed_training_modules: 1,
    total_training_modules: 8,
  },
  {
    target_email: "nassim.b@corp.local",
    osint_profile_id: "00000000-0000-0000-0000-000000000002",
    seniority: "senior",
    exposed_on_linkedin: true,
    breached: true,
    breach_count: 3,
    completed_training_modules: 3,
    total_training_modules: 8,
  },
  {
    target_email: "laura.m@corp.local",
    osint_profile_id: "00000000-0000-0000-0000-000000000003",
    seniority: "manager",
    exposed_on_linkedin: true,
    breached: true,
    breach_count: 4,
    breach_includes_passwords: true,
    completed_training_modules: 2,
    total_training_modules: 8,
  },
  {
    target_email: "yanis.t@corp.local",
    osint_profile_id: "00000000-0000-0000-0000-000000000004",
    seniority: "mid",
    exposed_on_linkedin: false,
    breached: true,
    breach_count: 2,
    completed_training_modules: 5,
    total_training_modules: 8,
  },
];

const gradeColor: Record<string, string> = {
  A: "text-emerald-300",
  B: "text-green-300",
  C: "text-amber-300",
  D: "text-orange-300",
  E: "text-rose-300",
  F: "text-red-400",
};

async function getDashboardData(): Promise<RiskScoreReport[]> {
  try {
    return await computeRiskScoreBatch(MOCK_TARGETS);
  } catch {
    // Backend unavailable — return empty to keep UI functional
    return [];
  }
}

export default async function DashboardPage() {
  const reports = await getDashboardData();

  const avgScore =
    reports.length > 0
      ? Math.round(reports.reduce((s, r) => s + r.score, 0) / reports.length)
      : null;

  const highRisk = reports.filter((r) => ["E", "F"].includes(r.grade));
  const criticalCount = reports.filter((r) => r.grade === "F").length;

  const metrics = [
    {
      label: "Score moyen global",
      value: avgScore !== null ? `${avgScore}/100` : "—",
      delta: avgScore !== null ? `Grade ${reports[0]?.grade ?? "—"}` : "Backend hors ligne",
    },
    {
      label: "Profils analysés",
      value: reports.length > 0 ? String(reports.length) : "—",
      delta: `${highRisk.length} à risque élevé`,
    },
    {
      label: "Profils critiques (F)",
      value: String(criticalCount),
      delta: criticalCount > 0 ? "Action immédiate requise" : "Aucun profil F",
    },
    {
      label: "Recommandations",
      value: String(reports.reduce((s, r) => s + r.recommendations.length, 0)),
      delta: "Actions RSSI disponibles",
    },
  ];

  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {metrics.map((m) => (
            <StatCard key={m.label} {...m} />
          ))}
        </div>

        <div className="mt-6 grid gap-6 xl:grid-cols-2">
          <RiskScoreChart />
          <CampaignChart />
        </div>

        <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <Card>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white">Scores de risque — temps réel</h3>
                <p className="text-sm text-slate-400">Données calculées via POST /risk/score/batch</p>
              </div>
              <Badge variant="warning">{highRisk.length} prioritaires</Badge>
            </div>

            {reports.length === 0 ? (
              <p className="text-sm text-slate-400">Backend indisponible — démarrez docker compose up --build</p>
            ) : (
              <div className="space-y-3">
                {reports.map((report) => (
                  <div
                    key={report.report_id}
                    className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3"
                  >
                    <div>
                      <p className="font-medium text-white">{report.target_email}</p>
                      <p className="text-xs text-slate-400">
                        {report.factors.length} facteurs analysés
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-slate-400">Score {Math.round(report.score)}/100</p>
                      <p className={`font-semibold ${gradeColor[report.grade] ?? "text-white"}`}>
                        Grade {report.grade}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card>
            <h3 className="text-lg font-semibold text-white">Recommandations RSSI</h3>
            <div className="mt-4 space-y-2">
              {reports.length === 0 ? (
                <p className="text-sm text-slate-400">Aucune donnée</p>
              ) : (
                [...new Set(reports.flatMap((r) => r.recommendations))]
                  .slice(0, 5)
                  .map((rec, i) => (
                    <div
                      key={i}
                      className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-3 text-sm text-slate-300"
                    >
                      {rec}
                    </div>
                  ))
              )}
            </div>
          </Card>
        </div>
      </section>
    </main>
  );
}
