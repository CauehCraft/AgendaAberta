import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import AdicionarHorario from './pages/AdicionarHorario/AdicionarHorario';
import EditarHorario from './pages/EditarHorario/EditarHorario';
import VisualizarAgenda from './pages/VisualizarAgenda/VisualizarAgenda';
import Welcome from './pages/Welcome/Welcome';

function App() {
  const isAuthenticated = true;

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} >
          <Route index element={<Welcome />} /> 
          <Route path="adicionar-horario" element={<AdicionarHorario />} />
          <Route path="editar-horario" element={<EditarHorario />} />
          <Route path="visualizar-agenda" element={<VisualizarAgenda />} />
        </Route>

        <Route path="/" element={<Navigate to={isAuthenticated ? "/dashboard/adicionar-horario" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;