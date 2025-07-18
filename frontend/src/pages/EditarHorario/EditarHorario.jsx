import React, { useState } from 'react';
import { FaEdit, FaTrashAlt } from 'react-icons/fa';
import './EditarHorario.css';
import ModalConfirmacao from '../../components/ModalConfirmacao/ModalConfirmacao';

// Dados de exemplo
const initialHorarios = [
  { id: 1, dia: 'Segunda-feira', inicio: '09:00', fim: '10:00', materia: 'Matemática' },
  { id: 2, dia: 'Terça-feira', inicio: '11:00', fim: '12:00', materia: 'Física' },
  { id: 3, dia: 'Quarta-feira', inicio: '14:00', fim: '15:00', materia: 'Química' },
  { id: 4, dia: 'Quinta-feira', inicio: '10:00', fim: '11:00', materia: 'Biologia' },
  { id: 5, dia: 'Sexta-feira', inicio: '13:00', fim: '14:00', materia: 'História' },
  { id: 6, dia: 'Segunda-feira', inicio: '15:00', fim: '16:00', materia: 'Cálculo I' },
  { id: 7, dia: 'Terça-feira', inicio: '08:00', fim: '09:00', materia: 'Algoritmos' },
];

const EditarHorario = () => {
  // Estado para armazenar a lista de horários
  const [horarios, setHorarios] = useState(initialHorarios);

  // Estado para controlar a paginação
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Estados para controlar o modal de confirmação
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [itemParaDeletar, setItemParaDeletar] = useState(null);

  // Lógica da Paginação
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = horarios.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(horarios.length / itemsPerPage);

  // --- Funções de Ação ---

  const handleEdit = (id) => {
    // A lógica para editar será implementada no futuro
    alert(`Editar item com ID: ${id}`);
  };

  const handleOpenDeleteModal = (id) => {
    setItemParaDeletar(id); 
    setIsModalOpen(true); 
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setItemParaDeletar(null); 
  };

  const handleConfirmDelete = () => {
    const novaLista = horarios.filter((item) => item.id !== itemParaDeletar);
    setHorarios(novaLista);
    handleCloseModal();    
  };

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="table-container">
      <h1 className="table-title">Horários Cadastrados</h1>
      
      <table>
        <thead>
          <tr>
            <th>Dia da Semana</th>
            <th>Horário de Início</th>
            <th>Horário de Término</th>
            <th>Matéria</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.map((horario) => (
            <tr key={horario.id}>
              <td>{horario.dia}</td>
              <td>{horario.inicio}</td>
              <td>{horario.fim}</td>
              <td>{horario.materia}</td>
              <td className="actions-cell">
                <button onClick={() => handleEdit(horario.id)} className="action-btn edit-btn">
                  <FaEdit /> Editar
                </button>
                <button onClick={() => handleOpenDeleteModal(horario.id)} className="action-btn delete-btn">
                  <FaTrashAlt /> Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Renderização da Paginação */}
      <div className="pagination">
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index + 1}
            onClick={() => paginate(index + 1)}
            className={`page-btn ${currentPage === index + 1 ? 'active' : ''}`}
          >
            {index + 1}
          </button>
        ))}
      </div>

      {/* Renderização do Modal de Confirmação */}
      <ModalConfirmacao
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onConfirm={handleConfirmDelete}
        title="Confirmar Exclusão"
      >
        <p>Você tem certeza de que deseja excluir este horário? Esta ação não pode ser desfeita.</p>
      </ModalConfirmacao>
    </div>
  );
};

export default EditarHorario;