import React from "react";
import { Link } from "react-router-dom";
import "./Main.css";
import Tasks from "../frontILIA/my-app/src/Tasks"

const Main = () => {
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
        <Tasks />
      </div>
    </div>
  );
};

export default Main;