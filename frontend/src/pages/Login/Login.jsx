import { useState } from "react";
import { useAuth } from "../../hooks/useAuth"; // hook de autenticação
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "./Login.css";
import loginImage from "../../assets/imagem-login.png";

const Login = () => {
  // Cria estados para os campos do formulário
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault(); // Impede o recarregamento da página
    setError(null);
    try {
      await login(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError("Falha no login. Verifique seu usuário e senha.");
      console.error("Erro de login:", err);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form-wrapper">
        <div className="login-form">
          <h1>Bem-vindo(a)</h1>
          {error && <p className="error-message">{error}</p>}

          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="username">Usuário</label>
              <input
                type="text"
                id="username"
                placeholder="Seu nome de usuário"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Senha</label>
              <input
                type="password"
                id="password"
                placeholder="Sua senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn btn-primary">
              Entrar
            </button>
            <div className="form-link">
              <p>
                Ainda não tem uma conta? <Link to="/cadastro">Cadastre-se</Link>
              </p>
            </div>
          </form>
        </div>
      </div>
      <div className="login-image-wrapper">
        <img src={loginImage} alt="Sala de aula" />
      </div>
    </div>
  );
};

export default Login;
