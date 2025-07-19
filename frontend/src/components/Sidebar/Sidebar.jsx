import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { FaUserCircle, FaCalendarPlus, FaClock, FaEdit, FaCalendarAlt, FaSignOutAlt, FaBars, FaTimes } from 'react-icons/fa';
import './Sidebar.css';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <>
      <button className="mobile-menu-toggle" onClick={toggleMenu}>
        <FaBars />
      </button>

      <aside className={`sidebar ${isMenuOpen ? 'open' : ''}`}>
        <button className="sidebar-close-btn" onClick={toggleMenu}>
            <FaTimes />
        </button>

        <div className="sidebar-profile">
          <FaUserCircle className="sidebar-icon profile-icon" />
          <div>
            {user && <h3>{user.nome_completo || user.username}</h3>}
            {user && <p>{user.tipo.charAt(0).toUpperCase() + user.tipo.slice(1)}</p>}
          </div>
        </div>

        <nav className="sidebar-nav">
          <ul>
            {/* <li><NavLink to="/dashboard/criar-agenda" onClick={toggleMenu}><FaCalendarPlus className="sidebar-icon" /><span>Criar Agenda</span></NavLink></li>*/}
            <li><NavLink to="/dashboard/adicionar-horario" onClick={toggleMenu}><FaClock className="sidebar-icon" /><span>Adicionar Horário</span></NavLink></li>
            <li><NavLink to="/dashboard/editar-horario" onClick={toggleMenu}><FaEdit className="sidebar-icon" /><span>Editar/Deletar Horário</span></NavLink></li>
            <li><NavLink to="/dashboard/visualizar-agenda" onClick={toggleMenu}><FaCalendarAlt className="sidebar-icon" /><span>Visualizar Agenda</span></NavLink></li>
          </ul>
        </nav>
        
        <div className="sidebar-footer">
          <button className="logout-button" onClick={handleLogout}>
            <FaSignOutAlt className="sidebar-icon" />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {isMenuOpen && <div className="overlay" onClick={toggleMenu}></div>}
    </>
  );
};

export default Sidebar;