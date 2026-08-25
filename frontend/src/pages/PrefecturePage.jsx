import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { PREFECTURE_NAMES } from '../constants/prefectures';
import AddForm from '../components/AddForm';
import EditForm from '../components/EditForm';
import ResultsTable from '../components/ResultsTable';
import SearchForm from '../components/SearchForm';
import {
  bulkDeleteRoads,
  createRoad,
  getRouteNames,
  searchRoads,
  updateRoad,
} from '../api/client';

const defaultFilters = {
  routeName: 'すべて',
  lengthValue: '',
  lengthOp: 'gte',
  sortColumn: '',
  sortOrder: 'ASC',
};

function PrefecturePage() {
  const { prefecture } = useParams();
  const [routeNames, setRouteNames] = useState([]);
  const [filters, setFilters] = useState(defaultFilters);
  const [roads, setRoads] = useState([]);
  const [message, setMessage] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [editingRoad, setEditingRoad] = useState(null);

  const runSearch = useCallback(
    (currentFilters = filters) => {
      const params = {
        prefecture,
        route_name: currentFilters.routeName,
        length_value: currentFilters.lengthValue,
        length_op: currentFilters.lengthOp,
        sort_column: currentFilters.sortColumn,
        sort_order: currentFilters.sortOrder,
      };
      searchRoads(params)
        .then((data) => {
          setRoads(data);
          setMessage(`検索結果: ${data.length}件`);
        })
        .catch(() => setMessage('検索中にエラーが発生しました。'));
    },
    [prefecture, filters]
  );

  useEffect(() => {
    setFilters(defaultFilters);
    setRoads([]);
    setSelectedIds([]);
    setEditingRoad(null);
    getRouteNames(prefecture)
      .then((names) => {
        setRouteNames(names);
        runSearch(defaultFilters);
      })
      .catch(() => setRouteNames([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prefecture]);

  const handleAdd = (data) => {
    createRoad({ ...data, prefecture })
      .then(() => {
        setMessage('データを追加しました。');
        runSearch();
      })
      .catch(() => setMessage('データの追加に失敗しました（区間番号が重複している可能性があります）。'));
  };

  const handleUpdate = (id, data) => {
    updateRoad(id, { ...data, prefecture })
      .then(() => {
        setMessage(`区間番号 ${data.section_number} のデータを更新しました。`);
        setEditingRoad(null);
        runSearch();
      })
      .catch(() => setMessage('データの更新に失敗しました。'));
  };

  const handleBulkDelete = () => {
    if (selectedIds.length === 0) {
      setMessage('削除する項目を選択してください。');
      return;
    }
    bulkDeleteRoads(selectedIds)
      .then((res) => {
        setMessage(`${res.deleted}件のデータを削除しました。`);
        setSelectedIds([]);
        runSearch();
      })
      .catch(() => setMessage('削除中にエラーが発生しました。'));
  };

  return (
    <div className="prefecture-page">
      <header>交通情報マスター（{PREFECTURE_NAMES[prefecture] ?? prefecture}の道路）</header>
      <SearchForm
        routeNames={routeNames}
        filters={filters}
        onFiltersChange={setFilters}
        onSearch={() => runSearch()}
        onBulkDelete={handleBulkDelete}
      />
      {message && <div className="message">{message}</div>}
      <ResultsTable
        roads={roads}
        selectedIds={selectedIds}
        onSelectionChange={setSelectedIds}
        onEdit={setEditingRoad}
      />
      {editingRoad && (
        <EditForm road={editingRoad} onUpdate={handleUpdate} onCancel={() => setEditingRoad(null)} />
      )}
      <AddForm onAdd={handleAdd} />
    </div>
  );
}

export default PrefecturePage;
