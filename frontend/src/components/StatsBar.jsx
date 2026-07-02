import "./StatsBar.css";

const fmt = (n) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(
    n,
  );

export default function StatsBar({ stats }) {
  if (!stats) return null;

  const delinqBal = stats.total_delinquent_balance ?? 0;
  const chargedBal = stats.total_charged_off_balance ?? 0;

  const cards = [
    {
      label: "Total Accounts",
      value: stats.total_accounts ?? 0,
      sub: `${stats.current_count ?? 0} current`,
      color: "blue",
    },
    {
      label: "Delinquent",
      value: stats.delinquent_count ?? 0,
      sub: fmt(delinqBal),
      color: "yellow",
    },
    {
      label: "Charged Off",
      value: stats.charged_off_count ?? 0,
      sub: fmt(chargedBal),
      color: "red",
    },
    {
      label: "Total Exposure",
      value: fmt(delinqBal + chargedBal),
      sub: "delinquent + charged off",
      color: "purple",
    },
  ];

  return (
    <div className="stats-bar">
      {cards.map((c) => (
        <div key={c.label} className={`stat-card stat-${c.color}`}>
          <p className="stat-label">{c.label}</p>
          <p className="stat-value">{c.value}</p>
          <p className="stat-sub">{c.sub}</p>
        </div>
      ))}
    </div>
  );
}
