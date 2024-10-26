// src/data/tasks.js
const tasks = [
    // Задачи со статусом 'todo'
    { id: 1, title: 'Задача 1', body: 'Описание задачи 1', assignee: 'Иванов', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 2, title: 'Задача 2', body: 'Описание задачи 2', assignee: 'Петров', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 3, title: 'Задача 3', body: 'Описание задачи 3', assignee: 'Сидоров', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 4, title: 'Задача 4', body: 'Описание задачи 4', assignee: 'Козлов', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 5, title: 'Задача 5', body: 'Описание задачи 5', assignee: 'Михайлов', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 6, title: 'Задача 6', body: 'Описание задачи 6', assignee: 'Иванов', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
    { id: 7, title: 'Задача 7', body: 'Описание задачи 7', assignee: 'Петров', status: 'todo', menu: ['Действие 1', 'Действие 2'] },
  
    // Задачи со статусом 'todo_suka'
    { id: 8, title: 'Задача 8', body: 'Описание задачи 8', assignee: 'Иванов', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 9, title: 'Задача 9', body: 'Описание задачи 9', assignee: 'Петров', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 10, title: 'Задача 10', body: 'Описание задачи 10', assignee: 'Сидоров', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 11, title: 'Задача 11', body: 'Описание задачи 11', assignee: 'Козлов', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 12, title: 'Задача 12', body: 'Описание задачи 12', assignee: 'Михайлов', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 13, title: 'Задача 13', body: 'Описание задачи 13', assignee: 'Иванов', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
    { id: 14, title: 'Задача 14', body: 'Описание задачи 14', assignee: 'Петров', status: 'todo_suka', menu: ['Действие 1', 'Действие 2'] },
  
    // Задачи со статусом 'inProgress'
    { id: 15, title: 'Задача 15', body: 'Описание задачи 15', assignee: 'Иванов', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 16, title: 'Задача 16', body: 'Описание задачи 16', assignee: 'Петров', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 17, title: 'Задача 17', body: 'Описание задачи 17', assignee: 'Сидоров', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 18, title: 'Задача 18', body: 'Описание задачи 18', assignee: 'Козлов', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 19, title: 'Задача 19', body: 'Описание задачи 19', assignee: 'Михайлов', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 20, title: 'Задача 20', body: 'Описание задачи 20', assignee: 'Иванов', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
    { id: 21, title: 'Задача 21', body: 'Описание задачи 21', assignee: 'Петров', status: 'inProgress', menu: ['Действие 1', 'Действие 2'] },
  
    // Задачи со статусом 'testing'
    { id: 22, title: 'Задача 22', body: 'Описание задачи 22', assignee: 'Иванов', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 23, title: 'Задача 23', body: 'Описание задачи 23', assignee: 'Петров', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 24, title: 'Задача 24', body: 'Описание задачи 24', assignee: 'Сидоров', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 25, title: 'Задача 25', body: 'Описание задачи 25', assignee: 'Козлов', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 26, title: 'Задача 26', body: 'Описание задачи 26', assignee: 'Михайлов', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 27, title: 'Задача 27', body: 'Описание задачи 27', assignee: 'Иванов', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
    { id: 28, title: 'Задача 28', body: 'Описание задачи 28', assignee: 'Петров', status: 'testing', menu: ['Действие 1', 'Действие 2'] },
  
    // Задачи со статусом 'done'
    { id: 29, title: 'Задача 29', body: 'Описание задачи 29', assignee: 'Иванов', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 30, title: 'Задача 30', body: 'Описание задачи 30', assignee: 'Петров', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 31, title: 'Задача 31', body: 'Описание задачи 31', assignee: 'Сидоров', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 32, title: 'Задача 32', body: 'Описание задачи 32', assignee: 'Козлов', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 33, title: 'Задача 33', body: 'Описание задачи 33', assignee: 'Михайлов', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 34, title: 'Задача 34', body: 'Описание задачи 34', assignee: 'Иванов', status: 'done', menu: ['Действие 1', 'Действие 2'] },
    { id: 35, title: 'Задача 35', body: 'Описание задачи 35', assignee: 'Петров', status: 'done', menu: ['Действие 1', 'Действие 2'] },
  ];
  
  export default tasks;