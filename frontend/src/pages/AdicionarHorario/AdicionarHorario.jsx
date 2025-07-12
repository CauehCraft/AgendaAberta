import React, { useState } from 'react';
import DatePicker, { registerLocale } from 'react-datepicker';
import ptBR from 'date-fns/locale/pt-BR';
import 'react-datepicker/dist/react-datepicker.css';

import './AdicionarHorario.css';

registerLocale('pt-BR', ptBR);

const AdicionarHorario = () => {
  // 1. Estados para controlar todos os campos do formulário
  const [dataInicio, setDataInicio] = useState(null);
  const [dataFim, setDataFim] = useState(null);
  const [local, setLocal] = useState(''); // Estado para o local

  // 2. Função para lidar com a submissão do formulário
  const handleSubmit = (event) => {
    event.preventDefault(); // Previne o recarregamento da página

    // Validação básica
    if (!dataInicio || !dataFim || !local) {
      alert('Por favor, preencha todos os campos.');
      return;
    }

    // Objeto com os dados do formulário
    const dadosFormulario = {
      inicio: dataInicio,
      fim: dataFim,
      local: local,
    };

    console.log('Dados a serem salvos:', dadosFormulario);
    // Lógica para enviar os dados para um backend, etc.
    alert('Horário salvo com sucesso!');
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Adicionar Horário</h1>
      <form onSubmit={handleSubmit}>
        <div className="time-inputs-container">
          <div className="input-group">
            <label htmlFor="horario-inicio">Horário de Início</label>
            <DatePicker
              selected={dataInicio}
              onChange={(date) => setDataInicio(date)}
              selectsStart 
              startDate={dataInicio}
              endDate={dataFim}
              showTimeSelect
              locale="pt-BR"
              dateFormat="dd/MM/yyyy, HH:mm"
              timeFormat="HH:mm"
              placeholderText="Selecione data e hora"
              className="date-picker-input"
            />
          </div>
          <div className="input-group">
            <label htmlFor="horario-fim">Horário de Fim</label>
            <DatePicker
              selected={dataFim}
              onChange={(date) => setDataFim(date)}
              selectsEnd 
              startDate={dataInicio}
              endDate={dataFim}
              minDate={dataInicio}
              showTimeSelect
              locale="pt-BR"
              dateFormat="dd/MM/yyyy, HH:mm"
              timeFormat="HH:mm"
              placeholderText="Selecione data e hora"
              className="date-picker-input"
            />
          </div>
        </div>

        <div className="input-group dropdown-group">
          <label htmlFor="local">Local</label>
          <select
            id="local"
            value={local}
            onChange={(e) => setLocal(e.target.value)}
          >
            <option value="" disabled>Insira o Local</option>
            <option value="sala1">Sala 1</option>
            <option value="auditorio">Auditório</option>
            {/* ... outras opções ... */}
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