
# Лабораторна робота 1: Проєктування REST API

**ПІБ:** [Лайтарук І. Ф.]
**Група:** [КНІТ-63М]
**Дата:** [19.11.2025]

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

[Ваш опис]
