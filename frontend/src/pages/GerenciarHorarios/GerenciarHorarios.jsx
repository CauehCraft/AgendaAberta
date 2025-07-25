import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // useNavigate será útil para o botão de editar no futuro
import { FaEdit, FaTrashAlt } from "react-icons/fa";
import api from "../../services/api";
import "./GerenciarHorarios.css";
import ModalConfirmacao from "../../components/ModalConfirmacao/ModalConfirmacao";

const GerenciarHorarios = () => {
  // const navigate = useNavigate();

  const [horarios, setHorarios] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [itemParaDeletar, setItemParaDeletar] = useState(null);

  // useEffect para buscar os dados da API assim que o componente for montado
  useEffect(() => {
    const fetchHorarios = async () => {
      try {
        const response = await api.get("/horarios/"); // Faz a requisição GET
        setHorarios(response.data); // Preenche o estado com os dados recebidos
      } catch (err) {
        setError(
          "Não foi possível carregar os horários. Tente novamente mais tarde."
        );
        console.error("Erro ao buscar horários:", err);
      } finally {
        setIsLoading(false); // Finaliza o carregamento, com sucesso ou erro
      }
    };

    fetchHorarios();
  }, []); // O array vazio [] garante que a busca aconteça apenas uma vez

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = horarios.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(horarios.length / itemsPerPage);

  const handleEdit = (id) => {
    // A lógica para editar será implementada no futuro
    alert(`(Futuro) Editar item com ID: ${id}`);
    // navigate(`/dashboard/editar-horario/${id}`);
  };

  const handleOpenDeleteModal = (id) => {
    setItemParaDeletar(id);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setItemParaDeletar(null);
  };

  const handleConfirmDelete = async () => {
    if (!itemParaDeletar) return;

    try {
      await api.delete(`/horarios/${itemParaDeletar}/`);

      setHorarios(horarios.filter((item) => item.id !== itemParaDeletar));
    } catch (err) {
      console.error("Erro ao excluir horário:", err);
      alert("Não foi possível excluir o horário. Tente novamente.");
    } finally {
      handleCloseModal();
    }
  };

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  if (isLoading) {
    return (
      <div className="table-container">
        <h1 className="table-title">Carregando Horários...</h1>
      </div>
    );
  }

  if (error) {
    return (
      <div className="table-container">
        <h1 className="table-title error-message">{error}</h1>
      </div>
    );
  }

  return (
    <div className="table-container">
      <h1 className="table-title">Horários Cadastrados</h1>

      <table>
        <thead>
          <tr>
            <th>Dia da Semana</th>
            <th>Disciplina</th>
            <th>Horário de Início</th>
            <th>Horário de Término</th>
            <th>Local</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {currentItems.map((horario) => (
            <tr key={horario.id}>
              <td>{horario.dia_semana}</td>
              <td>{horario.disciplina.nome}</td>
              <td>{horario.hora_inicio}</td>
              <td>{horario.hora_fim}</td>
              <td>{horario.local}</td>
              <td className="actions-cell">
                <button
                  onClick={() => handleEdit(horario.id)}
                  className="action-btn edit-btn"
                >
                  <FaEdit /> Editar
                </button>
                <button
                  onClick={() => handleOpenDeleteModal(horario.id)}
                  className="action-btn delete-btn"
                >
                  <FaTrashAlt /> Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        {Array.from({ length: totalPages }, (_, index) => (
          <button
            key={index + 1}
            onClick={() => paginate(index + 1)}
            className={`page-btn ${currentPage === index + 1 ? "active" : ""}`}
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
        <p>
          Você tem certeza de que deseja excluir este horário? Esta ação não
          pode ser desfeita.
        </p>
      </ModalConfirmacao>
    </div>
  );
};

export default GerenciarHorarios;
