
# Лабораторна робота 1: Проєктування REST API

**ПІБ:** Лайтарук І. Ф.
**Група:** КНІТ-63М
**Дата:** 19.11.2025

## 1. Аналіз предметної області

### Таблиця ресурсів

| Ресурс | Основні атрибути | Типи даних |
|--------|------------------|------------|
| User | id, username, level, region, email, createdAt | UUID, string, integer, string, string, datetime |
| Champion | id, name, role, difficulty, releaseDate | UUID, string, string, integer, datetime |
| Match | id, username, level, region, email, createdAt | UUID, string, integer, string, string, datetime |
| Map | id, name, description | UUID, string, string |
| InventoryItem | id, itemName, rarity, ownedAt | UUID, string, string, datetime |

### Обов'язкові та необов'язкові поля

###**Обов’язкові поля:**  
- **User**
  - username  
  - region  
  - email  
  - createdAt (генерується автоматично)  
  - id (генерується автоматично)
 
- **Champion**
  - name  
  - role  
  - difficulty  
  - releaseDate  
  - id (генерується автоматично)

- **Match**
  - mapId  
  - duration  
  - result  
  - createdAt (генерується автоматично)  
  - id (генерується автоматично)

- **Map** 
  - name  
  - id (генерується)

- **InventoryItem** 
  - itemName  
  - rarity  
  - ownedAt (генерується автоматично)  
  - id (генерується автоматично)

# 2. Проєктування API Endpoints

---

## Таблиця API Endpoints

| **HTTP метод** | **Шлях URI** | **Опис** | **Статус-коди** |
|----------------|--------------|----------|------------------|
| **GET** | `/api/users` | Отримати список користувачів | 200, 500 |
| **GET** | `/api/users/{id}` | Отримати дані конкретного користувача | 200, 404, 500 |
| **GET** | `/api/champions` | Отримати список чемпіонів | 200, 500 |
| **GET** | `/api/champions/{id}` | Отримати інформацію про одного чемпіона | 200, 404, 500 |
| **GET** | `/champions?available=true` | Отримати список чемпіонів, доступних користувачу | 200, 500 |
| **GET** | `/api/matches` | Отримати список матчів | 200, 500 |
| **POST** | `/api/matches` | Створити запис матчу | 201, 400, 500 |
| **GET** | `/matches/last` | Отримати останній зіграний матч | 200, 404, 500 |
| **GET** | `/api/items` | Отримати список предметів інвентарю | 200, 500 |

---

## Фільтрація задач

GET /api/matches?result=win 
GET /api/users?region=EUW
GET /api/items?rarity=legendary&itemName=Rabadon%27s%20Deathcap
GET /api/champions?role=top&difficulty=2

## Обґрунтування

- Використовуються іменники у множині (`/users`, `/champions`, `/matches`, `/tasks`), що відповідає ресурсно-орієнтованому підходу.
- Метод **GET** застосовується виключно для читання даних, є безпечним та ідемпотентним — повторні запити не змінюють стан системи.
- Метод **POST** використовується для створення нових ресурсів і повертає **201 Created**, оскільки був доданий новий запис.
- Використання **404 Not Found** обґрунтоване у випадках, коли запитуваний ресурс (матч, користувач, чемпіон або задача) не існує.
- Код **400 Bad Request** застосовується при помилках валідації чи некоректних даних, переданих у запиті.
- Фільтрація реалізована через **query parameters** (наприклад, `/api/matches?result=win`).
- Спеціальні ендпоінти, такий як `/api/matches/last`, оформлені як окремі ресурси, оскільки вони повертають специфічні підмножини даних із чітким змістовним значенням.

# 3. Структури даних

---

### Відповідь Champion (ResponseDTO)
```json
{
  "id": "c8f4d2b1-7a4f-4e2d-bc1a-8f3a6e2d9a12",
  "name": "Ahri",
  "role": "mid",
  "difficulty": 3,
  "releaseDate": "2011-12-14T00:00:00Z"
}
```
###CreateChampionDTO
```json
{
  "name": "Zeri",
  "role": "adc",
  "difficulty": 2,
  "releaseDate": "2021-09-29T00:00:00Z"
}
```

**Пояснення полів:**
- name — обов’язкове, назва чемпіона
- role — обов’язкове, позиція на карті (top, mid, adc, support, jungle)
- difficulty — обов’язкове, числовий рівень складності (1–5)
- releaseDate — обов’язкове, дата виходу чемпіона

