import React from 'react';
import './ModalDetalhesEvento.css';
import { FaCalendarAlt, FaClock, FaMapMarkerAlt, FaTimes } from 'react-icons/fa';

const ModalDetalhesEvento = ({ isOpen, onClose, event }) => {
  if (!isOpen || !event) {
    return null;
  }

  // Formata as datas para exibição
  const formatTime = (date) => new Date(date).toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });

  const formatDate = (date) => new Date(date).toLocaleDateString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="modal-overlay-details" onClick={onClose}>
      <div className="modal-content-details" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-btn" onClick={onClose}>
          <FaTimes />
        </button>
        <h2 className="modal-details-title">{event.title}</h2>
        
        <div className="modal-details-body">
          <div className="detail-item">
            <FaCalendarAlt className="detail-icon" />
            <span>{formatDate(event.start)}</span>
          </div>
          <div className="detail-item">
            <FaClock className="detail-icon" />
            <span>{`${formatTime(event.start)} - ${formatTime(event.end)}`}</span>
          </div>
          {event.resource && (
            <div className="detail-item">
              <FaMapMarkerAlt className="detail-icon" />
              <span>{event.resource}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ModalDetalhesEvento;