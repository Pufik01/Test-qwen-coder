#!/usr/bin/env python3
"""
Конфигурационный файл для голосового помощника
Здесь можно настроить макросы, слово активации и другие параметры
"""

import json

CONFIG = {
    # Слово для активации ассистента
    "wake_word": "привет работа",
    
    # Ответ на слово активации
    "greeting": "доброе утро сэр",
    
    # Макросы - команды которые выполняют несколько действий
    "macros": {
        # Макрос "работа" - запускает рабочие приложения
        "работа": {
            "response": "включаю режим работы",
            "actions": [
                {"type": "speak", "text": "запускаю рабочие приложения"},
                {"type": "open_app", "app": "notepad"},
                {"type": "music", "action": "play"}
            ]
        },
        
        # Макрос "отдых" - включает режим отдыха
        "отдых": {
            "response": "включаю режим отдыха",
            "actions": [
                {"type": "speak", "text": "приятного отдыха"},
                {"type": "music", "action": "pause"}
            ]
        },
        
        # Макрос "время" - говорит текущее время
        "время": {
            "response": "",
            "actions": [
                {"type": "speak", "text": "текущее время"},
                {"type": "time"}
            ]
        },
        
        # Макрос "дата" - говорит текущую дату
        "дата": {
            "response": "",
            "actions": [
                {"type": "date"}
            ]
        }
    },
    
    # Автозапуск при старте системы
    "autostart": True,
    
    # Настройки голоса
    "voice": {
        "rate": 150,      # Скорость речи (слова в минуту)
        "volume": 0.9     # Громкость (0.0 - 1.0)
    }
}


def save_config():
    """Сохранить конфигурацию в файл"""
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(CONFIG, f, ensure_ascii=False, indent=2)
    print("Конфигурация сохранена в config.json")


if __name__ == "__main__":
    save_config()
    print("\nДоступные типы действий для макросов:")
    print("  - speak: произнести текст")
    print("  - open_app: открыть приложение")
    print("  - music: управление музыкой (play/pause/stop/next)")
    print("  - time: сказать текущее время")
    print("  - date: сказать текущую дату")
    print("\nПример добавления своего макроса:")
    print('''
    "мой_макрос": {
        "response": "выполняю действие",
        "actions": [
            {"type": "speak", "text": "начинаю выполнение"},
            {"type": "open_app", "app": "browser"},
            {"type": "music", "action": "play"}
        ]
    }
    ''')
