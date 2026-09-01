import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import ResultsTable from './ResultsTable';
import type { Road } from '../types';

const road: Road = {
  id: 1,
  prefecture: 'shizuoka',
  prefecture_display: '静岡県',
  section_number: 1,
  route_name: '国道1号',
  start_point: '',
  end_point: '',
  municipality_code: '',
  expressway_type: '',
  section_length: 1.2,
  upstream_point: '',
  upstream_traffic: 0,
  downstream_point: '',
  downstream_traffic: 0,
  total_traffic: 0,
  day_night_ratio: 0,
  congestion_degree: 0,
  upstream_speed: 0,
  downstream_speed: 0,
  road_width: 0,
  speed_limit: 0,
};

describe('ResultsTable', () => {
  it('データがないときはメッセージを表示する', () => {
    render(
      <ResultsTable
        roads={[]}
        startIndex={0}
        selectedIds={[]}
        onSelectionChange={vi.fn()}
        onEdit={vi.fn()}
      />
    );
    expect(screen.getByText('検索結果がありません')).toBeInTheDocument();
  });

  it('canEditがfalseのとき編集ボタン・選択チェックボックスを表示しない', () => {
    render(
      <ResultsTable
        roads={[road]}
        startIndex={0}
        selectedIds={[]}
        onSelectionChange={vi.fn()}
        onEdit={vi.fn()}
        canEdit={false}
      />
    );
    expect(screen.queryByRole('button', { name: '編集' })).not.toBeInTheDocument();
    expect(screen.queryByRole('checkbox')).not.toBeInTheDocument();
  });

  it('編集ボタンを押すとonEditが対象の道路データで呼ばれる', () => {
    const onEdit = vi.fn();
    render(
      <ResultsTable
        roads={[road]}
        startIndex={0}
        selectedIds={[]}
        onSelectionChange={vi.fn()}
        onEdit={onEdit}
      />
    );
    fireEvent.click(screen.getByRole('button', { name: '編集' }));
    expect(onEdit).toHaveBeenCalledWith(road);
  });
});
