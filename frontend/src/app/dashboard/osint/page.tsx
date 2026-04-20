"use client";

import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { lookupOsintProfile } from "@/lib/api";
import type { OsintProfile } from "@/lib/types";

export default function OsintPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [profiles, setProfiles] = useState<OsintProfile[]>([]);

  async function handleLookup() {
    if (!email) return;
    setLoading(true);
    setError(null);
    try {
      const res = await lookupOsintProfile(email, false);
      setProfiles((prev) => {
        const exists = prev.find((p) => p.id === res.profile.id);
        return exists ? prev : [res.profile, ...prev];
      });
      setEmail("");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <section className="flex-1 p-6 lg:p-10">
        <Topbar />

        <Card className="mb-6">
          <h3 className="mb-4 text-lg font-semibold text-white">Recherche OSINT</h3>
          <p className="mb-4 text-sm text-slate-400">
            Enrichit un profil via <code className="text-cyan-300">POST /osint/lookup</code>
          </p>
          <div className="flex gap-3">
            <input
              type="email"
              placeholder="prenom.nom@entreprise.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleLookup()}
              className="flex-1 rounded-xl border border-white/10 bg-slate-950 px-4 py-2 text-sm text-white placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
            <Button onClick={handleLookup} disabled={loading}>
              {loading ? "Recherche…" : "Analyser"}
            </Button>
          </div>
          {error && <p className="mt-3 text-sm text-rose-300">{error}</p>}
        </Card>

        <Card>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white">Profils OSINT enrichis</h3>
              <p className="text-sm text-slate-400">Données issues de POST /osint/lookup</p>
            </div>
            <Badge variant={profiles.length > 0 ? "danger" : "default"}>
              {profiles.length} profil{profiles.length > 1 ? "s" : ""}
            </Badge>
          </div>

          {profiles.length === 0 ? (
            <p className="text-sm text-slate-400">Aucun profil analysé — lancez une recherche ci-dessus.</p>
          ) : (
            <div className="space-y-3">
              {profiles.map((p) => (
                <div
                  key={p.id}
                  className="grid gap-3 rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-4 md:grid-cols-5"
                >
                  <div>
                    <p className="font-medium text-white">{p.full_name ?? p.email}</p>
                    <p className="text-xs text-slate-400">{p.email}</p>
                  </div>
                  <p className="text-sm text-slate-300">{p.job_title ?? "—"}</p>
                  <p className="text-sm text-slate-300">{p.company ?? "—"}</p>
                  <p className="text-sm text-slate-300">Brèches: {p.breach_count ?? 0}</p>
                  <p className="text-sm">
                    {p.exposed_on_linkedin ? (
                      <span className="text-amber-300">LinkedIn exposé</span>
                    ) : (
                      <span className="text-emerald-300">Non exposé</span>
                    )}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </section>
    </main>
  );
}
