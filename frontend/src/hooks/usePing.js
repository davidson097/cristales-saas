import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';

/**
 * Hook to test backend connectivity with ping
 */
export function usePing() {
  const [status, setStatus] = useState('idle'); // idle, loading, success, error
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    const ping = async () => {
      setStatus('loading');
      try {
        const result = await apiClient.ping();
        setData(result);
        setStatus('success');
        setError(null);
      } catch (err) {
        setStatus('error');
        setError(err.message);
        setData(null);
      }
    };

    ping();
  }, []);

  return { status, error, data };
}
