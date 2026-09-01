import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import PrefectureNav from './components/PrefectureNav';
import MultiPrefecturePage from './pages/MultiPrefecturePage';
import PrefecturePage from './pages/PrefecturePage';
import LoginPage from './pages/LoginPage';
import { AuthProvider } from './auth/AuthContext';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <PrefectureNav />
        <Routes>
          <Route path="/" element={<Navigate to="/shizuoka" replace />} />
          <Route path="/multi" element={<MultiPrefecturePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/:prefecture" element={<PrefecturePage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
