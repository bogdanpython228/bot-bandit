## ⚙️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/bogdanpython228/bot-bandit.git
cd bot-bandit
```

### 2. Создание БД
#### Создайте в папке app папку storage

### 3. Настройка окружения
#### Создайте в папке app папку core, а в папке core создайте файл config.py:
```ini
TOKEN='ваш_токен_бота'
ADMIN=ваш_телеграм_id
DATABASE_URL='sqlite+aiosqlite:///app/storage/db.sqlite3'
```

### 4. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 5. Запуск бота
```bash
python -m main.py
```
