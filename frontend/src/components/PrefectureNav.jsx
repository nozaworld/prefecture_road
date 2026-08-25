import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getPrefectures } from '../api/client';

function PrefectureNav() {
  const [prefectures, setPrefectures] = useState([]);
  const { prefecture: current } = useParams();

  useEffect(() => {
    getPrefectures()
      .then(setPrefectures)
      .catch(() => setPrefectures([]));
  }, []);

  return (
    <nav className="prefecture-nav">
      <ul>
        {prefectures.map((pref) => (
          <li key={pref.code}>
            <Link to={`/${pref.code}`} className={pref.code === current ? 'active' : ''}>
              {pref.name}の道路
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default PrefectureNav;
