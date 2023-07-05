import openai
import pyttsx3
import speech_recognition as sr
import random

# set openai api key

openai.api_key = "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"

model_id = 'gpt-3.5-turbo'

# initialize the text-to-speech engine

engine = pyttsx3.init()

# change speech rate
engine.setProperty('rate', 180)

# get the available voice
voices = engine.getProperty('voices')

# choose a voice based on the voice id
engine.setProperty('voice', voices[1].id)

# counter just for interacting purpose
interaction_counter = 0


def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print("")
            # print skipping unknown error


def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )

    api_useage = response['useage']
    print('Total token consumed: {0}'.format(api_useage['total_tokens']))
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


# starting convo
conversation = [{'role': 'user', 'content': 'Please, Act Like Friday AI from Iron Man, '
                                            'make a 1 sentence phrase introducing yourself without saying '
                                            'something that sounds like this chat its already'}]
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip))
speak_text(conversation[-1]['content'].strip())


def activate_assistant():
    starting_chat_phrases = ["Yes sir, how may I assist you?",
                             "Yes, what can I do for you?",
                             "How can I help you ,sir?",
                             "Friday here, how can I help you today?",
                             "Yes, what can I do for you today?",
                             "Yes sir, what is on your mind?",
                             "Friday ready to assist, what can I do for you?",
                             "At your command, sir. How may I help you today?",
                             "Yes boss, I'm here to help. What do you need from me?",
                             "Yes, I', listening. What can I do for you, sir?",
                             "How can I assist you today, sir?",
                             "Yes, sir. How cam I make your day easier?",
                             "Yes boss, what's the plan?",
                             "Yes, what's on your mind, sir?"]

    continued_chat_phrases = ["yes", "yes,sir", "yes,boss", "I'm all ears"]
    random_chat = ""
    if interaction_counter == 1:
        random_chat = random.choices(starting_chat_phrases)
    else:
        random_chat = random.choices(continued_chat_phrases)

    return random_chat


def append_to_log(text):
    with open("chat_log.txt", "a") as f:
        f.write(text + "\n")


while True:
    print("Say 'Friday' to start...")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "friday" in transcription.lower():
                interaction_counter += 1

                # record audio
                filename = "input.wav"

                readyToWork = activate_assistant()
                speak_text(readyToWork)
                print(readyToWork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())

                    # transcribe audio to text
                text = transcribe_audio_to_text(filename)

                if text:
                    print(f"You said: {text}")
                    append_to_log(f"You: {text}\n")

                    # generate response using chatGPT
                    print(f"Friday says: {conversation}")

                    prompt = text

                    conversation.append({'role': 'user', 'content': prompt})
                    conversation = ChatGPT_conversation(conversation)

                    print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content']))

                    append_to_log(f"Friday: {conversation[-1]['content'].strip()}\n")

                    # read response using text-to-speech
                    speak_text(conversation[-1]['content'].strip())

        except Exception as e:
            continue
            # print("An error occurred:{}".format(e))
