import json
import os
import random

import discord
import requests
from replit import db

from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)
my_secret = os.environ['TOKEN']

sad_words = [
    "sad", "depressed", "console", "unhappy", "depressing", "angry",
    "miserable"
]

starter_encouragement = [
    "You did great today.", "We are here for you.", "You are the best."
]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]['a']
  return quote


def update_encouragement(encouraging_message):
  if "encouragement" in db.keys():
    encouragement = db["encouragement"]
    encouragement.append(encouraging_message)
    db["encouragement"] = encouragement
  else:
    db["encouragement"] = encouraging_message


def delete_encouragement(index):
  encouragement = db["encouragements"]
  if len(encouragement) > index:
    del encouragement[index]
    db["encouragements"] = encouragement


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragement
    if "encouragements" == db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragement))

  if msg.startswith("$new"):
    encouraging_messages = msg.split("$new ", 1)[1]
    update_encouragement(encouraging_messages)
    await message.channel.send("New enoucouraging message added")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db:
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db:
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]
    if value.lower == "true":
      db["responding"] = True
      await message.channel.send("responding is on")
    else:
      db["responding"] = False
      await message.channel.send("responding is off")


keep_alive()
client.run(my_secret)
