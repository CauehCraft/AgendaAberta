import { useState, useEffect } from "react";
import useDebounce from "../../hooks/useDebounce";
import api from "../../services/api";
import "./BuscarHorarios.css";

const BuscarHorarios = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [horarios, setHorarios] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  // Estado para a paginação
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5; // Define quantos itens por página você quer

  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(() => {
    const fetchHorarios = async () => {
      if (debouncedSearchTerm) {
        setIsLoading(true);
        setError("");
        try {
          const response = await api.get(
            `/horarios-publicos/?search=${debouncedSearchTerm}`
          );
          setHorarios(response.data.results || response.data);
        } catch (err) {
          setError("Não foi possível realizar a busca.");
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      } else {
        setHorarios([]); // Limpa os resultados se a busca estiver vazia
      }
    };

    fetchHorarios();
    setCurrentPage(1);
  }, [debouncedSearchTerm]);

  // Lógica da Paginação
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = horarios.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(horarios.length / itemsPerPage);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  return (
    <div className="search-container">
      <h1 className="search-title">Buscar Horários de Atendimento</h1>
      <div className="search-bar-wrapper">
        <input
          type="text"
          placeholder="Busque por disciplina ou nome do professor/monitor..."
          className="search-input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {isLoading && <p>Buscando...</p>}
      {error && <p className="error-message">{error}</p>}

      {!isLoading && !error && (
        <>
          <table className="data-table">
            <thead>
              <tr>
                <th>Responsável</th>
                <th>Dia da Semana</th>
                <th>Horário de Início</th>
                <th>Horário de Término</th>
                <th>Disciplina</th>
                <th>Local</th>
              </tr>
            </thead>
            <tbody>
              {currentItems.length > 0 ? (
                currentItems.map((horario) => (
                  <tr key={horario.id}>
                    <td data-label="Responsável">{horario.professor_nome}</td>
                    <td data-label="Dia da Semana">{horario.dia_semana}</td>
                    <td data-label="Início">{horario.hora_inicio}</td>
                    <td data-label="Término">{horario.hora_fim}</td>
                    <td data-label="Disciplina">{horario.disciplina_nome}</td>
                    <td data-label="Local">{horario.local}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="no-results">
                    {debouncedSearchTerm
                      ? "Nenhum horário encontrado para sua busca."
                      : "Digite algo para iniciar a busca."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>

          {/* Renderiza a paginação apenas se houver mais de uma página */}
          {totalPages > 1 && (
            <div className="pagination">
              {Array.from({ length: totalPages }, (_, index) => (
                <button
                  key={index + 1}
                  onClick={() => paginate(index + 1)}
                  className={`page-btn ${
                    currentPage === index + 1 ? "active" : ""
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default BuscarHorarios;
