# Инструкция по установке и запуску

## Быстрый старт

### 1. Установка зависимостей

#### Для Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio espeak espeak-data libespeak-dev
pip install SpeechRecognition pyttsx3==2.90 pyaudio pynput psutil
```

#### Для Windows:
```bash
pip install SpeechRecognition pyttsx3==2.90 pynput psutil
# PyAudio установится автоматически
```

#### Для macOS:
```bash
brew install portaudio
pip install SpeechRecognition pyttsx3==2.90 pyaudio pynput psutil
```

### 2. Запуск ассистента

```bash
cd voice_assistant
python assistant.py
```

### 3. Использование

1. Скажите **"Привет работа"** для активации
2. Ассистент ответит **"Доброе утро сэр"**
3. Скажите команду, например:
   - **"работа"** - запустит рабочие приложения
   - **"время"** - скажет текущее время
   - **"отдых"** - включит режим отдыха

## Настройка автозапуска

### Linux (systemd):

1. Создайте файл сервиса:
```bash
sudo nano /etc/systemd/system/voice-assistant.service
```

2. Добавьте содержимое:
```ini
[Unit]
Description=Voice Assistant
After=sound.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/путь/к/voice_assistant
ExecStart=/usr/bin/python3 /путь/к/voice_assistant/assistant.py
Restart=always

[Install]
WantedBy=default.target
```

3. Включите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable voice-assistant.service
sudo systemctl start voice-assistant.service
```

### Windows:

1. Создайте ярлык для `assistant.py`
2. Нажмите `Win + R`, введите `shell:startup`
3. Переместите ярлык в открывшуюся папку

### macOS:

1. Откройте "Системные настройки" → "Пользователи" → "Объекты входа"
2. Добавьте `assistant.py` или скрипт запуска

## Требования к оборудованию

- **Микрофон** - обязателен для голосового управления
- **Динамики/наушники** - для голосовых ответов
- **Подключение к интернету** - для распознавания речи (Google Speech API)

## Проверка работы микрофона

```bash
# Проверка доступных устройств записи
arecord -l  # Linux
# или
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

## Решение проблем

### Микрофон не работает:
- Проверьте права доступа в настройках системы
- Убедитесь, что микрофон выбран устройством по умолчанию

### Распознавание не работает:
- Проверьте подключение к интернету
- Попробуйте говорить четче и громче

### Голос не звучит:
- Проверьте настройки громкости
- Убедитесь, что espeak установлен правильно

## Добавление своих макросов

Отредактируйте `config.json`:

```json
"мой_макрос": {
  "response": "выполняю действие",
  "actions": [
    {"type": "speak", "text": "начинаю выполнение"},
    {"type": "open_app", "app": "browser"},
    {"type": "music", "action": "play"}
  ]
}
```

## Поддерживаемые команды

По умолчанию доступны:
- **"привет работа"** - активация ассистента
- **"работа"** - режим работы
- **"отдых"** - режим отдыха
- **"время"** - текущее время
- **"дата"** - текущая дата
- **"как дела"**, **"кто ты"**, **"что умеешь"** - базовые ответы

---
Создано с ❤️ вашим Senior Developer
