import { useState } from 'react';
import { PREFECTURE_NAMES } from '../constants/prefectures';
import { REGIONS } from '../constants/regions';

const ALL_CODES = Object.keys(PREFECTURE_NAMES);

function PrefectureMultiSelect({ selected, onChange }) {
  const [collapsed, setCollapsed] = useState(false);

  const toggle = (code) => {
    if (selected.includes(code)) {
      onChange(selected.filter((c) => c !== code));
    } else {
      onChange([...selected, code]);
    }
  };

  const summary =
    selected.length === 0
      ? '未選択'
      : selected.length === ALL_CODES.length
        ? 'すべて選択中'
        : `${selected.length}件選択中`;

  return (
    <div className="prefecture-multi-select">
      <div className="prefecture-multi-select-header">
        <span>対象都道府県:</span>
        <button type="button" onClick={() => onChange(ALL_CODES)}>すべて選択</button>
        <button type="button" onClick={() => onChange([])}>選択解除</button>
        <button
          type="button"
          className="prefecture-multi-select-toggle"
          onClick={() => setCollapsed((prev) => !prev)}
        >
          {collapsed ? `県一覧を開く（${summary}）` : '県一覧を閉じる'}
        </button>
      </div>
      {!collapsed && (
        <div className="prefecture-multi-select-regions">
          {REGIONS.map((region) => (
            <div key={region.name} className="prefecture-multi-select-region">
              <div className="prefecture-multi-select-region-name">{region.name}</div>
              <div className="prefecture-multi-select-list">
                {region.codes.map((code) => (
                  <label key={code}>
                    <input
                      type="checkbox"
                      checked={selected.includes(code)}
                      onChange={() => toggle(code)}
                    />
                    {PREFECTURE_NAMES[code]}
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PrefectureMultiSelect;
