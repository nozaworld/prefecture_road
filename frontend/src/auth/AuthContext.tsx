import { useCallback, useEffect, useState, type ReactNode } from 'react';
import { fetchCurrentUser, login as loginRequest, logout as logoutRequest } from '../api/client';
import { AuthContext, type AuthContextValue } from './context';

interface AuthState {
  username: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const initialState: AuthState = {
  username: null,
  isAuthenticated: false,
  isLoading: true,
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>(initialState);

  useEffect(() => {
    fetchCurrentUser()
      .then((user) =>
        setState({ username: user.username, isAuthenticated: user.is_authenticated, isLoading: false })
      )
      .catch(() => setState({ username: null, isAuthenticated: false, isLoading: false }));
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const user = await loginRequest(username, password);
    setState({ username: user.username, isAuthenticated: user.is_authenticated, isLoading: false });
  }, []);

  const logout = useCallback(async () => {
    const user = await logoutRequest();
    setState({ username: user.username, isAuthenticated: user.is_authenticated, isLoading: false });
  }, []);

  const value: AuthContextValue = { ...state, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
