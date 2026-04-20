import { ArrowUpRight } from "lucide-react";
import { Card } from "@/components/ui/Card";

interface StatCardProps {
  label: string;
  value: string;
  delta: string;
}

export function StatCard({ label, value, delta }: StatCardProps) {
  return (
    <Card>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400">{label}</p>
          <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
        </div>
        <div className="rounded-xl bg-cyan-500/10 p-2 text-cyan-300">
          <ArrowUpRight className="h-5 w-5" />
        </div>
      </div>
      <p className="mt-4 text-sm text-emerald-300">{delta}</p>
    </Card>
  );
}
