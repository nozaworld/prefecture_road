import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import AddForm from '../components/AddForm';
import EditForm from '../components/EditForm';
import Pagination from '../components/Pagination';
import ResultsTable from '../components/ResultsTable';
import SearchForm from '../components/SearchForm';
import { PREFECTURE_NAMES } from '../constants/prefectures';
import {
  bulkDeleteRoads,
  createRoad,
  getRouteNames,
  searchRoads,
  updateRoad,
} from '../api/client';
import type { Filters, Road, RoadFormData } from '../types';

const PAGE_SIZE = 50;

const defaultFilters: Filters = {
  routeName: 'すべて',
  lengthValue: '',
  lengthOp: 'gte',
  sortColumn: '',
  sortOrder: 'ASC',
};

function PrefecturePage() {
  const { prefecture } = useParams<{ prefecture: string }>();
  const [routeNames, setRouteNames] = useState<string[]>([]);
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [roads, setRoads] = useState<Road[]>([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [message, setMessage] = useState('');
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [editingRoad, setEditingRoad] = useState<Road | null>(null);

  const runSearch = useCallback(
    (currentFilters: Filters = filters, targetPage = 1) => {
      const params = {
        prefecture: prefecture ?? '',
        route_name: currentFilters.routeName,
        length_value: currentFilters.lengthValue,
        length_op: currentFilters.lengthOp,
        sort_column: currentFilters.sortColumn,
        sort_order: currentFilters.sortOrder,
        page: targetPage,
        page_size: PAGE_SIZE,
      };
      searchRoads(params)
        .then((data) => {
          setRoads(data.results);
          setCount(data.count);
          setPage(targetPage);
          setMessage(`検索結果: ${data.count}件`);
        })
        .catch(() => setMessage('検索中にエラーが発生しました。'));
    },
    [prefecture, filters]
  );

  useEffect(() => {
    setFilters(defaultFilters);
    setRoads([]);
    setCount(0);
    setPage(1);
    setSelectedIds([]);
    setEditingRoad(null);
    if (!prefecture) return;
    getRouteNames(prefecture)
      .then((names) => {
        setRouteNames(names);
        runSearch(defaultFilters, 1);
      })
      .catch(() => setRouteNames([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [prefecture]);

  const handleAdd = (data: RoadFormData) => {
    createRoad({ ...data, prefecture })
      .then(() => {
        setMessage('データを追加しました。');
        runSearch(filters, page);
      })
      .catch(() => setMessage('データの追加に失敗しました（区間番号が重複している可能性があります）。'));
  };

  const handleUpdate = (id: number, data: Road) => {
    updateRoad(id, { ...data, prefecture })
      .then(() => {
        setMessage(`区間番号 ${data.section_number} のデータを更新しました。`);
        setEditingRoad(null);
        runSearch(filters, page);
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
        runSearch(filters, 1);
      })
      .catch(() => setMessage('削除中にエラーが発生しました。'));
  };

  const pageCount = Math.max(1, Math.ceil(count / PAGE_SIZE));

  return (
    <div className="prefecture-page">
      <header>交通情報マスター（{(prefecture && PREFECTURE_NAMES[prefecture]) ?? prefecture}の道路）</header>
      <SearchForm
        routeNames={routeNames}
        filters={filters}
        onFiltersChange={setFilters}
        onSearch={() => runSearch(filters, 1)}
        onBulkDelete={handleBulkDelete}
      />
      {message && <div className="message">{message}</div>}
      <ResultsTable
        roads={roads}
        startIndex={(page - 1) * PAGE_SIZE}
        selectedIds={selectedIds}
        onSelectionChange={setSelectedIds}
        onEdit={setEditingRoad}
      />
      <Pagination
        page={page}
        pageCount={pageCount}
        count={count}
        onPageChange={(nextPage) => runSearch(filters, nextPage)}
      />
      {editingRoad && (
        <EditForm road={editingRoad} onUpdate={handleUpdate} onCancel={() => setEditingRoad(null)} />
      )}
      <AddForm onAdd={handleAdd} />
    </div>
  );
}

export default PrefecturePage;
