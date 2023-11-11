import discord, os, datetime, json 
from collections import deque
from google.cloud import storage
from google.cloud import secretmanager
from discord.ext import commands

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

        data = get_file_from_bucket("dione", "data/NFL/")
        output = find_wong(data)
        channel = message.channel
        await channel.send(output)
        print(f"{datetime.datetime.now()} - sent message")


SECRET_ID = os.environ.get('SECRET_ID') or "projects/371661757130/secrets/wager-bot-discord-token/versions/latest"

sm_client = secretmanager.SecretManagerServiceClient()
response = sm_client.access_secret_version(request={"name": SECRET_ID})

payload = response.payload.data.decode("UTF-8")

client.run(payload)

def get_file_from_bucket(bucket_name, prefix):
    print("File From Bucket")
    try: 
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        
        # List objects in bucket, then get most recent object 
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
        dd = deque(blobs, maxlen=1)
        last_element = dd.pop()
        
        blob = bucket.blob(last_element.name)
        # print(last_element.name)
        contents = blob.download_as_string()
        # my_json = contents.decode('utf8').replace("'", '"')
        data = json.loads(contents)
                
        return data

    except Exception as e: 
        print("ERROR: ", e)


def find_wong(data):
    print("Starting Wong")

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