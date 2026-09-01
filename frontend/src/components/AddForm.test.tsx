import { render, screen, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import AddForm from './AddForm';

describe('AddForm', () => {
  it('入力した内容でonAddが呼ばれ，送信後にフォームがリセットされる', () => {
    const onAdd = vi.fn();
    render(<AddForm onAdd={onAdd} />);

    fireEvent.change(screen.getByPlaceholderText('区間番号*'), { target: { value: '5' } });
    fireEvent.change(screen.getByPlaceholderText('路線名*'), { target: { value: '国道1号' } });

    fireEvent.click(screen.getByRole('button', { name: '追加' }));

    expect(onAdd).toHaveBeenCalledTimes(1);
    expect(onAdd.mock.calls[0][0]).toMatchObject({
      section_number: '5',
      route_name: '国道1号',
    });
    expect(screen.getByPlaceholderText('区間番号*')).toHaveValue(null);
    expect(screen.getByPlaceholderText('路線名*')).toHaveValue('');
  });
});
