import React from "react";
import { Link } from "react-router-dom";
import "./AdminPanel.css";
import womanAvatar1 from "./woman-avatar-1.png";

export default () => {
    return (
        <div className="admin-panel">
            <div className="sidebar">
                <div className="component-2">
                    <div className="vertical-line"></div>
                    <div className="vertical-line"></div>
                    <div className="vertical-line"></div>
                </div>
            </div>
            <div className="main-content">
                <div className="header">
                    <div className="user-info">
                        <img
                            className="woman-avatar"
                            alt="Woman avatar"
                            src={womanAvatar1}
                        />
                        <div className="text-wrapper-2">Admin</div>
                    </div>
                    <Link to="/adm-pan">
                        <button className="back-button">Назад</button>
                    </Link>
                </div>
                <div className="content-split">
                    <div className="left-side">
                        <div className="input-group">
                            <label>Название проекта</label>
                            <input type="text" />
                        </div>
                        <div className="input-group">
                            <label>Описание проекта</label>
                            <textarea />
                        </div>
                        <div className="input-group">
                            <label>Стек технологий</label>
                            <input type="text" />
                        </div>
                        <div className="input-group">
                            <label>Список предлагаемых участников</label>
                            <div className="participants-list">
                                <div className="participant">
                                    <img src={womanAvatar1} alt="Participant" />
                                    <span>Трифанов И.Н.</span>
                                </div>
                                <div className="participant">
                                    <img src={womanAvatar1} alt="Participant" />
                                    <span>Алексеев П.К.</span>
                                </div>
                                <div className="participant">
                                    <img src={womanAvatar1} alt="Participant" />
                                    <span>Чипигин А.С.</span>
                                </div>
                                <div className="participant">
                                    <img src={womanAvatar1} alt="Participant" />
                                    <span>Иванов И.С.</span>
                                </div>
                            </div>
                        </div>
                        <button className="create-project-button">Создать проект</button>
                    </div>
                    <div className="right-side">
                        <div className="input-group">
                            <label>Название задания</label>
                            <input type="text" />
                        </div>
                        <div className="input-group">
                            <label>Добавить пункт задания</label>
                            <button className="add-task-button">+</button>
                        </div>
                        <div className="input-group">
                            <label>Добавить вложения</label>
                            <button className="add-attachment-button">+</button>
                        </div>
                        <div className="input-group">
                            <label>Комментарий</label>
                            <textarea />
                        </div>
                        <button className="save-button">Сохранить</button>
                    </div>
                </div>
            </div>
        </div>
    );
};