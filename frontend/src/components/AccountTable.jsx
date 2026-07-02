import "./AccountTable.css";

const STATUS_LABELS = {
  current: "Current",
  delinquent: "Delinquent",
  charged_off: "Charged Off",
};

const fmt = (n) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(
    n,
  );

export default function AccountTable({ accounts, loading, onEdit, onDelete }) {
  if (loading) {
    return (
      <div className="table-card">
        <div className="table-empty">Loading accounts…</div>
      </div>
    );
  }

  if (accounts.length === 0) {
    return (
      <div className="table-card">
        <div className="table-empty">No accounts found.</div>
      </div>
    );
  }

  return (
    <div className="table-card">
      <div className="table-scroll">
        <table className="acct-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Balance</th>
              <th>Days Past Due</th>
              <th>Status</th>
              <th>Phone</th>
              <th>Email</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((a) => (
              <tr key={a.id}>
                <td className="name-cell">{a.name}</td>
                <td className="balance-cell">{fmt(a.balance)}</td>
                <td>
                  <span
                    className={`dpd ${a.days_past_due > 90 ? "dpd-high" : a.days_past_due > 30 ? "dpd-mid" : ""}`}
                  >
                    {a.days_past_due}
                  </span>
                </td>
                <td>
                  <span className={`badge badge-${a.status}`}>
                    {STATUS_LABELS[a.status] ?? a.status}
                  </span>
                </td>
                <td className="muted">{a.phone ?? "—"}</td>
                <td className="muted">{a.email ?? "—"}</td>
                <td className="actions-cell">
                  <button className="btn-ghost" onClick={() => onEdit(a)}>
                    Edit
                  </button>
                  <button className="btn-danger" onClick={() => onDelete(a.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="table-footer">
        {accounts.length} account{accounts.length !== 1 ? "s" : ""}
      </p>
    </div>
  );
}
