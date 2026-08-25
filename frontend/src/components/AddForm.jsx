import { useState } from 'react';
import { ROAD_FIELDS } from '../constants/roadFields';

const emptyForm = () => {
  const base = { section_number: '' };
  ROAD_FIELDS.forEach((f) => {
    base[f.name] = '';
  });
  return base;
};

function AddForm({ onAdd }) {
  const [form, setForm] = useState(emptyForm());

  const handleChange = (name, value) => {
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onAdd(form);
    setForm(emptyForm());
  };

  return (
    <div className="add-section">
      <h3>新規データ追加</h3>
      <form className="add-form" onSubmit={handleSubmit}>
        <input
          type="number"
          placeholder="区間番号*"
          value={form.section_number}
          onChange={(e) => handleChange('section_number', e.target.value)}
          required
        />
        {ROAD_FIELDS.map((f) => (
          <input
            key={f.name}
            type={f.type}
            step={f.type === 'number' ? '0.01' : undefined}
            placeholder={f.formLabel + (f.required ? '*' : '')}
            value={form[f.name]}
            onChange={(e) => handleChange(f.name, e.target.value)}
            required={f.required}
          />
        ))}
        <button type="submit">追加</button>
      </form>
    </div>
  );
}

export default AddForm;
