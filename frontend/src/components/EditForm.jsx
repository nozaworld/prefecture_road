import { useEffect, useState } from 'react';
import { ROAD_FIELDS } from '../constants/roadFields';

function EditForm({ road, onUpdate, onCancel }) {
  const [form, setForm] = useState(road);

  useEffect(() => {
    setForm(road);
  }, [road]);

  if (!form) return null;

  const handleChange = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onUpdate(form.id, form);
  };

  return (
    <div className="update-section">
      <h3>データ更新（区間番号: {form.section_number}）</h3>
      <form className="update-form" onSubmit={handleSubmit}>
        {ROAD_FIELDS.map((f) => (
          <input
            key={f.name}
            type={f.type}
            step={f.type === 'number' ? '0.01' : undefined}
            placeholder={f.formLabel}
            value={form[f.name] ?? ''}
            onChange={(e) => handleChange(f.name, e.target.value)}
            required={f.required}
          />
        ))}
        <div className="button-group">
          <button type="submit">更新実行</button>
          <button type="button" onClick={onCancel}>キャンセル</button>
        </div>
      </form>
    </div>
  );
}

export default EditForm;
