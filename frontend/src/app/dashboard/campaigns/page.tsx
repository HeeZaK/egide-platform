import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

const campaigns = [
  { name: "Q2 Payroll Spoofing", target: "Finance", sent: 120, clicked: 14, reported: 31, status: "active" },
  { name: "CEO Fraud - COMEX", target: "Executive", sent: 25, clicked: 2, reported: 9, status: "planned" },
  { name: "SSO Reset", target: "All staff", sent: 640, clicked: 38, reported: 210, status: "completed" },
];

export default function CampaignsPage() {
  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />
        <Card>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white">Campagnes de simulation</h3>
              <p className="text-sm text-slate-400">Suivi des scénarios de social engineering</p>
            </div>
            <Badge variant="success">3 campagnes</Badge>
          </div>

          <div className="space-y-3">
            {campaigns.map((campaign) => (
              <div key={campaign.name} className="grid gap-3 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-4 md:grid-cols-5">
                <div>
                  <p className="font-medium text-white">{campaign.name}</p>
                  <p className="text-sm text-slate-400">{campaign.target}</p>
                </div>
                <p className="text-sm text-slate-300">Envoyés: {campaign.sent}</p>
                <p className="text-sm text-orange-300">Clics: {campaign.clicked}</p>
                <p className="text-sm text-emerald-300">Signalés: {campaign.reported}</p>
                <p className="text-sm text-slate-400">Statut: {campaign.status}</p>
              </div>
            ))}
          </div>
        </Card>
      </section>
    </main>
  );
}
