import { useAuth } from "../../hooks/useAuth";
import "./Welcome.css";

const Welcome = () => {
  const { user } = useAuth();

  return (
    <div className="welcome-container">
      <header className="main-header">
        <h1>Boas vindas, {user?.nome_completo || user?.username}!</h1>

        <p>
          Você está conectado como {user?.tipo}. Use o menu à esquerda para
          gerenciar sua agenda.
        </p>
      </header>
    </div>
  );
};

export default Welcome;