###UpdateChampionDTO
```json
{
  "role": "top",
  "difficulty": 4
}
```

**Відмінності від CreateDTO:**
- Усі поля необов’язкові, бо можна оновлювати лише вибрані атрибути чемпіона.
- Підтримує часткове оновлення без необхідності відправляти всі дані.

**Список предметів:**
```json
{
  "page": 1,
  "limit": 5,
  "totalItems": 12,
  "totalPages": 3,
  "items": [
    {
      "id": "e7a9c3b4-2d6f-4e8b-a1f2-8d4c7e5b9123",
      "itemName": "Infinity Edge",
      "rarity": "legendary",
      "ownedAt": "2025-05-10T14:30:00Z"
    },
    {
      "id": "a1b2c3d4-5e6f-7g8h-9i0j-123456789abc",
      "itemName": "Rabadon's Deathcap",
      "rarity": "epic",
      "ownedAt": "2025-06-12T10:15:00Z"
    },
    {
      "id": "f1e2d3c4-b5a6-7890-1f2e-3d4c5b6a7e8f",
      "itemName": "Boots of Swiftness",
      "rarity": "rare",
      "ownedAt": "2025-07-01T18:20:00Z"
    },
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "itemName": "Sunfire Aegis",
      "rarity": "epic",
      "ownedAt": "2025-07-15T09:45:00Z"
    },
    {
      "id": "9f8e7d6c-5b4a-3c2d-1f0e-123456abcdef",
      "itemName": "Thornmail",
      "rarity": "rare",
      "ownedAt": "2025-08-02T12:10:00Z"
    }
  ]
}
```

## 4. Обробка помилок

---

### **Структура помилки**
```json
{
  "errorCode": "string",
  "message": "string",
  "details": "string (optional)",
  "timestamp": "ISO 8601 datetime"
}
```
**Пояснення полів:**

- errorCode — внутрішній код помилки для програмної обробки
- message — зрозуміле повідомлення для користувача або розробника
- details — додаткова інформація (необов’язково), наприклад, поле, яке викликало помилку
- timestamp — мітка часу виникнення помилки

**Коди помилок**:
| HTTP статус | Код помилки | Коли виникає | Приклад |
|-------------|-------------|--------------|---------|
| 400 | INVALID_CHAMPION_ROLE | Клієнт надіслав некоректну роль для чемпіона | Роль 'super-mid' недопустима. Доступні: top, mid, adc, support, jungle |
| 400 | INVALID_MATCH_DURATION | Тривалість матчу некоректна (<=0 або надто велика) | Тривалість матчу повинна бути більше 0 секунд |
| 401 | UNAUTHORIZED | Користувач не авторизований | Токен авторизації відсутній або недійсний |
| 404 | CHAMPION_NOT_FOUND | Чемпіон не знайдено | Чемпіон з id 'c8f4d2b1-7a4f-4e2d-bc1a-8f3a6e2d9999' не існує |
| 409 | DUPLICATE_USER_EMAIL | Користувач з таким email вже існує | Користувач з email 'summoner.king@example.com' вже існує |

**Приклад 1: Некоректна роль чемпіона (400)**

```json
{
  "errorCode": "INVALID_CHAMPION_ROLE",
  "message": "Роль 'super-mid' недопустима. Доступні: top, mid, adc, support, jungle",
  "details": "role: 'super-mid'",
  "timestamp": "2025-11-19T21:10:00Z"
}
```

**Приклад 2: Матч не знайдено (404)**

```json
{
  "errorCode": "MATCH_NOT_FOUND",
  "message": "Матч з id 'f3d9b7a6-4c2e-45d2-a9b1-2d7f8c9b9999' не знайдено",
  "timestamp": "2025-11-19T21:12:00Z"
}
```

Ця система дозволяє відрізняти помилки гри від загальних помилок REST API, наприклад:
- INVALID_CHAMPION_ROLE або INVALID_MATCH_DURATION → специфічні бізнес-правила гри.
- USER_NOT_FOUND, MATCH_NOT_FOUND, CHAMPION_NOT_FOUND → відсутність ресурсу.
- DUPLICATE_USER_EMAIL → конфлікт унікальних даних.
- INTERNAL_ERROR → загальна внутрішня помилка сервера.


