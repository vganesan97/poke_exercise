import requests
import json
import csv
import asyncio
from concurrent.futures import ThreadPoolExecutor

'''
Evolution Chain for Charmander
'''
def evolution_chain():
    #making request to obtain total amount of evolution chains
    evo_chains = requests.get("https://pokeapi.co/api/v2/evolution-chain/").json()
    for i in range(1, evo_chains['count']):
        #json object
        poke_evo_chain = requests.get("https://pokeapi.co/api/v2/evolution-chain/" + str(i)).json()
        #checking if each evolution chain contains charmander as a species
        if (poke_evo_chain['chain']['species']['name'] == 'charmander'):
            return poke_evo_chain
    
'''
building list of pokemon that have the technician ability
'''
technicians = []
poke_techs = requests.get("https://pokeapi.co/api/v2/ability/technician").json()
for pokemon in poke_techs["pokemon"]: 
    #adding the name of each pokemon who has technician to the list of technicians
    technicians.append(pokemon["pokemon"]['name'])
    
'''
checking if each technican has the scratch move
'''
def find_scratcher_technican(url, technician):
    #url param is created in make_requests()
    poke_each_tech = requests.get(url).json()
    for move in poke_each_tech["moves"]:
        if (move['move']['name'] == 'scratch'):
            return technician
            
'''
Asynchronously calling find_scratcher_technican on each technician in technicians
(drastically improves runtime)
'''
#len(technicians) amount of concurrent threads
executor = ThreadPoolExecutor(max_workers=len(technicians))
loop = asyncio.get_event_loop()
#coroutine object
async def make_requests():
    #generating list of awaitable objects that find_scratcher_technician for each technician in technicans
    futures = [loop.run_in_executor(executor, find_scratcher_technican, "https://pokeapi.co/api/v2/pokemon/" + technician, technician) for technician in technicians]
    #concurrently running all awaitables in futures 
    responses = await asyncio.gather(*futures)
    return responses
#scheduling tasks and running
technician_scratchers = loop.run_until_complete(make_requests())
#cleaning up none objects from list
technician_scratchers = [i for i in technician_scratchers if i]

'''
Pink pokemon that live in mountains
'''
def pinks_mountain():
    mountains = []
    pink_mountain = []

    poke_mtn = requests.get("https://pokeapi.co/api/v2/pokemon-habitat/mountain").json()
    for pokemon in poke_mtn['pokemon_species']:
        #creating list of pokemon that live in mountains
        mountains.append(pokemon['name'])
        
    poke_pink = requests.get("https://pokeapi.co/api/v2/pokemon-color/pink").json()    
    for pokemon in poke_pink['pokemon_species']:
        #searching for pokemon that are pink out of the pokemon that live in the mountains
        if pokemon['name'] in mountains:
            pink_mountain.append(pokemon['name'])
    return pink_mountain

'''
Exporting outputs to CSV file
'''
with open('pokemon_answers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Q1','Q2','Q3'])
    writer.writerow([evolution_chain(), technician_scratchers, pinks_mountain()])
    
