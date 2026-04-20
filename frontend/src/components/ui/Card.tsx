import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface CardProps {
  className?: string;
  children: ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn("rounded-2xl border border-white/10 bg-slate-900/70 p-6 shadow-xl shadow-black/10 backdrop-blur", className)}>
      {children}
    </div>
  );
}
