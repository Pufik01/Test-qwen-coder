#!/usr/bin/env python3
"""
Voice Assistant - Голосовой помощник с поддержкой макросов
Автор: Senior Developer
Описание: Ассистент, который слушает голосовые команды и выполняет действия
"""

import speech_recognition as sr
import pyttsx3
import subprocess
import os
import json
import threading
from datetime import datetime
import psutil

# Пытаемся импортировать pynput, но не ломаем если не получится
try:
    from pynput import keyboard, mouse
    PYNPUT_AVAILABLE = True
except Exception:
    PYNPUT_AVAILABLE = False
    print("[INFO] pynput недоступен (нужен X server для GUI)")

# Конфигурация
CONFIG_FILE = "config.json"
WAKE_WORD = "привет работа"  # Слово для активации
GREETING_RESPONSE = "доброе утро сэр"

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.engine = pyttsx3.init()
        self.is_running = True
        self.is_listening = False
        self.config = self.load_config()
        
        # Попытка инициализировать микрофон
        try:
            self.microphone = sr.Microphone()
            print("[INFO] Микрофон успешно инициализирован")
        except Exception as e:
            print(f"[WARNING] Микрофон недоступен: {e}")
            print("[INFO] Работа без микрофона возможна только для тестирования")
        
        # Настройка голоса
        self.setup_voice()
        
        # Загрузка макросов
        self.macros = self.config.get("macros", {})
        
    def setup_voice(self):
        """Настройка параметров голоса"""
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                # Пытаемся найти русский голос или используем первый доступный
                ru_voice = None
                for voice in voices:
                    if 'ru' in str(voice).lower() or 'russian' in str(voice).lower():
                        ru_voice = voice.id
                        break
                
                if ru_voice:
                    self.engine.setProperty('voice', ru_voice)
                else:
                    self.engine.setProperty('voice', voices[0].id)
                    
            self.engine.setProperty('rate', 150)  # Скорость речи
            self.engine.setProperty('volume', 0.9)  # Громкость
            print("[INFO] Голосовой движок настроен")
        except Exception as e:
            print(f"[WARNING] Проблема с настройкой голоса: {e}")
            print("[INFO] Используем настройки по умолчанию")
        
    def load_config(self):
        """Загрузка конфигурации из файла"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.create_default_config()
    
    def create_default_config(self):
        """Создание конфигурации по умолчанию"""
        default_config = {
            "wake_word": WAKE_WORD,
            "greeting": GREETING_RESPONSE,
            "macros": {
                "работа": {
                    "response": "включаю режим работы",
                    "actions": [
                        {"type": "speak", "text": "запускаю рабочие приложения"},
                        {"type": "open_app", "app": "notepad"},
                        {"type": "music", "action": "play"}
                    ]
                },
                "отдых": {
                    "response": "включаю режим отдыха",
                    "actions": [
                        {"type": "speak", "text": "приятного отдыха"},
                        {"type": "music", "action": "pause"}
                    ]
                },
                "время": {
                    "response": "",
                    "actions": [
                        {"type": "speak", "text": "текущее время"},
                        {"type": "time"}
                    ]
                }
            },
            "autostart": True
        }
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
            
        return default_config
    
    def save_config(self):
        """Сохранение конфигурации"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def speak(self, text):
        """Произнесение текста"""
        print(f"[ASSISTANT]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Слушание микрофона"""
        if not self.microphone:
            print("[ERROR] Микрофон не доступен")
            return None
            
        try:
            with self.microphone as source:
                print("[LISTENING]: Слушаю...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            try:
                # Распознавание речи на русском языке
                text = self.recognizer.recognize_google(audio, language="ru-RU")
                print(f"[USER]: {text}")
                return text.lower()
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"[ERROR]: Проблема с сервисом распознавания: {e}")
                return None
                
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"[ERROR]: Ошибка при прослушивании: {e}")
            return None
    
    def execute_action(self, action):
        """Выполнение одного действия из макроса"""
        action_type = action.get("type")
        
        if action_type == "speak":
            self.speak(action.get("text", ""))
            
        elif action_type == "open_app":
            app = action.get("app", "")
            self.open_application(app)
            
        elif action_type == "music":
            music_action = action.get("action", "")
            self.control_music(music_action)
            
        elif action_type == "time":
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"сейчас {current_time}")
            
        elif action_type == "date":
            current_date = datetime.now().strftime("%d %m %Y")
            self.speak(f"сегодня {current_date}")
            
        elif action_type == "shutdown":
            self.speak("выключаю компьютер")
            # subprocess.run(["shutdown", "-h", "now"])  # Опасно, закомментировано
            
        elif action_type == "lock":
            self.speak("блокирую экран")
            # subprocess.run(["xdg-screensaver", "lock"])  # Для Linux
            
    def open_application(self, app_name):
        """Открытие приложения"""
        # Маппинг приложений для разных ОС
        app_mapping_linux = {
            "notepad": ["gedit"],
            "calculator": ["gnome-calculator"],
            "browser": ["google-chrome"],
            "firefox": ["firefox"],
            "terminal": ["gnome-terminal"],
            "code": ["code"],  # VS Code
            "spotify": ["spotify"],
            "files": ["nautilus"],
        }
        
        app_mapping_windows = {
            "notepad": ["notepad"],
            "calculator": ["calc"],
            "browser": ["start", "chrome"],
            "firefox": ["firefox"],
            "terminal": ["cmd"],
            "code": ["code"],
            "spotify": ["spotify"],
        }
        
        import platform
        system = platform.system().lower()
        
        if system == "linux":
            cmd = app_mapping_linux.get(app_name.lower(), [app_name])
        elif system == "windows":
            cmd = app_mapping_windows.get(app_name.lower(), [app_name])
        else:
            cmd = [app_name]
        
        try:
            subprocess.Popen(cmd, start_new_session=True)
            print(f"[ACTION]: Открыто приложение {app_name}")
        except Exception as e:
            print(f"[ERROR]: Не удалось открыть {app_name}: {e}")
            print(f"[INFO]: Приложение '{app_name}' не найдено в системе")
    
    def control_music(self, action):
        """Управление музыкой"""
        if action == "play":
            # Здесь можно интегрировать Spotify, VLC или другой плеер
            self.speak("включаю музыку")
            # Пример для VLC (нужно установить заранее)
            # subprocess.run(["vlc", "--intf", "rc", "playlist.m3u"])
        elif action == "pause":
            self.speak("пауза музыки")
        elif action == "stop":
            self.speak("останавливаю музыку")
        elif action == "next":
            self.speak("следующий трек")
    
    def process_command(self, command):
        """Обработка команды пользователя"""
        if not command:
            return
        
        # Проверка на слово активации
        if self.config["wake_word"] in command:
            self.speak(self.config["greeting"])
            # После приветствия слушаем следующую команду
            follow_up = self.listen()
            if follow_up:
                self.execute_macro(follow_up)
        else:
            # Попытка выполнить макрос напрямую
            self.execute_macro(command)
    
    def execute_macro(self, command):
        """Выполнение макроса по команде"""
        for macro_name, macro_data in self.macros.items():
            if macro_name in command:
                response = macro_data.get("response", "")
                if response:
                    self.speak(response)
                
                actions = macro_data.get("actions", [])
                for action in actions:
                    self.execute_action(action)
                return
        
        # Если макрос не найден, пробуем ответить как чат-бот
        self.default_response(command)
    
    def default_response(self, command):
        """Ответ по умолчанию на нераспознанные команды"""
        responses = {
            "как дела": "у меня всё отлично, спасибо что спросили",
            "кто ты": "я ваш персональный голосовой помощник",
            "что умеешь": "я могу открывать приложения, управлять музыкой, говорить время и выполнять макросы",
            "спасибо": "всегда пожалуйста сэр",
            "пока": "до свидания сэр",
        }
        
        for key, value in responses.items():
            if key in command:
                self.speak(value)
                return
        
        self.speak("извините, я не понял команду")
    
    def add_macro(self, name, response, actions):
        """Добавление нового макроса"""
        self.macros[name] = {
            "response": response,
            "actions": actions
        }
        self.config["macros"] = self.macros
        self.save_config()
        self.speak(f"макрос {name} добавлен")
    
    def run(self):
        """Основной цикл работы ассистента"""
        print("=" * 50)
        print("Голосовой помощник запущен!")
        print(f"Слово активации: {self.config['wake_word']}")
        print("=" * 50)
        
        self.speak("система запущена и готова к работе")
        
        while self.is_running:
            command = self.listen()
            if command:
                self.process_command(command)
    
    def stop(self):
        """Остановка ассистента"""
        self.is_running = False
        self.speak("выключаюсь")


def create_autostart_script():
    """Создание скрипта для автозапуска"""
    script_content = '''#!/bin/bash
# Автозапуск голосового помощника

cd "$(dirname "$0")"
python3 assistant.py &
'''
    
    with open("start_assistant.sh", 'w') as f:
        f.write(script_content)
    
    os.chmod("start_assistant.sh", 0o755)
    print("Скрипт автозапуска создан: start_assistant.sh")


def main():
    """Точка входа"""
    # Создание скрипта автозапуска
    create_autostart_script()
    
    # Запуск ассистента
    assistant = VoiceAssistant()
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\nОстановка по команде пользователя")
        assistant.stop()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        assistant.stop()


if __name__ == "__main__":
    main()
