import { Bell, Search } from "lucide-react";
import { Badge } from "@/components/ui/Badge";

export function Topbar() {
  return (
    <div className="mb-8 flex flex-col gap-4 border-b border-white/10 pb-6 md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-sm text-cyan-300">Tableau de bord RSSI</p>
        <h2 className="text-3xl font-semibold text-white">Pilotage du risque humain</h2>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-slate-900 px-4 py-2 text-slate-400">
          <Search className="h-4 w-4" />
          <span className="text-sm">Rechercher un collaborateur</span>
        </div>
        <button className="rounded-xl border border-white/10 bg-slate-900 p-3 text-slate-300">
          <Bell className="h-4 w-4" />
        </button>
        <Badge variant="success">Score global B</Badge>
      </div>
    </div>
  );
}
