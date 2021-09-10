# Публикуем комиксы в VK

Скрипт скачиваем рандомный комикс с XKCD и публикуем его в твоей группе в контакте.

### Как установить

Создайте группу в контакте. Затем тут создайте приложение в контакте, тип приложения standalone.
В приложении нажав кнопку редактировать увидите client_id(сохраните его).

Получите токен на Implicit Flow, следуйте инструкциям, права укажите следующие: photos, groups, wall и offline.

id группы в контакте можно узнать здесь.

Рядом с кодом создайте файл .env, туда положите
VK_TOKEN='ваш токен vk'
GROUP_ID='id группы в контакте'

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

pip install -r requirements.txt

### Как запустить

$ python publish_comic_vk.py

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
