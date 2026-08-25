import { ROAD_FIELDS } from '../constants/roadFields';

function ResultsTable({ roads, startIndex, selectedIds, onSelectionChange, onEdit, showPrefecture = false }) {
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
            {showPrefecture && <th>都道府県</th>}
            {ROAD_FIELDS.map((f) => (
              <th key={f.name}>{f.label}</th>
            ))}
            <th>選択</th>
            <th>編集</th>
          </tr>
        </thead>
        <tbody>
          {roads.length === 0 ? (
            <tr><td colSpan={ROAD_FIELDS.length + 3 + (showPrefecture ? 1 : 0)}>検索結果がありません</td></tr>
          ) : (
            roads.map((road, idx) => (
              <tr key={road.id}>
                <td>{startIndex + idx + 1}</td>
                {showPrefecture && <td>{road.prefecture_display}</td>}
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
