# 🎉 PartyHub

# Link: 
https://partyhub-c2bhdpargvgyhkey.italynorth-01.azurewebsites.net

Описание

PartyHub е модерна уеб платформа, създадена да свързва хора, които обичат да организират и посещават партита. С платформата можете лесно да създавате събития, да преглеждате налични партита, да купувате билети и да оставяте коментари за вашите любими събития.

⚙️ Основни функционалности

Създаване на партита:

Организаторите могат да създават и управляват събития с информация за дата, час, място и други детайли.

Добавяне на VIP и стандартни опции за билети.

Управление на билети:

Потребителите могат да купуват, преглеждат и изтриват своите билети.

Специална страница за детайли на билетите, включително статус (VIP или стандартен).

Коментари и отзиви:

Участниците могат да оставят коментари за събитията.

Организаторите могат да получават обратна връзка.

Персонализиран профил:

Преглед и управление на регистрирани билети.
История на участието в партита.

🛠️ Технологии

Backend: Django (Python)

Frontend: Django Templates, CSS

База данни: PostgreSQL

## Environment Variables
To run the project locally, you need the following `.env` file:

[Open `.env` file here](https://pastebin.com/t9D2SLic)  

**Note**: Remember to delete this file after reviewing.


# 🚀 Инструкции за стартиране на проекта

## Опция 1: Локално (без Docker)

1. Клонирай репозитория:
```bash
git clone https://github.com/3iqpotato/PartyHub
```
```bash
cd PartyHub_Project
```

2. Създай виртуална среда:
```bash
python -m venv venv
```
```bash
source venv/bin/activate (Windows: venv\Scripts\activate)
```

3. Създай .env файл и добави необходимите променливи.


4. Инсталирай зависимостите:
```bash
pip install -r requirements.txt
```

5. Изпълни миграциите:
```bash
python manage.py migrate
```

6. Стартирай сървъра:
```bash
python manage.py runserver
 ```
7. **🌐 Достъп до сайта:**  
Отвори любимия си браузър и посети: [http://localhost:8000](http://localhost:8000) 🚀

## Опция 2: With Docker

1. **Клонирай репозитория:**
```bash
git clone https://github.com/3iqpotato/PartyHub
cd PartyHub_Project
```

2. **Стартирай контейнерите:**
```bash
docker-compose up --build
```

3. **Влез в Django контейнера, за да пуснеш миграции:**

```bash
docker-compose exec web python manage.py migrate
```

4. **🌐 Достъп до сайта:**  
Отвори любимия си браузър и посети: [http://localhost:8000](http://localhost:8000) 🚀


## 📄 Подробна документация

Виж всички действия, които потребителят може да извърши в системата:  
👉 [Потребителски функционалности](docs/user-features.md)