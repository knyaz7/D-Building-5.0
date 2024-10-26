import React, { useState, useEffect } from 'react';
import './TaskBoard.css';
import { updateTaskStatus, GetTasks } from '../api';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

const TaskBoard = ({ onDeleteTask, onOpenTask, onMoveTask }) => {
  const columns = {
    1: 'To Do',
    2: 'To Do Faster',
    3: 'In Progress',
    4: 'Testing',
    5: 'Done',
  };

  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      setIsLoading(true);
      try {
        const stagesData = await GetTasks();
        
        // Добавляем статус для каждой задачи
        const loadedTasks = stagesData.flatMap(stage =>
          stage.tasks.map(task => ({ ...task, statusId: stage.id }))
        );
        
        setTasks(loadedTasks);
      } catch (error) {
        console.error('Ошибка при загрузке задач:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, []);

  const onDragEnd = async (result) => {
    const { draggableId, source, destination } = result;

    // Проверяем, что есть куда перемещать задачу
    if (!destination || source.droppableId === destination.droppableId) return;

    const taskId = parseInt(draggableId, 10);
    const fromColumnId = parseInt(source.droppableId, 10);
    const toColumnId = parseInt(destination.droppableId, 10);

    // Обновление на клиенте
    setTasks(prevTasks =>
      prevTasks.map(task => 
        task.id === taskId ? { ...task, statusId: toColumnId } : task
      )
    );

    // Отправка данных на сервер
    try {
      await updateTaskStatus(taskId, fromColumnId, toColumnId);
    } catch (error) {
      console.error('Ошибка при обновлении задачи на сервере:', error);
    }
  };

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="task-board">
        {isLoading ? (
          <div className="loading-indicator">Загрузка задач...</div>
        ) : (
          Object.keys(columns).map((statusId) => (
            <Droppable droppableId={statusId} key={statusId}>
              {(provided) => (
                <div
                  className="column"
                  data-status={statusId}
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                >
                  <h2>{columns[statusId]}</h2>
                  <ul>
                    {tasks
                      .filter(task => task.statusId === Number(statusId))
                      .map((task, index) => (
                        <Draggable key={task.id} draggableId={task.id.toString()} index={index}>
                          {(provided) => (
                            <li
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              className="task"
                            >
                              <h3>{task.title}</h3>
                              <p>Исполнитель: {task.assignee}</p>
                              <div>
                                <button onClick={() => onOpenTask(task.id)}>Открыть</button>
                                <button onClick={() => onDeleteTask(task.id)}>Удалить</button>
                              </div>
                            </li>
                          )}
                        </Draggable>
                      ))}
                    {provided.placeholder}
                  </ul>
                </div>
              )}
            </Droppable>
          ))
        )}
      </div>
    </DragDropContext>
  );
};

export default TaskBoard;