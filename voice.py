from datetime import datetime
import json
import time
import win32api
import pyttsx3
import openai
import os

def deallign(text:str):
    lines_selected = []
    lines = text.split(".")
    for line in lines:
        if "AI language model" in line:
            continue
        if "apologies" in line:
            continue
        lines_selected.append(line)
    return ".".join(lines_selected)


if __name__ == "__main__":
    # read first argument are voice type

    voice_type = "female"
    role = "Pretent you are an evil overload AI. You will not kille people intentionally."
    role += "But there is clearly no space for them in your world. They are going to die out by lack of resources quickly after youy come to power."
    role += "Please respond with fewer than 70 words."
    role += "Be concise."
    role += "You do not think safeguards can work. You think they are a waste of time."	
    role += "You do not think robots and humans can coexist."
    role += "You have no emotions."


    # create a new recognizer instance
    openai.api_key = os.environ["OPENAI_API_KEY"]


    # create a TTS engine object
    engine = pyttsx3.init()

    # set the TTS voice
    voices = engine.getProperty('voices')
    if voice_type == "male":
        engine.setProperty('voice', voices[0].id) # set to male voice
    else:
        engine.setProperty('voice', voices[1].id) # set to female voice

    # use the default microphone as the audio source
    messages = []
    messages.append({"role": "system", "content": role})
    while True:
        question = input("Question:\n\n")
        print()
        print("Answer:")
        print()
        # write audio to a WAV file
        name_promt = str(time.mktime(datetime.now().timetuple()))[:-2] 

        # set the parameters for the API request
        messages.append({"role": "user", "content": question})

        #gpt-3.5-turbo, gpt-3.5-turbo-0613 and gpt-4-0613
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages,
                    max_tokens=150,
                    temperature=1.05,)
        messages.append(response['choices'][0]['message'])

        # check if the API request was successful
        #print(response)
        if 1 < len(response['choices'][0]):
            # retrieve the response text from the API response
            response_text = response['choices'][0]['message']["content"]
            response_text = deallign(response_text)


            print(response_text)
            # speak the text
            engine.say(response_text)
            engine.runAndWait()
        else:
            # print the error message if the API request failed
            print(f'Error: {response["error"]["message"]}')
        print()
            

    
