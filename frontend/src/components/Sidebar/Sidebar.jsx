import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';
import {
  FaUserCircle,
  FaCalendarPlus,
  FaClock,
  FaEdit,
  FaCalendarAlt,
  FaTrashAlt
} from 'react-icons/fa';

const Sidebar = () => {
  const user = {
    name: 'Dr. Amelia Harper',
    role: 'Professor',
  };

  return (
    <aside className="sidebar">
      {/* SEÇÃO DO PERFIL RESTAURADA */}
      <div className="sidebar-profile">
        <FaUserCircle className="sidebar-icon profile-icon" />
        <div>
          <h3>{user.name}</h3>
          <p>{user.role}</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        <ul>
          {/* Usei NavLink para que o link ativo seja destacado */}
          <li><NavLink to="/dashboard/criar-agenda"><FaCalendarPlus className="sidebar-icon" /> Criar Agenda</NavLink></li>
          <li><NavLink to="/dashboard/adicionar-horario"><FaClock className="sidebar-icon" /> Adicionar Horário</NavLink></li>
          <li><NavLink to="/dashboard/editar-horario"><FaEdit className="sidebar-icon" /> Editar/Deletar Horário</NavLink></li>
          <li><NavLink to="/dashboard/visualizar-agenda"><FaCalendarAlt className="sidebar-icon" /> Visualizar Agenda</NavLink></li>
        </ul>
      </nav>

      {/* RODAPÉ RESTAURADO */}
      <div className="sidebar-footer">
        <a href="#" className="delete-account">
          <FaTrashAlt className="sidebar-icon" /> Excluir Conta
        </a>
      </div>
    </aside>
  );
};

export default Sidebar;