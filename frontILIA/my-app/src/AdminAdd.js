// Импорт необходимых модулей
import React, { useState, useEffect } from "react";
import "./AdminPanel.css";
import axiosInstance from './axiosInstance.js';

// Статические участники будут обновляться при выборе участников через кнопку
const initialParticipants = [];


// Функция для получения стеков
const GetSteck = async () => {
    try {
        const response = await axiosInstance.get('/tools/');
        return response.data;
    } catch (error) {
        console.error('Ошибка при получении стеков:', error);
        throw error;
    }
};

// Функция для добавления задачи в master_task
const addTaskToMasterTask = async (master_task_id, user_id, title, description, stack) => {
    try {
        const response = await axiosInstance.post(`/master_tasks/${master_task_id}/add_task/`, {
            user_id,
            title,
            description,
            stack,
        });
        return response.data;
    } catch (error) {
        console.error('Ошибка при добавлении задачи:', error);
        throw error;
    }
};

// Функция для добавления точки в задачу
const addPointToTask = async (task_id, text) => {
    try {
        const response = await axiosInstance.post(`/tasks/${task_id}/add_point/`, {
            text,
        });
        return response.data;
    } catch (error) {
        console.error('Ошибка при добавлении точки:', error);
        throw error;
    }
};

// Функция для добавления комментария в задачу
const addCommentToTask = async (task_id, user_id, text) => {
    try {
        const response = await axiosInstance.post(`/tasks/${task_id}/add_comment/`, {
            user_id,
            text,
        });
        return response.data;
    } catch (error) {
        console.error('Ошибка при добавлении комментария:', error);
        throw error;
    }
};

export default () => {
    const [selectedParticipant, setSelectedParticipant] = useState(null);
    const [tasks, setTasks] = useState([]);
    const [stacks, setStacks] = useState([]);
    const [projectName, setProjectName] = useState("");
    const [deadline, setDeadline] = useState("");
    const [selectedStack, setSelectedStack] = useState("");
    const [selectedParticipants, setSelectedParticipants] = useState([]);
    const [participants, setParticipants] = useState(initialParticipants);
    const [masterTaskId, setMasterTaskId] = useState(null);
    const [taskTitle, setTaskTitle] = useState(""); // Состояние для названия задания
    const [taskDescription, setTaskDescription] = useState(""); // Состояние для описания задания

    useEffect(() => {
        const fetchStacks = async () => {
            try {
                const stacksData = await GetSteck();
                setStacks(stacksData);
            } catch (error) {
                console.error("Ошибка при загрузке стеков:", error);
            }
        };

        fetchStacks();
    }, []);

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

    const handleSelectParticipants = async () => {
        try {
            const masterTaskResponse = await axiosInstance.post('/master_tasks/', {
                name: projectName,
                deadline: deadline
            });
    
            const masterTaskId = masterTaskResponse.data.id; // Используем masterTaskId
            setMasterTaskId(masterTaskId); // Сохранение masterTaskId в состояние
    
            const aiResponse = await axiosInstance.post('/ai/', {
                master_task_id: masterTaskId,
                stack: [selectedStack]
            });
    
            const updatedParticipants = aiResponse.data.map(user => ({
                id: user.id,
                name: user.fullname
            }));
    
            setParticipants(updatedParticipants);
        } catch (error) {
            console.error("Ошибка при подборе участников:", error);
        }
    };
    

    const createProject = async () => {
        try {
            for (const participant of selectedParticipants) {
                    console.log("Добавление задачи для участника:", participant);
                    const newTask = await addTaskToMasterTask(masterTaskId, participant.id, taskTitle, taskDescription, [parseInt(selectedStack)]);
                    
                    // Добавляем комментарий
                    // await addCommentToTask(newTask.id, participant.id, "Комментарий к задаче");

                    // Добавляем точки в задачу
                    // const points = task.points || []; // Предполагается, что задачи могут иметь массив точек
                    // for (const point of points) {
                    //     await addPointToTask(newTask.id, point);
                    // }
            }

            // Можно сбросить состояние после создания проекта
            setTasks([]);
            setSelectedParticipants([]);
            setProjectName("");
            setDeadline("");
            setSelectedStack("");
        } catch (error) {
            console.error("Ошибка при создании проекта:", error);
        }
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
                            <input 
                                type="text" 
                                placeholder="Название проекта" 
                                value={projectName} 
                                onChange={(e) => setProjectName(e.target.value)} 
                            />
                        </div>
                        <div className="input-group">
                            <textarea placeholder="Описание проекта" />
                        </div>
                        <div className="inp_fir">
                            <input 
                                type="date" 
                                placeholder="Дата завершения" 
                                value={deadline} 
                                onChange={(e) => setDeadline(e.target.value)} 
                            />
                        </div>
                        <div className="input-group">
                            <input 
                                type="text" 
                                placeholder="Стек технологий" 
                                list="technologies" 
                                value={selectedStack} 
                                onChange={(e) => setSelectedStack(e.target.value)} 
                            />
                            <datalist id="technologies">
                                {stacks.map((stack) => (
                                    <option key={stack.id} value={stack.id}>{stack.name}</option>
                                ))}
                            </datalist>
                        </div>
                        <button 
                            className="select-participants-button" 
                            onClick={handleSelectParticipants}
                        >
                            Подобрать участников
                        </button>

                        {/* Отображение обновленного списка участников */}
                        <div className="participants-list">
                            {participants.map((participant) => (
                                <div
                                    key={participant.id}
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
                                    <input 
                                        type="text" 
                                        placeholder="Название задания" 
                                        value={taskTitle} 
                                        onChange={(e) => setTaskTitle(e.target.value)} // Сохраняем название задания
                                    />
                                </div>
                                <div className="input-group">
                                    <textarea 
                                        placeholder="Описание" 
                                        rows="4" 
                                        value={taskDescription} 
                                        onChange={(e) => setTaskDescription(e.target.value)} // Сохраняем описание задания
                                    />
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
                                <button className="create-project-button" onClick={createProject}>Создать проект</button>
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
