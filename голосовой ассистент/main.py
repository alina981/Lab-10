import pyttsx3
import pyaudio
import vosk
import time
import json
import requests


class Speech:
    def __init__(self):
        self.speaker = 0
        self.tts = pyttsx3.init('sapi5')

    def set_voice(self, speaker):
        self.voices = self.tts.getProperty('voices')
        for count, voice in enumerate(self.voices):
            if count == 0:
                print('0')
                id = voice.id
            if speaker == count:
                id = voice.id
        return id

    def text2voice(self, speaker=0, text='Готов'):
        self.tts.setProperty('voice', self.set_voice(speaker))
        self.tts.say(text)
        self.tts.runAndWait()


class Recognize:
    def __init__(self):
        model = vosk.Model('vosk-model-small-ru-0.22')
        self.record = vosk.KaldiRecognizer(model, 16000)
        self.stream()

    def stream(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']


def speak(text):
    speech = Speech()
    speech.text2voice(speaker=0, text=text)


def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    response = requests.get(url)
    data = response.json()
    return data


def save_joke_to_file(joke_text):
    with open("jokes.txt", "a", encoding="utf-8") as file:
        file.write(joke_text + "\n")


if __name__ == '__main__':
    rec = Recognize()
    text_gen = rec.listen()
    rec.stream.stop_stream()
    speak('Вас приветствует ассистент для работы с шутками!')
    time.sleep(0.2)
    speak('Скажите одну из команд: "создать", "тип", "прочесть", "категория", "записать"')
    rec.stream.start_stream()

    current_joke = None

    for text in text_gen:
        time.sleep(0.5)
        if text:
            if text == 'создать':
                current_joke = get_joke()
                if current_joke["type"] == "single":
                    joke_text = current_joke["joke"]
                else:
                    joke_text = f"{current_joke['setup']} {current_joke['delivery']}"
                speak('Шутка создана. Хотите её прочесть?')
                print(f'Создана шутка: {joke_text}')

            elif text == 'тип' and current_joke:
                joke_type = "однострочная" if current_joke["type"] == "single" else "диалог"
                speak(f'Тип шутки: {joke_type}')
                print(f'Тип шутки: {joke_type}')

            elif text == 'прочесть' and current_joke:
                if current_joke["type"] == "single":
                    joke_text = current_joke["joke"]
                else:
                    joke_text = f"{current_joke['setup']} {current_joke['delivery']}"
                speak(joke_text)
                print(f'Шутка: {joke_text}')

            elif text == 'категория' and current_joke:
                category = current_joke["category"]
                speak(f'Категория шутки: {category}')
                print(f'Категория шутки: {category}')

            elif text == 'записать' and current_joke:
                if current_joke["type"] == "single":
                    joke_text = current_joke["joke"]
                else:
                    joke_text = f"{current_joke['setup']} {current_joke['delivery']}"
                save_joke_to_file(joke_text)
                speak('Шутка записана в файл.')
                print(f'Шутка записана в файл: {joke_text}')

            elif text == 'выход':
                speak('До свидания!')
                quit()

            else:
                if not current_joke and text in ['тип', 'прочесть', 'категория', 'записать']:
                    speak('Сначала создайте шутку командой "создать"')
                else:
                    speak('Команда не распознана. Попробуйте ещё раз.')