## Телеграм бот для управления подписками на каналы спонсоров

Этот бот предназначен для автоматизации процесса управления подписками пользователей на каналы спонсоров в Telegram. Он проверяет подписку пользователей и, в случае отсутствия подписки на необходимые каналы, отправляет предупреждение и предоставляет пользователю возможность подписаться на недостающие каналы. Если пользователь не подтверждает подписку в течение установленного срока, бот исключает его из целевого канала.

# Основные функции

1. Предоставление доступа в закрытый канал пользователям при выполнении условий

2. Регулярная проверка подписок: Бот периодически проверяет подписки пользователей на целевой канал спонсоров.

3. Предупреждение: В случае отсутствия подписки на какой-либо канал спонсора, бот отправляет предупреждение пользователю с ссылками на недостающие каналы.

4. Подтверждение подписки: Пользователь может подтвердить свою подписку, нажав на кнопку "Я ПОДПИСАЛСЯ" в сообщении от бота.

5. Исключение пользователей: Если пользователь не подтверждает подписку в установленный срок, бот исключает его из целевого канала спонсоров.

6. Ведение базы данных пользователей: Бот хранит информацию о пользователях в базе данных, чтобы управлять их подписками и исключениями.

# Как использовать

1. Внесите необходимые конфигурации в файлы в папке templates

2. Внесите токен бота в файл .env

3. Установите необходимые зависимости: отткройте командную строку или терминал в директории проекта и выполните следующую команду
    ```bash
    pip install -r requirements.txt
    ```
4. Запустите бота из директории проекта:
    ```bash
    python bot.py
    ```
   
# Зависимости 

aiogram==3.0.0

APScheduler==3.10.4

loguru==0.7.2

python-dotenv==1.0.0


