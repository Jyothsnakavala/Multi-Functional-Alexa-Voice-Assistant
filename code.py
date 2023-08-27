import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyowm
owm = pyowm.OWM('api key')

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()

def get_city_and_country():
    talk("Sure, please tell me the name of the city.")
    city = take_command().capitalize()
    talk("Great! Now, could you tell me the two-letter country code for that city?")
    country_code = take_command().upper()
    return city, country_code
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        city, country_code = get_city_and_country()
        try:
            observation = owm.weather_manager().weather_at_place(f'{city},{country_code}')
            weather = observation.weather
            temperature = weather.temperature('celsius')['temp']
            status = weather.status
            talk(
                f"The weather in {city}, {country_code} is {status} with a temperature of {temperature} degrees Celsius.")
        except pyowm.commons.exceptions.UnauthorizedError:
            talk("Error: Invalid API Key provided or insufficient permissions.")
    else:
        talk('Please say the command again.')


while True:
    run_alexa()
  
