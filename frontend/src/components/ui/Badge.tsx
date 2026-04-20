import { ReactNode } from "react";
import { cn } from "@/lib/utils";

const variants = {
  default: "bg-slate-800 text-slate-100 border border-slate-700",
  success: "bg-emerald-500/15 text-emerald-300 border border-emerald-500/20",
  warning: "bg-amber-500/15 text-amber-300 border border-amber-500/20",
  danger: "bg-rose-500/15 text-rose-300 border border-rose-500/20",
};

interface BadgeProps {
  children: ReactNode;
  variant?: keyof typeof variants;
}

export function Badge({ children, variant = "default" }: BadgeProps) {
  return (
    <span className={cn("inline-flex items-center rounded-full px-3 py-1 text-xs font-medium", variants[variant])}>
      {children}
    </span>
  );
}
