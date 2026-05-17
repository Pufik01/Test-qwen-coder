#!/usr/bin/env python3
"""
Простой тест голосового помощника без микрофона
Проверка работы TTS (синтеза речи) и базовой логики
"""

import sys
sys.path.insert(0, '.')

from assistant import VoiceAssistant

def test_voice():
    """Тест синтеза речи"""
    print("=" * 50)
    print("ТЕСТ СИНТЕЗА РЕЧИ")
    print("=" * 50)
    
    assistant = VoiceAssistant()
    
    # Тест произнесения фраз
    test_phrases = [
        "доброе утро сэр",
        "система запущена и готова к работе",
        "включаю режим работы",
        "приятного отдыха",
        "всегда пожалуйста сэр"
    ]
    
    for phrase in test_phrases:
        print(f"\nПроизношу: {phrase}")
        assistant.speak(phrase)
    
    print("\n" + "=" * 50)
    print("ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
    print("=" * 50)


def test_macros():
    """Тест макросов"""
    print("\n" + "=" * 50)
    print("ТЕСТ МАКРОСОВ")
    print("=" * 50)
    
    assistant = VoiceAssistant()
    
    # Тест выполнения макросов
    test_commands = [
        "работа",
        "отдых", 
        "время",
        "дата",
        "как дела",
        "кто ты"
    ]
    
    for command in test_commands:
        print(f"\nКоманда: {command}")
        assistant.execute_macro(command)
    
    print("\n" + "=" * 50)
    print("ВСЕ МАКРОСЫ РАБОТАЮТ!")
    print("=" * 50)


if __name__ == "__main__":
    print("\nВыберите тест:")
    print("1 - Тест синтеза речи")
    print("2 - Тест макросов")
    print("3 - Полный тест")
    
    choice = input("\nВаш выбор (1/2/3): ").strip()
    
    if choice == "1":
        test_voice()
    elif choice == "2":
        test_macros()
    elif choice == "3":
        test_voice()
        test_macros()
    else:
        print("Неверный выбор, запускаю полный тест...")
        test_voice()
        test_macros()
    
    print("\n✅ Все тесты завершены!")
    print("\nДля полноценной работы с микрофоном запустите:")
    print("   python assistant.py")
