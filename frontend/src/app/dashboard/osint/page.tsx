import { OsintLookup } from "./osint-lookup";

export default function OsintPage() {
  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-white">
          OSINT passif
        </h1>
        <p className="mt-2 text-sm text-zinc-400 leading-relaxed">
          Enrichissement B2B mocké et contrôle de fuites (HIBP mock). Les données
          sensibles au repos sont chiffrées côté backend si vous activez la
          persistance.
        </p>
      </div>
      <OsintLookup />
    </div>
  );
}
