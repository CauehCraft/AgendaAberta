import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/Login/Login";
import Cadastro from "./pages/Cadastro/Cadastro";
import Dashboard from "./pages/Dashboard/Dashboard";
import AdicionarHorario from "./pages/AdicionarHorario/AdicionarHorario";
import EditarHorario from "./pages/EditarHorario/EditarHorario";
import VisualizarAgenda from "./pages/VisualizarAgenda/VisualizarAgenda";
import Welcome from "./pages/Welcome/Welcome";
import { AuthProvider } from "./context/AuthProvider";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";

function App() {
  const isAuthenticated = true;

  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          {/* ROTA PROTEGIDA */}
          <Route element={<ProtectedRoute />}>
            <Route
              path="/dashboard"
              element={
                isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
              }
            >
              <Route index element={<Welcome />} />
              <Route path="adicionar-horario" element={<AdicionarHorario />} />
              <Route path="editar-horario" element={<EditarHorario />} />
              <Route path="visualizar-agenda" element={<VisualizarAgenda />} />
            </Route>
          </Route>

          <Route
            path="/"
            element={
              <Navigate
                to={isAuthenticated ? "/dashboard/adicionar-horario" : "/login"}
              />
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
