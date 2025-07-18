import React, { useState } from 'react';
import { AuthContext } from './AuthContext'; // Importa o contexto

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (username, password) => {
    console.log("Lógica de login a ser implementada", { username, password });
    setUser({ username: username, name: "Usuário Logado" });
  };

  const logout = () => {
    setUser(null);
  };

  const authContextValue = { user, login, logout };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};