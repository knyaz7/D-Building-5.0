<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Авторизация</title>
    <style>
        .error {
            color: red;
            display: none;
        }
    </style>
</head>
<body>

<h2>Форма авторизации</h2>
<form id="loginForm">
    <label for="username">Логин:</label>
    <input type="text" id="username" name="username" required>
    <br><br>
    
    <label for="password">Пароль:</label>
    <input type="password" id="password" name="password" required>
    <br><br>

    <button type="submit">Войти</button>
</form>

<div class="error" id="errorMessage">Некорректно введенные данные. Пожалуйста, проверьте логин и пароль.</div>

<script src="script.js"></script>
</body>
</html>