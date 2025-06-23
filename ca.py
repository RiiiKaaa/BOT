# continuous_assistant.py
from faster_whisper import WhisperModel
import pyaudio
import tempfile
import wave
import pyttsx3
import re
import string
import requests
import difflib

# Load the model
model = WhisperModel("base.en", device="cpu")

# Initialize text-to-speech
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

if "conversation_context" not in globals():
        conversation_context = {
            "awaiting_city": False
        }


def get_weather(city, api_key):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        condition = data['current']['condition']['text']
        temp_c = data['current']['temp_c']
        feels_like = data['current']['feelslike_c']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        return (
            f"Weather in {city}:\n"
            f"Condition: {condition}\n"
            f"Temperature: {temp_c}°C (Feels like {feels_like}°C)\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind_kph} km/h"
        )
    else:
        return "Sorry, I couldn't fetch the weather info right now."


# ENHANCED: Your get_response function with better intent recognition
def get_response(text):
    # ORIGINAL: Basic text cleaning (kept same)
    clean_text = text.translate(str.maketrans('', '', string.punctuation)).lower().strip()
    
    # NEW: Enhanced pattern matching - instead of simple "in" checks, we use regex patterns
    # This allows for more flexible matching and better intent recognition


    
    # ENHANCED: Greeting detection - now catches more variations
    greeting_patterns = [
    r'\b(hi|hello|hey|yo|howdy|hiya|sup|wassup|heya|hola)\b',  # Common casual greetings
    r'\b(good morning|good afternoon|good evening|good day|morning|evening|afternoon)\b',  # Time-based
    r'\b(what\'s up|what up|how are you|how\'s it going|how do you do|how you doing|how are things|what\'s new)\b',  # Casual small talk
    r'\b(greetings|nice to meet you|pleasure to meet you|long time no see|yo bro|yo man|namaste|salutations)\b',  # Formal and cultural
    ]
    # Check if any greeting pattern matches
    if any(re.search(pattern, clean_text) for pattern in greeting_patterns):
        return "Hello! How are you doing today?"
    

    
    # ENHANCED: How are you detection - more variations
    how_are_you_patterns = [
    r"\b(how are you|how're you|how r u|how are u)\b",  # Common phrasing
    r"\b(how do you do|how d'you do|how you doin'?|how u doing|how you doing)\b",  # Formal + slang
    r"\b(how is it going|how's it going|how goes it|how's things|how's everything)\b",  # Casual variations
    r"\b(what's up|wassup|sup|whats up)\b",  # Slangy casual check-ins
    r"\b(how's your day|how's your night|how's your morning|how was your day)\b",  # Time-specific
    r"\b(you good|you alright|everything good|all good|you okay|u okay|you ok)\b"  # Concerned variations
    ]
    if any(re.search(pattern, clean_text) for pattern in how_are_you_patterns):
        return "I'm doing great, thank you for asking! How about you?"
    


    I_am_good_patterns = [
    r"\b(i am good|i'm good|im good|i am fine|i'm fine|im fine)\b",
    r"\b(i am alright|i'm alright|im alright|i'm all right|i am all right)\b",
    r"\b(i feel good|i'm ok|im ok|i'm okay|i am okay|i'm okk|im okk|i'm okey)\b",
    r"\b(i feel fine|i'm feeling good|i'm doing well|i am doing well|i'm doing great|i'm doing fine)\b",
    r"\b(i'm extremely good|i am fantastic|i'm fantastic|i'm amazing|i feel awesome|i'm awesome)\b",
    r"\b(not bad|pretty good|can't complain|all good|doing okay|doing fine|everything's fine)\b"
    ]
    if any(re.search(pattern, clean_text) for pattern in I_am_good_patterns):
        return "Nice to hear that! I'm happy that you feel fine."
    

    
    # ENHANCED: Name inquiry - better detection
    name_patterns = [
    r"\b(what is your name|what's your name|who are you|who r u|who u)\b",
    r"\b(tell me your name|what do they call you|what are you called)\b",
    r"\b(what should i call you|how should i address you)\b",
    r"\b(do you have a name|may i know your name|can i know your name)\b",
    r"\b(your name please|name please|ur name)\b",
    r"\b(what can i call you|who am i talking to)\b"
    ]
    if any(re.search(pattern, clean_text) for pattern in name_patterns):
        return "I'm ReeKa! Your voice assistant."
    

    
    # ENHANCED: Farewell detection - more variations
    farewell_patterns = [
    r"\b(bye|goodbye|see you|see ya|farewell|later|peace out|ciao)\b",
    r"\b(take care|catch you later|talk to you later|talk soon|see you later|until next time)\b",
    r"\b(have a good day|have a great day|have a nice day|have a good one|see you around)\b",
    r"\b(i'm leaving|gotta go|i have to go|i’m out|i need to go|leaving now)\b",
    r"\b(bye bye|buh bye|see ya later|ttyl)\b"  # ttyl = talk to you later
    ]
    if any(re.search(pattern, clean_text) for pattern in farewell_patterns):
        return "Goodbye! Have a wonderful day!"
    



    # ENHANCED: Gratitude detection - broader recognition
    gratitude_patterns = [
    r"\b(thank you|thanks|thx|thanx|ty|thank ya|tysm|thank u|thanks a ton)\b",  # Common + shorthand
    r"\b(thanks a lot|thanks so much|thanks very much|thanks a bunch|many thanks)\b",  # Emphatic
    r"\b(i appreciate it|i really appreciate it|much appreciated|truly appreciated|so grateful|grateful)\b",  # Appreciative
    r"\b(thank you so much|thank you very much|i can't thank you enough)\b",  # Polite/formal
    r"\b(big thanks|huge thanks|lots of thanks|loads of thanks)\b"  # Colloquial
    ]
    if any(re.search(pattern, clean_text) for pattern in gratitude_patterns):
        return "You're very welcome! I'm happy to help you."
    



    # ENHANCED: Time inquiry - better pattern matching
    time_patterns = [
    r"\b(what time is it|what's the time|what time)\b",
    r"\b(current time|tell me the time|do you know the time)\b",
    r"\b(can you tell me the time|could you tell me the time)\b",
    r"\b(time please|do you have the time|know the time)\b",
    r"\b(what's the current time|any idea what time it is)\b",
    r"\b(got the time|time now|show time)\b"
    ]
    if any(re.search(pattern, clean_text) for pattern in time_patterns):
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"
    



    # ENHANCED: Date inquiry - more comprehensive
    date_patterns = [
    r"\b(what's the date today|what is the date today|today's date|what date is it|current date|what date)\b",
    r"\b(what day is it|what's today|what is today|tell me the date|date please)\b",
    r"\b(can you tell me the date|could you tell me the date|do you know the date)\b",
    r"\b(what day of the week is it|which day is it today)\b",
    r"\b(tell me today's date|any idea what the date is)\b"
    ]
    if any(re.search(pattern, clean_text) for pattern in date_patterns):
        from datetime import datetime
        return f"Today's date is {datetime.now().strftime('%B %d, %Y')}"
    



    # ENHANCED: Help request - better detection
    help_patterns = [
    r"\b(help|assist|support|aid|need assistance|i need help)\b",
    r"\b(can you help me|could you help me|will you help me|i need some help|help me out)\b",
    r"\b(what can you do|how can you help|what do you do|how do you work)\b",
    r"\b(guide me|show me|teach me|walk me through|explain this|how does this work)\b",
    r"\b(i'm stuck|i'm confused|i'm lost|can you explain|need guidance)\b",
    r"\b(give me instructions|i need support|help required|assist me)\b"
    ]
    if any(re.search(pattern, clean_text) for pattern in help_patterns):
        return "I'm here to help! I can tell you the time and date, answer basic questions, and have conversations with you. What would you like to know?"
    



    # NEW: Question detection - recognizes when user asks questions
    question_patterns = [
        r'^\s*(what|how|when|where|why|who|which)\b',  # Starts with question words
        r'\?$'  # Ends with question mark
    ]
    if any(re.search(pattern, clean_text) for pattern in question_patterns):
        return f"That's an interesting question! You asked: '{text}'. I'm still learning, but I'm here to help. Could you be more specific?"
    



    # ENHANCED: Math/calculation detection with full expression evaluation
    math_patterns = [
        r'\b(calculate|compute|solve|math)\b',
        r'\b(add|subtract|multiply|divide)\b',
        r'\b(what is|what\'s)\s*[\d\+\-\*\/\(\)\.\s]+\b',
        r'[\d\+\-\*\/\(\)\.\s]{3,}',
        r'\b(plus|minus|times|divided by)\b'
    ]
    
    if any(re.search(pattern, clean_text) for pattern in math_patterns):
        try:
            # Step 1: Convert word-based operators to symbols
            math_text = clean_text.lower()
            math_text = re.sub(r'\bplus\b', '+', math_text)
            math_text = re.sub(r'\badd\b', '+', math_text)
            math_text = re.sub(r'\bminus\b', '-', math_text)
            math_text = re.sub(r'\bsubtract\b', '-', math_text)
            math_text = re.sub(r'\btimes\b', '*', math_text)
            math_text = re.sub(r'\bmultiply\b', '*', math_text)
            math_text = re.sub(r'\bdivided by\b', '/', math_text)
            math_text = re.sub(r'\bdivide\b', '/', math_text)
            
            # Step 2: Convert number words to digits
            word_to_num = {
                'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
                'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
                'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20'
            }
            for word, num in word_to_num.items():
                math_text = re.sub(r'\b' + word + r'\b', num, math_text)

            # Step 3: Try to extract math expression after keywords
            expression_match = re.search(
                r'\b(?:what is|what\'s|calculate|compute|solve)\s+([\d\+\-\*\/\(\)\.\s]+)', math_text
            )
            if expression_match:
                expression = expression_match.group(1).strip()
            else:
                expression_match = re.search(r'([\d\+\-\*\/\(\)\.\s]{3,})', math_text)
                if expression_match:
                    expression = expression_match.group(1).strip()

            # Step 4: Clean and prepare expression
            if expression:
                expression = re.sub(r'\s+', '', expression)
                expression = re.sub(r'[\+\-\*\/]+$', '', expression)

                # Step 5: Safety check (only allow safe characters)
                if re.fullmatch(r'[\d\+\-\*\/\(\)\.]+', expression):
                    try:
                        result = eval(expression)
                        return f"The answer is {result}"
                    except Exception as eval_error:
                        return "Sorry, I couldn't evaluate the expression safely."
                else:
                    return "The expression seems unsafe or invalid."

        except Exception as e:
            print("Error during math expression processing:", str(e))
            return "Oops! Something went wrong while solving the math."





    # List of valid cities
    city_list = ["Delhi", "London", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Lucknow", "Pune", "Jaipur", "Agra", "Aligarh"]

    # Access the global conversation context
    global conversation_context
    
    def extract_city_fuzzy(user_input, city_list):
        user_input = user_input.lower()
        for word in user_input.split():
            match = difflib.get_close_matches(word, [c.lower() for c in city_list], n=1, cutoff=0.7)
            if match:
                for city in city_list:
                    if city.lower() == match[0]:
                        return city
        return None

    # Weather regex patterns
    weather_patterns = [
        r"\b(weather|temperature|forecast|climate|rain|sun|snow|wind|humidity)\b",
        r"\b(how's the weather|what's the weather like|is it raining|is it sunny|is it hot|is it cold)\b",
        r"\b(will it rain|weather today|today's forecast|tomorrow's forecast)\b",
        r"\b(what's the temperature|how hot is it|how cold is it|current weather)\b"
    ]

    # Check if we're waiting for a city name
    if conversation_context.get("awaiting_city"):
        city = extract_city_fuzzy(clean_text, city_list)
        if city:
            conversation_context["awaiting_city"] = False
            return get_weather(city, "25d4ff942f3b4a188b4140403252306")
        else:
            return "Sorry, I could not catch the city name. Could you say it again?"

    # Check for weather request in fresh input
    if any(re.search(pattern, clean_text, re.IGNORECASE) for pattern in weather_patterns):
        city = extract_city_fuzzy(clean_text, city_list)
        if city:
            return get_weather(city, "25d4ff942f3b4a188b4140403252306")
        else:
            conversation_context["awaiting_city"] = True
            return "Sure! Which city would you like the weather for?"




    # ENHANCED: Default response - now more helpful
    # Instead of just echoing back, we provide guidance
    return f"I heard you say: '{text}'. I'm still learning to understand everything, but I'm here to help! Try asking me about the time, date, or just say hello. You can also ask 'what can you do' for more options."


# Function to record audio (kept same)
def record_audio(duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("Say something...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        wf = wave.open(tmp_file.name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return tmp_file.name

# 🔁 Continuous loop (kept same)
def start_assistant():
    print("Assistant is now listening. Say 'stop conversation' to exit.\n")
    
    while True:
        audio_file = record_audio(duration=5)
        segments, info = model.transcribe(audio_file)
        text = "".join(segment.text for segment in segments).strip()
        
        if text:
            print("You said:", text)
            
            if "stop conversation" and "stop" in text.lower():
                print("Assistant: Goodbye! Conversation ended.")
                tts_engine.say("Goodbye! Conversation ended.")
                tts_engine.runAndWait()
                break
            
            # ENHANCED: Now using the improved get_response function
            response = get_response(text)
            print("Assistant:", response)
            tts_engine.say(response)
            tts_engine.runAndWait()
        else:
            print("No speech detected. Listening again...\n")



# Start the assistant when script is run directly
if __name__ == "__main__":
    start_assistant()


