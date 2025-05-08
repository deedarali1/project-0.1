import os
import time
import openai
import wikipedia
import speech_recognition as sr
import pyttsx3
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout

# 🔑 OpenAI Setup
openai.api_key = "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"

# 🔊 Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')

def speak(text):
    print(f"Zezo 🗣️: {text}")
    engine.say(text)
    engine.runAndWait()

# 🎙 Speech Recognition
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=5)
        try:
            command = r.recognize_google(audio, language="en-IN")
            print(f"You said: {command}")
            return command.lower()
        except:
            speak("Sorry, I didn't catch that.")
            return ""

# 💬 ChatGPT
def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except:
        return "ChatGPT is not available right now."

# 📚 Wikipedia
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "Nothing found on Wikipedia."

# 📱 Mobile App Open (for Android with Termux/pyjnius only)
def open_app(app_name):
    apps = {
        "chrome": "com.android.chrome",
        "whatsapp": "com.whatsapp",
        "settings": "com.android.settings"
    }
    if app_name in apps:
        os.system(f"am start -n {apps[app_name]}")
        speak(f"Opening {app_name}")
    else:
        speak("App not recognized.")

# 🔄 Command Handling
def handle_command(cmd):
    if not cmd:
        speak("Say that again, please.")
        return "Say that again, please."
    if "wikipedia" in cmd:
        topic = cmd.replace("wikipedia", "").strip()
        return search_wikipedia(topic)
    elif "time" in cmd:
        return time.strftime("It is %I:%M %p")
    elif "date" in cmd:
        return time.strftime("Today is %A, %d %B %Y")
    elif "open" in cmd:
        if "chrome" in cmd:
            open_app("chrome")
        elif "whatsapp" in cmd:
            open_app("whatsapp")
        elif "settings" in cmd:
            open_app("settings")
        else:
            return "Which app should I open?"
        return "Done"
    else:
        return ask_chatgpt(cmd)

# 🚀 GUI App
class ZezoApp(MDApp):
    def build(self):
        self.screen = BoxLayout(orientation="vertical")
        self.scroll_view = ScrollView()
        self.chat_area = BoxLayout(orientation="vertical", size_hint_y=None)
        self.chat_area.bind(minimum_height=self.chat_area.setter('height'))
        self.scroll_view.add_widget(self.chat_area)

        self.text_input = MDTextField(hint_text="Say something...", size_hint_y=None, height=50)
        self.text_input.bind(on_text_validate=self.on_enter)
        self.send_button = MDRaisedButton(text="Send", size_hint_y=None, height=50, on_release=self.on_send)
        self.voice_button = MDRaisedButton(text="Speak", size_hint_y=None, height=50, on_release=self.listen_voice)

        self.screen.add_widget(self.scroll_view)
        self.screen.add_widget(self.text_input)
        self.screen.add_widget(self.send_button)
        self.screen.add_widget(self.voice_button)
        return self.screen

    def on_enter(self, instance):
        command = self.text_input.text.strip()
        if command:
            self.text_input.text = ""
            self.add_message(command, "You")
            response = handle_command(command)
            self.add_message(response, "Zezo")
            speak(response)

    def on_send(self, instance):
        self.on_enter(instance)

    def listen_voice(self, instance):
        command = listen_command()
        if command:
            self.add_message(command, "You")
            response = handle_command(command)
            self.add_message(response, "Zezo")
            speak(response)

    def add_message(self, message, sender):
        label = MDLabel(text=f"{sender}: {message}", size_hint_y=None, height=40)
        self.chat_area.add_widget(label)
        self.scroll_view.scroll_to(label)

if __name__ == "__main__":
    ZezoApp().run()
