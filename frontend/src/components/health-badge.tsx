"use client";

import { useEffect, useState } from "react";

export function HealthBadge() {
  const [status, setStatus] = useState<"idle" | "ok" | "err">("idle");
  const [detail, setDetail] = useState<string>("");

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const r = await fetch("/api/egide/v1/health");
        const text = await r.text();
        if (cancelled) return;
        if (r.ok) {
          setStatus("ok");
          setDetail(text || "OK");
        } else {
          setStatus("err");
          setDetail(`${r.status} ${text}`);
        }
      } catch (e) {
        if (!cancelled) {
          setStatus("err");
          setDetail(e instanceof Error ? e.message : "Erreur réseau");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const color =
    status === "ok"
      ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
      : status === "err"
        ? "bg-red-500/15 text-red-300 border-red-500/30"
        : "bg-zinc-800 text-zinc-400 border-zinc-700";

  return (
    <div className="flex flex-wrap items-center gap-3">
      <span
        className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium ${color}`}
      >
        {status === "idle" && "Vérification…"}
        {status === "ok" && "API joignable"}
        {status === "err" && "API indisponible"}
      </span>
      {detail && (
        <code className="text-xs text-zinc-500 truncate max-w-md">{detail}</code>
      )}
    </div>
  );
}
