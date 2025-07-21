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
import { useAuth } from "./hooks/useAuth";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";

// componente simples para o redirecionamento inicial
const Root = () => {
  const { user } = useAuth();
  return <Navigate to={user ? "/dashboard" : "/login"} />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />

          {/* ROTAS PROTEGIDAS */}
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />}>
              <Route index element={<Welcome />} />
              <Route path="adicionar-horario" element={<AdicionarHorario />} />
              <Route
                path="editar-horario/:horarioId"
                element={<EditarHorario />}
              />{" "}
              <Route path="editar-horario" element={<EditarHorario />} />
              <Route path="visualizar-agenda" element={<VisualizarAgenda />} />
            </Route>
          </Route>

          {/* Rota inicial que usa o componente Root para decidir o redirecionamento */}
          <Route path="/" element={<Root />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
