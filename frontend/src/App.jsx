import { useState, useEffect, useCallback } from "react";
import StatsBar from "./components/StatsBar";
import AccountTable from "./components/AccountTable";
import AccountModal from "./components/AccountModal";
import "./App.css";

const API = "https://collections-dashboard-api.onrender.com";

export default function App() {
  const [accounts, setAccounts] = useState([]);
  const [stats, setStats] = useState(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modal, setModal] = useState({ open: false, account: null });
  const [notesPanel, setNotesPanel] = useState({
    open: false,
    account: null,
    notes: [],
  });
  const [noteForm, setNoteForm] = useState({
    outcome: "other",
    note_text: "",
    promise_amount: 0,
    promise_date: "",
  });

  const handleNoteChange = (e) => {
    const { name, value } = e.target;
    setNoteForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleNoteSubmit = async (e) => {
    e.preventDefault();
    await createNote(notesPanel.account.id, noteForm);
    setNoteForm({
      outcome: "other",
      note_text: "",
      promise_amount: 0,
      promise_date: "",
    });
  };

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

  const createNote = async (accountId, noteData) => {
    try {
      const res = await fetch(`${API}/accounts/${accountId}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(noteData),
      });
      if (!res.ok) throw new Error("Failed to create note");
      const data = await res.json();
      setNotesPanel((prev) => ({ ...prev, notes: [...prev.notes, data] }));
    } catch (err) {
      console.error(err);
    }
  };

  const fetchNotes = useCallback(async (accountId) => {
    try {
      const res = await fetch(`${API}/accounts/${accountId}/notes`);
      if (!res.ok) throw new Error("Failed to load notes");
      const data = await res.json();
      setNotesPanel((prev) => ({ ...prev, notes: data }));
    } catch (err) {
      console.error(err);
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
          onOpenNotes={(account) => {
            setNotesPanel({ open: true, account, notes: [] });
            fetchNotes(account.id);
          }}
        />
      </main>

      {notesPanel.open && (
        <div className="modal-overlay">
          <div className="modal-card">
            <div className="modal-header">
              <h2 className="modal-title">
                Notes for {notesPanel.account?.name}
              </h2>
              <button
                className="modal-close"
                onClick={() =>
                  setNotesPanel({ open: false, account: null, notes: [] })
                }
              >
                ❎
              </button>
            </div>
            <form onSubmit={handleNoteSubmit}>
              <select
                name="outcome"
                value={noteForm.outcome}
                onChange={handleNoteChange}
              >
                <option value="other">Other</option>
                <option value="promise_to_pay">Promise Made</option>
                <option value="payment_made">Payment Received</option>
              </select>
              <input
                type="text"
                name="note_text"
                value={noteForm.note_text}
                onChange={handleNoteChange}
                placeholder="Enter note text"
              />
              <input
                type="number"
                name="promise_amount"
                value={noteForm.promise_amount}
                onChange={handleNoteChange}
                placeholder="Enter promise amount"
              />
              <input
                type="date"
                name="promise_date"
                value={noteForm.promise_date}
                onChange={handleNoteChange}
              />
              <button type="submit">Add Note</button>
            </form>
            <ul>
              {notesPanel.notes.map((note, index) => (
                <li key={index}>{note.note_text}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

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
