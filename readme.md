# Django + Stripe Payment Integration

## Описание
Тестовое задание — интеграция Django с платежной системой Stripe через их официальное Python SDK и Checkout API. Реализовано:
- управление товарами, заказами, скидками, налогами через admin panel;
- создание Stripe-сессии для оплаты товара;
- отображение HTML-страницы с кнопкой "Buy";
- редирект пользователя на Stripe Checkout для оплаты.

**Проект доступен по адресу:**
https://mtunikov.pythonanywhere.com/

Данные для тестирования админ панели:
- username: **admin**
- password: **admin**



## Установка и запуск
1. Клонировать репозиторий

```
git clone https://github.com/mishatunikov/payment_app.git
```

2. Установить зависимости

```
pip install -r requirements/requirements.txt
```

3. Настроить переменные окружения. 
Создайте .env в соответствие с примером .evn_example.

4. Выполнить миграции и создать суперпользователя

```
python manage.py migrate
```
```
python manage.py createsuperuser
```

5. Запустить сервер

```
python manage.py runserver
```

## API Endpoints
## 📡 API Endpoints
- `GET /api/v1/item/<int:pk>/`  
  Отображает HTML-страницу с информацией о товаре и кнопкой **Buy** для перехода к оплате через Stripe.

- `GET /api/v1/buy/<int:pk>/`  
  Создаёт Stripe Checkout-сессию для оплаты одного товара (**Item**) и возвращает `session.id`.

- `GET /api/v1/order/<int:pk>/`  
  Показывает HTML-страницу с информацией о заказе (**Order**) и кнопкой **Buy** для перехода к оплате через Stripe.

- `GET /api/v1/order/<int:pk>/payment/`  
  Создаёт Stripe Checkout-сессию для оплаты всех товаров в заказе (**Order**) с учётом скидок и налогов.
