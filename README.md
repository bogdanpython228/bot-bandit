## ⚙️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/bogdanpython228/bot-bandit.git
cd bot-bandit
```

### 2. Настройка окружения
#### Создайте в папке app папку core, а в папке core создайте файл config.py:
```ini
TOKEN='ваш_токен_бота'
ADMIN=ваш_телеграм_id
DATABASE_URL='sqlite+aiosqlite:///app/storage/db.sqlite3'
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск бота
```bash
python -m main.py
```
