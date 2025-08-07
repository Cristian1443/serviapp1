// En tu archivo de rutas o en App.jsx
import RegisterPage from './pages/RegisterPage';

function App() {
    return (
        // ... tu router y otras páginas
        <Routes>
            {/* ... otras rutas */}
            <Route path="/register" element={<RegisterPage />} />
        </Routes>
    );
}