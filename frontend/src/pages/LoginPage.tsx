import { useEffect, useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/useAuth';

function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  if (isAuthenticated) return null;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await login(username, password);
      navigate('/', { replace: true });
    } catch {
      setError('ユーザー名またはパスワードが正しくありません。');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-page">
      <h2>ログイン</h2>
      <p className="login-note">
        アカウントの作成は管理者がDjango側（管理画面またはcreatesuperuser）で行います。
      </p>
      <form className="login-form" onSubmit={handleSubmit}>
        <label>
          ユーザー名
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </label>
        <label>
          パスワード
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        {error && <div className="login-error">{error}</div>}
        <button type="submit" disabled={submitting}>
          {submitting ? 'ログイン中…' : 'ログイン'}
        </button>
      </form>
    </div>
  );
}

export default LoginPage;
