import { useState, useEffect, useCallback } from "react";
import StatsBar from "./components/StatsBar";
import AccountTable from "./components/AccountTable";
import AccountModal from "./components/AccountModal";
import "./App.css";

const API = "/api";

export default function App() {
  const [accounts, setAccounts] = useState([]);
  const [stats, setStats] = useState(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modal, setModal] = useState({ open: false, account: null });

  const fetchAccounts = useCallback(async () => {
    try {
      setLoading(true);
      const url =
        statusFilter === "all"
          ? `${API}/accounts`
          : `${API}/accounts?status=${statusFilter}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to load accounts");
      const data = await res.json();
      setAccounts(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  const fetchStats = useCallback(async () => {
    try {
      const res = await fetch(`${API}/accounts/stats`);
      if (!res.ok) return;
      const data = await res.json();
      setStats(data);
    } catch {
      /* non-fatal */
    }
  }, []);

  useEffect(() => {
    fetchAccounts();
    fetchStats();
  }, [fetchAccounts, fetchStats]);

  const handleSave = async (formData, id) => {
    const url = id ? `${API}/accounts/${id}` : `${API}/accounts`;
    const method = id ? "PUT" : "POST";
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    if (!res.ok) throw new Error("Save Failed");
    setModal({ open: false, account: null });
    fetchAccounts();
    fetchStats();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this account?")) return;
    await fetch(`${API}/accounts/${id}`, { method: "DELETE" });
    fetchAccounts();
    fetchStats();
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-inner">
          <div>
            <h1 className="app-title">Collections Dashboard</h1>
            <p className="app-subtitle">Account receivables management</p>
          </div>
          <button
            className="btn btn-primary"
            onClick={() => setModal({ open: true, account: null })}
          >
            + Add Account
          </button>
        </div>
      </header>

      <main className="app-main">
        {stats && <StatsBar stats={stats} />}

        <div className="filter-bar">
          {["all", "current", "delinquent", "charged_off"].map((s) => (
            <button
              key={s}
              className={`filter-btn ${statusFilter === s ? "active" : ""} filter-${s}`}
              onClick={() => setStatusFilter(s)}
            >
              {s === "all"
                ? "All Accounts"
                : s.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
            </button>
          ))}
        </div>

        {error && <div className="error-banner">{error}</div>}

        <AccountTable
          accounts={accounts}
          loading={loading}
          onEdit={(account) => setModal({ open: true, account })}
          onDelete={handleDelete}
        />
      </main>

      {modal.open && (
        <AccountModal
          account={modal.account}
          onSave={handleSave}
          onClose={() => setModal({ open: false, account: null })}
        />
      )}
    </div>
  );
}
