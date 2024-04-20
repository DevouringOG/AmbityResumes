<br />
<div align="center">

  <h3 align="center">Ambity RESUMES</h3>

  <p align="center">
    Веб-приложение для сбора, анализа и рейтинга резюме.
    <br />
    <a href=""><strong>Сайт</strong></a>
    <br />
  </p>
</div>

* bash
  ```bash
  pip install -r requirements/prod.txt
  pip install -r requirements/dev.txt
  ```
2) В директории ambityresumes применяем миграции и собираем статику
* bash
  ```bash
  cd companyopscontrol
  python3 manage.py migrate
  python3 manage.py collectstatic
  ```
3) В файле .env определяем следующие переменные:
* .env
  ```env
    SECRET_KEY=django-insecure-ea=mfq2mi&6lc1&mb@mvq=&_6=xf+-s19t3+=6s1(s&osq4@w3
    DEBUG=true
    ALLOWED_HOSTS=loaclhost,127.0.0.1
    DB_NAME=my_database
    DB_USER=postgres
    DB_PASSWORD=root
    DB_HOST=127.0.0.1
    DB_PORT=5432
  ```

## Контакты
<a name="contact"></a>

TG: **@Artem0G**
