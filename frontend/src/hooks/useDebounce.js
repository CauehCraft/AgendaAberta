import { useState, useEffect } from 'react';

function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Configura um timer que só vai atualizar o valor "debatido"
    // após o 'delay' especificado (em milissegundos)
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Limpa o timer se o valor mudar (ex: usuário continua digitando)
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]); // Roda novamente apenas se o valor ou o delay mudar

  return debouncedValue;
}

export default useDebounce;