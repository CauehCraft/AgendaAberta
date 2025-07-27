import axios from 'axios';

// Cria uma "instância" do axios com configurações pré-definidas
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,

  // Define um tempo máximo para uma requisição (ex: 10 segundos)
  timeout: 10000,

  // Define headers padrão para todas as requisições
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;