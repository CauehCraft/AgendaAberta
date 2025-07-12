import React from 'react';
import { Outlet } from 'react-router-dom'; // Importe o Outlet
import Sidebar from '../../components/Sidebar/Sidebar';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="main-content">
        {/* O Outlet renderizará o componente da rota aninhada (ex: AdicionarHorario) */}
        <Outlet />
      </main>
    </div>
  );
};

export default Dashboard;