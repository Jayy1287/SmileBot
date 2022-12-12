import os
import discord
import requests  #allows module to make http requets
import json  #api returns a json
import random  #the bot chooses messages randomly
from replit import db  #lets us use replit database
from keep_alive import keep_alive

my_secret = os.environ['smile_bot_token']

#client = discord.Client()
intents = discord.Intents().all()
client = discord.Client(intents=intents)

sad_words = [
  "sad", "unhappy", "pain", "depressed", "depression", "fault", "cry"
]

starter_enc = ["You got this", "Cheer up", "It's okay", "I'm here for you"]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


def update_enc(enc_in):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_in)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_in]


def delete_enc(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send('Hello Smile Bot Welcomes you -Jayy')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_enc
    if "encouragements" in db.keys():
      options = options + db[
        "encouragements"].value  #added .value from stackoverflow

    if any(word in msg for word in sad_words):
      #await message.channel.send('Issokay')
      #enc = random.choice(starter_enc)
      #await message.channel.send(enc)
      await message.channel.send(random.choice(options))

  if msg.startswith('$new'):
    enc_in = msg.split("$new ", 1)[1]
    update_enc(enc_in)
    await message.channel.send("New encouraging message added. Thanks:)")

  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ", 1)[1])
      delete_enc(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith('$listenc'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements.value)

  if msg.startswith("$responding"):
    value = msg.split("responding ", 1)[1]
    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


keep_alive()
client.run(os.environ['smile_bot_token'])
