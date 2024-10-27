import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Перехват запросов для добавления токена
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Перехват ответов для обработки истекшего токена
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Проверка, что ошибка связана с истечением токена
    if (
      error.response &&
      error.response.data &&
      error.response.data.detail === 'Token expired'
    ) {
      try {
        // Получение refresh токена из localStorage
        const refreshToken = localStorage.getItem('refresh_token');

        if (!refreshToken) {
          throw new Error('Отсутствует refresh токен');
        }

        // Обновление токена
        const refreshResponse = await axios.post(
          'http://localhost:8000/api/v1/auth/token_refresh/',
          {
            refresh_token: refreshToken,
          }
        );

        const newToken = refreshResponse.data.access_key;
        localStorage.setItem('access_token', newToken);

        // Повторный запрос с обновленным токеном
        error.config.headers['Authorization'] = `Bearer ${newToken}`;
        return axiosInstance(error.config);

      } catch (refreshError) {
        console.error('Ошибка при обновлении токена:', refreshError);
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;