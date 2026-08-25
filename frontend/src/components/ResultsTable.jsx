import { ROAD_FIELDS } from '../constants/roadFields';

function ResultsTable({ roads, selectedIds, onSelectionChange, onEdit }) {
  const toggle = (id) => {
    if (selectedIds.includes(id)) {
      onSelectionChange(selectedIds.filter((v) => v !== id));
    } else {
      onSelectionChange([...selectedIds, id]);
    }
  };

  return (
    <div className="grid-section">
      <table>
        <thead>
          <tr>
            <th>No</th>
            {ROAD_FIELDS.map((f) => (
              <th key={f.name}>{f.label}</th>
            ))}
            <th>選択</th>
            <th>編集</th>
          </tr>
        </thead>
        <tbody>
          {roads.length === 0 ? (
            <tr><td colSpan={ROAD_FIELDS.length + 3}>検索結果がありません</td></tr>
          ) : (
            roads.map((road, idx) => (
              <tr key={road.id}>
                <td>{idx + 1}</td>
                {ROAD_FIELDS.map((f) => (
                  <td key={f.name}>{road[f.name]}</td>
                ))}
                <td>
                  <input
                    type="checkbox"
                    checked={selectedIds.includes(road.id)}
                    onChange={() => toggle(road.id)}
                  />
                </td>
                <td>
                  <button type="button" className="edit-btn" onClick={() => onEdit(road)}>編集</button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ResultsTable;
