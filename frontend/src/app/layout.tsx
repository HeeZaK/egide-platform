import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Égide Platform",
  description: "Plateforme souveraine de Human Risk Management",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="fr">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">{children}</body>
    </html>
  );
}
