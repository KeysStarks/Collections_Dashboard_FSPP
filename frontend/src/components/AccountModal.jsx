import { useState } from "react";
import "./AccountModal.css";

export default function AccountModal({ account, onSave, onClose }) {
  const [formData, setFormData] = useState({
    name: account?.name ?? "",
    balance: account?.balance ?? "",
    days_past_due: account?.days_past_due ?? "",
    status: account?.status ?? "current",
    phone: account?.phone ?? "",
    email: account?.email ?? "",
  });

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await onSave(
        {
          ...formData,
          balance: parseFloat(formData.balance) || 0,
          days_past_due: parseInt(formData.days_past_due) || 0,
        },
        account?.id,
      );
    } catch (err) {
      setError("Something went wrong. Try again.");
      setSaving(false);
    }
  };

  const isEditing = Boolean(account);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            {isEditing ? "Edit Account" : "Add Account"}
          </h2>
          <button className="modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Full Name *</label>
            <input
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Marcus Johnson"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Balance ($)</label>
              <input
                name="balance"
                type="number"
                min="0"
                step="0.01"
                value={formData.balance}
                onChange={handleChange}
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label>Days Past Due</label>
              <input
                name="days_past_due"
                type="number"
                min="0"
                value={formData.days_past_due}
                onChange={handleChange}
                placeholder="0"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="current">Current</option>
              <option value="delinquent">Delinquent</option>
              <option value="charged_off">Charged Off</option>
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Phone</label>
              <input
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="555-000-0000"
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="name@email.com"
              />
            </div>
          </div>

          {error && <p className="modal-error">{error}</p>}

          <div className="modal-actions">
            <button type="button" className="btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={saving}>
              {saving ? "Saving…" : isEditing ? "Save Changes" : "Add Account"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
