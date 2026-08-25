import { useCallback, useEffect, useState } from 'react';
import EditForm from '../components/EditForm';
import Pagination from '../components/Pagination';
import PrefectureMultiSelect from '../components/PrefectureMultiSelect';
import ResultsTable from '../components/ResultsTable';
import SearchForm from '../components/SearchForm';
import { PREFECTURE_NAMES } from '../constants/prefectures';
import { bulkDeleteRoads, getRouteNames, searchRoads, updateRoad } from '../api/client';

const PAGE_SIZE = 50;

const defaultFilters = {
  routeName: 'すべて',
  lengthValue: '',
  lengthOp: 'gte',
  sortColumn: '',
  sortOrder: 'ASC',
};

function MultiPrefecturePage() {
  const [selectedPrefectures, setSelectedPrefectures] = useState(Object.keys(PREFECTURE_NAMES));
  const [routeNames, setRouteNames] = useState([]);
  const [filters, setFilters] = useState(defaultFilters);
  const [roads, setRoads] = useState([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [message, setMessage] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [editingRoad, setEditingRoad] = useState(null);

  const runSearch = useCallback(
    (currentFilters = filters, targetPage = 1) => {
      if (selectedPrefectures.length === 0) {
        setRoads([]);
        setCount(0);
        setPage(1);
        setMessage('都道府県を1つ以上選択してください。');
        return;
      }
      const params = {
        prefecture: selectedPrefectures.join(','),
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
    [selectedPrefectures, filters]
  );

  useEffect(() => {
    setFilters(defaultFilters);
    setRoads([]);
    setCount(0);
    setPage(1);
    setSelectedIds([]);
    setEditingRoad(null);
    if (selectedPrefectures.length === 0) {
      setRouteNames([]);
      setMessage('都道府県を1つ以上選択してください。');
      return;
    }
    getRouteNames(selectedPrefectures.join(','))
      .then((names) => {
        setRouteNames(names);
        runSearch(defaultFilters, 1);
      })
      .catch(() => setRouteNames([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedPrefectures]);

  const handleUpdate = (id, data) => {
    // dataには編集対象の道路が元々持っていたprefectureがそのまま含まれている
    updateRoad(id, data)
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
      <header>交通情報マスター（複数県横断検索）</header>
      <PrefectureMultiSelect selected={selectedPrefectures} onChange={setSelectedPrefectures} />
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
        showPrefecture
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
      <p className="multi-mode-note">
        新規データの追加は，対象の都道府県のページから行ってください。
      </p>
    </div>
  );
}

export default MultiPrefecturePage;
