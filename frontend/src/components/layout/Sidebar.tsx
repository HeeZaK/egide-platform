import Link from "next/link";
import { Activity, LayoutDashboard, Radar, ShieldAlert } from "lucide-react";

const items = [
  { href: "/dashboard", label: "Vue d'ensemble", icon: LayoutDashboard },
  { href: "/dashboard/campaigns", label: "Campagnes", icon: Activity },
  { href: "/dashboard/osint", label: "OSINT", icon: Radar },
];

export function Sidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-white/10 bg-slate-950/80 p-6 lg:block">
      <div className="flex items-center gap-3">
        <div className="rounded-2xl bg-cyan-500/10 p-3 text-cyan-300">
          <ShieldAlert className="h-6 w-6" />
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Égide</p>
          <h1 className="text-xl font-semibold text-white">Cyber HRM</h1>
        </div>
      </div>

      <nav className="mt-10 space-y-2">
        {items.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="flex items-center gap-3 rounded-xl px-4 py-3 text-slate-300 transition hover:bg-slate-900 hover:text-white"
          >
            <Icon className="h-5 w-5" />
            <span>{label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
