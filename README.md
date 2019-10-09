CLI interface for Trello.com

<h1>Консольное приложение для работы с сервисом Trello</h1>
<h4>Для работы необходимо:</h4>

1.Сохранить репозиторий на своем компьютере.
2.В файле `trello_cli.py` в переменные `AUTHOR_PARAMS`, `BOARD_ID` внести данные своего аккаунта и доски. `BOARD_ID` – это короткий id из URL. Так называемый longId приложение узнает само.
3.В папке с файлом `trello_cli.py` запустить консоль.

<h4>Синтаксис команд:</h4>
<ol>
<li>Запуск приложения без аргументов, отображает все списки (колонки) и карточки доски. Цифры рядом с именами списков (колонок) отображают количество карточек (задач) в них.
 <br>
`python trello_cli.py`</li>
<li>Для создания карточки (задачи), используйте команду `create`, за которой следует имя списка (колонки) и имя карточки (задачи). Если используете имена с пробелами, заключайте их в кавычки.
<br>
`python trello_cli.py create my_list my_task`</li>
<li>Для перемещения карточек между списками используйте команду `move`. Далее идут имя карточки и имя списка, в который необходимо переместить карточку. Если используете имена с пробелами, заключайте их в кавычки.
<br>
`python trello_cli.py move my_task next_list`</li>
<li>Для создания списка, используйте команду `createlist`. Далее идет имя нового списка. Если используете имя с пробелами, заключайте его в кавычки.
<br>
`python trello_cli.py createlist list_name`</li>
<li>Подсказка вызывается командой `help`
<br>
`python trello_cli.py help`</li>
</ol>
