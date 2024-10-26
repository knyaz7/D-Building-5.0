import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from './axios'; // Импортируем настроенный экземпляр axios

function Register() {
  const [formData, setFormData] = useState({
    FIO: '',
    login: '',
    password: '',
    confirmPassword: '',
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
      case 'FIO':
        isValid = /^[А-Яа-яЁё\s-]{1,50}$/.test(value);
        errorMessage = isValid ? '' : 'ФИО должно содержать только кириллицу, пробелы и дефисы (до 50 символов).';
        break;
      case 'login':
        isValid = value.length <= 20;
        errorMessage = isValid ? '' : 'Логин должен быть не более 20 символов.';
        break;
      case 'password':
        isValid = value.length <= 20;
        errorMessage = isValid ? '' : 'Пароль должен быть не более 20 символов.';
        break;
      case 'confirmPassword':
        isValid = value === formData.password;
        errorMessage = isValid ? '' : 'Пароли не совпадают.';
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
        const response = await axios.post(
          '/users/',
          {
            username: formData.login,
            fullname: formData.FIO,
            password: formData.password
          },
          { headers: { 'Content-Type': 'application/json' } }
        );

        if (response.status === 200) {
          console.log('Пользователь успешно зарегистрирован:', response.data);

          // Сохранение токена в localStorage
          localStorage.setItem('token', response.data.access_key);

          // Перенаправление на главную страницу или другую страницу
          navigate('/');
        }
      } catch (error) {
        if (error.response && error.response.status === 422) {
          setErrors({ server: 'Ошибка валидации данных. Пожалуйста, проверьте введенные данные.' });
        } else if (error.response && error.response.status === 400) {
          setErrors({ server: 'Неверный запрос. Пожалуйста, проверьте введенные данные.' });
        } else {
          setErrors({ server: error.response?.data?.message || error.message });
        }
      }
    }
  };

  return (
    <div className="auth-container">
      <h2>Регистрация</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        {['FIO', 'login', 'password', 'confirmPassword'].map((field) => (
          <div className="form-group" key={field}>
            <label htmlFor={field}>
              {field === 'FIO' ? 'ФИО' : 
               field === 'login' ? 'Логин' : 
               field === 'password' ? 'Пароль' : 
               field === 'confirmPassword' ? 'Повторите пароль' : 
               field}:
            </label>
            <input
              type={field === 'password' || field === 'confirmPassword' ? 'password' : 'text'}
              id={field}
              name={field}
              value={formData[field]}
              onChange={handleChange}
            />
            {errors[field] && <span className="error">{errors[field]}</span>}
          </div>
        ))}
        <button type="submit" className="auth-button">Зарегистрироваться</button>
      </form>
      <p>
        Уже зарегистрированы? <Link to="/login">Войти</Link>
      </p>
      {errors.server && <span className="error">{errors.server}</span>}
    </div>
  );
}

export default Register;