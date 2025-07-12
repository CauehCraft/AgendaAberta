import React from 'react';
import './Login.css';
import loginImage from '../../assets/imagem-login.png'; 

const Login = () => {
  return (
    <div className="login-container">
      <div className="login-form-wrapper">
        <div className="login-form">
          <h1>Bem-vindo(a)</h1>
          <form>
            <div className="input-group">
              <label htmlFor="email">E-mail</label>
              <input
                type="email"
                id="email"
                placeholder="seuemail@email.com"
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Senha</label>
              <input type="password" id="password" placeholder="Sua senha" />
            </div>

            <div className="input-group">
              <label htmlFor="user-type">Tipo de usuário</label>
              <select id="user-type" defaultValue="">
                <option value="" disabled>
                  Selecione
                </option>
                <option value="professor">Professor</option>
                <option value="aluno">Aluno</option>
              </select>
            </div>
            <button type="submit" className="btn btn-primary">
              Entrar
            </button>
            <button type="button" className="btn btn-secondary">
              Cadastrar
            </button>
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