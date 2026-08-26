interface PaginationProps {
  page: number;
  pageCount: number;
  count: number;
  onPageChange: (page: number) => void;
}

function Pagination({ page, pageCount, count, onPageChange }: PaginationProps) {
  if (count === 0) return null;

  return (
    <div className="pagination">
      <button
        type="button"
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
      >
        前へ
      </button>
      <span>
        {page} / {pageCount}ページ（全{count}件）
      </span>
      <button
        type="button"
        onClick={() => onPageChange(page + 1)}
        disabled={page >= pageCount}
      >
        次へ
      </button>
    </div>
  );
}

export default Pagination;
