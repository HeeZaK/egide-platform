import Link from "next/link";

const nav = [
  { href: "/dashboard", label: "Vue d’ensemble" },
  { href: "/dashboard/osint", label: "OSINT" },
  { href: "/dashboard/campaigns", label: "Campagnes" },
  { href: "/dashboard/war-room", label: "War Room" },
  { href: "/login", label: "Jeton API" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex bg-zinc-950 text-zinc-100">
      <aside className="w-60 shrink-0 border-r border-zinc-800/80 p-5 flex flex-col gap-1">
        <Link href="/" className="mb-6 block">
          <span className="text-lg font-semibold tracking-tight text-emerald-400">
            Égide
          </span>
          <span className="block text-[10px] uppercase tracking-[0.2em] text-zinc-500 mt-1">
            Human Risk
          </span>
        </Link>
        <nav className="flex flex-col gap-0.5">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-md px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800/80 hover:text-white transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 min-w-0 p-6 sm:p-10">{children}</main>
    </div>
  );
}
