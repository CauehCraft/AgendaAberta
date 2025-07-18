import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const ProtectedRoute = () => {
  const { user } = useAuth();

  // Se não há usuário logado, redireciona para a página de login
  if (!user) {
    return <Navigate to="/login" />;
  }

  // Se o usuário está logado, renderiza o conteúdo da rota (o <Outlet />)
  return <Outlet />;
};

export default ProtectedRoute;