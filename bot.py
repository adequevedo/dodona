import discord
import os
import datetime
import json

from discord.ext import commands

def get_latest_json_file(directory):
  """Returns the latest JSON file in the given directory.

  Args:
    directory: The directory to search.

  Returns:
    The latest JSON file, or None if no JSON files are found.
  """

  files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(".json")]

  # Sort the files by timestamp, with the most recent file first.
  files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)

  # Return the most recent JSON file.
  if files:
    print(files[0])
    return files[0]
  else:
    return None

def find_wong(file_name):
    f = open(file_name)
    data = json.load(f)

    message = "Wong Teasers:\n\n"

    try: 
        for matchup in data: 
            home_team = matchup['home_team']
            # away_team = matchup['away_team']
            for y in matchup['bookmakers']:
                if y['key'] == 'betus' and y['markets'][1]['key'] == 'spreads':
                    # y['markets'][1]['outcomes'] is the either h2h, spread, totals; If this order is messed up, no h2h bc its a pickem
                    # 4 checks home and away favorite and dog 
                    if(y['markets'][1]['outcomes'][0]['point'] >= 1.5 and y['markets'][1]['outcomes'][0]['point'] <= 3):
                        # if home_team == y['markets'][1]['outcomes'][0]['name']: message += "(H) "
                        message += "(H) " if home_team == y['markets'][1]['outcomes'][0]['name'] else "(A) "
                        message += f'''{y['markets'][1]['outcomes'][0]['name']} +{y['markets'][1]['outcomes'][0]['point']}
vs
{y['markets'][1]['outcomes'][1]['name']}

'''

                    if(y['markets'][1]['outcomes'][0]['point'] <= -7.5 and y['markets'][1]['outcomes'][0]['point'] >= -9):
                        # if home_team == y['markets'][1]['outcomes'][0]['name']: message += "(H) "
                        message += "(H) " if home_team == y['markets'][1]['outcomes'][0]['name'] else "(A) "
                        message += f'''{y['markets'][1]['outcomes'][0]['name']} {y['markets'][1]['outcomes'][0]['point']}
vs
{y['markets'][1]['outcomes'][1]['name']}
                        
'''
                        
                    if(y['markets'][1]['outcomes'][1]['point'] >= 1.5 and y['markets'][1]['outcomes'][1]['point'] <= 3):
                        # if home_team == y['markets'][1]['outcomes'][1]['name']: message += "(H) "
                        message += "(H) " if home_team == y['markets'][1]['outcomes'][1]['name'] else "(A) "
                        message += f'''{y['markets'][1]['outcomes'][1]['name']} +{y['markets'][1]['outcomes'][1]['point']}
vs
{y['markets'][1]['outcomes'][0]['name']}

'''
                        
                    if(y['markets'][1]['outcomes'][1]['point'] <= -7.5 and y['markets'][1]['outcomes'][1]['point'] >= -9):
                        # if home_team == y['markets'][1]['outcomes'][1]['name']: message += "(H) "
                        message += "(H) " if home_team == y['markets'][1]['outcomes'][1]['name'] else "(A) "
                        message += f'''{y['markets'][1]['outcomes'][1]['name']} {y['markets'][1]['outcomes'][1]['point']}
vs
{y['markets'][1]['outcomes'][0]['name']}

'''
    except Exception as e: 
        print(e)
        
    return message

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('$wong'):

        file_name = "data/" + get_latest_json_file('data/')
        output = find_wong(file_name)
        channel = message.channel
        # channel = channel
        await channel.send(output)
        print(f"{datetime.datetime.now()} - sent message")

client.run(os.environ.get('DISCORD_KEY'))
