import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

const profiles = [
  { name: "Camille R.", department: "Finance", exposure: "Very high", breaches: 5, grade: "E" },
  { name: "Nassim B.", department: "Executive", exposure: "High", breaches: 3, grade: "D" },
  { name: "Laura M.", department: "Sales", exposure: "Very high", breaches: 4, grade: "E" },
  { name: "Yanis T.", department: "HR", exposure: "Moderate", breaches: 2, grade: "D" },
];

export default function OsintPage() {
  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />
        <Card>
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white">Profils OSINT</h3>
              <p className="text-sm text-slate-400">Analyse des collaborateurs les plus exposés</p>
            </div>
            <Badge variant="danger">4 profils critiques</Badge>
          </div>

          <div className="space-y-3">
            {profiles.map((profile) => (
              <div key={profile.name} className="grid gap-3 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-4 md:grid-cols-5">
                <p className="font-medium text-white">{profile.name}</p>
                <p className="text-sm text-slate-300">{profile.department}</p>
                <p className="text-sm text-slate-300">Exposition: {profile.exposure}</p>
                <p className="text-sm text-slate-300">Brèches: {profile.breaches}</p>
                <p className="font-semibold text-rose-300">Grade {profile.grade}</p>
              </div>
            ))}
          </div>
        </Card>
      </section>
    </main>
  );
}
