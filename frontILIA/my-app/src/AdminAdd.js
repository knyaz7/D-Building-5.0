import React, { useState } from "react";
import "./AdminPanel.css";
import womanAvatar1 from "./woman-avatar-1.png";

const participants = [
    { name: "Трифанов И.Н." },
    { name: "Алексеев П.К." },
    { name: "Чипигин А.С." },
    { name: "Иванов И.С." },
];

export default () => {
    const [selectedParticipant, setSelectedParticipant] = useState(null);
    const [selectedParticipants, setSelectedParticipants] = useState([]);
    const [tasks, setTasks] = useState([]);

    const handleParticipantClick = (participant) => {
        setSelectedParticipant(participant);
    };

    const handleCheckboxChange = (event, participant) => {
        if (event.target.checked) {
            setSelectedParticipants([...selectedParticipants, participant]);
        } else {
            setSelectedParticipants(selectedParticipants.filter(p => p !== participant));
        }
    };

    const addTask = () => {
        setTasks([...tasks, ""]);
    };

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
                <div className="content-split">
                    <div className="left-side">
                        <h1 className="create-project-title">Создание проекта</h1>
                        <div className="input-group">
                            <input type="text" placeholder="Название проекта" />
                        </div>
                        <div className="input-group">
                            <textarea placeholder="Описание проекта" />
                        </div>
                        <div className="inp_fir">
                            <div className="date-inputs">
                                <input type="date" placeholder="Начальная дата" />
                                <input type="date" placeholder="Конечная дата" />
                            </div>
                        </div>
                        <div className="input-group">
                            <input type="text" placeholder="Стек технологий" list="technologies" />
                            <datalist id="technologies">
                                <option value="Next.js" />
                                <option value="PHP" />
                                <option value="SQL" />
                                <option value="React.js" />
                                <option value="Docker" />
                            </datalist>
                        </div>
                        <button className="select-participants-button">Подобрать участников</button>
                        <div className="participants-list">
                            {participants.map((participant, index) => (
                                <div
                                    key={index}
                                    className={`participant ${selectedParticipant === participant ? "selected" : ""}`}
                                    onClick={() => handleParticipantClick(participant)}
                                >
                                    <span>{participant.name}</span>
                                    <input
                                        type="checkbox"
                                        checked={selectedParticipants.includes(participant)}
                                        onChange={(event) => handleCheckboxChange(event, participant)}
                                    />
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="right-side">
                        {selectedParticipant ? (
                            <>
                                <h2 className="participant-name">{selectedParticipant.name}</h2>
                                <div className="input-group">
                                    <input type="text" placeholder="Название задания" />
                                </div>
                                <div className="input-group">
                                    <textarea placeholder="Описание" rows="4" />
                                </div>
                                <div className="tasks-container">
                                    <div className="tasks-list">
                                        {tasks.map((task, index) => (
                                            <input
                                                key={index}
                                                type="text"
                                                placeholder={`Задача ${index + 1}`}
                                            />
                                        ))}
                                    </div>
                                    <button className="add-task-button" onClick={addTask}>+</button>
                                </div>
                                <div className="input-group">
                                    <textarea placeholder="Комментарий" rows="4" />
                                </div>
                                <button className="create-project-button">Создать проект</button>
                            </>
                        ) : (
                            <p className="no-participant-selected">Выберите участника</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};