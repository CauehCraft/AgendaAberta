import { useState, useCallback } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import ptBR from 'date-fns/locale/pt-BR';
import ModalDetalhesEvento from '../../components/ModalDetalhesEvento/ModalDetalhesEvento';

import 'react-big-calendar/lib/css/react-big-calendar.css';
import './VisualizarAgenda.css';

const locales = {
  'pt-BR': ptBR,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const mockEvents = [
{
    title: 'Atendimento de Cálculo I',
    start: new Date(2025, 5, 21, 9, 0, 0), // Ano, Mês (0-11), Dia, Hora, Min, Seg
    end: new Date(2025, 5, 21, 10, 0, 0),
    resource: 'Sala 201',
  },
  {
    title: 'Atendimento de Matemática',
    start: new Date(2025, 6, 21, 9, 0, 0), // Ano, Mês (0-11), Dia, Hora, Min, Seg
    end: new Date(2025, 6, 21, 10, 0, 0),
    resource: 'Sala 201',
  },
  {
    title: 'Atendimento de Física',
    start: new Date(2025, 6, 22, 11, 0, 0),
    end: new Date(2025, 6, 22, 12, 0, 0),
    resource: 'Laboratório 1',
  },
  {
    title: 'Atendimento de Química',
    start: new Date(2025, 6, 23, 14, 0, 0),
    end: new Date(2025, 6, 23, 15, 0, 0),
    resource: 'Online',
  },
];

const messages = {
  allDay: 'Dia Inteiro',
  previous: '<',
  next: '>',
  today: 'Hoje',
  month: 'Mês',
  week: 'Semana',
  day: 'Dia',
  agenda: 'Agenda',
  date: 'Data',
  time: 'Hora',
  event: 'Evento',
  showMore: (total) => `+ Ver mais (${total})`,
  noEventsInRange: 'Não há eventos neste período.',
};

const VisualizarAgenda = () => {
    // Estados para controlar a data e a visão atual
  const [date, setDate] = useState(new Date());
  const [view, setView] = useState('month'); // A visão inicial é 'month'

   // Estados para o modal de detalhes
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  // Funções que serão chamadas quando o usuário interagir com o calendário
  const handleNavigate = useCallback((newDate) => setDate(newDate), [setDate]);
  const onView = useCallback((newView) => setView(newView), [setView]);

  // Função para lidar com o clique em um evento
  const handleSelectEvent = useCallback((event) => {
    setSelectedEvent(event); // Guarda as informações do evento clicado
    setIsModalOpen(true);    // Abre o modal
  }, []);

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedEvent(null);
  };

return (
    <div className="calendar-container">
      <Calendar
        localizer={localizer}
        events={mockEvents}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 'calc(100vh - 10rem)' }}
        culture="pt-BR"
        messages={messages}
        date={date}
        view={view}
        onNavigate={handleNavigate}
        onView={onView}
        onSelectEvent={handleSelectEvent}
      />

      <ModalDetalhesEvento
        isOpen={isModalOpen}
        onClose={closeModal}
        event={selectedEvent}
      />
    </div>
  );
};

export default VisualizarAgenda;