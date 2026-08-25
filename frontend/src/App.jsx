import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import PrefectureNav from './components/PrefectureNav';
import MultiPrefecturePage from './pages/MultiPrefecturePage';
import PrefecturePage from './pages/PrefecturePage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <PrefectureNav />
      <Routes>
        <Route path="/" element={<Navigate to="/shizuoka" replace />} />
        <Route path="/multi" element={<MultiPrefecturePage />} />
        <Route path="/:prefecture" element={<PrefecturePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
