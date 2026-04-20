import { CampaignChart } from "@/components/charts/CampaignChart";
import { RiskScoreChart } from "@/components/charts/RiskScoreChart";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { StatCard } from "@/components/ui/StatCard";

const metrics = [
  { label: "Collaborateurs monitorés", value: "1 248", delta: "+8.2% ce mois" },
  { label: "Profils à risque élevé", value: "73", delta: "-12% vs mois dernier" },
  { label: "Campagnes actives", value: "12", delta: "+3 nouvelles campagnes" },
  { label: "Taux de signalement", value: "34%", delta: "+6 points" },
];

const highRiskProfiles = [
  { name: "Camille R.", role: "Finance Director", grade: "E", breaches: 5 },
  { name: "Nassim B.", role: "Executive Assistant", grade: "D", breaches: 3 },
  { name: "Laura M.", role: "Head of Sales", grade: "E", breaches: 4 },
  { name: "Yanis T.", role: "HR Manager", grade: "D", breaches: 2 },
];

export default function DashboardPage() {
  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {metrics.map((metric) => (
            <StatCard key={metric.label} {...metric} />
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
                <h3 className="text-lg font-semibold text-white">Profils prioritaires</h3>
                <p className="text-sm text-slate-400">Cibles à surveiller en priorité</p>
              </div>
              <Badge variant="warning">Action requise</Badge>
            </div>
            <div className="space-y-3">
              {highRiskProfiles.map((profile) => (
                <div key={profile.name} className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3">
                  <div>
                    <p className="font-medium text-white">{profile.name}</p>
                    <p className="text-sm text-slate-400">{profile.role}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-slate-400">{profile.breaches} brèches</p>
                    <p className="font-semibold text-rose-300">Grade {profile.grade}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <h3 className="text-lg font-semibold text-white">Recommandations RSSI</h3>
            <div className="mt-4 space-y-3 text-sm text-slate-300">
              <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 p-4">Lancer une campagne ciblée Finance + COMEX.</div>
              <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 p-4">Renforcer MFA sur les profils exposés LinkedIn.</div>
              <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4">Maintenir le taux de signalement au-dessus de 30%.</div>
            </div>
          </Card>
        </div>
      </section>
    </main>
  );
}
