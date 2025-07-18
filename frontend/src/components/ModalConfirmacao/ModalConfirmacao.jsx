import React from 'react';
import './ModalConfirmacao.css';
import { FaExclamationTriangle } from 'react-icons/fa';

const ModalConfirmacao = ({ isOpen, onClose, onConfirm, title, children }) => {
  if (!isOpen) {
    return null; // Não renderiza nada se não estiver aberto
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <FaExclamationTriangle className="modal-icon" />
          <h2 className="modal-title">{title}</h2>
        </div>
        <div className="modal-body">
          {children}
        </div>
        <div className="modal-footer">
          <button onClick={onClose} className="btn-cancel">
            Cancelar
          </button>
          <button onClick={onConfirm} className="btn-confirm">
            Confirmar Exclusão
          </button>
        </div>
      </div>
    </div>
  );
};

export default ModalConfirmacao;