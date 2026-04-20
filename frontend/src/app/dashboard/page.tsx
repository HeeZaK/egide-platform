import { HealthBadge } from "@/components/health-badge";

export default function DashboardPage() {
  return (
    <div className="max-w-3xl space-y-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-white">
          Tableau de bord RSSI
        </h1>
        <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
          Point d’entrée pour les modules MVP : état de l’API, enrichissement OSINT
          passif, et prochainement campagnes et War Room.
        </p>
      </div>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-6">
        <h2 className="text-sm font-medium text-zinc-300 mb-4">API backend</h2>
        <HealthBadge />
      </section>

      <section className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-6 text-sm text-zinc-400">
        <p>
          Les appels passent par la route Next{" "}
          <code className="text-emerald-400/90">/api/egide/…</code> (proxy
          serveur). Déposez un jeton Keycloak (rôle RSSI) depuis la page{" "}
          <span className="text-zinc-200">Jeton API</span> pour les actions
          protégées.
        </p>
      </section>
    </div>
  );
}
