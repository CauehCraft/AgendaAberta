import "./MeuEvento.css";

const MeuEvento = ({ event }) => {
  return (
    <div className="custom-event-container">
      <strong>{event.title}</strong>
      {/* Você pode adicionar mais informações aqui se quiser, como o local */}
      {/* <p>{event.resource}</p> */}
    </div>
  );
};

export default MeuEvento;
