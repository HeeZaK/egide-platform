"use client";

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card } from "@/components/ui/Card";

const data = [
  { name: "Finance", sent: 120, clicked: 14, reported: 31 },
  { name: "RH", sent: 80, clicked: 11, reported: 18 },
  { name: "IT", sent: 96, clicked: 4, reported: 42 },
  { name: "Sales", sent: 140, clicked: 27, reported: 25 },
];

export function CampaignChart() {
  return (
    <Card className="h-[320px]">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-white">Campagnes de sensibilisation</h3>
        <p className="text-sm text-slate-400">Envois, clics et signalements</p>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip contentStyle={{ backgroundColor: "#0f172a", border: "1px solid #334155" }} />
          <Legend />
          <Bar dataKey="sent" fill="#0891b2" radius={[6, 6, 0, 0]} />
          <Bar dataKey="clicked" fill="#f97316" radius={[6, 6, 0, 0]} />
          <Bar dataKey="reported" fill="#22c55e" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
