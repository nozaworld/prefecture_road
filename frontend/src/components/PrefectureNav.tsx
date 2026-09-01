import { type ChangeEvent } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { PREFECTURE_NAMES } from '../constants/prefectures';
import { REGIONS } from '../constants/regions';
import { useAuth } from '../auth/useAuth';

function PrefectureNav() {
  const navigate = useNavigate();
  const location = useLocation();
  const { username, isAuthenticated, isLoading, logout } = useAuth();
  // PrefectureNavは<Routes>の外（兄弟要素）に置かれているためuseParamsではURLパラメータを取得できない。
  // useLocationはRouter配下ならどこでも使えるため，パス名から現在地を判定する。
  const current = location.pathname.slice(1);

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    if (value) {
      navigate(`/${value}`);
    }
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="prefecture-nav">
      <select
        className="prefecture-select"
        value={PREFECTURE_NAMES[current] ? current : ''}
        onChange={handleChange}
      >
        <option value="" disabled>都道府県を選択</option>
        {REGIONS.map((region) => (
          <optgroup key={region.name} label={region.name}>
            {region.codes.map((code) => (
              <option key={code} value={code}>
                {PREFECTURE_NAMES[code]}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
      <Link to="/multi" className={current === 'multi' ? 'active' : ''}>
        複数県横断検索
      </Link>
      <div className="prefecture-nav-auth">
        {isLoading ? null : isAuthenticated ? (
          <>
            <span className="nav-username">{username}さん</span>
            <button type="button" className="logout-btn" onClick={handleLogout}>
              ログアウト
            </button>
          </>
        ) : (
          <Link to="/login" className={current === 'login' ? 'active' : ''}>
            ログイン
          </Link>
        )}
      </div>
    </nav>
  );
}

export default PrefectureNav;
