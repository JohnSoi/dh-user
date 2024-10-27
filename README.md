# Подсистема пользователей DH

---

## Описание 

Базовые механизмы работы с пользователями в приложениях экосистемы DH

---

## Состав

* ```exceptions``` - исключения
* ```helpers``` - вспомогательные функции
  * ```get_current_user``` - получение записи текущего пользователя
* ```models``` - модели
* ```repository``` - репозитории для работы с данными
* ```routes``` - конечные точки
* ```schemas``` - схемы данных
* ```services``` - сервисы
---

## Подключение

Для подключения используется команда:
```bash
poetry add git+https://github.com/JohnSoi/dh-user.git
```

В файл ```migrations/env.py``` нужно добавить импорт моделей:
```python
from dh_user.model import *
```

В файле ```.env``` должны быть следующие поля:

```dotenv
SECRET_KEY=
CRYPTO_CONTEXT_SCHEME=
ENCODE_ALGORITHM=
TOKEN_EXPIRE_DAY=
TOKEN_COOKIE_NAME=
CELERY_AUTH_NAME=
```