import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { AuthContext } from './AuthContext'; // Importa o contexto

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUserFromToken = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        try {
          api.defaults.headers['Authorization'] = `Bearer ${token}`;
          const response = await api.get('/users/me/');
          setUser(response.data); // Usuário logado com sucesso
        } catch (error) {
          console.error("Token inválido ou expirado. Fazendo logout.", error);
          // Se o token for inválido, limpa tudo
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }
      }
      setIsLoading(false); // Finaliza o carregamento inicial
    };

    loadUserFromToken();
  }, []); 

  const login = async (username, password) => {
    try {
      const response = await api.post('/login/', {
        username: username,
        password: password,
      });

      const { access, refresh } = response.data;

      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);

      api.defaults.headers['Authorization'] = `Bearer ${access}`;

      const userResponse = await api.get('/users/me/');
      setUser(userResponse.data);
      
    } catch (error) {
      console.error("Erro na autenticação:", error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    api.defaults.headers['Authorization'] = null;
  };

  const authContextValue = { user, login, logout, isLoading};
  
  if (isLoading) {
    return <h1>Carregando aplicação...</h1>;
  }

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};