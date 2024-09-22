import os
from openai import OpenAI 
from dotenv import load_dotenv
import requests
import webbrowser
from bs4 import BeautifulSoup
import urllib.parse
from youtube_search import YoutubeSearch

API = "" #generate api key and paste in  this variable
client = OpenAI(api_key=API)
load_dotenv()

# Dictionary for podcast categories with links and custom responses
podcast_data = {
    "comedy": {
        "link": "https://www.iheart.com/podcast/1119-really-no-really-107027693/",
        "response": "Here are the best episodes of 'Really? No, Really?'"
    },
    "entertainment": {
        "link": "https://www.iheart.com/podcast/268-watch-what-crappens-27937408/",
        "response": "here are the best episodes of 'Watch What Crappens'"
    },
    "curiosity": {
        "link": "https://www.iheart.com/podcast/1119-stuff-you-should-know-26940277/",
        "response": "Here are the best episodes of 'Stuff You Should Know'"
    },
    "food": {
        "link": "https://www.iheart.com/podcast/269-the-restaurant-guys-196620330/",
        "response": "Here are the best episodes of 'The Restaurant Guys'"
    },
    "fiction": {
        "link": "https://www.iheart.com/podcast/1119-table-read-109354461/",
        "response": "Here are the best episodes of 'Table Read'"
    },
    "health": {
        "link": "https://www.iheart.com/podcast/1119-on-purpose-with-jay-shett-30589432/",
        "response": "Here are the best episodes of 'On Purpose With Jay Shetty'"
    },
    "history": {
        "link": "https://www.iheart.com/podcast/867-the-rest-is-history-93597010/",
        "response": "Here are the best episodes of 'The Rest Is History'"
    },
    "news": {
        "link": "https://www.iheart.com/podcast/1119-crime-alert-hourly-update-29622237/",
        "response": "Here are the best episodes of 'Crime Alert Hourly Update'"
    },
    "mindfulness": {
        "link": "https://www.iheart.com/podcast/1119-the-psychology-of-your-20-106793541/",
        "response": "Here are the best episodes of 'The Psychology of your 20s'"
    },
    "politics": {
        "link": "https://www.iheart.com/podcast/256-the-al-franken-podcast-43060871/",
        "response": "Here are the best episodes of 'The AI Franken Podcast'"
    },
    "relationships": {
        "link": "https://www.iheart.com/podcast/274-we-can-do-hard-things-82211497/",
        "response": "Here are the best episodes of 'We Can Do Hard Things'"
    },
    "spirituality": {
        "link": "https://www.iheart.com/podcast/1119-bible-in-a-year-with-jack-102314784/",
        "response": "Here are the best episodes of 'Bible in a Year with Jack Graham'"
    },
    "spooky": {
        "link": "https://www.iheart.com/podcast/1119-unexplained-29139086/",
        "response": "Here are the best episodes of 'Unexplained'"
    },
    "sports": {
        "link": "https://www.iheart.com/podcast/1025-fantasy-football-today-31089186/",
        "response": "Here are the best episodes of 'Fantasy Football Today'"
    },
    "travel": {
        "link": "https://www.iheart.com/podcast/180-travel-with-rick-steves-23086009/",
        "response": "Here are the best episodes of 'Travel with Rick Steves'"
    },
    "society and culture": {
        "link": "https://www.iheart.com/podcast/313-this-american-life-18894588/",
        "response": "Here are the best episodes of 'The American Life'"
    },
    "science and technology": {
        "link": "https://www.iheart.com/podcast/272-something-you-should-know-27942189/",
        "response": "Here are the best episodes of 'Something You Should Know'"
    }
}

def show_podcast(category):
    """
    Play the selected podcast based on the category provided.
    """
    if category in podcast_data:
        podcast_url = podcast_data[category]["link"]
        response_message = podcast_data[category]["response"]
        webbrowser.open(podcast_url)
        return response_message
    else:
        return f"Sorry, I couldn't find the {category} podcast."

def navigate_route(destination):
    """
    Function to open a navigation service in the browser with the specified destination.
    :param destination: The destination to navigate to
    """
    # Open Google Maps with the destination
    google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={destination}"
    webbrowser.open(google_maps_url)
    print(f"Navigating to {destination} on Google Maps.")

def get_traffic_updates(location):
    """Open Google Maps with traffic layer to view traffic conditions."""
    traffic_url = f"https://www.google.com/maps/search/{location}/data=!5m1!1e1?layer=t"
    webbrowser.open(traffic_url)
    print(f"Showing traffic updates for {location}.")

def play_youtube_song(song_name):
    # Search for the song on YouTube and return the first result
    search_results = YoutubeSearch(song_name, max_results=1).to_dict()
    
    if search_results:
        video_url = f"https://www.youtube.com/watch?v={search_results[0]['id']}"
        webbrowser.open(video_url)
        return f"Playing '{song_name}' on YouTube."
    else:
        return f"Sorry, I couldn't find '{song_name}' on YouTube."

def ReplyBrain(question, chat_log=None):

    # Check if the AI detects the command to navigate
    if "navigate to" in question.lower() or "directions to" in question.lower():
        destination = question.lower().replace("navigate to", "").replace("directions to", "").strip()
        if destination:
            navigate_route(destination)
            return f"Navigating to {destination}."
        else:
            return "Sorry, I couldn't understand the destination."

    # Check for traffic update requests
    if "traffic update" in question.lower():
        location = question.lower().replace("traffic update", "").strip()
        if location:
            get_traffic_updates(location)
            return f"Showing traffic updates for {location}."
        else:
            return "Sorry, I couldn't understand the location for traffic updates."
        
    # Play YouTube song if command is detected
    if "play" in question.lower() and "on youtube" in question.lower():
        song_name = question.lower().replace("play", "").replace("on youtube", "").strip()
        if song_name:
            return play_youtube_song(song_name)
        else:
            return "Sorry, I couldn't understand the song name."
        
    # Detect command to play a podcast
    if "shows podcasts on" in question.lower():
        # Extract category from the question
        category = question.lower().replace("shows podcasts on", "").strip()
        return show_podcast(category)
        
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    chat_log_path = os.path.join(base_dir, "DataBase", "chat_log.txt")  # Construct the full path to the chat log

    with open(chat_log_path, "r", encoding= 'utf-8') as file_log:
        chat_log_template = file_log.read()

    if chat_log is None:
        chat_log = chat_log_template

    prompt = f'{chat_log}You : {question}\nMarsh : '
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "from now on you are an AI desktop assistant"},
            {"role": "system", "content": "your name is maarsh"},
            {"role": "system", "content": "you were created by  harsh and  maddy"},
            {"role": "system", "content": " harsh and  maddy are your creator"},
            {"role": "system", "content": " harsh and  maddy created you"},
            {"role": "system", "content": "you were made by  harsh and  maddy"},
            {"role": "system", "content": " harsh and  maddy are your makers"},
            {"role": "system", "content": " always add the prefix 'Sir' before mentioning Harsh and Maddy"},
            {"role": "system", "content": chat_log},
            {"role": "user", "content": question}
        ],
        temperature=0.5,
        max_tokens=100,
    )
    answer = response.choices[0].message.content.strip()

    chat_log_template_update = chat_log_template + f"\nYou : {question} \nMarsh : {answer}"
    with open(chat_log_path, "w", encoding='utf-8') as file_log:
        file_log.write(chat_log_template_update)

    return answer