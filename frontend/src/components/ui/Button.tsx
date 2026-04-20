import { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary";
}

export function Button({ children, className, variant = "primary", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-medium transition",
        variant === "primary"
          ? "bg-cyan-500 text-slate-950 hover:bg-cyan-400"
          : "bg-slate-800 text-slate-100 hover:bg-slate-700",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
