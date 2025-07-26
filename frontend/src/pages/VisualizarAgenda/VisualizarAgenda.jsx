import React, { useState, useCallback, useEffect } from "react";
import { Calendar, dateFnsLocalizer } from "react-big-calendar";
import { getDay, parse, startOfWeek, format } from "date-fns";
import ptBR from "date-fns/locale/pt-BR";
import ModalDetalhesEvento from "../../components/ModalDetalhesEvento/ModalDetalhesEvento";
import api from "../../services/api";

// Importação obrigatória do CSS da biblioteca
import "react-big-calendar/lib/css/react-big-calendar.css";
import "./VisualizarAgenda.css";

// Configuração do localizer para o date-fns com idioma português
const locales = {
  "pt-BR": ptBR,
};
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

// Tradução da interface do calendário
const messages = {
  allDay: "Dia Inteiro",
  previous: "<",
  next: ">",
  today: "Hoje",
  month: "Mês",
  week: "Semana",
  day: "Dia",
  agenda: "Agenda",
  date: "Data",
  time: "Hora",
  event: "Evento",
  showMore: (total) => `+ Ver mais (${total})`,
  noEventsInRange: "Não há eventos neste período.",
};

// Objeto auxiliar para converter o nome do dia em um número (padrão Date: 0=Domingo)
const diaSemanaParaNumero = {
  Domingo: 0,
  "Segunda-feira": 1,
  "Terça-feira": 2,
  "Quarta-feira": 3,
  "Quinta-feira": 4,
  "Sexta-feira": 5,
  Sábado: 6,
};

const VisualizarAgenda = () => {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [date, setDate] = useState(new Date());
  const [view, setView] = useState("month");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    const fetchAndMapHorarios = async () => {
      setIsLoading(true);
      try {
        const response = await api.get("/horarios/");
        const horariosSemanais = response.data.results || response.data; // Compatível com e sem paginação do DRF

        const mappedEvents = horariosSemanais.flatMap((horario) => {
          const eventosGerados = [];
          const targetDayOfWeek = diaSemanaParaNumero[horario.dia_semana];
          const [startHour, startMinute] = horario.hora_inicio
            .split(":")
            .map(Number);
          const [endHour, endMinute] = horario.hora_fim.split(":").map(Number);

          // Gera eventos para um intervalo de meses (anterior, atual, próximo) para cobrir a visualização
          for (let monthOffset = -1; monthOffset <= 1; monthOffset++) {
            let dataBase = new Date(
              date.getFullYear(),
              date.getMonth() + monthOffset,
              1
            );
            for (let day = 1; day <= 31; day++) {
              let diaCorrente = new Date(
                dataBase.getFullYear(),
                dataBase.getMonth(),
                day
              );

              // Garante que não pule para o próximo mês dentro do loop
              if (diaCorrente.getMonth() !== dataBase.getMonth()) continue;

              if (diaCorrente.getDay() === targetDayOfWeek) {
                eventosGerados.push({
                  id: horario.id, // ID original do horário para a edição
                  title: horario.disciplina.nome,
                  start: new Date(
                    diaCorrente.getFullYear(),
                    diaCorrente.getMonth(),
                    diaCorrente.getDate(),
                    startHour,
                    startMinute
                  ),
                  end: new Date(
                    diaCorrente.getFullYear(),
                    diaCorrente.getMonth(),
                    diaCorrente.getDate(),
                    endHour,
                    endMinute
                  ),
                  resource: horario.local,
                });
              }
            }
          }
          return eventosGerados;
        });

        setEvents(mappedEvents);
      } catch (error) {
        console.error("Erro ao buscar e mapear horários:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAndMapHorarios();
  }, [date]); // Re-executa quando o usuário navega para outro mês/ano

  const handleNavigate = useCallback((newDate) => setDate(newDate), [setDate]);
  const onView = useCallback((newView) => setView(newView), [setView]);

  const handleSelectEvent = useCallback((event) => {
    setSelectedEvent(event);
    setIsModalOpen(true);
  }, []);

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
  };

  return (
    <div className="calendar-container">
      {isLoading ? (
        <h1>Carregando agenda...</h1>
      ) : (
        <Calendar
          localizer={localizer}
          events={events}
          startAccessor="start"
          endAccessor="end"
          style={{ height: "calc(100vh - 10rem)" }}
          culture="pt-BR"
          messages={messages}
          date={date}
          view={view}
          onNavigate={handleNavigate}
          onView={onView}
          onSelectEvent={handleSelectEvent}
        />
      )}

      <ModalDetalhesEvento
        isOpen={isModalOpen}
        onClose={closeModal}
        event={selectedEvent}
      />
    </div>
  );
};

export default VisualizarAgenda;
