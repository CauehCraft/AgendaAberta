import React, { useState, useEffect } from "react";
import api from "../../services/api";
import "./AdicionarHorario.css";

const AdicionarHorario = () => {
  // Estados para os campos do formulário
  const [disciplina, setDisciplina] = useState("");
  const [diaSemana, setDiaSemana] = useState("");
  const [horaInicio, setHoraInicio] = useState("");
  const [horaFim, setHoraFim] = useState("");
  const [local, setLocal] = useState("");

  // Estados para carregar as disciplinas da API
  const [disciplinas, setDisciplinas] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Estado de erros aprimorado (permanece o mesmo)
  const [errors, setErrors] = useState({
    disciplina: null,
    dia_semana: null,
    hora_inicio: null,
    hora_fim: null,
    local: null,
    non_field_errors: null,
  });
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchDisciplinas = async () => {
      try {
        const response = await api.get("/disciplinas/");
        setDisciplinas(response.data);
      } catch (err) {
        setErrors({
          non_field_errors: "Não foi possível carregar as disciplinas.",
        });
        console.error("Erro ao carregar disciplinas:", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDisciplinas();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSuccessMessage("");
    setErrors({
      disciplina: null,
      dia_semana: null,
      hora_inicio: null,
      hora_fim: null,
      local: null,
      non_field_errors: null,
    });

    const payload = {
      disciplina,
      dia_semana: diaSemana,
      hora_inicio: horaInicio,
      hora_fim: horaFim,
      local,
    };

    try {
      await api.post("/horarios/", payload);
      setSuccessMessage("Horário cadastrado com sucesso!");
      setDisciplina("");
      setDiaSemana("");
      setHoraInicio("");
      setHoraFim("");
      setLocal("");
    } catch (err) {
      if (err.response && err.response.data && err.response.data.errors) {
        const backendErrors = err.response.data.errors;
        // console.error("Erros recebidos do backend:", backendErrors);
        const newErrors = {};
        for (const field in backendErrors) {
          newErrors[field] = backendErrors[field];
        }
        setErrors(newErrors);
      } else if (
        err.response &&
        err.response.data &&
        err.response.data.message
      ) {
        setErrors({ non_field_errors: err.response.data.message });
      } else {
        setErrors({
          non_field_errors: "Ocorreu um erro de comunicação. Tente novamente.",
        });
      }
    }
  };

  const errorMessages = Object.values(errors).filter((error) => error !== null);

  if (isLoading) {
    return <div className="form-container">Carregando...</div>;
  }

  return (
    <div className="form-container">
      <h1 className="form-title">Adicionar Horário Semanal</h1>
      <form onSubmit={handleSubmit}>
        {/* Dropdown para Disciplinas */}
        <div className="input-group">
          <label htmlFor="disciplina">Disciplina</label>
          <select
            id="disciplina"
            value={disciplina}
            onChange={(e) => setDisciplina(e.target.value)}
            required
          >
            <option value="" disabled>
              Selecione a disciplina
            </option>
            {disciplinas.map((d) => (
              <option key={d.id} value={d.id}>
                {d.nome} ({d.codigo})
              </option>
            ))}
          </select>
        </div>

        {/* Dropdown para Dia da Semana */}
        <div className="input-group">
          <label htmlFor="dia-semana">Dia da Semana</label>
          <select
            id="dia-semana"
            value={diaSemana}
            onChange={(e) => setDiaSemana(e.target.value)}
            required
          >
            <option value="" disabled>
              Selecione o dia
            </option>
            <option value="Segunda-feira">Segunda-feira</option>
            <option value="Terça-feira">Terça-feira</option>
            <option value="Quarta-feira">Quarta-feira</option>
            <option value="Quinta-feira">Quinta-feira</option>
            <option value="Sexta-feira">Sexta-feira</option>
            <option value="Sábado">Sábado</option>
          </select>
        </div>

        {/* Inputs de Horário */}
        <div className="time-inputs-container">
          <div className="input-group">
            <label htmlFor="hora-inicio">Hora de Início</label>
            <input
              type="time"
              id="hora-inicio"
              value={horaInicio}
              onChange={(e) => setHoraInicio(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="hora-fim">Hora de Fim</label>
            <input
              type="time"
              id="hora-fim"
              value={horaFim}
              onChange={(e) => setHoraFim(e.target.value)}
              required
            />
          </div>
        </div>

        {/* Input de Texto para Local */}
        <div className="input-group">
          <label htmlFor="local">Local</label>
          <input
            type="text"
            id="local"
            placeholder="Ex: Sala 201, Bloco B"
            value={local}
            onChange={(e) => setLocal(e.target.value)}
            required
          />
        </div>

        {/* Botão e Mensagens de Feedback */}
        <button type="submit" className="btn btn-primary btn-salvar">
          Salvar Horário
        </button>

        {successMessage && (
          <div className="mensagem-sucesso">{successMessage}</div>
        )}

        {/* Bloco para exibir TODAS as mensagens de erro */}
        {errorMessages.length > 0 && (
          <div className="mensagem-erro">
            {/* Mapeia cada mensagem de erro para um parágrafo */}
            {errorMessages.map((msg, index) => (
              <p key={index}>{msg}</p>
            ))}
          </div>
        )}
      </form>
    </div>
  );
};

export default AdicionarHorario;
