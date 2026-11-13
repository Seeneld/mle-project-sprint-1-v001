# Проект 1 спринта

Добро пожаловать в репозиторий-шаблон Практикума для проекта 1 спринта. Цель проекта — создать базовое решение для предсказания стоимости квартир Яндекс Недвижимости.

Полное описание проекта хранится в уроке «Проект. Разработка пайплайнов подготовки данных и обучения модели» на учебной платформе.

Здесь укажите имя вашего бакета: mle-20261110-a098f81ea7fe

## Этап 1: Сбор данных
- DAG: part1_airflow/dags/collect_data.py
- Функции DAG:
  - create_table - создание таблицы merged_flats
  - extract - извлечение данных из таблиц flats и buildings
  - transform - объединение таблиц через JOIN
  - load - загрузка результата в БД
  - notify_success - уведомление в Telegram об успехе
  - notify_failure - уведомление в Telegram об ошибке
- Результат: таблица merged_flats

## Этап 2: Очистка данных
- DAG: part1_airflow/dags/clean_data.py
- Функции очистки (part1_airflow/plugins/cleaning_functions.py):
  - remove_duplicates() - удаление дубликатов
  - handle_missing_values() - обработка пропусков
  - remove_outliers() - удаление выбросов
  - clean_data() - агрегирующая функция
- Jupyter Notebook: part1_airflow/notebooks/notebook.ipynb
- Результат: таблица cleaned_flats

## Этап 3: Создание DVC-пайплайна обучения модели
- Скрипты:
  - part2_dvc/scripts/get_data.py - загрузка данных из БД
  - part2_dvc/scripts/preprocess.py - предобработка и разделение на train/test
  - part2_dvc/scripts/fit.py - обучение модели RandomForestRegressor
  - part2_dvc/scripts/evaluate.py - оценка модели
- Конфигурация DVC-пайплайна:
  - part2_dvc/params.yaml - гиперпараметры модели
  - part2_dvc/dvc.yaml - описание пайплайна
  - part2_dvc/dvc.lock - зафиксированные версии артефактов

## Облачное хранилище
- S3 Bucket: mle-20261110-a098f81ea7fe
- Хранящиеся файлы:
  - Обученная модель (models/model.pkl)
  - Препроцессор (models/preprocessor.pkl)
  - Данные (data/)
  - Метрики (cv_results/metrics.json)

## Метрики модели
Метрики (MAE, RMSE, R2) в part2_dvc/cv_results/metrics.json

## Запуск проекта
- python3 -m venv venv
- source venv/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt

### part1_airflow
- cd part1_airflow
- docker compose up --build -d

Откройте http://localhost:8080 (логин/пароль: airflow/airflow) и запустите DAGи:
1. collect_real_estate_data
2. clean_real_estate_data

### part2_dvc
- source venv/bin/activate
- cd part2_dvc
- dvc repro
- dvc push