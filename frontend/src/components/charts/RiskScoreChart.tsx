"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "@/components/ui/Card";

const data = [
  { month: "Jan", score: 72 },
  { month: "Fév", score: 68 },
  { month: "Mar", score: 63 },
  { month: "Avr", score: 58 },
  { month: "Mai", score: 54 },
  { month: "Juin", score: 49 },
];

export function RiskScoreChart() {
  return (
    <Card className="h-[320px]">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">Évolution du risque humain</h3>
        <p className="text-sm text-slate-400">Score moyen global sur 6 mois</p>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.35} />
              <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="month" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
          <Area type="monotone" dataKey="score" stroke="#22d3ee" fill="url(#riskGradient)" strokeWidth={3} />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  );
}
