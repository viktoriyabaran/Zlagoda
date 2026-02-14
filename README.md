# Zlagoda — Інструкція з налаштування

Ця інструкція допоможе налаштувати проєкт на **Windows** за допомогою WSL (підсистема Windows для Linux) та Docker.

---

## Крок 1: Встановлення WSL

WSL дозволяє запускати Linux всередині Windows. Це потрібно, бо Docker краще працює з Linux.

1. Відкрий **PowerShell від імені адміністратора**:
   - Натисни `Win + X` і вибери "Windows PowerShell (Адміністратор)" або "Термінал (Адміністратор)"

2. Виконай цю команду:
   ```powershell
   wsl --install
   ```

3. **Перезавантаж комп'ютер**, коли система попросить.

4. Після перезавантаження автоматично відкриється вікно Ubuntu. Тебе попросять створити ім'я користувача та пароль. Вибери щось просте, що запам'ятаєш (це тільки для локального Linux, не пов'язано з проєктом).

5. Щоб перевірити, чи все працює, відкрий PowerShell і виконай:
   ```powershell
   wsl --version
   ```
   Ти маєш побачити номери версій, а не помилку.

---

## Крок 2: Встановлення Docker Desktop

Docker дозволяє запускати базу даних (PostgreSQL) у контейнері, тож не потрібно встановлювати її вручну.

1. Завантаж Docker Desktop за посиланням: https://www.docker.com/products/docker-desktop/

2. Запусти інсталятор. Під час встановлення:
   - ✅ Переконайся, що опція "Use WSL 2 instead of Hyper-V" увімкнена

3. Після встановлення **перезавантаж комп'ютер**.

4. Відкрий Docker Desktop. Запуск може зайняти хвилину. Коли він буде готовий, ти побачиш іконку кита в системному треї.

5. Щоб перевірити, чи все працює, відкрий PowerShell і виконай:
   ```powershell
   docker --version
   ```
   Ти маєш побачити щось на кшталт `Docker version 24.x.x`

---

## Крок 3: Встановлення VS Code (якщо ще немає)

1. Завантаж за посиланням: https://code.visualstudio.com/

2. Під час встановлення:
   - ✅ Постав галочку "Add to PATH"
   - ✅ Постав галочку "Register Code as an editor for supported file types"

3. Після встановлення відкрий VS Code і встанови розширення **WSL**:
   - Натисни `Ctrl + Shift + X`, щоб відкрити розширення
   - Знайди "WSL" і встанови те, що від Microsoft

---

## Крок 4: Клонування проєкту

Тепер завантажимо код проєкту.

1. Відкрий **Ubuntu** (знайди в меню Пуск)

2. Перейди туди, де хочеш зберігати проєкт. Наприклад, щоб покласти його в папку "Документи" Windows:
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents
   ```
   (Заміни `ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS` на своє справжнє ім'я користувача Windows)

3. Клонуй проєкт:
   ```bash
   git clone <посилання-на-репозиторій>
   cd Zlagoda
   ```

4. Відкрий проєкт у VS Code:
   ```bash
   code .
   ```
   Це відкриє VS Code, підключений до WSL. Ти маєш побачити "WSL: Ubuntu" в лівому нижньому куті.

---

## Крок 5: Встановлення Python і створення віртуального середовища

Віртуальне середовище зберігає пакети проєкту окремо від інших Python-проєктів.

1. У терміналі Ubuntu (або терміналі VS Code) переконайся, що ти в папці проєкту:
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   ```

2. Встанови Python і pip, якщо ще не встановлені:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

3. Створи віртуальне середовище:
   ```bash
   python3 -m venv venv
   ```

4. Активуй віртуальне середовище:
   ```bash
   source venv/bin/activate
   ```
   Ти маєш побачити `(venv)` на початку рядка в терміналі. Це означає, що віртуальне середовище активне.

   > ⚠️ **Важливо:** Кожного разу, коли відкриваєш новий термінал для роботи над проєктом, потрібно знову виконати `source venv/bin/activate`.

5. Встанови залежності проєкту:
   ```bash
   pip install -r requirements.txt
   ```

---

## Крок 6: Налаштування бази даних

1. Переконайся, що Docker Desktop запущений (перевір іконку кита в системному треї).

2. Запусти контейнер бази даних:
   ```bash
   docker-compose up db
   ```

   Перший раз він завантажить образ PostgreSQL (близько 400 МБ). Зачекай, поки побачиш:
   ```
   database system is ready to accept connections
   ```

3. **Залиш цей термінал працювати.** Відкрий новий термінал для наступних кроків.

---

## Крок 7: Запуск міграцій бази даних

Міграції створюють таблиці в базі даних на основі наших моделей.

1. Відкрий новий термінал і перейди до проєкту:
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   source venv/bin/activate
   ```

2. Запусти міграції:
   ```bash
   python manage.py migrate
   ```

   Ти маєш побачити вивід на кшталт:
   ```
   Applying contenttypes.0001_initial... OK
   Applying auth.0001_initial... OK
   ...
   ```

---

## Крок 8: Встановлення Tailwind CSS

Tailwind CSS відповідає за стилі (зовнішній вигляд) застосунку. Його потрібно встановити один раз після клонування проєкту.

1. У тому ж терміналі (з активованим venv) виконай:
   ```bash
   python manage.py tailwind install
   ```

   Це завантажить бінарний файл Tailwind (Node.js не потрібен).

---

## Крок 9: Запуск сервера розробки

Для розробки потрібно запустити **два процеси** — сервер Django і компілятор Tailwind.

1. У тому ж терміналі (з активованим venv) запусти Tailwind у режимі спостереження:
   ```bash
   python manage.py tailwind start
   ```
   Це автоматично перекомпілює CSS кожного разу, коли ти змінюєш шаблони. **Залиш цей термінал працювати.**

2. **Відкрий ще один термінал** і виконай:
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   source venv/bin/activate
   python manage.py runserver
   ```

3. Відкрий браузер і перейди за адресою: http://localhost:8000

   Ти маєш побачити запущений застосунок!

---

## Щоденний робочий процес

Кожного разу, коли хочеш працювати над проєктом:

1. **Відкрий Docker Desktop** (або переконайся, що він уже запущений)

2. **Термінал 1 — база даних:**
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   source venv/bin/activate
   docker-compose up db
   ```

3. **Термінал 2 — Tailwind CSS:**
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   source venv/bin/activate
   python manage.py tailwind start
   ```

4. **Термінал 3 — Django-сервер:**
   ```bash
   cd /mnt/c/Users/ТВОЄ_ІМYA_КОРИСТУВАЧА_WINDOWS/Documents/Zlagoda
   source venv/bin/activate
   python manage.py runserver
   ```

5. Відкрий http://localhost:8000 у браузері.

---

## Корисні команди

| Команда | Що робить |
|---------|-----------|
| `source venv/bin/activate` | Активує віртуальне середовище |
| `deactivate` | Деактивує віртуальне середовище |
| `docker-compose up db` | Запускає базу даних |
| `docker-compose down` | Зупиняє всі контейнери |
| `python manage.py runserver` | Запускає сервер розробки Django |
| `python manage.py tailwind start` | Запускає Tailwind у режимі спостереження (перекомпілює CSS при змінах) |
| `python manage.py tailwind build` | Одноразова компіляція CSS (для продакшену) |
| `python manage.py tailwind install` | Встановлює Tailwind (потрібно лише один раз) |
| `python manage.py migrate` | Застосовує міграції бази даних |
| `python manage.py makemigrations` | Створює нові міграції після зміни моделей |

---

## Вирішення проблем

### "docker: command not found"
- Переконайся, що Docker Desktop запущений
- Спробуй перезапустити термінал

### "could not translate host name 'db' to address"
- Перевір, що у файлі `.env` вказано `POSTGRES_HOST=localhost` (а не `db`)
- Переконайся, що контейнер бази даних запущений (`docker-compose up db`)

### "No module named 'django'"
- Переконайся, що віртуальне середовище активоване (ти маєш бачити `(venv)` в терміналі)
- Виконай `pip install -r requirements.txt`

### VS Code не розпізнає пакети Python
- Переконайся, що ти відкрив VS Code з WSL (команда `code .` в терміналі Ubuntu)
- Вибери правильний інтерпретатор Python: натисни `Ctrl + Shift + P`, введи "Python: Select Interpreter" і вибери той, що з `./venv/bin/python`

---

## Розширення VS Code

Коли відкриєш проєкт, VS Code запропонує встановити рекомендовані розширення. Натисни "Install All", щоб отримати:
- Підтримку Python
- Підтримку шаблонів Django
- Автодоповнення Tailwind CSS
- Інструменти SQL
- Та інше...
