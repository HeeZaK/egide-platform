"use client";

import { useState } from "react";

export function OsintLookup() {
  const [email, setEmail] = useState("");
  const [persist, setPersist] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const qs = persist ? "?persist=true" : "";
      const r = await fetch(`/api/egide/v1/osint/lookup${qs}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const text = await r.text();
      if (!r.ok) {
        setError(`${r.status}: ${text}`);
        return;
      }
      try {
        const json = JSON.parse(text);
        setResult(JSON.stringify(json, null, 2));
      } catch {
        setResult(text);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={onSubmit} className="space-y-4 max-w-xl">
        <div>
          <label
            htmlFor="email"
            className="block text-sm font-medium text-zinc-300 mb-1.5"
          >
            Adresse e-mail cible
          </label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="prenom.nom@entreprise.fr"
            className="w-full rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/40"
          />
        </div>
        <label className="flex items-center gap-2 text-sm text-zinc-400 cursor-pointer">
          <input
            type="checkbox"
            checked={persist}
            onChange={(e) => setPersist(e.target.checked)}
            className="rounded border-zinc-600 bg-zinc-900 text-emerald-500 focus:ring-emerald-500/40"
          />
          Persister le profil (chiffrement AES-256, clé backend requise)
        </label>
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50 transition-colors"
        >
          {loading ? "Analyse…" : "Lancer l’enrichissement"}
        </button>
      </form>

      {error && (
        <pre className="rounded-lg border border-red-500/30 bg-red-950/40 p-4 text-xs text-red-200 overflow-auto">
          {error}
        </pre>
      )}
      {result && (
        <pre className="rounded-lg border border-zinc-800 bg-black/40 p-4 text-xs text-zinc-300 overflow-auto max-h-[480px]">
          {result}
        </pre>
      )}
    </div>
  );
}
