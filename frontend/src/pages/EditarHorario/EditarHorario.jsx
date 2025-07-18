import React, { useState } from 'react';
import { FaEdit, FaTrashAlt } from 'react-icons/fa';
import './EditarHorario.css';

// 1. Dados de exemplo (substituir por dados da API no futuro)
const mockHorarios = [
  { id: 1, dia: 'Segunda-feira', inicio: '09:00', fim: '10:00', materia: 'Matemática' },
  { id: 2, dia: 'Terça-feira', inicio: '11:00', fim: '12:00', materia: 'Física' },
  { id: 3, dia: 'Quarta-feira', inicio: '14:00', fim: '15:00', materia: 'Química' },
  { id: 4, dia: 'Quinta-feira', inicio: '10:00', fim: '11:00', materia: 'Biologia' },
  { id: 5, dia: 'Sexta-feira', inicio: '13:00', fim: '14:00', materia: 'História' },
  { id: 6, dia: 'Segunda-feira', inicio: '15:00', fim: '16:00', materia: 'Cálculo I' },
  { id: 7, dia: 'Terça-feira', inicio: '08:00', fim: '09:00', materia: 'Algoritmos' },
];

const EditarHorario = () => {
  // 2. Estado para controlar a paginação
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5; // Quantos itens por página

  // 3. Lógica da Paginação
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = mockHorarios.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(mockHorarios.length / itemsPerPage);

  const handleEdit = (id) => {
    // Lógica para editar (será implementada no futuro)
    alert(`Editar item com ID: ${id}`);
  };

  const handleDelete = (id) => {
    // Lógica para deletar (será implementada no futuro)
    alert(`Deletar item com ID: ${id}`);
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
                <button onClick={() => handleDelete(horario.id)} className="action-btn delete-btn">
                  <FaTrashAlt /> Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* 4. Componente de Paginação */}
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
    </div>
  );
};

export default EditarHorario;