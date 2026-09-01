import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi, afterEach } from 'vitest';
import SearchForm from './SearchForm';
import type { Filters } from '../types';

const baseFilters: Filters = {
  routeName: 'すべて',
  lengthValue: '',
  lengthOp: 'gte',
  sortColumn: '',
  sortOrder: 'ASC',
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe('SearchForm', () => {
  it('検索ボタンを押すとonSearchが呼ばれる', () => {
    const onSearch = vi.fn();
    render(
      <SearchForm
        routeNames={[]}
        filters={baseFilters}
        onFiltersChange={vi.fn()}
        onSearch={onSearch}
        onBulkDelete={vi.fn()}
      />
    );
    fireEvent.click(screen.getByRole('button', { name: '検索' }));
    expect(onSearch).toHaveBeenCalledTimes(1);
  });

  it('canDeleteがfalseのとき削除ボタンを表示しない', () => {
    render(
      <SearchForm
        routeNames={[]}
        filters={baseFilters}
        onFiltersChange={vi.fn()}
        onSearch={vi.fn()}
        onBulkDelete={vi.fn()}
        canDelete={false}
      />
    );
    expect(screen.queryByRole('button', { name: '削除' })).not.toBeInTheDocument();
  });

  it('削除ボタンを押して確認するとonBulkDeleteが呼ばれる', () => {
    const onBulkDelete = vi.fn();
    vi.spyOn(window, 'confirm').mockReturnValue(true);
    render(
      <SearchForm
        routeNames={[]}
        filters={baseFilters}
        onFiltersChange={vi.fn()}
        onSearch={vi.fn()}
        onBulkDelete={onBulkDelete}
      />
    );
    fireEvent.click(screen.getByRole('button', { name: '削除' }));
    expect(onBulkDelete).toHaveBeenCalledTimes(1);
  });

  it('削除の確認でキャンセルするとonBulkDeleteは呼ばれない', () => {
    const onBulkDelete = vi.fn();
    vi.spyOn(window, 'confirm').mockReturnValue(false);
    render(
      <SearchForm
        routeNames={[]}
        filters={baseFilters}
        onFiltersChange={vi.fn()}
        onSearch={vi.fn()}
        onBulkDelete={onBulkDelete}
      />
    );
    fireEvent.click(screen.getByRole('button', { name: '削除' }));
    expect(onBulkDelete).not.toHaveBeenCalled();
  });
});
