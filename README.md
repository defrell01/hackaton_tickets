# SF-hack

Для работы с нашим микросервисом по сбору информации о стоимости авиабилетов из открытых источников был разработан пользовательский интерфейс. 
![telegram-cloud-photo-size-2-5472077038966920140-y](https://github.com/klshv/SF-hack/assets/75554915/beef5002-72f2-4e5b-a90b-c3681820fbfd)

Фронтенд проекта позволяет пользователям авторизоваться, заполнить информацию о городе отправления, городе прибытия, дате вылета, дате прилета, классе, количестве пассажиров и нажать кнопку "Найти билеты". После отправки формы, данные пользователя отправляются на сервер, который возвращает список рейсов с прогнозируемой ценой. Рейсы отображаются на странице в виде таблицы.

![telegram-cloud-photo-size-2-5472077038966920194-y](https://github.com/klshv/SF-hack/assets/75554915/7b6f4082-c9cb-40f2-aacc-9206ce1f8ef7)

***Авторизация планируется использоваться для хранения персональных данных и возможной будущей интеграции с сервисами для покупки билетов.***


## Запуск фронт-енда

Для запуска необходимо клонировать репозиторий и выполнить следующие команды в терминале:

```bash
pip install streamlit
pip install pandas

streamlit run front.py
```

## Запуск бэк-енда

```bash
pip install fastapi
pip install pydantin
pip install sqlit3
pip install uvicorn
pip install scikit-learn
pip install python-dotenv
pip install pickle
pip install joblib
pip install pandas

python.exe ./app.py
```
Так же необходимо предоставить .env файл с ключем для API "FlightAPI"

