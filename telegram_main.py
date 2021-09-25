from requests.models import Response
from telethon import TelegramClient, events
from requests.auth import HTTPBasicAuth
import requests
from creds import client_secret, client_id, api_id, api_hash, bot_token

endpoint = "https://www.udemy.com/api-2.0/"
NAME = "Peter Alkema"

def get_page(link, client_id, client_secret):
    response = requests.get(link, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()

def search_term(term):
    link_1 = endpoint + "courses/?page="
    link_2 = "&search=" + term
    rank = 1
    for page in range(1, 11):
        link = link_1 + str(page) + link_2
        page = get_page(link, client_id, client_secret)
        for course in page['results']:
            course_url = "https://www.udemy.com" + course['url']
            image = course["image_240x135"]
            course_name = course['title']
            for instructor in course['visible_instructors']:
                if instructor['title'] == NAME:
                    return [rank, course_url, image, course_name]
            rank += 1
    
    return [999, "#", "#", "#"]


bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hi!')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    query = event.text
    result = search_term(query)
    reply = f"RANK:   {result[0]} \nTITLE:   {result[3]} \nLINK:   {result[1]}"
    await event.respond(reply)

def main():
    """Start the bot."""
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()