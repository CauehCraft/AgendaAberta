import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../services/api";
import "./EditarHorario.css";

const EditarHorario = () => {
  const { horarioId } = useParams();
  const navigate = useNavigate();

  // Estados para o formulário
  const [formData, setFormData] = useState({
    disciplina: "",
    dia_semana: "",
    hora_inicio: "",
    hora_fim: "",
    local: "",
  });
  const [disciplinas, setDisciplinas] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState("");

  const [errors, setErrors] = useState({
    disciplina: null,
    dia_semana: null,
    hora_inicio: null,
    hora_fim: null,
    local: null,
    non_field_errors: null,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const disciplinasResponse = await api.get("/disciplinas/");
        setDisciplinas(disciplinasResponse.data);

        const horarioResponse = await api.get(`/horarios/${horarioId}/`);
        const horarioData = horarioResponse.data;

        setFormData({
          disciplina: horarioData.disciplina.id,
          dia_semana: horarioData.dia_semana,
          hora_inicio: horarioData.hora_inicio,
          hora_fim: horarioData.hora_fim,
          local: horarioData.local,
        });
      } catch (err) {
        setErrors({
          non_field_errors: "Não foi possível carregar os dados para edição.",
        });
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [horarioId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSuccessMessage("");
    // Limpa os erros antigos antes de cada submissão
    setErrors({
      disciplina: null,
      dia_semana: null,
      hora_inicio: null,
      hora_fim: null,
      local: null,
      non_field_errors: null,
    });

    try {
      // Usamos PATCH para atualizações parciais, o que é uma boa prática.
      await api.patch(`/horarios/${horarioId}/`, formData);
      setSuccessMessage("Horário atualizado com sucesso! Redirecionando...");

      setTimeout(() => navigate("/dashboard/gerenciar-horarios"), 2000);
    } catch (err) {
      // Lógica para extrair e exibir erros específicos do backend
      if (err.response && err.response.data && err.response.data.errors) {
        const backendErrors = err.response.data.errors;
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
        // Erro de rede ou outro problema não relacionado à validação
        setErrors({
          non_field_errors:
            "Ocorreu um erro de comunicação ao salvar as alterações.",
        });
      }
    }
  };

  const errorMessages = Object.values(errors).filter((error) => error !== null);

  if (isLoading) {
    return (
      <div className="form-container">
        <h1>Carregando dados para edição...</h1>
      </div>
    );
  }

  return (
    <div className="form-container">
      <h1 className="form-title">Editar Horário</h1>
      <form onSubmit={handleSubmit}>
        {/* Campo Disciplina */}
        <div className="input-group">
          <label htmlFor="disciplina">Disciplina</label>
          <select
            name="disciplina"
            id="disciplina"
            value={formData.disciplina}
            onChange={handleChange}
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

        {/* Campo Dia da Semana */}
        <div className="input-group">
          <label htmlFor="dia_semana">Dia da Semana</label>
          <select
            name="dia_semana"
            id="dia_semana"
            value={formData.dia_semana}
            onChange={handleChange}
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

        {/* Campos de Horário */}
        <div className="time-inputs-container">
          <div className="input-group">
            <label htmlFor="hora_inicio">Hora de Início</label>
            <input
              type="time"
              name="hora_inicio"
              id="hora_inicio"
              value={formData.hora_inicio}
              onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="hora_fim">Hora de Fim</label>
            <input
              type="time"
              name="hora_fim"
              id="hora_fim"
              value={formData.hora_fim}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        {/* Campo Local */}
        <div className="input-group">
          <label htmlFor="local">Local</label>
          <input
            type="text"
            name="local"
            id="local"
            placeholder="Ex: Sala 201, Bloco B"
            value={formData.local}
            onChange={handleChange}
            required
          />
        </div>

        {/* Botão e Mensagens de Feedback */}
        <button type="submit" className="btn btn-primary btn-salvar">
          Salvar Alterações
        </button>

        {successMessage && (
          <div className="mensagem-sucesso">{successMessage}</div>
        )}

        {/* Bloco para exibir TODAS as mensagens de erro */}
        {errorMessages.length > 0 && (
          <div className="mensagem-erro">
            {errorMessages.map((msg, index) => (
              <p key={index}>{msg}</p>
            ))}
          </div>
        )}
      </form>
    </div>
  );
};

export default EditarHorario;
