import React from "react";
import { Link } from "react-router-dom";
import "./Home/Main.css";
import enotImage from "./image-2-1.png"; // Замените на путь к вашей картинке

const Welcome = () => {
  return (
    <div className="main-container">
      <div className="main-content">
        <div className="header">
          <h4 className="logo">Логотип</h4>

          <div className="nav">
            <h4 className="nav-item active">Главная</h4>
            <h4 className="nav-item">О нас</h4>
          </div>

          <div className="buttons">
            <Link to="/login">
              <button className="button outlined">Войти</button>
            </Link>
            <Link to="/register">
              <button className="button contained">Регистрация</button>
            </Link>
          </div>
        </div>

        <div className="content-wrapper">
          <div className="text-content">
            <p>Ваш текст здесь</p>
          </div>
          <div className="image-content">
            <img src={enotImage} alt="Описание изображения" className="enot" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Welcome;