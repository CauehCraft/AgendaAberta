import { Outlet } from 'react-router-dom';
import Sidebar from '../../components/Sidebar/Sidebar';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Dashboard;