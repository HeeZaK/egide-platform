import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 py-20 bg-gradient-to-b from-zinc-950 via-zinc-950 to-zinc-900">
      <div className="max-w-lg text-center space-y-6">
        <p className="text-xs uppercase tracking-[0.25em] text-emerald-500/90">
          Souveraineté des données
        </p>
        <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-white">
          Égide
        </h1>
        <p className="text-zinc-400 text-sm leading-relaxed">
          MVP Human Risk Management : OSINT passif, contrôle de fuites mocké,
          persistance chiffrée et tableau de bord RSSI. Prochaines étapes :
          campagnes IA et War Room.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center pt-4">
          <Link
            href="/dashboard"
            className="inline-flex justify-center rounded-lg bg-emerald-600 px-6 py-3 text-sm font-medium text-white hover:bg-emerald-500 transition-colors"
          >
            Ouvrir le tableau de bord
          </Link>
          <Link
            href="/login"
            className="inline-flex justify-center rounded-lg border border-zinc-600 px-6 py-3 text-sm text-zinc-300 hover:bg-zinc-800/80 transition-colors"
          >
            Configurer le jeton
          </Link>
        </div>
      </div>
    </div>
  );
}
