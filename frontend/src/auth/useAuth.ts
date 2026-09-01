import { useContext } from 'react';
import { AuthContext, type AuthContextValue } from './context';

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuthはAuthProviderの内側で使ってください');
  }
  return ctx;
}
