import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import LoginPage from './LoginPage';
import * as api from '../api/client';
import { AuthProvider } from '../auth/AuthContext';

vi.mock('../api/client');

describe('LoginPage', () => {
  beforeEach(() => {
    vi.mocked(api.fetchCurrentUser).mockResolvedValue({ username: null, is_authenticated: false });
  });

  it('正しい情報でログインするとログインAPIが呼ばれる', async () => {
    vi.mocked(api.login).mockResolvedValue({ username: 'tester', is_authenticated: true });
    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>
    );

    await waitFor(() => expect(screen.getByRole('button', { name: 'ログイン' })).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText('ユーザー名'), { target: { value: 'tester' } });
    fireEvent.change(screen.getByLabelText('パスワード'), { target: { value: 'testpass123' } });
    fireEvent.click(screen.getByRole('button', { name: 'ログイン' }));

    await waitFor(() => expect(api.login).toHaveBeenCalledWith('tester', 'testpass123'));
  });

  it('誤った情報でログインするとエラーメッセージを表示する', async () => {
    vi.mocked(api.login).mockRejectedValue(new Error('unauthorized'));
    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider>
          <LoginPage />
        </AuthProvider>
      </MemoryRouter>
    );

    await waitFor(() => expect(screen.getByRole('button', { name: 'ログイン' })).toBeInTheDocument());

    fireEvent.change(screen.getByLabelText('ユーザー名'), { target: { value: 'tester' } });
    fireEvent.change(screen.getByLabelText('パスワード'), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: 'ログイン' }));

    expect(await screen.findByText('ユーザー名またはパスワードが正しくありません。')).toBeInTheDocument();
  });
});
