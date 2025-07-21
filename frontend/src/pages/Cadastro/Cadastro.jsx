import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../services/api";
import "./Cadastro.css";

const Cadastro = () => {
  const [formData, setFormData] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    tipo: "aluno",
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const navigate = useNavigate();

  const validateField = (name, value) => {
    if (name === "username" && value.includes(" ")) {
      return "O nome de usuário não pode conter espaços.";
    }
    if (
      name === "email" &&
      value.length > 0 &&
      !/@(ufersa\.edu\.br|alunos\.ufersa\.edu\.br)$/.test(value)
    ) {
      return "O email deve ser @ufersa.edu.br ou @alunos.ufersa.edu.br.";
    }
    return "";
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    const fieldError = validateField(name, value);
    setErrors({ ...errors, [name]: fieldError });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError("");

    for (const key in formData) {
      const fieldError = validateField(key, formData[key]);
      if (fieldError) {
        setErrors((prev) => ({ ...prev, [key]: fieldError }));
        return;
      }
    }

    try {
      await api.post("/register/", formData);
      alert(
        "Cadastro realizado com sucesso! Você será redirecionado para o login."
      );
      navigate("/login");
    } catch (err) {
      const backendErrors = err.response?.data;
      if (backendErrors) {
        setErrors(backendErrors);
      } else {
        setApiError("Ocorreu um erro inesperado. Tente novamente.");
      }
    }
  };

  return (
    <div className="form-container-wrapper">
      <div className="form-box">
        <h1>Crie sua Conta</h1>
        {apiError && <p className="api-error-message">{apiError}</p>}
        <form onSubmit={handleSubmit} noValidate>
          <div className="input-group">
            <label htmlFor="first_name">Nome</label>
            <input
              type="text"
              name="first_name"
              id="first_name"
              required
              onChange={handleChange}
            />
          </div>
          <div className="input-group">
            <label htmlFor="last_name">Sobrenome</label>
            <input
              type="text"
              name="last_name"
              id="last_name"
              required
              onChange={handleChange}
            />
          </div>
          <div className="input-group">
            <label htmlFor="username">Nome de Usuário</label>
            <input
              type="text"
              name="username"
              id="username"
              required
              onChange={handleChange}
            />
            {errors.username && (
              <p className="field-error-message">{errors.username}</p>
            )}
          </div>
          <div className="input-group">
            <label htmlFor="email">E-mail Institucional</label>
            <input
              type="email"
              name="email"
              id="email"
              required
              onChange={handleChange}
            />
            {errors.email && (
              <p className="field-error-message">{errors.email}</p>
            )}
          </div>
          <div className="input-group">
            <label htmlFor="password">Senha</label>
            <input
              type="password"
              name="password"
              id="password"
              required
              onChange={handleChange}
            />
            {errors.password && (
              <p className="field-error-message">{errors.password}</p>
            )}
          </div>
          <div className="input-group">
            <label htmlFor="tipo">Eu sou:</label>
            <select
              name="tipo"
              id="tipo"
              value={formData.tipo}
              onChange={handleChange}
            >
              <option value="aluno">Aluno</option>
              <option value="professor">Professor</option>
              <option value="monitor">Monitor</option>
            </select>
          </div>
          <button type="submit" className="btn-primary">
            Cadastrar
          </button>
          <div className="form-link">
            <p>
              Já tem uma conta? <Link to="/login">Faça o login</Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Cadastro;
