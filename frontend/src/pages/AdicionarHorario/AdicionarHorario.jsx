import React from 'react';
import './AdicionarHorario.css';

const AdicionarHorario = () => {
  return (
    <div className="form-container">
      <h1 className="form-title">Adicionar Horário</h1>
      <form>
        <div className="input-group dropdown-group">
          <label htmlFor="dia-semana">Dia da Semana</label>
          <select id="dia-semana" defaultValue="">
            <option value="" disabled>Selecione o Dia</option>
            <option value="seg">Segunda-feira</option>
            <option value="ter">Terça-feira</option>
            <option value="qua">Quarta-feira</option>
            <option value="qui">Quinta-feira</option>
            <option value="sex">Sexta-feira</option>
          </select>
        </div>

        <div className="time-inputs-container">
          <div className="input-group">
            <label htmlFor="horario-inicio">Horário de Início</label>
            <div className="time-input-wrapper">
              <input id="horario-inicio" type="datetime-local" />
            </div>
          </div>
          <div className="input-group">
            <label htmlFor="horario-fim">Horário de Fim</label>
            <div className="time-input-wrapper">
              <input id="horario-fim" type="datetime-local" />
            </div>
          </div>
        </div>

        <div className="input-group dropdown-group">
          <label htmlFor="local">Local</label>
          <select id="local" defaultValue="">
            <option value="" disabled>Insira o Local</option>
            <option value="sala_201">Sala 201</option>
            <option value="lab_info_1">Laboratório de Informática 1</option>
            <option value="online">Online</option>
          </select>
        </div>

        <button type="submit" className="btn btn-primary btn-salvar">
          Salvar
        </button>
      </form>
    </div>
  );
};

export default AdicionarHorario;