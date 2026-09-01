import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { AuthProvider } from './AuthContext';
import { useAuth } from './useAuth';
import * as api from '../api/client';

vi.mock('../api/client');

function Probe() {
  const { username, isAuthenticated, isLoading, login, logout } = useAuth();
  if (isLoading) return <div>loading</div>;
  return (
    <div>
      <div data-testid="status">{isAuthenticated ? `in:${username}` : 'out'}</div>
      <button onClick={() => login('tester', 'pass')}>login</button>
      <button onClick={() => logout()}>logout</button>
    </div>
  );
}

describe('AuthProvider / useAuth', () => {
  beforeEach(() => {
    vi.mocked(api.fetchCurrentUser).mockResolvedValue({ username: null, is_authenticated: false });
  });

  it('初期状態では未ログインとして扱う', async () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId('status')).toHaveTextContent('out'));
  });

  it('ログインに成功すると状態が更新される', async () => {
    vi.mocked(api.login).mockResolvedValue({ username: 'tester', is_authenticated: true });
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId('status')).toHaveTextContent('out'));
    fireEvent.click(screen.getByText('login'));
    await waitFor(() => expect(screen.getByTestId('status')).toHaveTextContent('in:tester'));
  });

  it('ログアウトすると未ログイン状態に戻る', async () => {
    vi.mocked(api.fetchCurrentUser).mockResolvedValue({ username: 'tester', is_authenticated: true });
    vi.mocked(api.logout).mockResolvedValue({ username: null, is_authenticated: false });
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>
    );
    await waitFor(() => expect(screen.getByTestId('status')).toHaveTextContent('in:tester'));
    fireEvent.click(screen.getByText('logout'));
    await waitFor(() => expect(screen.getByTestId('status')).toHaveTextContent('out'));
  });
});
