import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import PrefectureNav from './PrefectureNav';
import { useAuth } from '../auth/useAuth';

vi.mock('../auth/useAuth');

describe('PrefectureNav', () => {
  it('未ログイン時はログインリンクを表示する', () => {
    vi.mocked(useAuth).mockReturnValue({
      username: null,
      isAuthenticated: false,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });
    render(
      <MemoryRouter>
        <PrefectureNav />
      </MemoryRouter>
    );
    expect(screen.getByRole('link', { name: 'ログイン' })).toBeInTheDocument();
  });

  it('ログイン時はユーザー名とログアウトボタンを表示する', () => {
    vi.mocked(useAuth).mockReturnValue({
      username: 'tester',
      isAuthenticated: true,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
    });
    render(
      <MemoryRouter>
        <PrefectureNav />
      </MemoryRouter>
    );
    expect(screen.getByText('testerさん')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'ログアウト' })).toBeInTheDocument();
  });
});
