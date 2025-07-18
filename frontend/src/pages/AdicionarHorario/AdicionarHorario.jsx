import React, { useState, useEffect, useRef } from 'react';
import DatePicker, { registerLocale } from 'react-datepicker';
import ptBR from 'date-fns/locale/pt-BR';

import 'react-datepicker/dist/react-datepicker.css';
import './AdicionarHorario.css';

registerLocale('pt-BR', ptBR);

const AdicionarHorario = () => {
  const [dataInicio, setDataInicio] = useState(null);
  const [dataFim, setDataFim] = useState(null);
  const [local, setLocal] = useState('');
  const [mensagemSucesso, setMensagemSucesso] = useState('');
  
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      clearTimeout(timerRef.current);
    };
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault(); 
    setMensagemSucesso('');
    clearTimeout(timerRef.current); // Limpa qualquer timer anterior

    if (!dataInicio || !dataFim || !local) {
      alert('Por favor, preencha todos os campos obrigatórios.');
      return;
    }
    
    if (dataFim <= dataInicio) {
      alert('Erro: O horário de fim deve ser posterior ao horário de início.');
      return;
    }

    setMensagemSucesso('Horário salvo com sucesso!');

    // Limpa os campos do formulário
    setDataInicio(null);
    setDataFim(null);
    setLocal('');
    
    timerRef.current = setTimeout(() => {
      setMensagemSucesso('');
    }, 4000);
  };

  return (
    <div className="form-container">
      <h1 className="form-title">Adicionar Horário</h1>
      
      <form onSubmit={handleSubmit}>
        <div className="time-inputs-container">
          <div className="input-group">
            <label htmlFor="horario-inicio">Horário de Início</label>
            <DatePicker
              id="horario-inicio"
              selected={dataInicio}
              onChange={(date) => {
                setDataInicio(date);
                setDataFim(null);
              }}
              selectsStart
              startDate={dataInicio}
              endDate={dataFim}
              minDate={new Date()}
              showTimeSelect
              locale="pt-BR"
              dateFormat="dd/MM/yyyy, HH:mm"
              timeFormat="HH:mm"
              placeholderText="Selecione data e hora"
              autoComplete="off"
            />
          </div>
          <div className="input-group">
            <label htmlFor="horario-fim">Horário de Fim</label>
            <DatePicker
              id="horario-fim"
              selected={dataFim}
              onChange={(date) => setDataFim(date)}
              selectsEnd
              startDate={dataInicio}
              endDate={dataFim}
              minDate={dataInicio}
              showTimeSelect={!!dataInicio}
              locale="pt-BR"
              dateFormat="dd/MM/yyyy, HH:mm"
              placeholderText={dataInicio ? "Selecione data e hora" : "Selecione o início primeiro"}
              autoComplete="off"
              disabled={!dataInicio}
            />
          </div>
        </div>

        <div className="input-group dropdown-group">
          <label htmlFor="local">Local</label>
          <select id="local" value={local} onChange={(e) => setLocal(e.target.value)}>
            <option value="" disabled>Insira o Local</option>
            <option value="Sala de Reuniões 1">Sala de Reuniões 1</option>
            <option value="Sala de Reuniões 2">Sala de Reuniões 2</option>
            <option value="Auditório Principal">Auditório Principal</option>
            <option value="Laboratório de Inovação">Laboratório de Inovação</option>
            <option value="Espaço Café">Espaço Café</option>
          </select>
        </div>

        <button type="submit" className="btn btn-primary btn-salvar">
          Salvar
        </button>
      </form>
      
      {mensagemSucesso && (
        <div className="mensagem-sucesso"> 
          {mensagemSucesso}
        </div>
      )}
    </div>
  );
};

export default AdicionarHorario;