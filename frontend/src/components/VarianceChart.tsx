import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { CategorySummary } from "../types/budgetLine";

interface Props {
  categories: CategorySummary[];
}

const COLOR_DEPASSEMENT = "var(--diverging-positive)";
const COLOR_ECONOMIE = "var(--diverging-negative)";

interface TooltipPayloadItem {
  payload: CategorySummary & { ecart: number };
}

function ChartTooltip({ active, payload }: { active?: boolean; payload?: TooltipPayloadItem[] }) {
  if (!active || !payload || payload.length === 0) return null;
  const data = payload[0].payload;
  return (
    <div
      style={{
        background: "var(--surface-1)",
        border: "1px solid var(--border)",
        borderRadius: 4,
        padding: 8,
        color: "var(--text-primary)",
        fontSize: "0.85rem",
      }}
    >
      <strong>{data.categorie}</strong>
      <div>Prévu : {data.total_prevu}</div>
      <div>Réalisé : {data.total_realise}</div>
      <div>Écart : {data.ecart_valeur}</div>
    </div>
  );
}

export default function VarianceChart({ categories }: Props) {
  if (categories.length === 0) {
    return <p>Pas encore de données pour le graphique.</p>;
  }

  const data = categories.map((c) => ({ ...c, ecart: Number(c.ecart_valeur) }));

  return (
    <div>
      <div className="legend">
        <span>
          <span className="legend-swatch" style={{ background: COLOR_DEPASSEMENT }} />
          Dépassement
        </span>
        <span>
          <span className="legend-swatch" style={{ background: COLOR_ECONOMIE }} />
          Économie
        </span>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 8 }}>
          <CartesianGrid stroke="var(--gridline)" vertical={false} />
          <XAxis dataKey="categorie" stroke="var(--text-muted)" tick={{ fontSize: 12 }} />
          <YAxis stroke="var(--text-muted)" tick={{ fontSize: 12 }} />
          <ReferenceLine y={0} stroke="var(--baseline)" />
          <Tooltip content={<ChartTooltip />} />
          <Bar dataKey="ecart" radius={[4, 4, 0, 0]} maxBarSize={24}>
            {data.map((entry) => (
              <Cell
                key={entry.categorie}
                fill={entry.ecart >= 0 ? COLOR_DEPASSEMENT : COLOR_ECONOMIE}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
