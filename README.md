# SiteInsurance
Сайт-посредник для оформления ОСАГО на Альфастрахование, 21 Век, ВСК, Югория и др. страховых компаниях. 
![image](https://user-images.githubusercontent.com/70958549/173882645-1a2fe5a0-93eb-41fd-af42-661c92c30a36.png)
![enter image description here](https://user-images.githubusercontent.com/70958549/173885485-b97361fd-2eed-4323-9bfd-0a9ab689cf59.png)
## Стек
 - Python 3.9
 - Flask
 - SqlAlchemy
 - Pydantic
 - Jinja2
 - VueJs
 - flask_socketio
 - flask_login

## Quick Start

    git clone https://github.com/XronoZ-create/SiteInsurance.git

    py -3.9 run.py
    
## Структура проекта
```
├── README.md
├── config.py
├── run.py
├── app
	├── admin
		├── __init__.py
		├── views.py
		├── generate_email_address.py
	├── alfa
		├── __init__.py
		├── marks.py
		├── veiws.py
	├── api
		├── __init__.py
		├── views.py
	├── arm
		├── __init__.py
		├── marks.py
		├── veiws.py
	├── auth
		├── __init__.py
		├── veiws.py
	├── databases
		├── json
			├── pydantic_models.py
		├── db_bot_methods.py
		├── database_insurance.py
		├── database_email.py
		├── models_insurance.py
		├── models_email.py
	├── error
		├── __init__.py
		├── veiws.py
	├── hooker
		├── __init__.py
		├── veiws.py
	├── main
		├── __init__.py
		├── veiws.py
	├── osk
		├── __init__.py
		├── veiws.py
		├── mark.py
	├── request_insurance
		├── __init__.py
		├── veiws.py
	├── static
		...
	├── statistic
		├── __init__.py
		├── veiws.py
	├── templates
		...
	├── ugsk
		├── __init__.py
		├── veiws.py
	├── vek21
		├── __init__.py
		├── veiws.py
	├── vsk
		├── __init__.py
		├── veiws.py
	├── __init__.py
	├── strah_comps.py
```
## TO DO

 - [x] Авторизация по логину/паролю
 - [x] Вэб-сокеты
 - [x] Звуковые оповещения
 - [x] Роли пользователей
 - [x] Диаграмма регистрации заявок
 - [x] API для микро-ботов 
 - [x] Клонирование заявок. Массовый запуск. Перенос заявки на другую страховую
