import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from './axios'; // Импортируем настроенный экземпляр axios

function Login() {
  const [formData, setFormData] = useState({
    login: '',
    password: '',
  });

  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    validateField(name, value);
  };

  const validateField = (name, value) => {
    let isValid = true;
    let errorMessage = '';

    switch (name) {
      case 'login':
        isValid = value.length <= 20;
        errorMessage = isValid ? '' : 'Логин должен быть не более 20 символов.';
        break;
      case 'password':
        isValid = value.length <= 20;
        errorMessage = isValid ? '' : 'Пароль должен быть не более 20 символов.';
        break;
      default:
        break;
    }

    setErrors((prevErrors) => ({ ...prevErrors, [name]: errorMessage }));
    return isValid;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    for (const field in formData) {
      if (!validateField(field, formData[field])) {
        newErrors[field] = errors[field];
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      try {
        const formDataToSend = new FormData();
        formDataToSend.append('username', formData.login);
        formDataToSend.append('password', formData.password);

        const response = await axios.post(
          '/auth/login/',
          formDataToSend,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        );

        if (response.status === 200) {
          console.log('Авторизация успешна:', response.data);

          // Сохранение токена в localStorage
          localStorage.setItem('access_token', response.data.access_token);
          localStorage.setItem('refresh_token', response.data.refresh_token);

          // Перенаправление на главную страницу или другую страницу
          navigate('/');
        }
      } catch (error) {
        if (error.response && error.response.status === 422) {
          setErrors({ server: 'Ошибка валидации данных. Пожалуйста, проверьте введенные данные.' });
        } else if (error.response && error.response.status === 400) {
          setErrors({ server: 'Неверный запрос. Пожалуйста, проверьте введенные данные.' });
        } else {
          setErrors({ server: error.response?.data?.message || 'Неверный логин или пароль.' });
        }
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Авторизация</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        {['login', 'password'].map((field) => (
          <div className="form-group" key={field}>
            <label htmlFor={field}>{field === 'login' ? 'Логин' : 'Пароль'}:</label>
            <input
              type={field === 'password' ? 'password' : 'text'}
              id={field}
              name={field}
              value={formData[field]}
              onChange={handleChange}
            />
            {errors[field] && <span className="error">{errors[field]}</span>}
          </div>
        ))}
        <button type="submit" className="auth-button">Вход</button>
      </form>
      <p>
        Не зарегистрированы? <Link to="/register">Создать аккаунт</Link>
      </p>
      {errors.server && <span className="error">{errors.server}</span>}
    </div>
  );
}

export default Login;