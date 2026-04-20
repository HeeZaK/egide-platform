"use client";

import { useState } from "react";
import Link from "next/link";

export default function LoginPage() {
  const [token, setToken] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  async function save(e: React.FormEvent) {
    e.preventDefault();
    setMsg(null);
    const r = await fetch("/api/auth/session", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      setMsg((j as { error?: string }).error ?? "Erreur");
      return;
    }
    setMsg("Jeton enregistré (cookie httpOnly). Vous pouvez ouvrir le tableau de bord.");
  }

  async function clear() {
    await fetch("/api/auth/session", { method: "DELETE" });
    setToken("");
    setMsg("Session effacée.");
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-md rounded-xl border border-zinc-800 bg-zinc-900/50 p-8 shadow-xl">
        <Link
          href="/dashboard"
          className="text-xs text-emerald-400 hover:text-emerald-300"
        >
          ← Tableau de bord
        </Link>
        <h1 className="mt-4 text-xl font-semibold text-white">Jeton API</h1>
        <p className="mt-2 text-sm text-zinc-400">
          Collez un access token Keycloak (rôle RSSI) pour que le proxy Next
          l’envoie au backend sur les routes protégées.
        </p>
        <form onSubmit={save} className="mt-6 space-y-4">
          <textarea
            value={token}
            onChange={(e) => setToken(e.target.value)}
            rows={6}
            placeholder="eyJhbGciOiJSUzI1NiIs..."
            className="w-full rounded-lg border border-zinc-700 bg-black/50 px-3 py-2 text-xs font-mono text-zinc-200 focus:outline-none focus:ring-2 focus:ring-emerald-500/40"
          />
          <div className="flex gap-2">
            <button
              type="submit"
              className="flex-1 rounded-lg bg-emerald-600 py-2 text-sm font-medium text-white hover:bg-emerald-500"
            >
              Enregistrer
            </button>
            <button
              type="button"
              onClick={clear}
              className="rounded-lg border border-zinc-600 px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-800"
            >
              Effacer
            </button>
          </div>
        </form>
        {msg && (
          <p className="mt-4 text-sm text-zinc-300 border-t border-zinc-800 pt-4">
            {msg}
          </p>
        )}
      </div>
    </div>
  );
}
