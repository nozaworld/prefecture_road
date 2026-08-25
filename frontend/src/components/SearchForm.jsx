import RouteAutocomplete from './RouteAutocomplete';
import { SORT_OPTIONS } from '../constants/roadFields';

function SearchForm({ routeNames, filters, onFiltersChange, onSearch, onBulkDelete }) {
  const handleSubmit = (event) => {
    event.preventDefault();
    onSearch();
  };

  const handleDelete = (event) => {
    event.preventDefault();
    if (window.confirm('選択した項目を削除しますか？')) {
      onBulkDelete();
    }
  };

  return (
    <div className="search-section">
      <h3>検索条件</h3>
      <form className="search-form" onSubmit={handleSubmit}>
        <div className="search-form-route">
          <label>路線名（必須）:</label>
          <RouteAutocomplete
            routeNames={['すべて', ...routeNames]}
            value={filters.routeName}
            onChange={(value) => onFiltersChange({ ...filters, routeName: value })}
          />
        </div>
        <div className="search-form-length">
          <label>区間延長（km）:</label>
          <input
            type="number"
            step="0.01"
            placeholder="数値を入力"
            value={filters.lengthValue}
            onChange={(e) => onFiltersChange({ ...filters, lengthValue: e.target.value })}
          />
          <select
            value={filters.lengthOp}
            onChange={(e) => onFiltersChange({ ...filters, lengthOp: e.target.value })}
          >
            <option value="gte">以上</option>
            <option value="lte">以下</option>
          </select>
        </div>
        <div className="search-form-sort">
          <label>ソート項目:</label>
          <select
            className="sort-column"
            value={filters.sortColumn}
            onChange={(e) => onFiltersChange({ ...filters, sortColumn: e.target.value })}
          >
            <option value="">選択してください</option>
            {SORT_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <select
            value={filters.sortOrder}
            onChange={(e) => onFiltersChange({ ...filters, sortOrder: e.target.value })}
          >
            <option value="ASC">昇順</option>
            <option value="DESC">降順</option>
          </select>
        </div>
        <div className="search-form-buttons">
          <button type="submit">検索</button>
          <button type="button" className="delete-btn" onClick={handleDelete}>削除</button>
        </div>
      </form>
    </div>
  );
}

export default SearchForm;
