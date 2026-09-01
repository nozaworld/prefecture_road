import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import Pagination from './Pagination';

describe('Pagination', () => {
  it('件数が0のときは何も表示しない', () => {
    const { container } = render(
      <Pagination page={1} pageCount={1} count={0} onPageChange={vi.fn()} />
    );
    expect(container).toBeEmptyDOMElement();
  });

  it('ページ番号と件数を表示する', () => {
    render(<Pagination page={2} pageCount={5} count={123} onPageChange={vi.fn()} />);
    expect(screen.getByText('2 / 5ページ（全123件）')).toBeInTheDocument();
  });

  it('先頭ページでは「前へ」が無効になる', () => {
    render(<Pagination page={1} pageCount={3} count={10} onPageChange={vi.fn()} />);
    expect(screen.getByRole('button', { name: '前へ' })).toBeDisabled();
    expect(screen.getByRole('button', { name: '次へ' })).not.toBeDisabled();
  });

  it('最終ページでは「次へ」が無効になる', () => {
    render(<Pagination page={3} pageCount={3} count={10} onPageChange={vi.fn()} />);
    expect(screen.getByRole('button', { name: '次へ' })).toBeDisabled();
  });

  it('「次へ」を押すとonPageChangeが次のページ番号で呼ばれる', () => {
    const onPageChange = vi.fn();
    render(<Pagination page={2} pageCount={5} count={100} onPageChange={onPageChange} />);
    fireEvent.click(screen.getByRole('button', { name: '次へ' }));
    expect(onPageChange).toHaveBeenCalledWith(3);
  });
});
