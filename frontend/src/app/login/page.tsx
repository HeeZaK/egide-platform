import Link from "next/link";
import { ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top,_rgba(34,211,238,0.15),_transparent_40%),_#020617] px-6">
      <div className="w-full max-w-md rounded-3xl border border-white/10 bg-slate-900/80 p-8 shadow-2xl shadow-cyan-950/30 backdrop-blur">
        <div className="mb-8 flex items-center gap-4">
          <div className="rounded-2xl bg-cyan-500/10 p-4 text-cyan-300">
            <ShieldCheck className="h-8 w-8" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Égide</p>
            <h1 className="text-2xl font-semibold text-white">Connexion sécurisée</h1>
          </div>
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-4 text-sm text-slate-300">
            Authentification SSO Keycloak RS256 avec environnement souverain.
          </div>
          <Button className="w-full">Se connecter avec SSO</Button>
          <Link href="/dashboard" className="block text-center text-sm text-slate-400 hover:text-white">
            Accéder au mode démo
          </Link>
        </div>
      </div>
    </main>
  );
}
