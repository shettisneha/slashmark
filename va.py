import speech_recognition as sr
import pyttsx3
import openai
import wikipedia
import webbrowser
import requests
import datetime

# Initialize speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


openai.api_key = "your_openai_api_key"

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listens for a voice command and returns it as text"""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""

def chat_with_gpt(prompt):
    """Get AI-generated response from OpenAI GPT"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def search_wikipedia(query):
    """Search Wikipedia and return a summary"""
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Try being more specific. Some options: {e.options[:3]}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on Wikipedia."

def get_weather(city):
    """Get weather updates using OpenWeather API"""
    api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather data."

if __name__ == "__main__":
    speak("How can I assist you?")
    while True:
        command = take_command()

        if command:
            if "hello" in command:
                speak("Hello! How can I help you today?")
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            elif "time" in command:
                now = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The time is {now}")
            elif "open google" in command:
                webbrowser.open("https://www.google.com")
                speak("Opening Google")
            elif "search wikipedia for" in command:
                topic = command.replace("search wikipedia for", "").strip()
                result = search_wikipedia(topic)
                speak(result)
            elif "what's the weather in" in command:
                city = command.replace("what's the weather in", "").strip()
                weather_info = get_weather(city)
                speak(weather_info)
            else:
                response = chat_with_gpt(command)
                speak(response)
