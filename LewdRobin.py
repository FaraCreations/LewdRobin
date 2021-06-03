import discord
import re
import os
import configparser
from discord import channel
import requests
from math import ceil
import random
import time
import datetime
import pytz
import asyncio
import socket

# global variables
botToken = "XXXXXX"
intents = discord.Intents.default()
intents.bans = False
intents.emojis = True
intents.guilds = True
intents.messages = True
intents.integrations = False
intents.invites = False
intents.members = True
intents.presences = False
intents.reactions = True
intents.typing = False
intents.value = False
intents.voice_states = False
intents.webhooks = False
UTC = pytz.utc
dt = datetime
dtt = datetime.datetime
ns = time.time_ns
nsMinute = 60000000000
bot = discord.Client(Intents=intents)
ap = os.path.abspath
main = os.path.dirname(ap(__file__))
promptLogs = f'{main}/promptLogs'
serverConfigs = f'{main}/serverConfigs'
task = bot.loop.create_task
initialize = {}
initialize["on_ready"] = False
initialize["guildCommands"] = True
initialize["globalCommands"] = True
initialize["deleteGlobalCommands"] = True
initialize["deleteGuildCommands"] = True
headers = {"Authorization": f"Bot {botToken}"}
promptHeader = ">>> **New LewdRobin Writing Prompt**"
promptHeaderActive = ">>> **Active LewdRobin Writing Prompt**"
promptHeaderCondluded = ">>> **LewdRobin Writing Prompt**"
promptReminder = "\n*Reactions: :white_check_mark: join this prompt; :x: drop from the prompt; :play_pause: pause or resume the prompt;  :arrows_counterclockwise: generate a new prompt; :question: open the help menu.*"
promptReminderActive = "\n*Reactions: :white_check_mark: join this prompt; :x: drop from the prompt; :play_pause: pause or resume the prompt;  :arrows_counterclockwise: generate a new prompt; :question: open the help menu; :scroll: show the story log*"
promptReminderConcluded = "\n*Reactions: :question: open the help menu; :scroll: show the story log*"
listEnvironments = []
listCharacterTypes = []
listCharacterSpecies = []
listScenes = []
listPlay = []
guildIDList = []
pinMessages = {}
contributors = {}
timers = {}
tempTimers = {}
DMConfigDefault = {'environments': True, 'characters': True, 'scenes': True, 'play': True, 'character_number': 4, 'play_number': 4, 'japan': True, 'europe': True, 'america': True, 'historical': True, 'modern': True, 'futuristic': True, 'fantasy': True, 'cis_men': True, 'cis_women': True, 'nonbinary': True, 'trans_men': True, 'trans_women': True, 'futanari': True, 'mammals': True, 'reptiles': True, 'fish': False, 'birds': False, 'insects': False, 'arachnids': False, 'humans': True, 'elves': True, 'dwarves': True, 'halflings': True, 'gnomes': False, 'tieflings': True, 'merfolk': True, 'orcs': True, 'goliaths': True, 'goblinoids': False, 'ilithids': False, 'slimes': True, 'tentacles': True, 'dryads': True, 'harpies': False, 'lamia': False, 'centaurs': False, 'minotaurs': False, 'giants': False, 'werebeasts': True, 'vampires': True, 'undead': False, 'demons': True, 'angels': True, 'faeries': True, 'cyborgs': True, 'androids': True, 'robots': False, 'humanoid_aliens': True, 'aliens': False, 'urban': True, 'rural': True, 'college': True, 'magical': True, 'tech': True, 'romance': True, 'kissing': True, 'cuddling': True, 'petting': True, 'grinding': True, 'titjobs': True, 'ass_play': True, 'anal_sex': True, 'manual_sex': True, 'oral_sex': True, 'intercrural_sex': True, 'penetrative_sex': True, 'basic_toys': True, 'age_play': False, 'bondage': False, 'biting': False, 'breast_play': False, 'impact_play': False, 'orgasm_control': False, 'genitorture': False, 'cuckoldry': False, 'cupping': False, 'dom_and_sub': False, 'knife_play': False, 'electro_play': False, 'food_play': False, 'temperature_play': False, 'fire_play': False, 'fisting': False, 'foot_play': False, 'degradation': False, 'exhibition': False, 'pet_play': False, 'piss_play': False, 'consensual_nonconsent': False, 'sensory_deprivation': False, 'sounding': False, 'intoxicants': False, 'incest': False, 'bestiality': False, 'size_play': False, 'partial_growth': False, 'extreme_insertions': False, 'inflation': False, 'transformation': False, 'impregnation': False, 'oviposition': False, 'dubious_consent': False, 'nonconsent': False, 'torture': False, 'gore': False, 'soft_vore': False, 'hard_vore': False, 'snuff': False, 'necrophilia': False}
DMConfig = {}

#directory configuration
os.chdir(main)
try:
    os.mkdir(promptLogs)
except:
    pass
try:
    os.mkdir(serverConfigs)
except:
    pass

#classes
class ld:
    def __init__(self, text, *args):
        self.text = text
        self.tags = []
        for i in args:
            self.tags.append(i)
    def addTo(self, listName):
        listName.append(self)

class Interaction:
    def __init__(self, client):
        self._client = client
        self.client_id = str(client.user.id)
        client._connection.parsers["INTERACTION_CREATE"] = self._function_runner
    def _function_runner(self, data):
        try:
            task(on_interaction(data))
        except:
            pass

# function library
def listPopulator():
    listEnvironments.clear()
    listCharacterTypes.clear()
    listCharacterSpecies.clear()
    listScenes.clear()
    listPlay.clear()
    year = dtt.today().year
    ld('Hiroshima, Japan, Era of Living Kami', 'japan', 'fantasy').addTo(listEnvironments)
    ld('Kyoto, Japan, 1708', 'japan', 'historical').addTo(listEnvironments)
    ld('Kawagoe Village, Japan, 1545', 'japan', 'historical').addTo(listEnvironments)
    ld('Tokyo, Japan, 1979', 'japan', 'historical').addTo(listEnvironments)
    ld(f'Osaka, Japan, {year}', 'japan', 'modern').addTo(listEnvironments)
    ld(f'Mount Fuji, Japan, {year}', 'japan', 'modern').addTo(listEnvironments)
    ld('Tokyo, Japan, 2050', 'japan', 'futuristic').addTo(listEnvironments)
    ld('Tokyo ULTRA, Geosynchronous Orbit above Japan, 2364', 'japan', 'futuristic').addTo(listEnvironments)
    ld('Avalon, Arthurian England', 'europe', 'fantasy').addTo(listEnvironments)
    ld('Crete, Greece, Mythical Era', 'europe', 'fantasy').addTo(listEnvironments)
    ld('London, England, 1941', 'europe', 'historical').addTo(listEnvironments)
    ld('Paris, France, 1789', 'europe', 'historical').addTo(listEnvironments)
    ld('Rome, Italy, 117 AD', 'europe', 'historical').addTo(listEnvironments)
    ld('Roskilde, Denmark, 1069', 'europe', 'historical').addTo(listEnvironments)
    ld(f'Liverpool, England, {year}', 'europe', 'modern').addTo(listEnvironments)
    ld(f'Cote d\'Azure, France, {year}', 'europe', 'modern').addTo(listEnvironments)
    ld(f'The Alps, Switzerland, {year}', 'europe', 'modern').addTo(listEnvironments)
    ld(f'Berlin, Germany, {year}', 'europe', 'modern').addTo(listEnvironments)
    ld('Fallen London, England Undersea, 2146', 'europe', 'futuristic', 'fantasy').addTo(listEnvironments)
    ld('Conclave of the United Earth, Switzerland, 2285', 'europe', 'futuristic').addTo(listEnvironments)
    ld('Pink District, French Space Elevator, 2099', 'europe', 'futuristic').addTo(listEnvironments)
    ld('NSS Ragnarok, Oslo Spaceport, Norway, 2323', 'europe', 'futuristic').addTo(listEnvironments)
    ld('Boston, Massachusets, 1776', 'america', 'historical').addTo(listEnvironments)
    ld('Plymouth, Massachutsets, 1620', 'america', 'historical').addTo(listEnvironments)
    ld('New Orleans, Louisiana, 1803', 'america', 'historical').addTo(listEnvironments)
    ld('Sedona, Arizona, 1895', 'america', 'historical').addTo(listEnvironments)
    ld('San Francisco, California, 1969', 'america', 'historical').addTo(listEnvironments)
    ld('Chicago, Illinois, 1920', 'america', 'historical').addTo(listEnvironments)
    ld(f'Los Angelas, California, {year}', 'america', 'modern').addTo(listEnvironments)
    ld(f'Austin, Texas, {year}', 'america', 'modern').addTo(listEnvironments)
    ld(f'New York, New York, {year}', 'america', 'modern').addTo(listEnvironments)
    ld(f'Key West, Florida, {year}', 'america', 'modern').addTo(listEnvironments)
    ld(f'Spokane, Washington, {year}', 'america', 'modern').addTo(listEnvironments)
    ld('Shady Sands, New California Republic, 2196', 'america', 'futuristic').addTo(listEnvironments)
    ld('VirtuVegas, Nevadan Cyberspace, 2088', 'america', 'futuristic').addTo(listEnvironments)
    ld('Unity City, Worker\'s Republic of America, 2121', 'america', 'futuristic').addTo(listEnvironments)
    ld('Shady Sands, New California Republic, 2196', 'america', 'futuristic').addTo(listEnvironments)
    ld('Hudson Arcology 4, New York, 2250', 'america', 'futuristic').addTo(listEnvironments)
    ld('Palace of the Omnarch, Earth Lagrange 1, 80th Year of the 4th Imperial Era', 'futuristic').addTo(listEnvironments)
    ld('Flagstand, Mare Tranquillitatis, Luna, 2065', 'futuristic').addTo(listEnvironments)
    ld('New California, Valles Marineris, Mars, 2206', 'futuristic').addTo(listEnvironments)
    ld('ESS Conquistador, Interstellar Space, 2330', 'futuristic').addTo(listEnvironments)
    ld('Last Hope Outpost, Alpha Centaura-3, 2440', 'futuristic').addTo(listEnvironments)
    ld('Waterdeep, The Sword Coast, Faerûn', 'fantasy').addTo(listEnvironments)
    ld('The Shire, Middle Earth', 'fantasy').addTo(listEnvironments)
    ld('Mithranous, Tevinter Imperium, Thedas', 'fantasy').addTo(listEnvironments)
    ld('Beauclair, Toussaint', 'fantasy').addTo(listEnvironments)
    ld('trans man', 'trans_men').addTo(listCharacterTypes)
    ld('trans woman', 'trans_women').addTo(listCharacterTypes)
    ld('cis woman', 'cis_women').addTo(listCharacterTypes)
    ld('cis man', 'cis_men').addTo(listCharacterTypes)
    ld('enby', 'nonbinary').addTo(listCharacterTypes)
    ld('futanari', 'futanari').addTo(listCharacterTypes)
    ld('an anthro cat', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro tiger', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro dog', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro wolf', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro fox', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro bear', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro mouse', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro rabbit', 'mammals').addTo(listCharacterSpecies)
    ld('an anthro snake', 'reptiles').addTo(listCharacterSpecies)
    ld('an anthro lizard', 'reptiles').addTo(listCharacterSpecies)
    ld('an anthro dragon', 'reptiles').addTo(listCharacterSpecies)
    ld('an anthro fish', 'fish').addTo(listCharacterSpecies)
    ld('an anthro shark', 'fish').addTo(listCharacterSpecies)
    ld('an anthro octopus', 'fish').addTo(listCharacterSpecies)
    ld('an anthro squid', 'fish').addTo(listCharacterSpecies)
    ld('an anthro ant', 'insects').addTo(listCharacterSpecies)
    ld('an anthro wasp', 'insects').addTo(listCharacterSpecies)
    ld('an anthro bee', 'insects').addTo(listCharacterSpecies)
    ld('an anthro mantis', 'insects').addTo(listCharacterSpecies)
    ld('an anthro spider', 'arachnids').addTo(listCharacterSpecies)
    ld('an anthro scorpion', 'arachnids').addTo(listCharacterSpecies)
    ld('a human', 'humans').addTo(listCharacterSpecies)
    ld('a half-elf', 'elves').addTo(listCharacterSpecies)
    ld('a high elf', 'elves').addTo(listCharacterSpecies)
    ld('a wood elf', 'elves').addTo(listCharacterSpecies)
    ld('a drow', 'elves').addTo(listCharacterSpecies)
    ld('a hill dwarf', 'dwarves').addTo(listCharacterSpecies)
    ld('a mountain dwarf', 'dwarves').addTo(listCharacterSpecies)
    ld('a deep dwarf', 'dwarves').addTo(listCharacterSpecies)
    ld('a lightfoot halfling', 'halflings').addTo(listCharacterSpecies)
    ld('a stout halfling', 'halflings').addTo(listCharacterSpecies)
    ld('a gnome', 'gnomes').addTo(listCharacterSpecies)
    ld('a deep gnome', 'gnomes').addTo(listCharacterSpecies)
    ld('a demon-blooded tiefling', 'tieflings').addTo(listCharacterSpecies)
    ld('a devil-blooded tiefling', 'tieflings').addTo(listCharacterSpecies)
    ld('a fae-blooded tiefling', 'tieflings').addTo(listCharacterSpecies)
    ld('a dragon-blooded tiefling', 'tieflings').addTo(listCharacterSpecies)
    ld('an eldritch-blooded tiefling', 'tieflings').addTo(listCharacterSpecies)
    ld('a merfolk', 'merfolk').addTo(listCharacterSpecies)
    ld('an orc', 'orcs').addTo(listCharacterSpecies)
    ld('a half-orc', 'orcs').addTo(listCharacterSpecies)
    ld('a half-giant', 'goliaths').addTo(listCharacterSpecies)
    ld('a goblin', 'goblinoids').addTo(listCharacterSpecies)
    ld('a hobgoblin', 'goblinoids').addTo(listCharacterSpecies)
    ld('a bugbear', 'goblinoids').addTo(listCharacterSpecies)
    ld('a mind flayer', 'ilithids').addTo(listCharacterSpecies)
    ld('a slime', 'slimes').addTo(listCharacterSpecies)
    ld('an ooze', 'slimes').addTo(listCharacterSpecies)
    ld('a jelly', 'slimes').addTo(listCharacterSpecies)
    ld('a tentacle monster', 'tentacles').addTo(listCharacterSpecies)
    ld('a tentacle-sprouting', 'tentacles').addTo(listCharacterSpecies)
    ld('a forest dryad', 'dryads').addTo(listCharacterSpecies)
    ld('a wood nymph', 'dryads').addTo(listCharacterSpecies)
    ld('a vine-sprouting dryad', 'dryads').addTo(listCharacterSpecies)
    ld('a harpy', 'harpies').addTo(listCharacterSpecies)
    ld('a lamia', 'lamia').addTo(listCharacterSpecies)
    ld('a centaur', 'centaurs').addTo(listCharacterSpecies)
    ld('a minotaur', 'minotaurs').addTo(listCharacterSpecies)
    ld('a hill giant', 'giants').addTo(listCharacterSpecies)
    ld('a frost giant', 'giants').addTo(listCharacterSpecies)
    ld('a fire giant', 'giants').addTo(listCharacterSpecies)
    ld('a troll', 'giants').addTo(listCharacterSpecies)
    ld('an ogre', 'giants').addTo(listCharacterSpecies)
    ld('a werewolf', 'werebeasts').addTo(listCharacterSpecies)
    ld('a weretiger', 'werebeasts').addTo(listCharacterSpecies)
    ld('a werebear', 'werebeasts').addTo(listCharacterSpecies)
    ld('a wereshark', 'werebeasts').addTo(listCharacterSpecies)
    ld('a fledgling vampire', 'vampires').addTo(listCharacterSpecies)
    ld('a vampire', 'vampires').addTo(listCharacterSpecies)
    ld('an elder vampire', 'vampires').addTo(listCharacterSpecies)
    ld('a zombie', 'undead').addTo(listCharacterSpecies)
    ld('a lich', 'undead').addTo(listCharacterSpecies)
    ld('a mummy', 'undead').addTo(listCharacterSpecies)
    ld('a ghost', 'undead').addTo(listCharacterSpecies)
    ld('a half-demon', 'demons').addTo(listCharacterSpecies)
    ld('a demon', 'demons').addTo(listCharacterSpecies)
    ld('a devil', 'demons').addTo(listCharacterSpecies)
    ld('an archdemon', 'demons').addTo(listCharacterSpecies)
    ld('a succubus', 'demons').addTo(listCharacterSpecies)
    ld('an incubus', 'demons').addTo(listCharacterSpecies)
    ld('an angel', 'angels').addTo(listCharacterSpecies)
    ld('an archangel', 'angels').addTo(listCharacterSpecies)
    ld('a cherubim', 'angels').addTo(listCharacterSpecies)
    ld('a seraphim', 'angels').addTo(listCharacterSpecies)
    ld('a sprite', 'faeries').addTo(listCharacterSpecies)
    ld('a fairy', 'faeries').addTo(listCharacterSpecies)
    ld('a changeling', 'faeries').addTo(listCharacterSpecies)
    ld('a half-fae', 'faeries').addTo(listCharacterSpecies)
    ld('a fae', 'faeries').addTo(listCharacterSpecies)
    ld('a archfae', 'faeries').addTo(listCharacterSpecies)
    ld('a cyborg', 'cyborgs').addTo(listCharacterSpecies)
    ld('a heavily implanted', 'cyborgs').addTo(listCharacterSpecies)
    ld('a metal-armed', 'cyborgs').addTo(listCharacterSpecies)
    ld('a metal-legged', 'cyborgs').addTo(listCharacterSpecies)
    ld('a synthetic', 'androids').addTo(listCharacterSpecies)
    ld('an android', 'androids').addTo(listCharacterSpecies)
    ld('a covert android', 'androids').addTo(listCharacterSpecies)
    ld('a military android', 'androids').addTo(listCharacterSpecies)
    ld('a robotic', 'robots').addTo(listCharacterSpecies)
    ld('a robot', 'robots').addTo(listCharacterSpecies)
    ld('a many-limbed robotic', 'robots').addTo(listCharacterSpecies)
    ld('a vehicular robot', 'robots').addTo(listCharacterSpecies)
    ld('a blue psychic alien', 'humanoid_aliens').addTo(listCharacterSpecies)
    ld('a bulky warlike alien', 'humanoid_aliens').addTo(listCharacterSpecies)
    ld('a tall aquiline alien', 'humanoid_aliens').addTo(listCharacterSpecies)
    ld('a short furred alien', 'humanoid_aliens').addTo(listCharacterSpecies)
    ld('an incorporeal alien', 'aliens').addTo(listCharacterSpecies)
    ld('a bestial alien', 'aliens').addTo(listCharacterSpecies)
    ld('a many-appendaged alien', 'aliens').addTo(listCharacterSpecies)
    ld('a multiple-bodied alien', 'aliens').addTo(listCharacterSpecies)
    ld('cthonic ritual, Altar to the Deep Ones', 'fantasy').addTo(listScenes)
    ld('demonic binding, Coven of the Seven', 'fantasy').addTo(listScenes)
    ld('Little Shoppe of Tentacles, Night Market', 'fantasy', 'modern').addTo(listScenes)
    ld('tea service, Café Neko Neko', 'modern').addTo(listScenes)
    ld('morning coffee, Sablestone Coffee', 'modern').addTo(listScenes)
    ld('romantic dinner, Cosa Fiorenta', 'modern').addTo(listScenes)
    ld('drinks with friends, Club Ziggurat', 'modern').addTo(listScenes)
    ld('doomsday lockdown, PrepTech Luxury Vault 404', 'futuristic').addTo(listScenes)
    ld('gladitorial games, BloodRage Cyber Arena', 'futuristic').addTo(listScenes)
    ld('stuck in aerial traffic, Clydesdale HoverLimo', 'futuristic').addTo(listScenes)
    ld('ripperdoc clinic, Kotari Void-Market', 'futuristic').addTo(listScenes)
    ld('partaking of emotion-vapor, Neon Death Snail Vape Bar, Pleasuretown', 'futuristic').addTo(listScenes)
    ld('shuttle malfunction, TeslaShuttle T-72', 'futuristic').addTo(listScenes)
    ld('regional lockdown, Invasion of Unkonwn Extraterestrials', 'futuristic').addTo(listScenes)
    ld('celebration of the Moon Godess, forest clearing', 'fantasy', 'historical').addTo(listScenes)
    ld('practical eromancy class, Universitas Arcanorum', 'fantasy', 'modern').addTo(listScenes)
    ld('lecture on defense against demonic temptation, Sanctum of Gilded Light', 'fantasy', 'historical').addTo(listScenes)
    ld('Comparative Sexuality SEX:2369, Wellspray College', 'college').addTo(listScenes)
    ld('office hours, Dyne Hall for Applied Chemistry, Wellspray College', 'college').addTo(listScenes)
    ld('wild party, ABO House, Hedera University', 'modern').addTo(listScenes)
    ld('dorm move-in day, Reed Hall, Hedera University', 'modern').addTo(listScenes)
    ld('harvest festival, Honeydrop Farm', 'historical').addTo(listScenes)
    ld('strangers visiting a farmhouse, Honeydrop Farm', 'historical').addTo(listScenes)
    ld('wagon broken down, Unnamed Town', 'historical').addTo(listScenes)
    ld('visitors arriving after dark, Unnamed Town', 'historical').addTo(listScenes)
    ld('city under siege, Devilspawn Invasion', 'historical', 'fantasy').addTo(listScenes)
    ld('dark alley, Tavern District', 'historical').addTo(listScenes)
    ld('conscripted into militia, Ironspike Garrison', 'historical').addTo(listScenes)
    ld('summoned for royal feast, Grand Hall, Ebongold Palace', 'historical').addTo(listScenes)
    playList = ['cuddling', 'petting', 'grinding', 'titjobs', 'ass_play', 'anal_sex', 'manual_sex', 'oral_sex', 'intercrural_sex', 'penetrative_sex', 'age_play', 'bondage', 'biting', 'breast_play', 'orgasm_control', 'genitorture', 'cuckoldry', 'cupping', 'dom_and_sub', 'knife_play', 'electro_play', 'food_play', 'temperature_play', 'fire_play', 'fisting', 'foot_play', 'degradation', 'exhibition', 'pet_play', 'piss_play', 'consensual_nonconsent', 'sensory_deprivation', 'sounding', 'intoxicants', 'incest', 'bestiality', 'size_play', 'partial_growth', 'extreme_insertions', 'inflation', 'transformation', 'impregnation', 'oviposition', 'dubious_consent', 'nonconsent', 'torture', 'gore', 'soft_vore', 'hard_vore', 'snuff', 'necrophilia']
    for pl in playList:
        ld(f'{pl.replace("_", " ")}', pl).addTo(listPlay)
    ld('handholding', 'romance').addTo(listPlay)
    ld('a romantic date', 'romance').addTo(listPlay)
    ld('soul staring', 'romance').addTo(listPlay)
    ld('heartfelt confessions', 'romance').addTo(listPlay)
    ld('kissing on the lips', 'kissing').addTo(listPlay)
    ld('neck kissing', 'kissing').addTo(listPlay)
    ld('hickies', 'kissing').addTo(listPlay)
    ld('ear nibbling', 'kissing').addTo(listPlay)
    ld('trailing kisses', 'kissing').addTo(listPlay)
    ld('spanking', 'impact_play').addTo(listPlay)
    ld('slapping', 'impact_play').addTo(listPlay)
    ld('whipping', 'impact_play').addTo(listPlay)
    ld('flogging', 'impact_play').addTo(listPlay)
    ld('paddeling', 'impact_play').addTo(listPlay)
    ld('caning', 'impact_play').addTo(listPlay)
    ld('dildos', 'basic_toys').addTo(listPlay)
    ld('vibrators', 'basic_toys').addTo(listPlay)
    ld('hitachi', 'basic_toys').addTo(listPlay)
    ld('fleshlights', 'basic_toys').addTo(listPlay)

def getConfig(guildID, channelID, configName):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    try:
        if f'{channelID}' in config.sections():
            if configName in config[f'{channelID}']:
                return config[f'{channelID}'][configName]
            else:
                return config['default'][configName]
        else: 
            return config['default'][configName]
    except:
        return None

def getConfigInt(guildID, channelID, configName):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    if f'{channelID}' in config.sections():
        if configName in config[f'{channelID}']:
            return config[f'{channelID}'].getint(configName)
        else:
            return config['default'].getint(configName)
    else: 
        return config['default'].getint(configName)

def getConfigBool(guildID, channelID, configName):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    if f'{channelID}' in config.sections():
        if configName in config[f'{channelID}']:
            return config[f'{channelID}'].getboolean(configName)
        else:
            return config['default'].getboolean(configName) 
    else: 
        return config['default'].getboolean(configName)

def getConfigDM(userID, configName):
    if f"{userID}" in DMConfig:
        if configName in DMConfig[f"{userID}"]:
            return DMConfig[f"{userID}"][configName]
        else:
            return DMConfigDefault[configName]
    else:
        return DMConfigDefault[configName]

def getConfigDisplay(guildID, channelID, configName):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    try:
        if f'{channelID}' in config.sections():
            if configName in config[f'{channelID}']:
                return [config[f'{channelID}'][configName], False]
            else:
                return [config['default'][configName], True]
        else: 
            return [config['default'][configName], True]
    except:
        return None

def getConfigDMDisplay(userID, configName):
    if f"{userID}" in DMConfig:
        if configName in DMConfig[f"{userID}"]:
            return [DMConfig[f"{userID}"][configName], False]
        else:
            return [DMConfigDefault[configName], True]
    else:
        return [DMConfigDefault[configName], True]

def addConfig(guildID, channelID, configName, configValue):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    if f'{channelID}' not in config.sections():
        config.add_section(f'{channelID}')
    config.set(f'{channelID}', f'{configName}', f'{configValue}')
    with open(configPath, 'w') as configfile:
        config.write(configfile)

def addReactable(messageID):
    with open("reactables.txt", "a") as f:
        f.write(f" {messageID}")

def removeReactable(messageID):
    with open("reactables.txt", "r") as f:
        reactables = f.read()
    reactables.replace(f" {messageID}", "")
    with open("reactables.txt", "w") as f:
        f.write(reactables)

def getReactables():
    with open("reactables.txt", "r") as f:
        reactables = f.read().split()
        return [int(id) for id in reactables]

def contributorsConfig(guildID, channelID):
    contributors["postMode"] = {}
    contributors[f"{guildID}"][f"{channelID}"] = {}
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    conChannel["pool"] = []
    conChannel["kicked"] = []
    conChannel["posts"] = []
    conChannel["turn"] = 0
    conChannel["promptStarted"] = False
    conChannel["multipost"] = False
    conChannel["timer"] = 0
    conChannel["context"] = ["I couldn't find any previous posts for this prompt :(", None, None]
    conChannel["paused"] = False

def promptGenerator(guildID, channelID, userID, addText):
    americaNames = {}
    japanNames = {}
    europeNames = {}
    fantasyNames = {}
    futuristicNames = {}
    americaNames["masc"] = ['Liam', 'Noah', 'Oliver', 'Elijah', 'William', 'James', 'Benjamin', 'Lucas', 'Henry', 'Alexander', 'Mason', 'Michael', 'Ethan', 'Daniel', 'Jacob', 'Logan', 'Jackson', 'Levi', 'Sebastian', 'Mateo', 'Jack', 'Owen', 'Theodore', 'Aiden', 'Samuel', 'Joseph', 'John', 'David', 'Wyatt', 'Matthew', 'Luke', 'Asher', 'Carter', 'Julian', 'Grayson', 'Leo', 'Jayden', 'Gabriel', 'Isaac', 'Lincoln', 'Anthony', 'Hudson', 'Dylan', 'Ezra', 'Thomas', 'Charles', 'Christopher', 'Jaxon', 'Maverick', 'Josiah', 'Isaiah', 'Andrew', 'Elias', 'Joshua', 'Nathan', 'Caleb', 'Ryan', 'Adrian', 'Miles', 'Eli', 'Nolan', 'Christian', 'Aaron', 'Cameron', 'Ezekiel', 'Colton', 'Luca', 'Landon', 'Hunter', 'Jonathan', 'Santiago', 'Axel', 'Easton', 'Cooper', 'Jeremiah', 'Angel', 'Roman', 'Connor', 'Jameson', 'Robert', 'Greyson', 'Jordan', 'Ian', 'Carson', 'Jaxson', 'Leonardo', 'Nicholas', 'Dominic', 'Austin', 'Everett', 'Brooks', 'Xavier', 'Kai', 'Jose', 'Parker', 'Adam', 'Jace', 'Wesley', 'Kayden', 'Silas', 'Bennett', 'Declan', 'Waylon', 'Weston', 'Evan', 'Emmett', 'Micah', 'Ryder', 'Beau', 'Damian', 'Brayden', 'Gael', 'Rowan', 'Harrison', 'Bryson', 'Sawyer', 'Amir', 'Kingston', 'Jason', 'Giovanni', 'Vincent', 'Ayden', 'Chase', 'Myles', 'Diego', 'Nathaniel', 'Legend', 'Jonah', 'River', 'Tyler', 'Cole', 'Braxton', 'George', 'Milo', 'Zachary', 'Ashton', 'Luis', 'Jasper', 'Kaiden', 'Adriel', 'Gavin', 'Bentley', 'Calvin', 'Zion', 'Juan', 'Maxwell', 'Max', 'Ryker', 'Carlos', 'Emmanuel', 'Jayce', 'Lorenzo', 'Ivan', 'Jude', 'August', 'Kevin', 'Malachi', 'Elliott', 'Rhett', 'Archer', 'Karter', 'Arthur', 'Luka', 'Elliot', 'Thiago', 'Brandon', 'Camden', 'Justin', 'Jesus', 'Maddox', 'King', 'Theo', 'Enzo', 'Matteo', 'Emiliano', 'Dean', 'Hayden', 'Finn', 'Brody', 'Antonio', 'Abel', 'Alex', 'Tristan', 'Graham', 'Zayden', 'Judah', 'Xander', 'Miguel', 'Atlas', 'Messiah', 'Barrett', 'Tucker', 'Timothy', 'Alan', 'Edward', 'Leon', 'Dawson', 'Eric', 'Ace', 'Victor', 'Abraham', 'Nicolas', 'Jesse', 'Charlie', 'Patrick', 'Walker', 'Joel', 'Richard', 'Beckett', 'Blake', 'Alejandro', 'Avery', 'Grant', 'Peter', 'Oscar', 'Matias', 'Amari', 'Lukas', 'Andres', 'Arlo', 'Colt', 'Adonis', 'Kyrie', 'Steven', 'Felix', 'Preston', 'Marcus', 'Holden', 'Emilio', 'Remington', 'Jeremy', 'Kaleb', 'Brantley', 'Bryce', 'Mark', 'Knox', 'Israel', 'Phoenix', 'Kobe', 'Nash', 'Griffin', 'Caden', 'Kenneth', 'Kyler', 'Hayes', 'Jax', 'Rafael', 'Beckham', 'Javier', 'Maximus', 'Simon', 'Paul', 'Omar', 'Kaden', 'Kash', 'Lane', 'Bryan', 'Riley', 'Zane', 'Louis', 'Aidan', 'Paxton', 'Maximiliano', 'Karson', 'Cash', 'Cayden', 'Emerson', 'Tobias', 'Ronan', 'Brian', 'Dallas', 'Bradley', 'Jorge', 'Walter', 'Josue', 'Khalil', 'Damien', 'Jett', 'Kairo', 'Zander', 'Andre', 'Cohen', 'Crew', 'Hendrix', 'Colin', 'Chance', 'Malakai', 'Clayton', 'Daxton', 'Malcolm', 'Lennox', 'Martin', 'Jaden', 'Kayson', 'Bodhi', 'Francisco', 'Cody', 'Erick', 'Kameron', 'Atticus', 'Dante', 'Jensen', 'Cruz', 'Finley', 'Brady', 'Joaquin', 'Anderson', 'Gunner', 'Muhammad', 'Zayn', 'Derek', 'Raymond', 'Kyle', 'Angelo', 'Reid', 'Spencer', 'Nico', 'Jaylen', 'Jake', 'Prince', 'Manuel', 'Ali', 'Gideon', 'Stephen', 'Ellis', 'Orion', 'Rylan', 'Eduardo', 'Mario', 'Rory', 'Cristian', 'Odin', 'Tanner', 'Julius', 'Callum', 'Sean', 'Kane', 'Ricardo', 'Travis', 'Wade', 'Warren', 'Fernando', 'Titus', 'Leonel', 'Edwin', 'Cairo', 'Corbin', 'Dakota', 'Ismael', 'Colson', 'Killian', 'Major', 'Tate', 'Gianni', 'Elian', 'Remy', 'Lawson', 'Niko', 'Nasir', 'Kade', 'Armani', 'Ezequiel', 'Marshall', 'Hector', 'Desmond', 'Kason', 'Garrett', 'Jared', 'Cyrus', 'Russell', 'Cesar', 'Tyson', 'Malik', 'Donovan', 'Jaxton', 'Cade', 'Romeo', 'Nehemiah', 'Sergio', 'Iker', 'Caiden', 'Jay', 'Pablo', 'Devin', 'Jeffrey', 'Otto', 'Kamari', 'Ronin', 'Johnny', 'Clark', 'Ari', 'Marco', 'Edgar', 'Bowen', 'Jaiden', 'Grady', 'Zayne', 'Sullivan', 'Jayceon', 'Sterling', 'Andy', 'Conor', 'Raiden', 'Royal', 'Royce', 'Solomon', 'Trevor', 'Winston', 'Emanuel', 'Finnegan', 'Pedro', 'Luciano', 'Harvey', 'Franklin', 'Noel', 'Troy', 'Princeton', 'Johnathan', 'Erik', 'Fabian', 'Oakley', 'Rhys', 'Porter', 'Hugo', 'Frank', 'Damon', 'Kendrick', 'Mathias', 'Milan', 'Peyton', 'Wilder', 'Callan', 'Gregory', 'Seth', 'Matthias', 'Briggs', 'Ibrahim', 'Roberto', 'Conner', 'Quinn', 'Kashton', 'Sage', 'Santino', 'Kolton', 'Alijah', 'Dominick', 'Zyaire', 'Apollo', 'Kylo', 'Reed', 'Philip', 'Kian', 'Shawn', 'Kaison', 'Leonidas', 'Ayaan', 'Lucca', 'Memphis', 'Ford', 'Baylor', 'Kyson', 'Uriel', 'Allen', 'Collin', 'Ruben', 'Archie', 'Dalton', 'Esteban', 'Adan', 'Forrest', 'Alonzo', 'Isaias', 'Leland', 'Jase', 'Dax', 'Kasen', 'Gage', 'Kamden', 'Marcos', 'Jamison', 'Francis', 'Hank', 'Alexis', 'Tripp', 'Frederick', 'Jonas', 'Stetson', 'Cassius', 'Izaiah', 'Eden', 'Maximilian', 'Rocco', 'Tatum', 'Keegan', 'Aziel', 'Moses', 'Bruce', 'Lewis', 'Braylen', 'Omari', 'Mack', 'Augustus', 'Enrique', 'Armando', 'Pierce', 'Moises', 'Asa', 'Shane', 'Emmitt', 'Soren', 'Dorian', 'Keanu', 'Zaiden', 'Raphael', 'Deacon', 'Abdiel', 'Kieran', 'Phillip', 'Ryland', 'Zachariah', 'Casey', 'Zaire', 'Albert', 'Baker', 'Corey', 'Kylan', 'Denver', 'Gunnar', 'Jayson', 'Drew', 'Callen', 'Jasiah', 'Drake', 'Kannon', 'Braylon', 'Sonny', 'Bo', 'Moshe', 'Huxley', 'Quentin', 'Rowen', 'Santana', 'Cannon', 'Kenzo', 'Wells', 'Julio', 'Nikolai', 'Conrad', 'Jalen', 'Makai', 'Benson', 'Derrick', 'Gerardo', 'Davis', 'Abram', 'Mohamed', 'Ronald', 'Raul', 'Arjun', 'Dexter', 'Kaysen', 'Jaime', 'Scott', 'Lawrence', 'Ariel', 'Skyler', 'Danny', 'Roland', 'Chandler', 'Yusuf', 'Samson', 'Case', 'Zain', 'Roy', 'Rodrigo', 'Sutton', 'Boone', 'Saint', 'Saul', 'Jaziel', 'Hezekiah', 'Alec', 'Arturo', 'Jamari', 'Jaxtyn', 'Julien', 'Koa', 'Reece', 'Landen', 'Koda', 'Darius', 'Sylas', 'Ares', 'Kyree', 'Boston', 'Keith', 'Taylor', 'Johan', 'Edison', 'Sincere', 'Watson', 'Jerry', 'Nikolas', 'Quincy', 'Shepherd', 'Brycen', 'Marvin', 'Dariel', 'Axton', 'Donald', 'Bodie', 'Finnley', 'Onyx', 'Rayan', 'Raylan', 'Brixton', 'Colby', 'Shiloh', 'Valentino', 'Layton', 'Trenton', 'Landyn', 'Alessandro', 'Ahmad', 'Gustavo', 'Ledger', 'Ridge', 'Ander', 'Ahmed', 'Kingsley', 'Issac', 'Mauricio', 'Tony', 'Leonard', 'Mohammed', 'Uriah', 'Duke', 'Kareem', 'Lucian', 'Marcelo', 'Aarav', 'Leandro', 'Reign', 'Clay', 'Kohen', 'Dennis', 'Samir', 'Ermias', 'Otis', 'Emir', 'Nixon', 'Ty', 'Sam', 'Fletcher', 'Wilson', 'Dustin', 'Hamza', 'Bryant', 'Flynn', 'Lionel', 'Mohammad', 'Cason', 'Jamir', 'Aden', 'Dakari', 'Justice', 'Dillon', 'Layne', 'Zaid', 'Alden', 'Nelson', 'Devon', 'Titan', 'Chris', 'Khari', 'Zeke', 'Noe', 'Alberto', 'Roger', 'Brock', 'Rex', 'Quinton', 'Alvin', 'Cullen', 'Azariah', 'Harlan', 'Kellan', 'Lennon', 'Marcel', 'Keaton', 'Morgan', 'Ricky', 'Trey', 'Karsyn', 'Langston', 'Miller', 'Chaim', 'Salvador', 'Amias', 'Tadeo', 'Curtis', 'Lachlan', 'Amos', 'Anakin', 'Krew', 'Tomas', 'Jefferson', 'Yosef', 'Bruno', 'Korbin', 'Augustine', 'Cayson', 'Mathew', 'Vihaan', 'Jamie', 'Clyde', 'Brendan', 'Jagger', 'Carmelo', 'Harry', 'Nathanael', 'Mitchell', 'Darren', 'Ray', 'Jedidiah', 'Jimmy', 'Lochlan', 'Bellamy', 'Eddie', 'Rayden', 'Reese', 'Stanley', 'Joe', 'Houston', 'Douglas', 'Vincenzo', 'Casen', 'Emery', 'Joziah', 'Leighton', 'Marcellus', 'Atreus', 'Aron', 'Hugh', 'Musa', 'Tommy', 'Alfredo', 'Junior', 'Neil', 'Westley', 'Banks', 'Eliel', 'Melvin', 'Maximo', 'Briar', 'Colten', 'Lance', 'Nova', 'Trace', 'Axl', 'Ramon', 'Vicente', 'Brennan', 'Caspian', 'Remi', 'Deandre', 'Legacy', 'Lee', 'Valentin', 'Ben', 'Louie', 'Westin', 'Wayne', 'Benicio', 'Grey', 'Zayd', 'Gatlin', 'Mekhi', 'Orlando', 'Bjorn', 'Harley', 'Alonso', 'Rio', 'Aldo', 'Byron', 'Eliseo', 'Ernesto', 'Talon', 'Thaddeus', 'Brecken', 'Kace', 'Kellen', 'Enoch', 'Kiaan', 'Lian', 'Creed', 'Rohan', 'Callahan', 'Jaxxon', 'Ocean', 'Crosby', 'Dash', 'Gary', 'Mylo', 'Ira', 'Magnus', 'Salem', 'Abdullah', 'Kye', 'Tru', 'Forest', 'Jon', 'Misael', 'Madden', 'Braden', 'Carl', 'Hassan', 'Emory', 'Kristian', 'Alaric', 'Ambrose', 'Dario', 'Allan', 'Bode', 'Boden', 'Juelz', 'Kristopher', 'Genesis', 'Idris', 'Ameer', 'Anders', 'Darian', 'Kase', 'Aryan', 'Dane', 'Guillermo', 'Elisha', 'Jakobe', 'Thatcher', 'Eugene', 'Ishaan', 'Larry', 'Wesson', 'Yehuda', 'Alvaro', 'Bobby', 'Bronson', 'Dilan', 'Kole', 'Kyro', 'Tristen', 'Blaze', 'Brayan', 'Jadiel', 'Kamryn', 'Demetrius', 'Maurice', 'Arian', 'Kabir', 'Rocky', 'Rudy', 'Randy', 'Rodney', 'Yousef', 'Felipe', 'Robin', 'Aydin', 'Dior', 'Kaiser', 'Van', 'Brodie', 'London', 'Eithan', 'Stefan', 'Ulises', 'Camilo', 'Branson', 'Jakari', 'Judson', 'Yahir', 'Zavier', 'Damari', 'Jakob', 'Jaxx', 'Bentlee', 'Cain', 'Niklaus', 'Rey', 'Zahir', 'Aries', 'Blaine', 'Kyng', 'Castiel', 'Henrik', 'Joey', 'Khalid', 'Bear', 'Graysen', 'Jair', 'Kylen', 'Darwin', 'Alfred', 'Ayan', 'Kenji', 'Zakai', 'Avi', 'Cory', 'Fisher', 'Jacoby', 'Osiris', 'Harlem', 'Jamal', 'Santos', 'Wallace', 'Brett', 'Fox', 'Leif', 'Maison', 'Reuben', 'Adler', 'Zev', 'Calum', 'Kelvin', 'Zechariah', 'Bridger', 'Mccoy', 'Seven', 'Shepard', 'Azrael', 'Leroy', 'Terry', 'Harold', 'Mac', 'Mordechai', 'Ahmir', 'Cal', 'Franco', 'Trent', 'Blaise', 'Coen', 'Dominik', 'Marley', 'Davion', 'Jeremias', 'Riggs', 'Jones', 'Will', 'Damir', 'Dangelo', 'Canaan', 'Dion', 'Jabari', 'Landry', 'Salvatore', 'Kody', 'Hakeem', 'Truett', 'Gerald', 'Lyric', 'Gordon', 'Jovanni', 'Kamdyn', 'Alistair', 'Cillian', 'Foster', 'Terrance', 'Murphy', 'Zyair', 'Cedric', 'Rome', 'Abner', 'Colter', 'Dayton', 'Jad', 'Xzavier', 'Rene', 'Vance', 'Duncan', 'Frankie', 'Bishop', 'Davian', 'Everest', 'Heath', 'Jaxen', 'Marlon', 'Maxton', 'Reginald', 'Harris', 'Jericho', 'Keenan', 'Korbyn', 'Wes', 'Eliezer', 'Jeffery', 'Kalel', 'Kylian', 'Turner', 'Willie', 'Rogelio', 'Ephraim']
    americaNames["fem"] = ['Olivia', 'Emma', 'Ava', 'Charlotte', 'Sophia', 'Amelia', 'Isabella', 'Mia', 'Evelyn', 'Harper', 'Camila', 'Gianna', 'Abigail', 'Luna', 'Ella', 'Elizabeth', 'Sofia', 'Emily', 'Avery', 'Mila', 'Scarlett', 'Eleanor', 'Madison', 'Layla', 'Penelope', 'Aria', 'Chloe', 'Grace', 'Ellie', 'Nora', 'Hazel', 'Zoey', 'Riley', 'Victoria', 'Lily', 'Aurora', 'Violet', 'Nova', 'Hannah', 'Emilia', 'Zoe', 'Stella', 'Everly', 'Isla', 'Leah', 'Lillian', 'Addison', 'Willow', 'Lucy', 'Paisley', 'Natalie', 'Naomi', 'Eliana', 'Brooklyn', 'Elena', 'Aubrey', 'Claire', 'Ivy', 'Kinsley', 'Audrey', 'Maya', 'Genesis', 'Skylar', 'Bella', 'Aaliyah', 'Madelyn', 'Savannah', 'Anna', 'Delilah', 'Serenity', 'Caroline', 'Kennedy', 'Valentina', 'Ruby', 'Sophie', 'Alice', 'Gabriella', 'Sadie', 'Ariana', 'Allison', 'Hailey', 'Autumn', 'Nevaeh', 'Natalia', 'Quinn', 'Josephine', 'Sarah', 'Cora', 'Emery', 'Samantha', 'Piper', 'Leilani', 'Eva', 'Everleigh', 'Madeline', 'Lydia', 'Jade', 'Peyton', 'Brielle', 'Adeline', 'Vivian', 'Rylee', 'Clara', 'Raelynn', 'Melanie', 'Melody', 'Julia', 'Athena', 'Maria', 'Liliana', 'Hadley', 'Arya', 'Rose', 'Reagan', 'Eliza', 'Adalynn', 'Kaylee', 'Lyla', 'Mackenzie', 'Alaia', 'Isabelle', 'Charlie', 'Arianna', 'Mary', 'Remi', 'Margaret', 'Iris', 'Parker', 'Ximena', 'Eden', 'Ayla', 'Kylie', 'Elliana', 'Josie', 'Katherine', 'Faith', 'Alexandra', 'Eloise', 'Adalyn', 'Amaya', 'Jasmine', 'Amara', 'Daisy', 'Reese', 'Valerie', 'Brianna', 'Cecilia', 'Andrea', 'Summer', 'Valeria', 'Norah', 'Ariella', 'Esther', 'Ashley', 'Emerson', 'Aubree', 'Isabel', 'Anastasia', 'Ryleigh', 'Khloe', 'Taylor', 'Londyn', 'Lucia', 'Emersyn', 'Callie', 'Sienna', 'Blakely', 'Kehlani', 'Genevieve', 'Alina', 'Bailey', 'Juniper', 'Maeve', 'Molly', 'Harmony', 'Georgia', 'Magnolia', 'Catalina', 'Freya', 'Juliette', 'Sloane', 'June', 'Sara', 'Ada', 'Kimberly', 'River', 'Ember', 'Juliana', 'Aliyah', 'Millie', 'Brynlee', 'Teagan', 'Morgan', 'Jordyn', 'London', 'Alaina', 'Olive', 'Rosalie', 'Alyssa', 'Ariel', 'Finley', 'Arabella', 'Journee', 'Hope', 'Leila', 'Alana', 'Gemma', 'Vanessa', 'Gracie', 'Noelle', 'Marley', 'Elise', 'Presley', 'Kamila', 'Zara', 'Amy', 'Kayla', 'Payton', 'Blake', 'Ruth', 'Alani', 'Annabelle', 'Sage', 'Aspen', 'Laila', 'Lila', 'Rachel', 'Trinity', 'Daniela', 'Alexa', 'Lilly', 'Lauren', 'Elsie', 'Margot', 'Adelyn', 'Zuri', 'Brooke', 'Sawyer', 'Lilah', 'Lola', 'Selena', 'Mya', 'Sydney', 'Diana', 'Ana', 'Vera', 'Alayna', 'Nyla', 'Elaina', 'Rebecca', 'Angela', 'Kali', 'Alivia', 'Raegan', 'Rowan', 'Phoebe', 'Camilla', 'Joanna', 'Malia', 'Vivienne', 'Dakota', 'Brooklynn', 'Evangeline', 'Camille', 'Jane', 'Nicole', 'Catherine', 'Jocelyn', 'Julianna', 'Lena', 'Lucille', 'Mckenna', 'Paige', 'Adelaide', 'Charlee', 'Mariana', 'Myla', 'Mckenzie', 'Tessa', 'Miriam', 'Oakley', 'Kailani', 'Alayah', 'Amira', 'Adaline', 'Phoenix', 'Milani', 'Annie', 'Lia', 'Angelina', 'Harley', 'Cali', 'Maggie', 'Hayden', 'Leia', 'Fiona', 'Briella', 'Journey', 'Lennon', 'Saylor', 'Jayla', 'Kaia', 'Thea', 'Adriana', 'Mariah', 'Juliet', 'Oaklynn', 'Kiara', 'Alexis', 'Haven', 'Aniyah', 'Delaney', 'Gracelynn', 'Kendall', 'Winter', 'Lilith', 'Logan', 'Amiyah', 'Evie', 'Alexandria', 'Gracelyn', 'Gabriela', 'Sutton', 'Harlow', 'Madilyn', 'Makayla', 'Evelynn', 'Gia', 'Nina', 'Amina', 'Giselle', 'Brynn', 'Blair', 'Amari', 'Octavia', 'Michelle', 'Talia', 'Demi', 'Alaya', 'Kaylani', 'Izabella', 'Fatima', 'Tatum', 'Makenzie', 'Lilliana', 'Arielle', 'Palmer', 'Melissa', 'Willa', 'Samara', 'Destiny', 'Dahlia', 'Celeste', 'Ainsley', 'Rylie', 'Reign', 'Laura', 'Adelynn', 'Gabrielle', 'Remington', 'Wren', 'Brinley', 'Amora', 'Lainey', 'Collins', 'Lexi', 'Aitana', 'Alessandra', 'Kenzie', 'Raelyn', 'Elle', 'Everlee', 'Haisley', 'Hallie', 'Wynter', 'Daleyza', 'Gwendolyn', 'Paislee', 'Ariyah', 'Veronica', 'Heidi', 'Anaya', 'Cataleya', 'Kira', 'Avianna', 'Felicity', 'Aylin', 'Miracle', 'Sabrina', 'Lana', 'Ophelia', 'Elianna', 'Royalty', 'Madeleine', 'Esmeralda', 'Joy', 'Kalani', 'Esme', 'Jessica', 'Leighton', 'Ariah', 'Makenna', 'Nylah', 'Viviana', 'Camryn', 'Cassidy', 'Dream', 'Luciana', 'Maisie', 'Stevie', 'Kate', 'Lyric', 'Daniella', 'Alicia', 'Daphne', 'Frances', 'Charli', 'Raven', 'Paris', 'Nayeli', 'Serena', 'Heaven', 'Bianca', 'Helen', 'Hattie', 'Averie', 'Mabel', 'Selah', 'Allie', 'Marlee', 'Kinley', 'Regina', 'Carmen', 'Jennifer', 'Jordan', 'Alison', 'Stephanie', 'Maren', 'Kayleigh', 'Angel', 'Annalise', 'Jacqueline', 'Braelynn', 'Emory', 'Rosemary', 'Scarlet', 'Amanda', 'Danielle', 'Emelia', 'Ryan', 'Carolina', 'Astrid', 'Kensley', 'Shiloh', 'Maci', 'Francesca', 'Rory', 'Celine', 'Kamryn', 'Zariah', 'Liana', 'Poppy', 'Maliyah', 'Keira', 'Skyler', 'Noa', 'Skye', 'Nadia', 'Addilyn', 'Rosie', 'Eve', 'Sarai', 'Edith', 'Jolene', 'Maddison', 'Meadow', 'Charleigh', 'Matilda', 'Elliott', 'Madelynn', 'Holly', 'Leona', 'Azalea', 'Katie', 'Mira', 'Ari', 'Kaitlyn', 'Danna', 'Cameron', 'Kyla', 'Bristol', 'Kora', 'Armani', 'Nia', 'Malani', 'Dylan', 'Remy', 'Maia', 'Dior', 'Legacy', 'Alessia', 'Shelby', 'Maryam', 'Sylvia', 'Yaretzi', 'Lorelei', 'Madilynn', 'Abby', 'Helena', 'Jimena', 'Elisa', 'Renata', 'Amber', 'Aviana', 'Carter', 'Emmy', 'Haley', 'Alondra', 'Elaine', 'Erin', 'April', 'Emely', 'Imani', 'Kennedi', 'Lorelai', 'Hanna', 'Kelsey', 'Aurelia', 'Colette', 'Jaliyah', 'Kylee', 'Macie', 'Aisha', 'Dorothy', 'Charley', 'Kathryn', 'Adelina', 'Adley', 'Monroe', 'Sierra', 'Ailani', 'Miranda', 'Mikayla', 'Alejandra', 'Amirah', 'Jada', 'Jazlyn', 'Jenna', 'Jayleen', 'Beatrice', 'Kendra', 'Lyra', 'Nola', 'Emberly', 'Mckinley', 'Myra', 'Katalina', 'Antonella', 'Zelda', 'Alanna', 'Amaia', 'Priscilla', 'Briar', 'Kaliyah', 'Itzel', 'Oaklyn', 'Alma', 'Mallory', 'Novah', 'Amalia', 'Fernanda', 'Alia', 'Angelica', 'Elliot', 'Justice', 'Mae', 'Cecelia', 'Gloria', 'Ariya', 'Virginia', 'Cheyenne', 'Aleah', 'Jemma', 'Henley', 'Meredith', 'Leyla', 'Lennox', 'Ensley', 'Zahra', 'Reina', 'Frankie', 'Lylah', 'Nalani', 'Reyna', 'Saige', 'Ivanna', 'Aleena', 'Emerie', 'Ivory', 'Leslie', 'Alora', 'Ashlyn', 'Bethany', 'Bonnie', 'Sasha', 'Xiomara', 'Salem', 'Adrianna', 'Dayana', 'Clementine', 'Karina', 'Karsyn', 'Emmie', 'Julie', 'Julieta', 'Briana', 'Carly', 'Macy', 'Marie', 'Oaklee', 'Christina', 'Malaysia', 'Ellis', 'Irene', 'Anne', 'Anahi', 'Mara', 'Rhea', 'Davina', 'Dallas', 'Jayda', 'Mariam', 'Skyla', 'Siena', 'Elora', 'Marilyn', 'Jazmin', 'Megan', 'Rosa', 'Savanna', 'Allyson', 'Milan', 'Coraline', 'Johanna', 'Melany', 'Chelsea', 'Michaela', 'Melina', 'Angie', 'Cassandra', 'Yara', 'Kassidy', 'Liberty', 'Lilian', 'Avah', 'Anya', 'Laney', 'Navy', 'Opal', 'Amani', 'Zaylee', 'Mina', 'Sloan', 'Romina', 'Ashlynn', 'Aliza', 'Liv', 'Malaya', 'Blaire', 'Janelle', 'Kara', 'Analia', 'Hadassah', 'Hayley', 'Karla', 'Chaya', 'Cadence', 'Kyra', 'Alena', 'Ellianna', 'Katelyn', 'Kimber', 'Laurel', 'Lina', 'Capri', 'Braelyn', 'Faye', 'Kamiyah', 'Kenna', 'Louise', 'Calliope', 'Kaydence', 'Nala', 'Tiana', 'Aileen', 'Sunny', 'Zariyah', 'Milana', 'Giuliana', 'Eileen', 'Elodie', 'Rayna', 'Monica', 'Galilea', 'Journi', 'Lara', 'Marina', 'Aliana', 'Harmoni', 'Jamie', 'Holland', 'Emmalyn', 'Lauryn', 'Chanel', 'Tinsley', 'Jessie', 'Lacey', 'Elyse', 'Janiyah', 'Jolie', 'Ezra', 'Marleigh', 'Roselyn', 'Lillie', 'Louisa', 'Madisyn', 'Penny', 'Kinslee', 'Treasure', 'Zaniyah', 'Estella', 'Jaylah', 'Khaleesi', 'Alexia', 'Dulce', 'Indie', 'Maxine', 'Waverly', 'Giovanna', 'Miley', 'Saoirse', 'Estrella', 'Greta', 'Rosalia', 'Mylah', 'Teresa', 'Bridget', 'Kelly', 'Adalee', 'Aubrie', 'Lea', 'Harlee', 'Anika', 'Itzayana', 'Hana', 'Kaisley', 'Mikaela', 'Naya', 'Avalynn', 'Margo', 'Sevyn', 'Florence', 'Keilani', 'Lyanna', 'Joelle', 'Kataleya', 'Royal', 'Averi', 'Kallie', 'Winnie', 'Baylee', 'Martha', 'Pearl', 'Alaiya', 'Rayne', 'Sylvie', 'Brylee', 'Jazmine', 'Ryann', 'Kori', 'Noemi', 'Haylee', 'Julissa', 'Celia', 'Laylah', 'Rebekah', 'Rosalee', 'Aya', 'Bria', 'Adele', 'Aubrielle', 'Tiffany', 'Addyson', 'Kai', 'Bellamy', 'Leilany', 'Princess', 'Chana', 'Estelle', 'Selene', 'Sky', 'Dani', 'Thalia', 'Ellen', 'Rivka', 'Amelie', 'Andi', 'Kynlee', 'Raina', 'Vienna', 'Alianna', 'Livia', 'Madalyn', 'Mercy', 'Novalee', 'Ramona', 'Vada', 'Berkley', 'Gwen', 'Persephone', 'Milena', 'Paula', 'Clare', 'Kairi', 'Linda', 'Paulina', 'Kamilah', 'Amoura', 'Hunter', 'Isabela', 'Karen', 'Marianna', 'Sariyah', 'Theodora', 'Annika', 'Kyleigh', 'Nellie', 'Scarlette', 'Keyla', 'Kailey', 'Mavis', 'Lilianna', 'Rosalyn', 'Sariah', 'Tori', 'Yareli', 'Aubriella', 'Bexley', 'Bailee', 'Jianna', 'Keily', 'Annabella', 'Azariah', 'Denisse', 'Promise', 'August', 'Hadlee', 'Halle', 'Fallon', 'Oakleigh', 'Zaria', 'Jaylin', 'Paisleigh', 'Crystal', 'Ila', 'Aliya', 'Cynthia', 'Giana', 'Maleah', 'Rylan', 'Aniya', 'Denise', 'Emmeline', 'Scout', 'Simone', 'Noah', 'Zora', 'Meghan', 'Landry', 'Ainhoa', 'Lilyana', 'Noor', 'Belen', 'Brynleigh', 'Cleo', 'Meilani', 'Karter', 'Amaris', 'Frida', 'Iliana', 'Violeta', 'Addisyn', 'Nancy', 'Denver', 'Leanna', 'Braylee', 'Kiana', 'Wrenley', 'Barbara', 'Khalani', 'Aspyn', 'Ellison', 'Judith', 'Robin', 'Valery', 'Aila', 'Deborah', 'Cara', 'Clarissa', 'Iyla', 'Lexie', 'Anais', 'Kaylie', 'Nathalie', 'Alisson', 'Della', 'Addilynn', 'Elsa', 'Zoya', 'Layne', 'Marlowe', 'Jovie', 'Kenia', 'Samira', 'Jaylee', 'Jenesis', 'Etta', 'Shay', 'Amayah', 'Avayah', 'Egypt', 'Flora', 'Raquel', 'Whitney', 'Zola', 'Giavanna', 'Raya', 'Veda', 'Halo', 'Paloma', 'Nataly', 'Whitley', 'Dalary', 'Drew', 'Guadalupe', 'Kamari', 'Esperanza', 'Loretta', 'Malayah', 'Natasha', 'Stormi', 'Ansley', 'Carolyn', 'Corinne', 'Paola', 'Brittany', 'Emerald', 'Freyja', 'Zainab', 'Artemis', 'Jillian', 'Kimora', 'Zoie', 'Aislinn', 'Emmaline', 'Ayleen', 'Queen', 'Jaycee', 'Murphy', 'Nyomi', 'Elina', 'Hadleigh', 'Marceline', 'Marisol', 'Yasmin', 'Zendaya', 'Chandler', 'Emani', 'Jaelynn', 'Kaiya', 'Nathalia', 'Violette', 'Joyce', 'Paityn', 'Elisabeth', 'Emmalynn', 'Luella', 'Yamileth', 'Aarya', 'Luisa', 'Zhuri', 'Araceli', 'Harleigh', 'Madalynn', 'Melani', 'Laylani', 'Magdalena', 'Mazikeen', 'Belle', 'Kadence']
    americaNames["neut"] = ['Addison', 'Adrian', 'Archer', 'Arden', 'Arlo', 'Aubrey', 'Auden', 'Austin', 'Avery', 'Bailey', 'Baylor', 'Bellamy', 'Blakely', 'Bodhi', 'Carson', 'Cassidy', 'Cohen', 'Colby', 'Dakota', 'Dallas', 'Declan', 'Delaney', 'Drew', 'Dylan', 'Easton', 'Eden', 'Emery', 'Ellery', 'Elliot', 'Ellis', 'Ellison', 'Emerson', 'Emmett', 'Finley', 'Hadley', 'Harlow', 'Harper', 'Hartley', 'Haven', 'Hayden', 'Hunter', 'Jaden', 'James', 'Jude', 'Kaden', 'Kelsey', 'Kendall', 'Kennedy', 'Kenley', 'Landry', 'Lane', 'Leighton', 'Linden', 'Lennon', 'Lennox', 'Logan', 'Madison', 'Mallory', 'Marley', 'Marlow', 'Mason', 'Maxwell', 'Mercer', 'Morgan', 'Nico', 'Noah', 'Orion', 'Owen', 'Palmer', 'Parker', 'Payton', 'Piper', 'Presley', 'Quinn', 'Reagan', 'Reese', 'Reeve', 'Remy', 'Riley', 'River', 'Rory', 'Rowan', 'Rylan', 'Salem', 'Sasha', 'Sawyer', 'Saylor', 'Shea', 'Shelby', 'Sloane', 'Skylar', 'Spencer', 'Sterling', 'Tate', 'Vesper', 'Wilmer', 'Winter', 'Wyatt', 'Zaire', 'Zuri']
    americaNames["sur"] = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson', 'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes', 'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez', 'Powell', 'Jenkins', 'Perry', 'Russell', 'Sullivan', 'Bell', 'Coleman', 'Butler', 'Henderson', 'Barnes', 'Gonzales', 'Fisher', 'Vasquez', 'Simmons', 'Romero', 'Jordan', 'Patterson', 'Alexander', 'Hamilton', 'Graham', 'Reynolds', 'Griffin', 'Wallace', 'Moreno', 'West', 'Cole', 'Hayes', 'Bryant', 'Herrera', 'Gibson', 'Ellis', 'Tran', 'Medina', 'Aguilar', 'Stevens', 'Murray', 'Ford', 'Castro', 'Marshall', 'Owens', 'Harrison', 'Fernandez', 'Mcdonald', 'Woods', 'Washington', 'Kennedy', 'Wells', 'Vargas', 'Henry', 'Chen', 'Freeman', 'Webb', 'Tucker', 'Guzman', 'Burns', 'Crawford', 'Olson', 'Simpson', 'Porter', 'Hunter', 'Gordon', 'Mendez', 'Silva', 'Shaw', 'Snyder', 'Mason', 'Dixon', 'Munoz', 'Hunt', 'Hicks', 'Holmes', 'Palmer', 'Wagner', 'Black', 'Robertson', 'Boyd', 'Rose', 'Stone', 'Salazar', 'Fox', 'Warren', 'Mills', 'Meyer', 'Rice', 'Schmidt', 'Garza', 'Daniels', 'Ferguson', 'Nichols', 'Stephens', 'Soto', 'Weaver', 'Ryan', 'Gardner', 'Payne', 'Grant', 'Dunn', 'Kelley', 'Spencer', 'Hawkins', 'Arnold', 'Pierce', 'Vazquez', 'Hansen', 'Peters', 'Santos', 'Hart', 'Bradley', 'Knight', 'Elliott', 'Cunningham', 'Duncan', 'Armstrong', 'Hudson', 'Carroll', 'Lane', 'Riley', 'Andrews', 'Alvarado', 'Ray', 'Delgado', 'Berry', 'Perkins', 'Hoffman', 'Johnston', 'Matthews', 'Pena', 'Richards', 'Contreras', 'Willis', 'Carpenter', 'Lawrence', 'Sandoval', 'Guerrero', 'George', 'Chapman', 'Rios', 'Estrada', 'Ortega', 'Watkins', 'Greene', 'Nunez', 'Wheeler', 'Valdez', 'Harper', 'Burke', 'Larson', 'Santiago', 'Maldonado', 'Morrison', 'Franklin', 'Carlson', 'Austin', 'Dominguez', 'Carr', 'Lawson', 'Jacobs', 'Obrien', 'Lynch', 'Singh', 'Vega', 'Bishop', 'Montgomery', 'Oliver', 'Jensen', 'Harvey', 'Williamson', 'Gilbert', 'Dean', 'Sims', 'Espinoza', 'Howell', 'Li', 'Wong', 'Reid', 'Hanson', 'Le', 'Mccoy', 'Garrett', 'Burton', 'Fuller', 'Wang', 'Weber', 'Welch', 'Rojas', 'Lucas', 'Marquez', 'Fields', 'Park', 'Yang', 'Little', 'Banks', 'Padilla', 'Day', 'Walsh', 'Bowman', 'Schultz', 'Luna', 'Fowler', 'Mejia', 'Davidson', 'Acosta', 'Brewer', 'May', 'Holland', 'Juarez', 'Newman', 'Pearson', 'Curtis', 'Cortez', 'Douglas', 'Schneider', 'Joseph', 'Barrett', 'Navarro', 'Figueroa', 'Keller', 'Avila', 'Wade', 'Molina', 'Stanley', 'Hopkins', 'Campos', 'Barnett', 'Bates', 'Chambers', 'Caldwell', 'Beck', 'Lambert', 'Miranda', 'Byrd', 'Craig', 'Ayala', 'Lowe', 'Frazier', 'Powers', 'Neal', 'Leonard', 'Gregory', 'Carrillo', 'Sutton', 'Fleming', 'Rhodes', 'Shelton', 'Schwartz', 'Norris', 'Jennings', 'Watts', 'Duran', 'Walters', 'Cohen', 'Mcdaniel', 'Moran', 'Parks', 'Steele', 'Vaughn', 'Becker', 'Holt', 'Deleon', 'Barker', 'Terry', 'Hale', 'Leon', 'Hail', 'Benson', 'Haynes', 'Horton', 'Miles', 'Lyons', 'Pham', 'Graves', 'Bush', 'Thornton', 'Wolfe', 'Warner', 'Cabrera', 'Mckinney', 'Mann', 'Zimmerman', 'Dawson', 'Lara', 'Fletcher', 'Page', 'Mccarthy', 'Love', 'Robles', 'Cervantes', 'Solis', 'Erickson', 'Reeves', 'Chang', 'Klein', 'Salinas', 'Fuentes', 'Baldwin', 'Daniel', 'Simon', 'Velasquez', 'Hardy', 'Higgins', 'Aguirre', 'Lin', 'Cummings', 'Chandler', 'Sharp', 'Barber', 'Bowen', 'Ochoa', 'Dennis', 'Robbins', 'Liu', 'Ramsey', 'Francis', 'Griffith', 'Paul', 'Blair', 'Oconnor', 'Cardenas', 'Pacheco', 'Cross', 'Calderon', 'Quinn', 'Moss', 'Swanson', 'Chan', 'Rivas', 'Khan', 'Rodgers', 'Serrano', 'Fitzgerald', 'Rosales', 'Stevenson', 'Christensen', 'Manning', 'Gill', 'Curry', 'Mclaughlin', 'Harmon', 'Mcgee', 'Gross', 'Doyle', 'Garner', 'Newton', 'Burgess', 'Reese', 'Walton', 'Blake', 'Trujillo', 'Adkins', 'Brady', 'Goodman', 'Roman', 'Webster', 'Goodwin', 'Fischer', 'Huang', 'Potter', 'Delacruz', 'Montoya', 'Todd', 'Wu', 'Hines', 'Mullins', 'Castaneda', 'Malone', 'Cannon', 'Tate', 'Mack', 'Sherman', 'Hubbard', 'Hodges', 'Zhang', 'Guerra', 'Wolf', 'Valencia', 'Saunders', 'Franco', 'Rowe', 'Gallagher', 'Farmer', 'Hammond', 'Hampton', 'Townsend', 'Ingram', 'Wise', 'Gallegos', 'Clarke', 'Barton', 'Schroeder', 'Maxwell', 'Waters', 'Logan', 'Camacho', 'Strickland', 'Norman', 'Person', 'Colon', 'Parsons', 'Frank', 'Harrington', 'Glover', 'Osborne', 'Buchanan', 'Casey', 'Floyd', 'Patton', 'Ibarra', 'Ball', 'Tyler', 'Suarez', 'Bowers', 'Orozco', 'Salas', 'Cobb', 'Gibbs', 'Andrade', 'Bauer', 'Conner', 'Moody', 'Escobar', 'Mcguire', 'Lloyd', 'Mueller', 'Hartman', 'French', 'Kramer', 'Mcbride', 'Pope', 'Lindsey', 'Velazquez', 'Norton', 'Mccormick', 'Sparks', 'Flynn', 'Yates', 'Hogan', 'Marsh', 'Macias', 'Villanueva', 'Zamora', 'Pratt', 'Stokes', 'Owen', 'Ballard', 'Lang', 'Brock', 'Villarreal', 'Charles', 'Drake', 'Barrera', 'Cain', 'Patrick', 'Pineda', 'Burnett', 'Mercado', 'Santana', 'Shepherd', 'Bautista', 'Ali', 'Shaffer', 'Lamb', 'Trevino', 'Mckenzie', 'Hess', 'Beil', 'Olsen', 'Cochran', 'Morton', 'Nash', 'Wilkins', 'Petersen', 'Briggs', 'Shah', 'Roth', 'Nicholson', 'Holloway', 'Lozano', 'Rangel', 'Flowers', 'Hoover', 'Short', 'Arias', 'Mora', 'Valenzuela', 'Bryan', 'Meyers', 'Weiss', 'Underwood', 'Bass', 'Greer', 'Summers', 'Houston', 'Carson', 'Morrow', 'Clayton', 'Whitaker', 'Decker', 'Yoder', 'Collier', 'Zuniga', 'Carey', 'Wilcox', 'Melendez', 'Poole', 'Roberson', 'Larsen', 'Conley', 'Davenport', 'Copeland', 'Massey', 'Lam', 'Huff', 'Rocha', 'Cameron', 'Jefferson', 'Hood', 'Monroe', 'Anthony', 'Pittman', 'Huynh', 'Randall', 'Singleton', 'Kirk', 'Combs', 'Mathis', 'Christian', 'Skinner', 'Bradford', 'Richard', 'Galvan', 'Wall', 'Boone', 'Kirby', 'Wilkinson', 'Bridges', 'Bruce', 'Atkinson', 'Velez', 'Meza', 'Roy', 'Vincent', 'York', 'Hodge', 'Villa', 'Abbott', 'Allison', 'Tapia', 'Gates', 'Chase', 'Sosa', 'Sweeney', 'Farrell', 'Wyatt', 'Dalton', 'Horn', 'Barron', 'Phelps', 'Yu', 'Dickerson', 'Heath', 'Foley', 'Atkins', 'Mathews', 'Bonilla', 'Acevedo', 'Benitez', 'Zavala', 'Hensley', 'Glenn', 'Cisneros', 'Harrell', 'Shields', 'Rubio', 'Huffman', 'Choi', 'Boyer', 'Garrison', 'Arroyo', 'Bond', 'Kane', 'Hancock', 'Callahan', 'Dillon', 'Cline', 'Wiggins', 'Grimes', 'Arellano', 'Melton', 'Oneill', 'Savage', 'Ho', 'Beltran', 'Pitts', 'Parrish', 'Ponce', 'Rich', 'Booth', 'Koch', 'Golden', 'Ware', 'Brennan', 'Mcdowell', 'Marks', 'Cantu', 'Humphrey', 'Baxter', 'Sawyer', 'Clay', 'Tanner', 'Hutchinson', 'Kaur', 'Berg', 'Wiley', 'Gilmore', 'Russo', 'Villegas', 'Hobbs', 'Keith', 'Wilkerson', 'Ahmed', 'Beard', 'Mcclain', 'Montes', 'Mata', 'Rosario', 'Vang', 'Walter', 'Henson', 'Oneal', 'Mosley', 'Mcclure', 'Beasley', 'Stephenson', 'Snow', 'Huerta', 'Preston', 'Vance', 'Barry', 'Johns', 'Eaton', 'Blackwell', 'Dyer', 'Prince', 'Macdonald', 'Solomon', 'Guevara', 'Stafford', 'English', 'Hurst', 'Woodard', 'Cortes', 'Shannon', 'Kemp', 'Nolan', 'Mccullough', 'Merritt', 'Murillo', 'Moon', 'Salgado', 'Strong', 'Kline', 'Cordova', 'Barajas', 'Roach', 'Rosas', 'Winters', 'Jacobson', 'Lester', 'Knox', 'Bullock', 'Kerr', 'Leach', 'Meadows', 'Orr', 'Davila', 'Whitehead', 'Pruitt', 'Kent', 'Conway', 'Mckee', 'Barr', 'David', 'Dejesus', 'Marin', 'Berger', 'Mcintyre', 'Blankenship', 'Gaines', 'Palacios', 'Cuevas', 'Bartlett', 'Durham', 'Dorsey', 'Mccall', 'Odonnell', 'Stein', 'Browning', 'Stout', 'Lowery', 'Sloan', 'Mclean', 'Hendricks', 'Calhoun', 'Sexton', 'Chung', 'Gentry', 'Hull', 'Duarte', 'Ellison', 'Nielsen', 'Gillespie', 'Buck', 'Middleton', 'Sellers', 'Leblanc', 'Esparza', 'Hardin', 'Bradshaw', 'Mcintosh', 'Howe', 'Livingston', 'Frost', 'Glass', 'Morse', 'Knapp', 'Herman', 'Stark', 'Bravo', 'Noble', 'Spears', 'Weeks', 'Corona', 'Frederick', 'Buckley', 'Mcfarland', 'Hebert', 'Enriquez', 'Hickman', 'Quintero', 'Randolph', 'Schaefer', 'Walls', 'Trejo', 'House', 'Reilly', 'Pennington', 'Michael', 'Conrad', 'Giles', 'Benjamin', 'Crosby', 'Fitzpatrick', 'Donovan', 'Mays', 'Mahoney', 'Valentine', 'Raymond', 'Medrano', 'Hahn', 'Mcmillan', 'Small', 'Bentley', 'Felix', 'Peck', 'Lucero', 'Boyle', 'Hanna', 'Pace', 'Rush', 'Hurley', 'Harding', 'Mcconnell', 'Bernal', 'Nava', 'Ayers', 'Everett', 'Ventura', 'Avery', 'Pugh', 'Mayer', 'Bender', 'Shepard', 'Mcmahon', 'Landry', 'Case', 'Sampson', 'Moses', 'Magana', 'Blackburn', 'Dunlap', 'Gould', 'Duffy', 'Vaughan', 'Herring', 'Mckay', 'Espinosa', 'Rivers', 'Farley', 'Bernard', 'Ashley', 'Friedman', 'Potts', 'Truong', 'Costa', 'Correa', 'Blevins', 'Nixon', 'Clements', 'Fry', 'Delarosa', 'Best', 'Benton', 'Lugo', 'Portillo', 'Dougherty', 'Crane', 'Haley', 'Phan', 'Villalobos', 'Blanchard', 'Horne', 'Finley', 'Quintana', 'Lynn', 'Esquivel', 'Bean', 'Dodson', 'Mullen', 'Xiong', 'Hayden', 'Cano', 'Levy', 'Huber', 'Richmond', 'Moyer', 'Lim', 'Frye', 'Sheppard', 'Mccarty', 'Avalos', 'Booker', 'Waller', 'Parra', 'Woodward', 'Jaramillo', 'Krueger', 'Rasmussen', 'Brandt', 'Peralta', 'Donaldson', 'Stuart', 'Faulkner', 'Maynard', 'Galindo', 'Coffey', 'Estes', 'Sanford', 'Burch', 'Maddox', 'Vo', 'Oconnell', 'Vu', 'Andersen', 'Spence', 'Mcpherson', 'Church', 'Schmitt', 'Stanton', 'Leal', 'Cherry', 'Compton', 'Dudley', 'Sierra', 'Pollard', 'Alfaro', 'Hester', 'Proctor', 'Lu', 'Hinton', 'Novak', 'Good', 'Madden', 'Mccann', 'Terrell', 'Jarvis', 'Dickson', 'Reyna', 'Cantrell', 'Mayo', 'Branch', 'Hendrix', 'Rollins', 'Rowland', 'Whitney', 'Duke', 'Odom', 'Daugherty', 'Travis', 'Tang', 'Archer']
    japanNames["masc"] = ['Akifumi', 'Akihiro', 'Akihito', 'Akimasa', 'Akinari', 'Akinori', 'Akisada', 'Akito', 'Akitoshi', 'Akiya', 'Akiyuki', 'Arata', 'Arihiro', 'Arinobu', 'Asahiko', 'Asayama', 'Atsuhiko', 'Atsuji', 'Atsunobu', 'Atsushi', 'Atsuya', 'Banri', 'Bunta', 'Chikao', 'Chikashi', 'Chobyo', 'Choki', 'Chujiro', 'Dai', 'Daichi', 'Daigo', 'Daihachi', 'Daijiro', 'Daiki', 'Dairoku', 'Daishi', 'Daisuke', 'Daizo', 'Eiichi', 'Eiji', 'Eiken', 'Einosuke', 'Eisen', 'Eisuke', 'Eitaro', 'Emon', 'Etsuji', 'Fujio', 'Fumiaki', 'Fumihiro', 'Fuminori', 'Fumitaka', 'Fumiya', 'Fusao', 'Futoshi', 'Fuyukichi', 'Gaku', 'Gen', 'Gen', 'Genjiro', 'Genta', 'Genzo', 'Gin', 'Ginji', 'Goichi', 'Gota', 'Hachiro', 'Haruaki', 'Haruhiko', 'Haruhisa', 'Harukichi', 'Harunobu', 'Haruo', 'Haruto', 'Haruyoshi', 'Hayanari', 'Hayata', 'Heihachiro', 'Heisuke', 'Hide', 'Hideharu', 'Hidehisa', 'Hideji', 'Hideki', 'Hidemasa', 'Hidemitsu', 'Hidenori', 'Hideomi', 'Hidetada', 'Hidetaka', 'Hidetoshi', 'Hideya', 'Hideyoshi', 'Hideyuki', 'Hiroaki', 'Hirohide', 'Hiroji', 'Hirokazu', 'Hirokuni', 'Hiromichi', 'Hiromori', 'Hironari', 'Hironori', 'Hirooki', 'Hiroshi', 'Hirotaka', 'Hiroto', 'Hirotomo', 'Hirotsugu', 'Hiroyasu', 'Hiroyuki', 'Hisahito', 'Hisaki', 'Hisamoto', 'Hisanori', 'Hisashi', 'Hisateru', 'Hisatoshi', 'Hisayasu', 'Hisayuki', 'Hokuto', 'Ichiei', 'Ichizo', 'Iehiro', 'Iemasa', 'Iesada', 'Ikko', 'Ikuro', 'Ippei', 'Isamu', 'Issei', 'Issho', 'Itsuo', 'Iwao', 'Jiichiro', 'Jin', 'Jinpachi', 'Jiro', 'Jirokichi', 'Joichiro', 'Jokichi', 'Jubei', 'Jun', 'Jun', 'Junji', 'Junnosuke', 'Junto', 'Junzo', 'Jutaro', 'Kagemori', 'Kagetaka', 'Kaichi', 'Kaiji', 'Kaito', 'Kaku', 'Kakuei', 'Kakutaro', 'Kanehira', 'Kanehisa', 'Kanematsu', 'Kanesuke', 'Kaneto', 'Kaneyoshi', 'Kanji', 'Kankuro', 'Kanta', 'Kantaro', 'Katsuhiko', 'Katsuhisa', 'Katsuji', 'Katsukiyo', 'Katsumoto', 'Katsunari', 'Katsunosuke', 'Katsushi', 'Katsutaro', 'Katsutomo', 'Katsuya', 'Katsuyuki', 'Kazuaki', 'Kazuharu', 'Kazuhiro', 'Kazuhito', 'Kazuma', 'Kazumichi', 'Kazunori', 'Kazuoki', 'Kazushi', 'Kazutaka', 'Kazutoki', 'Kazuya', 'Kazuyoshi', 'Keigo', 'Keiichi', 'Keiji', 'Keiju', 'Keinosuke', 'Keisuke', 'Keizaburo', 'Ken', 'Ken', 'Ken', 'Kengo', 'Ken', 'Kenji', 'Kenjiro', 'Kenkichi', 'Kensaku', 'Kenshi', 'Kenshin', 'Kenta', 'Kento', 'Kenzo', 'Kihachi', 'Kihei', 'Kiichi', 'Kijuro', 'Kimihiro', 'Kimitoshi', 'Kin', 'Kin', 'Kinji', 'Kinsuke', 'Kin', 'Kisaburo', 'Kishio', 'Kiyoaki', 'Kiyohide', 'Kiyohiro', 'Kiyokazu', 'Kiyomoto', 'Kiyonori', 'Kiyoshi', 'Kiyotaka', 'Kiyoto', 'Kodai', 'Kogo', 'Kohei', 'Koichi', 'Koji', 'Kojiro', 'Kokichi', 'Korechika', 'Koro', 'Kosaku', 'Koshi', 'Koson', 'Kota', 'Kotaro', 'Kouki', 'Koyo', 'Kozo', 'Kuniaki', 'Kunihiro', 'Kunimitsu', 'Kunishige', 'Kuniyoshi', 'Kuranosuke', 'Kyogo', 'Kyoichi', 'Kyosuke', 'Mahiro', 'Makio', 'Mamoru', 'Manato', 'Manjiro', 'Mareo', 'Masaaki', 'Masachika', 'Masaharu', 'Masahiko', 'Masahisa', 'Masaichi', 'Masaji', 'Masakata', 'Masakazu', 'Masakoto', 'Masamichi', 'Masamori', 'Masamune', 'Masamura', 'Masanao', 'Masanobu', 'Masanosuke', 'Masaomi', 'Masasada', 'Masashige', 'Masatake', 'Masateru', 'Masatomi', 'Masatoshi', 'Masatsune', 'Masayoshi', 'Masazumi', 'Masuo', 'Matabei', 'Matsuki', 'Matsushige', 'Michiharu', 'Michihiro', 'Michinori', 'Michiro', 'Michitaro', 'Michiyoshi', 'Mikito', 'Mikuni', 'Mineo', 'Minoru', 'Mitsugi', 'Mitsuharu', 'Mitsuhiko', 'Mitsuhiro', 'Mitsumasa', 'Mitsunobu', 'Mitsuo', 'Mitsushige', 'Mitsutaka', 'Mitsuteru', 'Mitsuyasu', 'Mitsuyoshi', 'Mitsuzo', 'Mokichi', 'Morihiro', 'Morimasa', 'Morishige', 'Moritaka', 'Mosuke', 'Motofumi', 'Motohiko', 'Motohiro', 'Motojiro', 'Motoki', 'Motonobu', 'Motoshi', 'Motosuke', 'Mototsugu', 'Motoyoshi', 'Motoyuki', 'Mukuro', 'Munehisa', 'Munenobu', 'Muneo', 'Munetaka', 'Munetoshi', 'Murashige', 'Mutsuhiko', 'Mutsuo', 'Nagaharu', 'Nagamasa', 'Naganao', 'Nagatoki', 'Nagayasu', 'Nankichi', 'Naoharu', 'Naohiro', 'Naohito', 'Naokatsu', 'Naomasa', 'Naomori', 'Naoshi', 'Naotake', 'Naoya', 'Naozumi', 'Nariakira', 'Naritaka', 'Nariyuki', 'Naruhito', 'Naruki', 'Natsuhiko', 'Nobuaki', 'Nobuharu', 'Nobuhiro', 'Nobuhito', 'Nobukazu', 'Nobumasa', 'Nobumoto', 'Nobunao', 'Nobuo', 'Nobusuke', 'Nobutaka', 'Nobutoki', 'Nobutoshi', 'Nobuyasu', 'Nobuyuki', 'Noriaki', 'Norifusa', 'Norihiko', 'Norihisa', 'Norikazu', 'Norimichi', 'Norio', 'Noriyasu', 'Noriyuki', 'Okimoto', 'Otohiko', 'Raizo', 'Reiji', 'Rentaro', 'Riichi', 'Rikichi', 'Rikiya', 'Risaburo', 'Rokuro', 'Ryohei', 'Ryoji', 'Ryokichi', 'Ryosei', 'Ryota', 'Ryoya', 'Ryu', 'Ryuhei', 'Ryuji', 'Ryuki', 'Ryunosuke', 'Ryusei', 'Ryushi', 'Ryuta', 'Ryuya', 'Saburo', 'Sachio', 'Sadaharu', 'Sadahiro', 'Sadakazu', 'Sadao', 'Sadatoshi', 'Sadayuki', 'Saiichi', 'Sakutaro', 'Sankichi', 'Satonari', 'Satoshi', 'Sawao', 'Seigo', 'Seiichi', 'Seiji', 'Seijiro', 'Seikichi', 'Seishi', 'Seitaro', 'Seizo', 'Senkichi', 'Setsuo', 'Shichiro', 'Shigefumi', 'Shigehiro', 'Shigekazu', 'Shigemasa', 'Shigemi', 'Shigemori', 'Shigenaga', 'Shigenori', 'Shigeru', 'Shigetaka', 'Shigetoshi', 'Shigeyasu', 'Shigeyuki', 'Shin', 'Shingo', 'Shin', 'Shin', 'Shinji', 'Shinjo', 'Shinkichi', 'Shinpachi', 'Shinsaku', 'Shinta', 'Shinya', 'Shiro', 'Shizuo', 'Shogo', 'Shoichi', 'Shoji', 'Shojiro', 'Shosuke', 'Shotaro', 'Shozo', 'Shugo', 'Shuji', 'Shun', 'Shungo', 'Shun', 'Shunji', 'Shunkichi', 'Shunsaku', 'Shunsuke', 'Shuntaro', 'Shunzo', 'Shusuke', 'Shuto', 'Shuya', 'So', 'Soichi', 'Soji', 'Sonosuke', 'Sota', 'Suehiro', 'Suguru', 'Sukemasa', 'Suketoshi', 'Sukeyuki', 'Sumimoto', 'Sumiyoshi', 'Sunao', 'Sutemi', 'Tadaaki', 'Tadafumi', 'Tadahiko', 'Tadahito', 'Tadamasa', 'Tadamitsu', 'Tadanaga', 'Tadanari', 'Tadanori', 'Tadaoki', 'Tadataka', 'Tadatomo', 'Tadatsugu', 'Tadayo', 'Tadayuki', 'Taichiro', 'Taiichi', 'Taiki', 'Taishi', 'Taishin', 'Taisuke', 'Taizo', 'Takaaki', 'Takaharu', 'Takahide', 'Takahira', 'Takahisa', 'Takaji', 'Takakazu', 'Takamasa', 'Takamori', 'Takanobu', 'Takao', 'Takashi', 'Takato', 'Takatoshi', 'Takauji', 'Takayasu', 'Takayuki', 'Takefumi', 'Takehiko', 'Takehisa', 'Takeichi', 'Takenaga', 'Takenori', 'Takero', 'Takeshi', 'Taketo', 'Taketoshi', 'Takeyoshi', 'Takezo', 'Takuji', 'Takumi', 'Takuo', 'Takuto', 'Takuzo', 'Tamotsu', 'Tasuku', 'Tatsuaki', 'Tatsuhiro', 'Tatsuji', 'Tatsumi', 'Tatsunosuke', 'Tatsuro', 'Tatsuya', 'Tatsuyuki', 'Teiichi', 'Teijiro', 'Teizo', 'Teruaki', 'Teruhisa', 'Teruki', 'Terunobu', 'Teruyasu', 'Teruyuki', 'Tetsuharu', 'Tetsuji', 'Tetsunosuke', 'Tetsuro', 'Tetsutaro', 'Tetsuzo', 'Togo', 'Toichi', 'Tokio', 'Tokuji', 'Tokujiro', 'Tokuro', 'Tokuzo', 'Tomio', 'Tomochika', 'Tomohide', 'Tomohiro', 'Tomohito', 'Tomokazu', 'Tomomichi', 'Tomonobu', 'Tomoo', 'Tomoya', 'Tomoyoshi', 'Torahiko', 'Toru', 'Toshi', 'Toshiaki', 'Toshifumi', 'Toshihide', 'Toshihiro', 'Toshihito', 'Toshikatsu', 'Toshiki', 'Toshimichi', 'Toshinaga', 'Toshinari', 'Toshinori', 'Toshiro', 'Toshitaka', 'Toshiya', 'Toshiyoshi', 'Toshizo', 'Toyoaki', 'Toyokazu', 'Toyomatsu', 'Toyotaro', 'Tsugio', 'Tsugumichi', 'Tsuneharu', 'Tsunehisa', 'Tsunekazu', 'Tsunemi', 'Tsunenori', 'Tsuneyoshi', 'Tsutomu', 'Tsuyoshi', 'Umanosuke', 'Uryu', 'Wataru', 'Yahiko', 'Yamato', 'Yashiro', 'Yasufumi', 'Yasuhide', 'Yasuhiro', 'Yasuji', 'Yasukazu', 'Yasumasa', 'Yasumichi', 'Yasunobu', 'Yasuo', 'Yasuro', 'Yasutaka', 'Yasutaro', 'Yasutoshi', 'Yasuyuki', 'Yawara', 'Yo', 'Yoichi', 'Yoichiro', 'Yojiro', 'Yorinobu', 'Yoritaka', 'Yoritsune', 'Yoshiaki', 'Yoshiharu', 'Yoshihiko', 'Yoshihisa', 'Yoshiie', 'Yoshikatsu', 'Yoshiki', 'Yoshikuni', 'Yoshimatsu', 'Yoshimichi', 'Yoshimori', 'Yoshinaga', 'Yoshinari', 'Yoshinori', 'Yoshiro', 'Yoshishige', 'Yoshitaka', 'Yoshitaro', 'Yoshito', 'Yoshitsugu', 'Yoshiyasu', 'Yoshizumi', 'Yota', 'Yudai', 'Yugo', 'Yuhei', 'Yuichi', 'Yuji', 'Yukichi', 'Yukihiko', 'Yukimasa', 'Yukinobu', 'Yukio', 'Yukitaka', 'Yukitoshi', 'Yukiyoshi', 'Yusaku', 'Yushi', 'Yuta', 'Yutaro', 'Yuya', 'Yuzuru', 'Zenji', 'Zenjiro', 'Zentaro']
    japanNames["fem"] = ['Ai', 'Aika', 'Aimi', 'Airi', 'Akari', 'Akemi', 'Aki', 'Akie', 'Akiko', 'Akina', 'Akiyo', 'Ami', 'Anzu', 'Arisa', 'Asako', 'Asuka', 'Asumi', 'Atsuko', 'Aya', 'Ayaka', 'Ayako', 'Ayami', 'Ayane', 'Ayu', 'Ayuka', 'Ayumi', 'Azusa', 'Chidori', 'Chieko', 'Chigusa', 'Chiho', 'Chikage', 'Chinami', 'Chisato', 'Chiya', 'Chiyo', 'Chizuko', 'Eiko', 'Emi', 'Emiko', 'Eri', 'Erika', 'Eriko', 'Etsuko', 'Fujie', 'Fuka', 'Fukumi', 'Fumie', 'Fumika', 'Fumino', 'Fusako', 'Fuyuko', 'Hana', 'Hanae', 'Harue', 'Haruko', 'Haruno', 'Hasumi', 'Hatsumi', 'Hidemi', 'Himeko', 'Hinako', 'Hiroka', 'Hiroyo', 'Hisae', 'Hisayo', 'Honami', 'Honoka', 'Ichiko', 'Ikuko', 'Ikuyo', 'Itsuko', 'Jitsuko', 'Juri', 'Kaguya', 'Kahori', 'Kana', 'Kanade', 'Kanako', 'Kanna', 'Kanoko', 'Kaoruko', 'Karin', 'Kasumi', 'Katsuko', 'Kaya', 'Kayoko', 'Kazuha', 'Kazusa', 'Keiki', 'Keiko', 'Kiho', 'Kikue', 'Kimi', 'Kinuko', 'Kiyoko', 'Komako', 'Kotoe', 'Kotono', 'Kou', 'Kozue', 'Kumiko', 'Kurenai', 'Kyoko', 'Maaya', 'Machi', 'Machiko', 'Maho', 'Maki', 'Makiko', 'Mamiko', 'Mana', 'Manaka', 'Mao', 'Mari', 'Marie', 'Marika', 'Marina', 'Marumi', 'Masae', 'Masayo', 'Mayako', 'Mayu', 'Mayuka', 'Mayumi', 'Megu', 'Mei', 'Meiko', 'Meisa', 'Mie', 'Miharu', 'Miho', 'Miiko', 'Mikako', 'Mikiko', 'Mikuru', 'Mina', 'Minae', 'Minami', 'Mineko', 'Miori', 'Misaki', 'Misako', 'Misumi', 'Mitsuki', 'Mitsuyo', 'Miwa', 'Miya', 'Miyako', 'Miyo', 'Miyoshi', 'Miyu', 'Miyumi', 'Mizuko', 'Moeka', 'Momo', 'Momoka', 'Motoko', 'Mutsumi', 'Nagako', 'Nako', 'Nana', 'Nanae', 'Nanako', 'Nanase', 'Naoko', 'Natsue', 'Natsume', 'Nene', 'Noa', 'Nobue', 'Nodoka', 'Noriko', 'Omi', 'Otoha', 'Ran', 'Ranko', 'Reiko', 'Rena', 'Rie', 'Riho', 'Rika', 'Riko', 'Rino', 'Rio', 'Risako', 'Rumi', 'Rumiko', 'Ruri', 'Ryoka', 'Sachi', 'Sachie', 'Sadako', 'Saeko', 'Saiko', 'Sakie', 'Saku', 'Sakura', 'Sakurako', 'Saori', 'Satoko', 'Sawa', 'Saya', 'Sayako', 'Sayoko', 'Sayumi', 'Seiko', 'Setsuko', 'Shiho', 'Shihori', 'Shimako', 'Shino', 'Shizue', 'Shizuru', 'Shuko', 'Sugako', 'Sumika', 'Sumiko', 'Suzue', 'Suzuko', 'Taeko', 'Takayo', 'Tamako', 'Tamao', 'Tamiko', 'Tazuko', 'Teruko', 'Tokiko', 'Tomie', 'Tomiko', 'Tomoko', 'Toshiko', 'Tsukiko', 'Tsuru', 'Umeko', 'Waka', 'Wakana', 'Yae', 'Yasue', 'Yayoi', 'Yoko', 'Yoriko', 'Yoshino', 'Yuika', 'Yuka', 'Yukako', 'Yukie', 'Yukiko', 'Yukino', 'Yumeko', 'Yumie', 'Yumiko', 'Yuria', 'Yurie', 'Yuriko', 'Yuumi', 'Yuzuki']
    japanNames["neut"] = ['Akemi', 'Aki', 'Akiho', 'Akira', 'Anri', 'Aoi', 'Asuka', 'Ayumu', 'Chiaki', 'Hajime', 'Haruka', 'Harumi', 'Hayate', 'Hibiki', 'Hikari', 'Hikaru', 'Hiromi', 'Hiromu', 'Hiyori', 'Ibuki', 'Iori', 'Izumi', 'Jun', 'Kaede', 'Kaname', 'Katsumi', 'Kazu', 'Kei', 'Kou', 'Kunie', 'Kyo', 'Maiko', 'Maki', 'Mako', 'Masaki', 'Masami', 'Matoi', 'Mayumi', 'Michi', 'Michiyo', 'Mikoto', 'Mirai', 'Misao', 'Mitsuki', 'Mitsuyo', 'Mizuki', 'Nagisa', 'Naomi', 'Natsuki', 'Nozomi', 'Rei', 'Ren', 'Rin', 'Rui', 'Ryo', 'Ryuko', 'Sakae', 'Satsuki', 'Shigeri', 'Shion', 'Sora', 'Subaru', 'Takemi', 'Tamaki', 'Tatsuki', 'Tomo', 'Tomomi', 'Tsubasa', 'Yoshi', 'Yoshika', 'Yu', 'Yuri']
    japanNames["sur"] = ['Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Nakamura', 'Kobayashi', 'Yamamoto', 'Yoshida', 'Yamada', 'Sasaki', 'Yamaguchi', 'Matsumoto', 'Inoue', 'Kimura', 'Shimizu', 'Hayashi', 'Yamasaki', 'Nakashima', 'Mori', 'Abe', 'Ikeda', 'Hashimoto', 'Ishikawa', 'Yamashita', 'Ogawa', 'Ishii', 'Hasegawa', 'Okada', 'Maeda', 'Fujita', 'Aoki', 'Sakamoto', 'Murakami', 'Kaneko', 'Fujii', 'Fukuda', 'Nishimura', 'Miura', 'Takeuchi', 'Nakagawa', 'Okamoto', 'Matsuda', 'Harada', 'Nakano', 'Ono', 'Tamura', 'Fujihara', 'Nakayama', 'Ishida', 'Kojima', 'Wada', 'Morita', 'Uchida', 'Shibata', 'Sakai', 'Hara', 'Takaki', 'Yokoyama', 'Miyasaki', 'Ueta', 'Shimada', 'Miyamoto', 'Sugiyama', 'Imai', 'Maruyama', 'Masuda', 'Takata', 'Murata', 'Hirano', 'Sugahara', 'Taketa', 'Arai', 'Oyama', 'Noguchi', 'Sakurai', 'Chiba', 'Iwasaki', 'Sano', 'Taniguchi', 'Ueno', 'Matsui', 'Kawano', 'Ichikawa', 'Watabe', 'Nomura', 'Kikuchi', 'Kinoshita']
    europeNames["masc"] = ['Noel', 'Joel', 'Mateo', 'Ergi', 'Luis', 'Aron', 'Samuel', 'Roan', 'Roel', 'Xhoel', 'Marc', 'Eric', 'Jan', 'Daniel', 'Enzo', 'Ian', 'Pol', 'Àlex', 'Jordi', 'Marti', 'Lukas', 'Maximilian', 'Jakob', 'David', 'Tobias', 'Paul', 'Jonas', 'Felix', 'Alexander', 'Elias', 'Artsiom', 'Артем', 'Mikhail', 'Maksim', 'Максим', 'Ivan', 'Иван', 'Roman', 'Роман', 'Aleksandr', 'Александр', 'Danyl', 'Lucas', 'Louis', 'Noah', 'Nathan', 'Adam', 'Arthur', 'Mohamed', 'Victor', 'Mathis', 'Liam', 'Lucas', 'Liam', 'Louis', 'Wout', 'Mathis', 'Lars', 'Vince', 'Kobe', 'Finn', 'Noah', 'Nathan', 'Hugo', 'Louis', 'Theo', 'Ethan', 'Noah', 'Lucas', 'Gabriel', 'Arthur', 'Tom', 'Adam', 'Mohamed', 'Rayan', 'Gabriel', 'Anas', 'David', 'Lucas', 'Yanis', 'Nathan', 'Ibrahim', 'Ahmed', 'Daris', 'Amar', 'Davud', 'Adin', 'Hamza', 'Harun', 'Vedad', 'Imran', 'Tarik', 'Stefan', 'Luka', 'Lazar', 'Nikola', 'Pavle', 'David', 'Marko', 'Mihajlo', 'Andrej', 'Milos', 'Georgi', 'Aleksandar', 'Martin', 'Dimitar', 'Ivan', 'Nikolay', 'Nikola', 'Daniel', 'Viktor', 'Kristian', 'Luka', 'David', 'Ivan', 'Jakov', 'Marko', 'Petar', 'Filip', 'Matej', 'Mateo', 'Leon', 'Andreas', 'Georgios', 'Konstantinos', 'Christos', 'Nikolaos', 'Michalis', 'Panagiotis', 'Ioannis', 'Marios', 'Dimitrios', 'Jakub', 'Jan', 'Tomas', 'David', 'Adam', 'Matyas', 'Filip', 'Vojtěch', 'Ondřej', 'Lukas', 'William', 'Noah', 'Oscar', 'Lucas', 'Victor', 'Malthe', 'Oliver', 'Alfred', 'Carl', 'Valdemar', 'Oliver', 'George', 'Harry', 'Jack', 'Jacob', 'Noah', 'Charlie', 'Muhammad', 'Thomas', 'Oscar', 'Aleksandr', 'Vladimir', 'Sergei', 'Andrei', 'Aleksei', 'Martin', 'Andres', 'Dmitri', 'Igor', 'Toomas', 'Benjamin', 'Liam', 'Rokur', 'Aron', 'Brandur', 'Friði', 'Kristian', 'Noa', 'David', 'Elias', 'Filip', 'Mattias', 'Leo', 'Elias', 'Oliver', 'Eino', 'Väino', 'Eeli', 'Noel', 'Leevi', 'Onni', 'Hugo', 'Emil', 'Liam', 'William', 'Oliver', 'Edvin', 'Max', 'Hugo', 'Benjamin', 'Elias', 'Leo', 'Gabriel', 'Louis', 'Raphaël', 'Jules', 'Adam', 'Lucas', 'Leo', 'Hugo', 'Arthur', 'Nathan', 'Giorgi', 'Nikoloz', 'Andria', 'Gabrieli', 'Luka', 'Saba', 'Davit', 'Aleksandre', 'Ben', 'Jonas', 'Leon', 'Elias', 'Finn', 'Fynn', 'Noah', 'Paul', 'Luis', 'Louis', 'Lukas', 'Lucas', 'Luca', 'Luka', 'Georgios', 'Ioannis', 'Konstantinos', 'Dimitrios', 'Nikolaos', 'Panagiotis', 'Vasileios', 'Christos', 'Athanasios', 'Michail', 'Charlie', 'Harry', 'William', 'Alexander', 'Lewis', 'Charles', 'Bence', 'Mate', 'Levente', 'Adam', 'David', 'Daniel', 'Marcell', 'Balazs', 'Milan', 'Dominik', 'Aron', 'Alexander', 'Viktor', 'Victor', 'Kristjan', 'Kristian', 'Christian', 'Jon', 'Guðmundur', 'Kristofer', 'Gunnar', 'Olafur', 'Olav', 'Benedikt', 'Dagur', 'Emil', 'Jack', 'James', 'Daniel', 'Conor', 'Sean', 'Adam', 'Noah', 'Michael', 'Charlie', 'Luke', 'James', 'Jamie', 'Joshua', 'Harry', 'Harrison', 'Connor', 'Jackson', 'Alfie', 'Alfred', 'Lucas', 'Luke', 'Benjamin', 'Thomas', 'Charles', 'Jake', 'William', 'Daniel', 'Lee', 'Theo', 'Leonardo', 'Francesco', 'Alessandro', 'Lorenzo', 'Mattia', 'Andrea', 'Gabriele', 'Riccardo', 'Tommaso', 'Edoardo', 'Roberts', 'Markuss', 'Artjoms', 'Ralfs', 'Gustavs', 'Maksims', 'Arturs', 'Aleksandrs', 'Emils', 'Daniels', 'Benjamin', 'Elias', 'Raphael', 'Rafael', 'Jonas', 'Paul', 'David', 'Liam', 'Robin', 'Lukas', 'Matas', 'Nojus', 'Dominykas', 'Jokubas', 'Emilis', 'Jonas', 'Kajus', 'Gabrielius', 'Dovydas', 'Gabriel', 'Leo', 'Luca', 'Noah', 'David', 'Tom', 'Ben', 'Aleksandar', 'Zoran', 'Nikola', 'Goran', 'Dragan', 'Dejan', 'Petar', 'Igor', 'Ilija', 'Stefan', 'Mihail', 'Damjan', 'Petar', 'Marko', 'Andrej', 'David', 'Jovan', 'Luka', 'Matej', 'Stefan', 'Luke', 'Luca', 'Lucas', 'Matthew', 'Matthias', 'Matteo', 'Jacob', 'Jake', 'Zachary', 'Zak', 'Zack', 'Michael', 'Miguel', 'Mikhail', 'Liam', 'William', 'John', 'Jean', 'Jonathan', 'Juan', 'Gan', 'Benjamin', 'Ben', 'Kaiden', 'Kayden', 'Kai', 'Alexander', 'Alessandro', 'Alec', 'Andrew', 'Andreas', 'Andre', 'Andy', 'David', 'Maxim', 'Alexandru', 'Artiom', 'Ion', 'Bogdan', 'Daniel', 'Matthew', 'Nikita', 'Michael', 'Gabriel', 'Alexandre', 'Lucas', 'Ethan', 'Aaron', 'Nikola', 'Marko', 'Dragan', 'Milos', 'Zoran', 'Milan', 'Aleksandar', 'Ivan', 'Petar', 'Luka', 'Luka', 'Vuk', 'Lazar', 'Pavle', 'Vasilije', 'Petar', 'Stefan', 'Jovan', 'Andrej', 'David', 'Daan', 'Noah', 'Sem', 'Lucas', 'Jesse', 'Finn', 'Milan', 'Max', 'Levi', 'Luuk', 'James', 'Jack', 'Noah', 'Charlie', 'Daniel', 'Oliver', 'Matthew', 'Harry', 'Thomas', 'Jake', 'William', 'Oskar', 'Lucas', 'Mathias', 'Filip', 'Oliver', 'Jakob', 'Jacob', 'Emil', 'Noah', 'Aksel', 'Antoni', 'Jakub', 'Jan', 'Szymon', 'Aleksander', 'Franciszek', 'Filip', 'Mikołaj', 'Wojciech', 'Kacper', 'João', 'Martim', 'Rodrigo', 'Santiago', 'Francisco', 'Afonso', 'Tomas', 'Miguel', 'Guilherme', 'Gabriel', 'Andrei', 'David', 'Alexandru', 'Gabriel', 'Mihai', 'Cristian', 'Stefan', 'Luca', 'Ionut', 'Darius', 'Alexander', 'Maxim', 'Artyom', 'Artem', 'Mikhail', 'Daniil', 'Danila', 'Danil', 'Ivan', 'Dmitry', 'Kirill', 'Andrey', 'Yegor', 'Alexander', 'Sergei', 'Dmitry', 'Andrei', 'Alexey', 'Maxim', 'Evgeny', 'Ivan', 'Mikhail', 'Artyom', 'Jack', 'James', 'Oliver', 'Lewis', 'Logan', 'Harry', 'Noah', 'Leo', 'Charlie', 'Alexander', 'Dragan', 'Milan', 'Aleksandar', 'Zoran', 'Nikola', 'Milos', 'Marko', 'Goran', 'Dusan', 'Dejan', 'Nikola', 'Luka', 'Stefan', 'Marko', 'Lazar', 'Aleksandar', 'Filip', 'Jovan', 'Nemanja', 'Milos', 'Jakub', 'Adam', 'Samuel', 'Lukas', 'Martin', 'Tomas', 'Michal', 'Filip', 'Matej', 'Matus', 'Luka', 'Jakob', 'Mark', 'Filip', 'Nik', 'Tim', 'Jaka', 'Zan', 'Jan', 'Lovro', 'Hugo', 'Daniel', 'Martin', 'Pablo', 'Alejandro', 'Lucas', 'Alvaro', 'Adrian', 'Mateo', 'David', 'Markel', 'Aimar', 'Jon', 'Ibai', 'Julen', 'Ander', 'Unax', 'Oier', 'Mikel', 'Iker', 'Marc', 'Àlex', 'Marti', 'Hugo', 'Biel', 'Èric', 'Nil', 'Jan', 'Pol', 'Pau', 'Oscar', 'Lucas', 'William', 'Liam', 'Oliver', 'Hugo', 'Alexander', 'Elias', 'Charlie', 'Noah', 'Noah', 'Liam', 'Gabriel', 'Luca', 'Leon', 'Elias', 'David', 'Samuel', 'Louis', 'Julian', 'Artem', 'Matviy', 'Maksym', 'David', 'Nikita', 'Mykyta', 'Mykhailo', 'Daniil', 'Danylo', 'Bohdan', 'Andriy', 'Oleksandr', 'Oliver', 'Jacob', 'Noah', 'Jack', 'Oscar', 'Harry', 'Charlie', 'Alfie', 'George', 'William']
    europeNames["fem"] = ['Amelia', 'Ajla', 'Melisa', 'Amelija', 'Klea', 'Sara', 'Kejsi', 'Noemi', 'Alesia', 'Leandra', 'Laia', 'Carlota', 'Emma', 'Lara', 'Martina', 'Aina', 'Maria', 'Blanca', 'Laura', 'Valentina', 'Anna', 'Hannah', 'Sophia', 'Emma', 'Marie', 'Lena', 'Sarah', 'Sophie', 'Laura', 'Mia', 'Sofiya', 'Marya', 'Polina', 'Eva', 'Anna', 'Darya', 'Kseniya', 'Alisa', 'Emma', 'Louise', 'Olivia', 'Elise', 'Alice', 'Juliette', 'Mila', 'Lucie', 'Marie', 'Camille', 'Maria', 'Marie', 'Dominique', 'Martine', 'Nathalie', 'Anne', 'Rita', 'Nicole', 'Anna', 'Christiane', 'Emma', 'Marie', 'Elise', 'Julie', 'Louise', 'Noor', 'Lotte', 'Fien', 'Nina', 'Ella', 'Lore', 'Lea', 'Lucie', 'Emma', 'Zoe', 'Louise', 'Camille', 'Manon', 'Chloe', 'Alice', 'Clara', 'Aya', 'Yasmine', 'Lina', 'Sara', 'Sarah', 'Sofia', 'Louise', 'Nour', 'Lea', 'Malak', 'Amina', 'Merjem', 'Sara', 'Asja', 'Lamija', 'Ema', 'Emina', 'Hana', 'Lejla', 'Esma', 'Marija', 'Sofija', 'Ana', 'Milica', 'Sara', 'Dunja', 'Teodora', 'Anastasija', 'Andela', 'Katarina', 'Viktoria', 'Maria', 'Nikol', 'Aleksandra', 'Gabriela', 'Daria', 'Raya', 'Yoana', 'Sofia', 'Simona', 'Mia', 'Lucija', 'Sara', 'Ana', 'Ema', 'Petra', 'Lana', 'Nika', 'Marta', 'Elena', 'Maria', 'Eleni', 'Androula', 'Georgia', 'Panagiota', 'Anna', 'Christina', 'Katerina', 'Ioanna', 'Kyriaki', 'Eliska', 'Tereza', 'Anna', 'Adela', 'Natalie', 'Sofie', 'Kristýna', 'Karolina', 'Viktorie', 'Barbora', 'Ida', 'Emma', 'Alma', 'Ella', 'Sofia', 'Freja', 'Josefine', 'Clara', 'Anna', 'Karla', 'Olivia', 'Amelia', 'Emily', 'Isla', 'Ava', 'Jessica', 'Isabella', 'Lily', 'Ella', 'Mia', 'Olga', 'Irina', 'Jelena', 'Tatjana', 'Svetlana', 'Valentina', 'Anna', 'Galina', 'Natalja', 'Maria', 'Eva', 'Emma', 'Hanna', 'Maria', 'Ro', 'Elsa', 'Lea', 'Sofia', 'Isabella', 'Lilja', 'Liva', 'Mia', 'Ronja', 'Rosa', 'Aino', 'Aada', 'Sofia', 'Eevi', 'Olivia', 'Lilja', 'Helmi', 'Ellen', 'Emilia', 'Ella', 'Saga', 'Emma', 'Stella', 'Ellen', 'Alva', 'Ebba', 'Olivia', 'Selma', 'Alma', 'Ella', 'Emma', 'Louise', 'Jade', 'Alice', 'Chloe', 'Lina', 'Mila', 'Lea', 'Manon', 'Rose', 'Mariami', 'Barbare', 'Elene', 'Anastasia', 'Nino', 'Nia', 'Ana', 'Elizaveta', 'Mia', 'Emma', 'Hannah', 'Hanna', 'Sofia', 'Sophia', 'Anna', 'Emilia', 'Lina', 'Marie', 'Lena', 'Mila', 'Maria', 'Eleni', 'Aikaterini', 'Vasiliki', 'Basiliki', 'Sophia', 'Angeliki', 'Georgia', 'Dimitra', 'Konstantina', 'Paraskevi', 'Paraskeui', 'Chloe', 'Olivia', 'Daisy', 'Isla', 'Jessica', 'Hanna', 'Anna', 'Jazmin', 'Lili', 'Zsofia', 'Emma', 'Luca', 'Boglarka', 'Zoe', 'Nora', 'Margret', 'Margrjet', 'Margret', 'Anna', 'Emma', 'Isabella', 'Isabel', 'Isabella', 'Isabel', 'Eva', 'Hekla', 'Kristin', 'Viktoria', 'Emilia', 'Emelia', 'Katrin', 'Emily', 'Emma', 'Ava', 'Sophie', 'Amelia', 'Ella', 'Lucy', 'Grace', 'Chloe', 'Mia', 'Isabella', 'Eva', 'Evie', 'Lilly', 'Sofia', 'Amelia', 'Emma', 'Olivia', 'Abbie', 'Chloe', 'Holly', 'Grace', 'Maisie', 'Mia', 'Sienna', 'Sofia', 'Giulia', 'Aurora', 'Alice', 'Ginevra', 'Emma', 'Giorgia', 'Greta', 'Beatrice', 'Anna', 'Sofija', 'Emilija', 'Alise', 'Anna', 'Marta', 'Viktorija', 'Elizabete', 'Estere', 'Anastasija', 'Paula', 'Anna', 'Noemi', 'Emilija', 'Austeja', 'Vilte', 'Gabija', 'Liepa', 'Kamile', 'Leja', 'Ugne', 'Ema', 'Urte', 'Emma', 'Lara', 'Zoe', 'Amy', 'Sarah', 'Charlotte', 'Emily', 'Marija', 'Elena', 'Biljana', 'Vesna', 'Snezana', 'Violeta', 'Aleksandra', 'Suzana', 'Katerina', 'Ivana', 'Sara', 'Jana', 'Jovana', 'Sofija', 'Ana', 'Mila', 'Marija', 'Eva', 'Anastasija', 'Ilina', 'Elena', 'Elenia', 'Helena', 'Ella', 'Julia', 'Yulia', 'Julianne', 'Emma', 'Emmanuela', 'Ema', 'Eliza', 'Elisa', 'Elizabeth', 'Elise', 'Catherine', 'Katrina', 'Kate', 'Katya', 'Maya', 'Mia', 'Myah', 'Lea', 'Leah', 'Leia', 'Emilia', 'Emily', 'Emelie', 'Amy', 'Aimee', 'Maria', 'Marija', 'Mariah', 'Marie', 'Anna', 'Hannah', 'Ann', 'Sofia', 'Anastasia', 'Daria', 'Victoria', 'Alexandra', 'Evelina', 'Amelia', 'Andreea', 'Valeria', 'Gabriela', 'Victoria', 'Giulia', 'Chloe', 'Emma', 'Anna', 'Jelena', 'Milica', 'Marija', 'Ivana', 'Milena', 'Ana', 'Dragana', 'Radmila', 'Vesna', 'Ljiljana', 'Sofija', 'Sara', 'Masa', 'Dunja', 'Jana', 'Teodora', 'Jovana', 'Helena', 'Anja', 'Hana', 'Anna', 'Emma', 'Tess', 'Sophie', 'Julia', 'Zoë', 'Evi', 'Mila', 'Sara', 'Eva', 'Fenna', 'Lotte', 'Emily', 'Ella', 'Grace', 'Sophie', 'Olivia', 'Anna', 'Amelia', 'Aoife', 'Lucy', 'Ava', 'Nora', 'Emma', 'Sara', 'Sofie', 'Sofia', 'Maja', 'Olivia', 'Ella', 'Ingrid', 'Emilie', 'Zuzanna', 'Julia', 'Lena', 'Maja', 'Hanna', 'Zofia', 'Amelia', 'Alicja', 'Aleksandra', 'Natalia', 'Maria', 'Leonor', 'Matilde', 'Beatriz', 'Carolina', 'Mariana', 'Ana', 'Inês', 'Margarida', 'Sofia', 'Maria', 'Elena', 'Ioana', 'Andreea', 'Sofia', 'Alexandra', 'Antonia', 'Daria', 'Ana', 'Gabriela', 'Sofiya', 'Sofya', 'Mariya', 'Marya', 'Anna', 'Anastasiya', 'Viktoriya', 'Yelizaveta', 'Polina', 'Alisa', 'Darya', 'Dariya', 'Alexandra', 'Anastasia', 'Yelena', 'Olga', 'Natalia', 'Yekaterina', 'Anna', 'Tatiana', 'Maria', 'Irina', 'Yulia', 'Olivia', 'Emily', 'Sophie', 'Isla', 'Ava', 'Amelia', 'Jessica', 'Ella', 'Lucy', 'Charlotte', 'Milica', 'Jelena', 'Marija', 'Mirjana', 'Dragana', 'Snezana', 'Ljiljana', 'Ivana', 'Ana', 'Gordana', 'Milica', 'Andela', 'Jovana', 'Ana', 'Teodora', 'Katarina', 'Marija', 'Sara', 'Anastasija', 'Aleksandra', 'Sofia', 'Nina', 'Natalia', 'Nela', 'Viktoria', 'Ema', 'Laura', 'Michaela', 'Kristina', 'Simona', 'Zala', 'Eva', 'Ema', 'Lara', 'Sara', 'Masa', 'Mia', 'Ana', 'Neza', 'Zoja', 'Lucia', 'Martina', 'Maria', 'Sofia', 'Paula', 'Daniela', 'Valeria', 'Alba', 'Julia', 'Noa', 'Ane', 'June', 'Nahia', 'Irati', 'Laia', 'Nora', 'Izaro', 'Lucia', 'Malen', 'Uxue', 'Martina', 'Julia', 'Laia', 'Lucia', 'Maria', 'Emma', 'Aina', 'Paula', 'Noa', 'Carla', 'Alice', 'Lilly', 'Maja', 'Elsa', 'Ella', 'Alicia', 'Olivia', 'Julia', 'Ebba', 'Wilma', 'Mia', 'Emma', 'Elena', 'Sofia', 'Lena', 'Emilia', 'Lara', 'Anna', 'Laura', 'Mila', 'Sofiya', 'Anastasiya', 'Anna', 'Hanna', 'Mariya', 'Alisa', 'Viktoriya', 'Veronika', 'Polina', 'Luna', 'Olivia', 'Amelia', 'Ella', 'Ava', 'Isla', 'Emily', 'Evie', 'Mia', 'Lily', 'Isabelle']
    europeNames["neut"] = ['Aderyn', 'Aednat', 'Aemilia', 'Aeron', 'Aeschere', 'Aeslin', 'Afallon', 'Aiko', 'Aislin', 'Angus', 'Ashley', 'Avery', 'Awen', 'Bairn', 'Beagan', 'Blaine', 'Blair', 'Briar', 'Bryn', 'Cailean', 'Cameron', 'Carlyn', 'Carol', 'Clair', 'Coney', 'Cory', 'Cymbaline', 'Daire', 'Dove', 'Dylan', 'Earley', 'Eldhrimnir', 'Endewyn', 'Esprit', 'Evelyn', 'Fannar', 'Greer', 'Gwyneira', 'Harden', 'Harley', 'Hayden', 'Heidrun', 'Ivo', 'Kai', 'Kieran', 'Korrigan', 'Lumi', 'Murtagh', 'Neave', 'Nevada', 'Orla', 'Osier', 'Paris', 'Quince', 'Raleigh', 'Rana', 'Robin', 'Also', 'Rowan', 'Ruari', 'Rue', 'Ryan', 'Savin', 'Savine', 'Seanan', 'Seren', 'Shannon', 'Solana', 'Starling', 'Suvi', 'Teagan', 'Thorley', 'Tyler', 'Vail', 'Vale', 'Vernal', 'Vyri', 'Wynnfrith', 'Yvonne', 'Zenon']
    europeNames["sur"] = ['Gruber', 'Huber', 'Bauer', 'Wagner', 'Muller', 'Pichler', 'Steiner', 'Moser', 'Mayer', 'Azerbaijan', 'Quliyev', 'Abdullayev', 'Abbasov', 'Belgium', 'January', 'December', 'Dubois', 'Lambert', 'Dupont', 'Martin', 'Simon', 'Bosnia', 'Hodzic', 'Hadzic', 'Cengic', 'Delic', 'Demirovic', 'Kovacevic', 'Tahirovic', 'Ferhatovic', 'Muratovic', 'Ibrahimovic', 'Hasanovic', 'Mehmedovic', 'Salihovic', 'Terzic', 'Ademovic', 'Adilovic', 'Delemovic', 'Zukic', 'Krlicevic', 'Suljic', 'Ahmetovic', 'Kovacevic', 'Subotic', 'Savic', 'Popovic', 'Jovanovic', 'Petrovic', 'Duric', 'Babic', 'Lukic', 'Knezevic', 'Markovic', 'Ilic', 'Dukic', 'Vukovic', 'Vujic', 'Simic', 'Radic', 'Nikolic', 'Maric', 'Mitrovic', 'Tomic', 'Bozic', 'Golubovic', 'Mirkovic', 'Croatia', 'Horvat', 'Kovacevic', 'Babic', 'Maric', 'Juric', 'Novak', 'Kovacic', 'Knezevic', 'Vukovic', 'Markovic', 'Petrovic', 'Matic', 'Tomic', 'Pavlovic', 'Kovac', 'Bozic', 'Blazevic', 'Grgic', 'Pavic', 'Radic', 'Peric', 'Filipovic', 'Saric', 'Lovric', 'Vidovic', 'Perkovic', 'Popovic', 'Bosnjak', 'Jukic', 'Barisic', 'Denmark', 'January', 'Nielsen', 'Jensen', 'Hansen', 'Pedersen', 'Andersen', 'Christensen', 'Larsen', 'Sorensen', 'Rasmussen', 'Estonia', 'Tamm', 'Saar', 'Sepp', 'Mägi', 'Kask', 'Kukk', 'Rebane', 'Ilves', 'Pärn', 'Koppel', 'Ivanov', 'Smirnov', 'Vassiljev', 'Petrov', 'Kuznetsov', 'Mihhailov', 'Pavlov', 'Semjonov', 'Andrejev', 'Aleksejev', 'Most', 'Joensen', 'Hansen', 'Jacobsen', 'Olsen', 'Petersen', 'Poulsen', 'Johannesen', 'Thomsen', 'Nielsen', 'Finland', 'Korhonen', 'Virtanen', 'Mäkinen', 'Nieminen', 'Mäkelä', 'Hämäläinen', 'Laine', 'Heikkinen', 'Koskinen', 'Most', 'Johansson', 'Nyman', 'Lindholm', 'Karlsson', 'Andersson', 'France', 'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel', 'Girard', 'Andre', 'Lefèvre', 'Mercier', 'Dupont', 'Lambert', 'Bonnet', 'Francois', 'Martinez', 'Muller', 'Schmidt', 'Schneider', 'Fischer', 'Meyer', 'Weber', 'Wagner', 'Schulz', 'Becker', 'Nagy', 'Kovacs', 'Toth', 'Szabo', 'Horvath', 'Varga', 'Kiss', 'Molnar', 'Nemeth', 'Farkas', 'Balogh', 'Papp', 'Lakatos', 'Takacs', 'Juhasz', 'Meszaros', 'Olah', 'Simon', 'Racz', 'Fekete', 'Szilagyi', 'Torok', 'Feher', 'Balazs', 'Gal', 'Most', 'Blondal', 'Thorarensen', 'Hansen', 'Olsen', 'Andersen', 'Petersen', 'Moller', 'Nielsen', 'Waage', 'Fjeldsted', 'Norðdahl', 'Ireland', 'Murphy', 'Walsh', 'Smith', 'Doyle', 'Mccarthy', 'Kennedy', 'Lynch', 'Murray', 'Rossi', 'Red', 'Russo', 'Ferrari', 'Blacksmith', 'Esposito', 'Exposed', 'Bianchi', 'White', 'Romano', 'Roman', 'Colombo', 'Dove', 'Bruno', 'Brown', 'Ricci', 'Curly', 'Greco', 'Greek', 'Marino', 'Gallo', 'Rooster', 'Conti', 'Count', 'Costa', 'Coast', 'Mancini', 'Left', 'Giordano', 'Jordan', 'Rizzo', 'Curly', 'Lombardi', 'Lombard', 'Barbieri', 'Barber', 'Moretti', 'Brown', 'Fontana', 'Fountain', 'Caruso', 'Mariani', 'Marian', 'Ferrara', 'Blacksmith', 'Santoro', 'Sanctorum', 'Rinaldi', 'Reynold', 'Leone', 'Lion', 'Longo', 'Long', 'Galli', 'Roosters', 'Martini', 'Martin', 'Martinelli', 'Martin', 'Serra', 'Saw', 'Conte', 'Count', 'Vitale', 'Vitale', 'Marchetti', 'Messina', 'Messina', 'Gentile', 'Gentle', 'Villa', 'Marini', 'Lombardo', 'Lombard', 'Coppola', 'Ferri', 'Parisi', 'Bianco', 'White', 'Amato', 'Beloved', 'Fabbri', 'Blacksmith', 'Gatti', 'Cats', 'Sala', 'Sala', 'Morelli', 'Grasso', 'Fat', 'Pellegrini', 'Pilgrims', 'Ferraro', 'Blacksmith', 'Monti', 'Mountains', 'Palumbo', 'Pigeon', 'Grassi', 'Fat', 'Testa', 'Head', 'Valentini', 'Carbone', 'Coal', 'Benedetti', 'Silvestri', 'Farina', 'Flour', 'Martino', 'Martin', 'Bernardi', 'Barnard', 'Caputo', 'Big', 'Mazza', 'Sanna', 'Fang', 'Fiore', 'Flower', 'Pellegrino', 'Pilgrim', 'Giuliani', 'Rizzi', 'Curly', 'Di', 'Cattaneo', 'Captain', 'Rossetti', 'Orlando', 'Basile', 'Basil', 'Neri', 'Black', 'Barone', 'Baron', 'Palmieri', 'Palmer', 'Riva', 'Shore', 'Romeo', 'Franco', 'Frank', 'Sorrentino', 'Pagano', 'Pagan', 'Piras', 'Pear', 'Ruggiero', 'Rodger', 'Montanari', 'Highlander', 'Battaglia', 'Fight', 'Bellini', 'Castelli', 'Castles', 'Guerra', 'War', 'Poli', 'Valente', 'Ferretti', 'Krasniqi', 'Gashi', 'Berisha', 'Morina', 'Shala', 'Bytyqi', 'Hasani', 'Kastrati', 'Kryeziu', 'Latvia', 'Berzins', 'Kalnins', 'Ozolins', 'Jansons', 'Ozols', 'Liepins', 'Krumins', 'Balodis', 'Eglitis', 'Zarins', 'Petersons', 'Vitols', 'Klavins', 'Karklins', 'Vanags', 'Kazlauskas', 'Jankauskas', 'Petrauskas', 'Stankevicius', 'Vasiliauskas', 'Butkus', 'Zukauskas', 'Paulauskas', 'Urbonas', 'Kavaliauskas', 'Entries', 'Borg', 'Camilleri', 'Vella', 'Farrugia', 'Zammit', 'Galea', 'Micallef', 'Grech', 'Attard', 'Spiteri', 'Rusu', 'Ceban', 'Ciobanu', 'Turcan', 'Cebotari', 'Sîrbu', 'Lungu', 'Munteanu', 'Rotari', 'Montenegro', 'Popovic', 'Markovic', 'Vujovic', 'Radovic', 'Ivanovic', 'Radulovic', 'Jovanovic', 'Perovic', 'Vukovic', 'Kovacevic', 'County', 'Percent', 'English', 'Jansen', 'Johnson', 'Van', 'Van', 'Bakker', 'Baker', 'Janssen', 'Johnson', 'Visser', 'Fisher', 'Smit', 'Smith', 'Mayor', 'Mulder', 'Miller', 'Bos', 'Bush', 'Vos', 'Fox', 'Peters', 'Peters', 'Hendriks', 'Henderson', 'Van', 'Dekker', 'Thatcher', 'Brouwer', 'Brewer', 'Dijkstra', 'Smits', 'Smith', 'Van', 'Vd', 'Van', 'Van', 'Andov', 'Angelov', 'Bogdanov', 'Bozinov', 'Brankov', 'Damcevski', 'Davidov', 'Dimitrov', 'Donev', 'Filipov', 'Georgiev', 'Ivanov', 'Ivanovski', 'Janev', 'Kitanovski', 'Koloski', 'Kostovski', 'Kostov', 'Manasievski', 'Markov', 'Markovski', 'Markoski', 'Matovski', 'Mladenovski', 'Nikolovski', 'Pavlovski', 'Penov', 'Petkov', 'Petrevski', 'Petrovski', 'Popoff', 'Popovski', 'Ristevski', 'Stojanov', 'Trajanoski', 'Trajanovski', 'Trajcevski', 'Trajkovski', 'Hansen', 'Johansen', 'Olsen', 'Larsen', 'Andersen', 'Pedersen', 'Nilsen', 'Kristiansen', 'Jensen', 'Karlsen', 'Johnsen', 'Pettersen', 'Eriksen', 'Berg', 'Haugen', 'Hagen', 'Johannessen', 'Andreassen', 'Jacobsen', 'Dahl', 'Jorgensen', 'Halvorsen', 'Henriksen', 'Lund', 'Nowak', 'Kowalski', 'Wisniewski', 'Wojcik', 'Kowalczyk', 'Kaminski', 'Lewandowski', 'Zielinski', 'Szymanski', 'Polish', 'Most', 'Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues', 'Martins', 'Jesus', 'Sousa', 'Fernandes', 'Goncalves', 'Gomes', 'Lopes', 'Marques', 'Alves', 'Almeida', 'Ribeiro', 'Pinto', 'Carvalho', 'Teixeira', 'Moreira', 'Correia', 'Mendes', 'Nunes', 'Soares', 'Vieira', 'Monteiro', 'Cardoso', 'Rocha', 'Neves', 'Coelho', 'Cruz', 'Cunha', 'Pires', 'Duarte', 'Reis', 'Simões', 'Antunes', 'Matos', 'Fonseca', 'Machado', 'Araujo', 'Barbosa', 'Tavares', 'Lourenco', 'Castro', 'Figueiredo', 'Azevedo', 'Freitas', 'Popa', 'Popescu', 'Pop', 'Radu', 'Dumitru', 'Stan', 'Stoica', 'Gheorghe', 'Matei', 'Ciobanu', 'Ionescu', 'Rusu', 'Most', 'Those', 'Jovanovic', 'Petrovic', 'Nikolic', 'Markovic', 'Dordevic', 'Stojanovic', 'Ilic', 'Stankovic', 'Pavlovic', 'Milosevic', 'Horvath', 'Kovac', 'Varga', 'Toth', 'Nagy', 'Balaz', 'Szabo', 'Molnar', 'Balog', 'Lukac', 'Novak', 'Kovacs', 'Polak', 'Gajdos', 'Kollar', 'Hudak', 'Nemeth', 'Kovacik', 'Olah', 'Oravec', 'Hungarians', 'Novak', 'Horvat', 'Kovacic', 'Krajnc', 'Zupancic', 'Potocnik', 'Kovac', 'Mlakar', 'Kos', 'Vidmar', 'Golob', 'Turk', 'Bozic', 'Kralj', 'Korosec', 'Zupan', 'Bizjak', 'Hribar', 'Kotnik', 'Kavcic', 'Rozman', 'Kastelic', 'Oblak', 'Zagar', 'Petek', 'Hocevar', 'Kolar', 'Kosir', 'Koren', 'Klemencic', 'Garcia', 'Fernandez', 'Gonzalez', 'Rodriguez', 'Lopez', 'Martinez', 'Sanchez', 'Perez', 'Martin', 'Gomez', 'Ruiz', 'Hernandez', 'Jimenez', 'Diaz', 'Alvarez', 'Moreno', 'Munoz', 'Alonso', 'Variation', 'Gutierrez', 'Romero', 'Pilgrim', 'Navarro', 'Torres', 'Dominguez', 'Gil', 'Vazquez', 'Serrano', 'Highlander', 'Ramos', 'Blanco', 'White', 'Sanz', 'Castro', 'Suarez', 'Ortega', 'Rubio', 'Molina', 'Delgado', 'Skinny', 'Ramirez', 'Morales', 'Blackberry', 'Ortiz', 'Marin', 'Latin', 'Iglesias', 'Churches', 'Data', 'Gonzalez', 'Rodriguez', 'Hernandez', 'Perez', 'Garcia', 'Martin', 'Santana', 'Diaz', 'Suarez', 'Sweden', 'Andersson', 'Johansson', 'Karlsson', 'Nilsson', 'Eriksson', 'Larsson', 'Olsson', 'Persson', 'Svensson', 'Gustafsson', 'Pettersson', 'Jonsson', 'Jansson', 'Hansson', 'Bengtsson', 'Jonsson', 'Lindberg', 'Jakobsson', 'Magnusson', 'Olofsson', 'Andersson', 'Johansson', 'Nilsson', 'Larsson', 'Persson', 'Blind', 'Jonsson', 'Eriksson', 'Nutti', 'Labba', 'Bianchi', 'Bernasconi', 'Fontana', 'Crivelli', 'Galli', 'Cereghetti', 'Colombo', 'Rossi', 'Ferrari', 'Cavadini', 'Sante', 'Ravelli', 'Giovanni', 'Piero', 'Muller', 'Meier', 'Schmid', 'Keller', 'Weber', 'Huber', 'Meyer', 'Schneider', 'Steiner', 'Fischer', 'Brunner', 'Baumann', 'Gerber', 'Frei', 'Moser', 'Yilmaz', 'Kaya', 'Demir', 'Sahin', 'Celik', 'Yildiz', 'Yildirim', 'Ozturk', 'Aydin', 'Ozdemir', 'Arslan', 'Dogan', 'Kilic', 'Aslan', 'Khan', 'Kara', 'Koc', 'Kurt', 'Ozkan', 'Simsek', 'Melnyk', 'Shevchenko', 'Boyko', 'Kovalenko', 'Bondarenko', 'Tkachenko', 'Kovalchuk', 'Kravchenko', 'Oliynyk', 'Shevchuk', 'Koval', 'Polishchuk', 'Bondar', 'Tkachuk', 'Moroz', 'Marchenko', 'Lysenko', 'Rudenko', 'Savchenko', 'Petrenko', 'Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Robinson', 'Greater', 'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas', 'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson', 'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander', 'Wilson', 'Campbell', 'Kelly', 'Johnston', 'Moore', 'Thompson', 'Smyth', 'Brown', 'Scotland', 'Smith', 'Brown', 'Wilson', 'Robertson', 'Thomson', 'Campbell', 'Stewart', 'Anderson', 'Scott', 'Wales', 'Jones', 'Williams', 'Davies', 'Evans', 'Thomas', 'Roberts', 'Lewis', 'Hughes', 'Morgan']
    fantasyNames["masc"] = ['Lydan', 'Syrin', 'Ptorik', 'Joz', 'Varog', 'Gethrod', 'Hezra', 'Feron', 'Ophni', 'Colborn', 'Fintis', 'Gatlin', 'Jinto', 'Hagalbar', 'Krinn', 'Lenox', 'Revvyn', 'Hodus', 'Dimian', 'Paskel', 'Kontas', 'Weston', 'Azamarr', 'Jather', 'Tekren', 'Jareth', 'Adon', 'Zaden', 'Eune', 'Graff', 'Tez', 'Jessop', 'Gunnar', 'Pike', 'Domnhar', 'Baske', 'Jerrick', 'Mavrek', 'Riordan', 'Wulfe', 'Straus', 'Tyvrik', 'Henndar', 'Favroe', 'Whit', 'Jaris', 'Renham', 'Kagran', 'Lassrin', 'Vadim', 'Arlo', 'Quintis', 'Vale', 'Caelan', 'Yorjan', 'Khron', 'Ishmael', 'Jakrin', 'Fangar', 'Roux', 'Baxar', 'Hawke', 'Gatlen', 'Barak', 'Nazim', 'Kadric', 'Paquin', 'Kent', 'Moki', 'Rankar', 'Lothe', 'Ryven', 'Clawsen', 'Pakker', 'Embre', 'Cassian', 'Verssek', 'Dagfinn', 'Ebraheim', 'Nesso', 'Eldermar', 'Rivik', 'Rourke', 'Barton', 'Hemm', 'Sarkin', 'Blaiz', 'Talon', 'Agro', 'Zagaroth', 'Turrek', 'Esdel', 'Lustros', 'Zenner', 'Baashar', 'Dagrod', 'Gentar', 'Feston']
    fantasyNames["fem"] = ['Syrana', 'Resha', 'Varin', 'Wren', 'Yuni', 'Talis', 'Kessa', 'Magaltie', 'Aeris', 'Desmina', 'Krynna', 'Asralyn', 'Herra', 'Pret', 'Kory', 'Afia', 'Tessel', 'Rhiannon', 'Zara', 'Jesi', 'Belen', 'Rei', 'Ciscra', 'Temy', 'Renalee', 'Estyn', 'Maarika', 'Lynorr', 'Tiv', 'Annihya', 'Semet', 'Tamrin', 'Antia', 'Reslyn', 'Basak', 'Vixra', 'Pekka', 'Xavia', 'Beatha', 'Yarri', 'Liris', 'Sonali', 'Razra', 'Soko', 'Maeve', 'Everen', 'Yelina', 'Morwena', 'Hagar', 'Palra', 'Elysa', 'Sage', 'Ketra', 'Lynx', 'Agama', 'Thesra', 'Tezani', 'Ralia', 'Esmee', 'Heron', 'Naima', 'Rydna', 'Sparrow', 'Baakshi', 'Ibera', 'Phlox', 'Dessa', 'Braithe', 'Taewen', 'Larke', 'Silene', 'Phressa', 'Esther', 'Anika', 'Rasy', 'Harper', 'Indie', 'Vita', 'Drusila', 'Minha', 'Surane', 'Lassona', 'Merula', 'Kye', 'Jonna', 'Lyla', 'Zet', 'Orett', 'Naphtalia', 'Turi', 'Rhays', 'Shike', 'Hartie', 'Beela', 'Leska', 'Vemery', 'Lunex', 'Fidess', 'Tisette', 'Partha']
    fantasyNames["neut"] = ['Aderyn', 'Aednat', 'Aemilia', 'Aeron', 'Aeschere', 'Aeslin', 'Afallon', 'Aiko', 'Aislin', 'Angus', 'Ashley', 'Avery', 'Awen', 'Bairn', 'Beagan', 'Blaine', 'Blair', 'Briar', 'Bryn', 'Cailean', 'Cameron', 'Carlyn', 'Carol', 'Clair', 'Coney', 'Cory', 'Cymbaline', 'Daire', 'Dove', 'Dylan', 'Earley', 'Eldhrimnir', 'Endewyn', 'Esprit', 'Evelyn', 'Fannar', 'Greer', 'Gwyneira', 'Harden', 'Harley', 'Hayden', 'Heidrun', 'Ivo', 'Kai', 'Kieran', 'Korrigan', 'Lumi', 'Murtagh', 'Neave', 'Nevada', 'Orla', 'Osier', 'Paris', 'Quince', 'Raleigh', 'Rana', 'Robin', 'Also', 'Rowan', 'Ruari', 'Rue', 'Ryan', 'Savin', 'Savine', 'Seanan', 'Seren', 'Shannon', 'Solana', 'Starling', 'Suvi', 'Teagan', 'Thorley', 'Tyler', 'Vail', 'Vale', 'Vernal', 'Vyri', 'Wynnfrith', 'Yvonne', 'Zenon']
    fantasyNames["sur"] = ['Atwater', 'Agassi', 'Apatow', 'Akagawa', 'Averescu', 'Arrington', 'Agrippa', 'Aiken', 'Albertson', 'Alexander', 'Amado', 'Anders', 'Ashsorrow', 'Humblecut', 'Ashbluff', 'Marblemaw', 'Armas', 'Akka', 'Aoki', 'Aldrich', 'Apak', 'Alinsky', 'Desai', 'Darby', 'Draper', 'Dwyer', 'Dixon', 'Danton', 'Desmith', 'Ditka', 'Dominguez', 'Decker', 'Dobermann', 'Dunlop', 'Dumont', 'Dandridge', 'Diamond', 'Dobra', 'Dukas', 'Agnello', 'Alterio', 'Bidbury', 'Botkin', 'Benoit', 'Biddercombe', 'Baldwin', 'Bennett', 'Bourland', 'Boadle', 'Bender', 'Best', 'Bobshaw', 'Bersa', 'Belt', 'Bourn', 'Barke', 'Beebe', 'Banu', 'Bozzelli', 'Bogaerts', 'Blanks', 'Evert', 'Eastwood', 'Elway', 'Eslinger', 'Ellerbrock', 'Eno', 'Endo', 'Etter', 'Ebersol', 'Everson', 'Esapa', 'Ekker', 'Escobar', 'Eggleston', 'Ermine', 'Erickson', 'Keller', 'Kessler', 'Kobayashi', 'Klecko', 'Kicklighter', 'Kidder', 'Kershaw', 'Kaminsky', 'Kirby', 'Keene', 'Kenny', 'Keogh', 'Kipps', 'Kendrick', 'Kuang', 'Fairchild', 'October', 'Vespertine', 'Fellowes', 'Omen', 'Willow', 'Gannon', 'Presto', 'Windward', 'Grell', 'Powers', 'Wixx', 'Halliwell', 'Quellings', 'Xanthos', 'Hightower', 'Quill', 'Xenides', 'Idlewind', 'Rast', 'Chamillet', 'Bougaitelet', 'Hallowswift', 'Coldsprinter', 'Winddane', 'Yarrow', 'Illfate', 'Riddle', 'Yew', 'Jacaranda', 'Yearwood', 'Yellen', 'Yaeger', 'Yankovich', 'Yamaguchi', 'Yarborough', 'Youngblood', 'Yanetta', 'Yadao', 'Winchell', 'Winters', 'Walsh', 'Whalen', 'Watson', 'Wooster', 'Woodson', 'Winthrop', 'Wall', 'Sacredpelt', 'Rapidclaw', 'Hazerider', 'Shadegrove', 'Wight', 'Webb', 'Woodard', 'Wixx', 'Wong', 'Whesker', 'Yale', 'Yasumoto', 'Yates', 'Younger', 'Yoakum', 'York', 'Rigby', 'Zaba', 'Surrett', 'Swiatek', 'Sloane', 'Stapleton', 'Seibert', 'Stroud', 'Strode', 'Stockton', 'Scardino', 'Spacek', 'Spieth', 'Stitchen', 'Stiner', 'Soria', 'Saxon', 'Shields', 'Stelly', 'Steele', 'Chanassard', 'Ronchessac', 'Boneflare', 'Monsterbelly', 'Truthbelly', 'Sacredmore', 'Malfoy', 'Moses', 'Moody', 'Morozov', 'Mason', 'Metcalf', 'Mc', 'Montero', 'Molinari', 'Marsh', 'Moffett', 'Mc', 'Manus', 'Malenko', 'Mullinax', 'Morrissey', 'Mantooth', 'Mintz']
    futuristicNames["masc"] = ['Adlai', 'Alaric', 'Anakin', 'Arsenio', 'Artemis', 'Aurelius', 'Auryn', 'Azriel', 'Cael', 'Calihan', 'Carrew', 'Cashel', 'Caspian', 'Cassian', 'Cedro', 'Cian', 'Cillian', 'Colton', 'Crispin', 'Drake', 'Derry', 'Edsel', 'Elson', 'Elwyn', 'Ephraim', 'Esai', 'Espen', 'Evander', 'Everard', 'Eythor', 'Finian', 'Fio', 'Freddy', 'Harlin', 'Jacob', 'Jax', 'Jethro', 'Jonas', 'Kaiser', 'Kalel', 'Kasper', 'Klay', 'Knox', 'Luca', 'Ludek', 'Micaiah', 'Mircea', 'Noe', 'Nye', 'Oren', 'Perrin', 'Renan', 'Rivo', 'Ruairi', 'Rui', 'Rune', 'Rye', 'Ryker', 'Sagan', 'Salix', 'Saylor', 'Schyler', 'Silas', 'Solon', 'Stellan', 'Sulien', 'Sven', 'Tae', 'Theron', 'Tovio', 'Torin', 'Tyrion', 'Uriah', 'Wilbur', 'Wystan', 'Xander', 'Xavion', 'Zaiden', 'Zen', 'Zephyr']
    futuristicNames["fem"] = ['Alessa', 'Annora', 'Archie', 'Ariana', 'Ariella', 'Arvilla', 'Arwen', 'Arya', 'Astoria', 'Astra', 'Astrid', 'Ayelet', 'Azura', 'Baila', 'Blaise', 'Blythe', 'Caia', 'Calla', 'Callista', 'Camila', 'Candela', 'Carabelle', 'Ceres', 'Charolet', 'Colma', 'Cosima', 'Crescentia', 'Cytherea', 'Dael', 'Dalla', 'Dawnelle', 'Delya', 'Drea', 'Eila', 'Elenyi', 'Eliette', 'Elowen', 'Elya', 'Ensley', 'Eowyn', 'Erinna', 'Etta', 'Eulalie', 'Evrim', 'Evuska', 'Ezri', 'Falynn', 'Fantasia', 'Felicity', 'Harper', 'Ilaria', 'Imelda', 'Ivara', 'Jada', 'Junia', 'Juniper', 'Karis', 'Kiska', 'Luna', 'Lyra', 'Lystra', 'Malone', 'Mazarine', 'Minerva', 'Morena', 'Natania', 'Neriah', 'Nolwenn', 'Novelia', 'Ophelia', 'Orsa', 'Paisley', 'Rhett', 'Riella', 'Saretta', 'Secora', 'Siloh', 'Thyra', 'Tove', 'Vanina', 'Violet', 'Wynn', 'Zeline', 'Zosia']
    futuristicNames["neut"] = ['Aderyn', 'Aednat', 'Aemilia', 'Aeron', 'Aeschere', 'Aeslin', 'Afallon', 'Aiko', 'Aislin', 'Angus', 'Ashley', 'Avery', 'Awen', 'Bairn', 'Beagan', 'Blaine', 'Blair', 'Briar', 'Bryn', 'Cailean', 'Cameron', 'Carlyn', 'Carol', 'Clair', 'Coney', 'Cory', 'Cymbaline', 'Daire', 'Dove', 'Dylan', 'Earley', 'Eldhrimnir', 'Endewyn', 'Esprit', 'Evelyn', 'Fannar', 'Greer', 'Gwyneira', 'Harden', 'Harley', 'Hayden', 'Heidrun', 'Ivo', 'Kai', 'Kieran', 'Korrigan', 'Lumi', 'Murtagh', 'Neave', 'Nevada', 'Orla', 'Osier', 'Paris', 'Quince', 'Raleigh', 'Rana', 'Robin', 'Also', 'Rowan', 'Ruari', 'Rue', 'Ryan', 'Savin', 'Savine', 'Seanan', 'Seren', 'Shannon', 'Solana', 'Starling', 'Suvi', 'Teagan', 'Thorley', 'Tyler', 'Vail', 'Vale', 'Vernal', 'Vyri', 'Wynnfrith', 'Yvonne', 'Zenon']
    futuristicNames["sur"] = ['Alcantar', 'Alken', 'Kiani', 'Verrill', 'Racine', 'Kiani', 'Solari', 'Jaenke', 'Bowdoin', 'Racine', 'Weyer', 'Wynn', 'Sanghvi', 'McRaven', 'Severt', 'Lavigne', 'Solari', 'Lockley', 'Vangelos', 'Irani', 'Wescott', 'Kniffin', 'Graydon', 'Bowdoin', 'Wyse', 'Lavigne', 'Dewitt', 'Kader', 'Nesheim', 'Woldt', 'Wakeman', 'Dilucca', 'Alcantar', 'Dewitt', 'Amano', 'Maille', 'Rhyne', 'Solari', 'Sabine', 'Berrett', 'Mo-Chi', 'Siu', 'Fu', 'Liu-Sho', 'Bo-She', 'Xi', 'Sai', 'Wei', 'Kway-Koi', 'Hwa', 'Hi', 'Zhao', 'Chao-Loo', 'Chi', 'Hu-Tao', 'Too', 'Zi', 'Huo', 'Mao', 'Le-Ju', 'Hu-Jue', 'Miao', 'Chwai-Hai', 'Xia', 'Fei-Na', 'Lee-Li', 'Xue-Ha', 'Mae-Jai', 'Shoi-Xiu', 'Na', 'Ku', 'Fu', 'Yuan', 'Na', 'Wei', 'Shu', 'Gui', 'Xia', 'Pei', 'Jue', 'Teiki', 'Hiro', 'Kako', 'Sane', 'Tada', 'Toyoto', 'Toshi', 'Tetsu', 'Taki', 'Masu', 'Kumi', 'Yumit', 'Mayoko', 'Fusu', 'Yukomi', 'Mide', 'Suzue', 'Sachie', 'Shina', 'Kichi', 'Gavrina', 'Tukhborei', 'Mikova', 'Groshistya', 'Bobore', 'Kina', 'Ovanov', 'Gova', 'Biniky', 'Plobenko', 'Pina', 'Mova', 'Kova', 'Ploudema', 'Nikofa', 'Tyrsko', 'Semonte', 'Sova', 'Moltova', 'Pova', 'Kuva', 'Lebore', 'Bina', 'Pove', 'Ginova', 'Supoloi', 'Ovarov', 'Kova', 'Olev', 'Cherova', 'Mova', 'Prova', 'Metukhba', 'Ovarnov', 'Denkatze', 'Gulova', 'Sovelai', 'Biky', 'Sova', 'Kolina', 'Pere', 'Brusson', 'Rookson', 'Diazal', 'Whowards', 'Hezal', 'Righte', 'Hayeson', 'Rogers', 'Garce', 'Jamoor', 'Robak', 'Cooker', 'Tere', 'Wisanch', 'Bryante', 'Grownes', 'Butly', 'Turnes', 'Carte', 'Russon', 'Reedez', 'Wriffost', 'Jenker', 'Rodra', 'Grezal', 'Grodre', 'Ancher', 'Colee', 'Thomart', 'Helly', 'Coxand', 'Sones', 'Pery', 'Jamill', 'Sanchy', 'Coxand', 'Kera', 'Grezal', 'Wison']
    listExceptionsEnvironment = ["japan", "europe", "america", "historical", "modern", "futuristic", "fantasy"]
    listExceptionsCharacterTypes = ["cis_men", "cis_women", "nonbinary", "trans_men", "trans_women", "futanari"]
    listExceptionsCharacterSpecies = ['mammals', 'reptiles', 'fish', 'birds', 'insects', 'arachnids', 'humans', 'elves', 'dwarves', 'halflings', 'gnomes', 'tieflings', 'merfolk', 'orcs', 'goliaths', 'goblinoids', 'ilithids', 'slimes', 'tentacles', 'dryads', 'harpies', 'lamia', 'centaurs', 'minotaurs', 'giants', 'werebeasts', 'vampires', 'undead', 'demons', 'angels', 'faeries', 'cyborgs', 'androids', 'robots', 'humanoid_aliens', 'aliens']
    listExceptionsPlay = ['romance', 'kissing', 'cuddling', 'petting', 'grinding', 'titjobs', 'ass_play', 'manual_sex', 'oral_sex', 'intercrural_sex', 'penetrative_sex', 'basic_toys', 'age_play', 'bondage', 'biting', 'breast_play', 'impact_play', 'orgasm_control', 'genitorture', 'cuckoldry', 'cupping', 'dom_and_sub', 'knife_play', 'electro_play', 'food_play', 'temperature_play', 'fire_play', 'fisting', 'foot_play', 'degradation', 'exhibition', 'pet_play', 'piss_play', 'consensual_nonconsent', 'sensory_deprivation', 'sounding', 'intoxicants', 'incest', 'bestiality', 'size_play', 'partial_growth', 'extreme_insertions', 'inflation', 'transformation', 'impregnation', 'oviposition', 'dubious_consent', 'nonconsent', 'torture', 'gore', 'soft_vore', 'hard_vore', 'snuff', 'necrophilia']
    poolEnvironments = []
    poolCharacterTypes = []
    poolCharacterSpecies = []
    poolScenes = []
    poolPlay = []
    def exceptionTrimmer(listName):
        config = configparser.ConfigParser()
        configPath = ap(f'{serverConfigs}\{guildID}.ini')
        config.read(configPath)
        if f'{channelID}' in config.sections():
            def getLISection(li):
                if li in config[f'{channelID}']:
                    return config[f'{channelID}']
                else:
                    return config['default']
            listName[:] = [li for li in listName if not getLISection(li).getboolean(li)]        
        else:
            listName[:] = [li for li in listName if not config['default'].getboolean(li)]       
    def exceptionTrimmerDM(listName):
        if f"{userID}" in DMConfig:
            def getLIDefault(li):
                if li in DMConfig[f"{userID}"]:
                    return DMConfig[f"{userID}"]
                else:
                    return DMConfigDefault
            listName[:] = [li for li in listName if not getLIDefault(li)[li]]
        else:
            listName[:] = [li for li in listName if not DMConfigDefault[li]]
    def poolPopulator(listName, exceptionsName, poolName):
        for ld in listName:
            if not any(item in ld.tags for item in exceptionsName):
                poolName.append(ld)
    if guildID:
        exceptionTrimmer(listExceptionsEnvironment)
        exceptionTrimmer(listExceptionsCharacterTypes)
        exceptionTrimmer(listExceptionsCharacterSpecies)
        exceptionTrimmer(listExceptionsPlay)
        playNumber = getConfigInt(guildID, channelID, "play_number")
        characterNumber = getConfigInt(guildID, channelID, "character_number")
        cisMen = getConfigBool(guildID, channelID, "cis_men")
        cisWomen = getConfigBool(guildID, channelID, "cis_women")
        humans = getConfigBool(guildID, channelID, "humans")
    else:
        exceptionTrimmerDM(listExceptionsEnvironment)
        exceptionTrimmerDM(listExceptionsCharacterTypes)
        exceptionTrimmerDM(listExceptionsCharacterSpecies)
        exceptionTrimmerDM(listExceptionsPlay)
        playNumber = getConfigDM(userID, "play_number")
        characterNumber = getConfigDM(userID, "character_number")
        cisMen = getConfigDM(userID, "cis_men")
        cisWomen = getConfigDM(userID, "cis_women")
        humans = getConfigDM(userID, "humans")
    poolPopulator(listEnvironments, listExceptionsEnvironment, poolEnvironments)
    poolPopulator(listCharacterTypes, listExceptionsCharacterTypes, poolCharacterTypes)
    poolPopulator(listCharacterSpecies, listExceptionsCharacterSpecies, poolCharacterSpecies)
    poolPopulator(listPlay, listExceptionsPlay, poolPlay)
    try:
        if cisMen or cisWomen:
            cisgenderBias = []
            if cisMen:
                cisgenderBias.append(ld('cis man', 'cis_men'))
            if cisWomen:
                cisgenderBias.append(ld('cis woman', 'cis_women'))
            for cis in range(0, ceil(len(poolCharacterTypes)*1.6)):
                poolCharacterTypes.append(random.choice(cisgenderBias))      
        if humans:
            for hu in range(0, len(poolCharacterSpecies)):
                poolCharacterSpecies.append(ld('a human', 'humans'))    
        environment = random.choice(poolEnvironments)
        for sce in listScenes:
            if all(item in environment.tags for item in sce.tags):
                poolScenes.append(sce) 
        scene = random.choice(poolScenes)
        characterText = []
        for ct in range(0, characterNumber):
            tempType = random.choice(poolCharacterTypes)
            tempSpecies = random.choice(poolCharacterSpecies)
            def nameFinder(type):
                if "europe" in environment.tags:
                    n = random.randint(1,12)
                    if n > 4:
                        return random.choice(europeNames[type])
                    if n == 4:
                        return random.choice(americaNames[type])
                    if n == 3:
                        return random.choice(japanNames[type])
                    if n == 2:
                        return random.choice(fantasyNames[type])
                    if n == 1:
                        return random.choice(futuristicNames[type])
                elif "japan" in environment.tags:
                    n = random.randint(1,12)
                    if n > 4:
                        return random.choice(japanNames[type])
                    if n == 4:
                        return random.choice(americaNames[type])
                    if n == 3:
                        return random.choice(europeNames[type])
                    if n == 2:
                        return random.choice(fantasyNames[type])
                    if n == 1:
                        return random.choice(futuristicNames[type])
                elif "fantasy" in environment.tags and len(environment.tags) == 1:
                    n = random.randint(1,12)
                    if n > 4:
                        return random.choice(fantasyNames[type])
                    if n == 4:
                        return random.choice(americaNames[type])
                    if n == 3:
                        return random.choice(japanNames[type])
                    if n == 2:
                        return random.choice(europeNames[type])
                    if n == 1:
                        return random.choice(futuristicNames[type])
                elif "futuristic" in environment.tags and len(environment.tags) == 1:
                    n = random.randint(1,12)
                    if n > 4:
                        return random.choice(futuristicNames[type])
                    if n == 4:
                        return random.choice(americaNames[type])
                    if n == 3:
                        return random.choice(japanNames[type])
                    if n == 2:
                        return random.choice(fantasyNames[type])
                    if n == 1:
                        return random.choice(europeNames[type])
                else:
                    n = random.randint(1,12)
                    if n > 4:
                        return random.choice(americaNames[type])
                    if n == 4:
                        return random.choice(europeNames[type])
                    if n == 3:
                        return random.choice(japanNames[type])
                    if n == 2:
                        return random.choice(fantasyNames[type])
                    if n == 1:
                        return random.choice(futuristicNames[type])
            if tempType.text in ["cis man", "trans man"]:
                tempFirstName = nameFinder("masc")
            elif tempType.text in ["cis woman", "trans woman", "futanari"]:
                tempFirstName = nameFinder("fem")
            else:
                tempFirstName = nameFinder("neut")
            tempSurName = nameFinder("sur")
            characterText.append(f"\n*{tempFirstName} {tempSurName}:* {tempSpecies.text} {tempType.text}")
        characterText = "".join(characterText)
        if playNumber <= len(poolPlay):
            playList = random.sample(poolPlay, playNumber)
        else:
            playList = poolPlay
        playText = []
        for pl in playList:
            playText.append(pl.text)
        playText = ", ".join(playText)
        promptText = ""
        if guildID:
            if getConfigBool(guildID, channelID, "environments"):
                promptText += f"\n**Setting:** {environment.text}"
            if getConfigBool(guildID, channelID, "characters"):
                promptText += f"\n**Characters:** {characterText}"
            if getConfigBool(guildID, channelID, "scenes"):
                promptText += f"\n**Scene:** {scene.text}"
            if getConfigBool(guildID, channelID, "play"):
                promptText += f"\n**Play Suggestions:** {playText}"
        else:
            if getConfigDM(userID,  "environments"):
                promptText += f"\n**Setting:** {environment.text}"
            if getConfigDM(userID,  "characters"):
                promptText += f"\n**Characters:** {characterText}"
            if getConfigDM(userID,  "scenes"):
                promptText += f"\n**Scene:** {scene.text}"
            if getConfigDM(userID,  "play"):
                promptText += f"\n**Play Suggestions:** {playText}"            
        if not addText:
            text = f">>> **LewdRobin Writing Prompt**{promptText}"
            return [text, True]
        else:
            promptCode = str(random.randint(1, 9999)).zfill(4)
            promptCodeLine = f"\n**Prompt Code:** {promptCode}"
            addConfig(guildID, channelID, "promptText", promptText)
            conMin = getConfig(guildID, channelID, "contributor_minimum")
            conMax = getConfig(guildID, channelID, "contributor_maximum")
            promptConLine = f"\n**Contributors:** 0/{conMax} ({conMin} required)"
            addConfig(guildID, channelID, "promptCode", promptCode)
            addConfig(guildID, channelID, "promptContributions", 0)
            contributorsConfig(guildID, channelID)
            text = promptHeader + promptText + promptCodeLine + promptConLine + promptReminder
            return [text, True]
    except:
        if addText:
            text = "Prompt generation failed. This happens on occasion. Press :arrows_counterclockwise: to try again. If generation continues to fail, make sure you have at least one item allowed from each prompt settings category."
            return [text, False]
        else:
            text = "Prompt generation failed. This happens on occasion. Press :arrows_clockwise: to try again. If generation continues to fail, make sure you have at least one item allowed from each prompt settings category."
            return [text, False]

def createGuildConfig(guildID):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    config.add_section('default')
    config.set('default', 'admin', 'none')
    config.set('default', 'moderator', 'none')
    config.set('default', 'genid', '0')
    config.set('default', 'concluded', '')
    config.set('default', 'start_time', 'None')
    config.set('default', 'interval', '0')
    config.set('default', 'runs', '0')
    config.set('default', 'run_mondays', 'false')
    config.set('default', 'run_tuesdays', 'false')
    config.set('default', 'run_wednsdays', 'false')
    config.set('default', 'run_thursdays', 'false')
    config.set('default', 'run_fridays', 'false')
    config.set('default', 'run_saturdays', 'false')
    config.set('default', 'run_sundays', 'false')
    config.set('default', 'environments', 'true')
    config.set('default', 'characters', 'true')
    config.set('default', 'scenes', 'true')
    config.set('default', 'play', 'true')
    config.set('default', 'turn_length', '30')
    config.set('default', 'contributor_minimum', '2')
    config.set('default', 'contributor_maximum', '10')
    config.set('default', 'character_number', '4')
    config.set('default', 'play_number', '4')
    config.set('default', 'japan', 'true')
    config.set('default', 'europe', 'true')
    config.set('default', 'america', 'true')
    config.set('default', 'historical', 'true')
    config.set('default', 'modern', 'true')
    config.set('default', 'futuristic', 'true')
    config.set('default', 'fantasy', 'true')
    config.set('default', 'cis_men', 'true')
    config.set('default', 'cis_women', 'true')
    config.set('default', 'nonbinary', 'true')
    config.set('default', 'trans_men', 'true')
    config.set('default', 'trans_women', 'true')
    config.set('default', 'futanari', 'true')
    config.set('default', 'mammals', 'true')
    config.set('default', 'reptiles', 'true')
    config.set('default', 'fish', 'false')
    config.set('default', 'birds', 'false')
    config.set('default', 'insects', 'false')
    config.set('default', 'arachnids', 'false')
    config.set('default', 'humans', 'true')
    config.set('default', 'elves', 'true')
    config.set('default', 'dwarves', 'true')
    config.set('default', 'halflings', 'true')
    config.set('default', 'gnomes', 'false')
    config.set('default', 'tieflings', 'true')
    config.set('default', 'merfolk', 'true')
    config.set('default', 'orcs', 'true')
    config.set('default', 'goliaths', 'true')
    config.set('default', 'goblinoids', 'false')
    config.set('default', 'ilithids', 'false')
    config.set('default', 'slimes', 'true')
    config.set('default', 'tentacles', 'true')
    config.set('default', 'dryads', 'true')
    config.set('default', 'harpies', 'false')
    config.set('default', 'lamia', 'false')
    config.set('default', 'centaurs', 'false')
    config.set('default', 'minotaurs', 'false')
    config.set('default', 'giants', 'false')
    config.set('default', 'werebeasts', 'true')
    config.set('default', 'vampires', 'true')
    config.set('default', 'undead', 'false')
    config.set('default', 'demons', 'true')
    config.set('default', 'angels', 'true')
    config.set('default', 'faeries', 'true')
    config.set('default', 'cyborgs', 'true')
    config.set('default', 'androids', 'true')
    config.set('default', 'robots', 'false')
    config.set('default', 'humanoid_aliens', 'true')
    config.set('default', 'aliens', 'false')
    config.set('default', 'urban', 'true')
    config.set('default', 'rural', 'true')
    config.set('default', 'college', 'true')
    config.set('default', 'magical', 'true')
    config.set('default', 'tech', 'true')
    config.set('default', 'romance', 'true')
    config.set('default', 'kissing', 'true')
    config.set('default', 'cuddling', 'true')
    config.set('default', 'petting', 'true')
    config.set('default', 'grinding', 'true')
    config.set('default', 'titjobs', 'true')
    config.set('default', 'ass_play', 'true')
    config.set('default', 'anal_sex', 'true')
    config.set('default', 'manual_sex', 'true')
    config.set('default', 'oral_sex', 'true')
    config.set('default', 'intercrural_sex', 'true')
    config.set('default', 'penetrative_sex', 'true')
    config.set('default', 'basic_toys', 'true')
    config.set('default', 'age_play', 'false')
    config.set('default', 'bondage', 'false')
    config.set('default', 'biting', 'false')
    config.set('default', 'breast_play', 'false')
    config.set('default', 'impact_play', 'false')
    config.set('default', 'orgasm_control', 'false')
    config.set('default', 'genitorture', 'false')
    config.set('default', 'cuckoldry', 'false')
    config.set('default', 'cupping', 'false')
    config.set('default', 'dom_and_sub', 'false')
    config.set('default', 'knife_play', 'false')
    config.set('default', 'electro_play', 'false')
    config.set('default', 'food_play', 'false')
    config.set('default', 'temperature_play', 'false')
    config.set('default', 'fire_play', 'false')
    config.set('default', 'fisting', 'false')
    config.set('default', 'foot_play', 'false')
    config.set('default', 'degradation', 'false')
    config.set('default', 'exhibition', 'false')
    config.set('default', 'pet_play', 'false')
    config.set('default', 'piss_play', 'false')
    config.set('default', 'consensual_nonconsent', 'false')
    config.set('default', 'sensory_deprivation', 'false')
    config.set('default', 'sounding', 'false')
    config.set('default', 'intoxicants', 'false')
    config.set('default', 'incest', 'false')
    config.set('default', 'bestiality', 'false')
    config.set('default', 'size_play', 'false')
    config.set('default', 'partial_growth', 'false')
    config.set('default', 'extreme_insertions', 'false')
    config.set('default', 'inflation', 'false')
    config.set('default', 'transformation', 'false')
    config.set('default', 'impregnation', 'false')
    config.set('default', 'oviposition', 'false')
    config.set('default', 'dubious_consent', 'false')
    config.set('default', 'nonconsent', 'false')
    config.set('default', 'torture', 'false')
    config.set('default', 'gore', 'false')
    config.set('default', 'soft_vore', 'false')
    config.set('default', 'hard_vore', 'false')
    config.set('default', 'snuff', 'false')
    config.set('default', 'necrophilia', 'false')
    with open(configPath, 'w') as configfile:
        config.write(configfile)

def existsCheck(j, url, post):
    exists = False
    for js in j:
        if js["name"] == post["name"]:
            exists = True
            break
    if not exists:
        time.sleep(4)
        r = requests.post(url, headers=headers, json=post)
        print(f'{post["name"]} command created.\nJSON: {r.text}')

def createGuildCommands(guildID):    
    url = f"https://discord.com/api/v8/applications/{bot.user.id}/guilds/{guildID}/commands"
    g = requests.get(url, headers=headers)
    j = g.json()

    post = {
        "name": "roles",
        "description": "Set LewdRobin admin / moderator roles. You will need to enable dev mode to get the IDs.",
        "type": 1,
        "options": [
            {
                "name": "admin",
                "description": "Set a role to have LewdRobin setting configuration priveledges.",
                "type": 3,
                "required": True
            },
            {
                "name": "moderator",
                "description": "Set a role to have prompt generation and kick/ban priveledges.",
                "type": 3,
                "required": True
            }
        ],
    }
    existsCheck(j, url, post)

    post = {
        "name": "time",
        "description": "Configure when prompts automatically run in this channel.",
        "type": 1,
        "options": [
            {
                "name": "start_time",
                "description": "Time for initial prompt generation in GMT. Ex, 16:30",
                "type": 3,
                "required": True,
            },
            {
                "name": "interval",
                "description": "Time between prompt generations, in hours.",
                "type": 4,
                "required": True,
            },
            {
                "name": "runs",
                "description": "The number of times prompts are generated per run before stopping",
                "type": 4,
                "required": True,
            },                
            {
                "name": "run_mondays",
                "description": "Whether prompts are generated on Mondays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_tuesdays",
                "description": "Whether prompts are generated on Tuesdays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_wednesdays",
                "description": "Whether prompts are generated on Wednesdays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_thursdays",
                "description": "Whether prompts are generated on Thursdays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_fridays",
                "description": "Whether prompts are generated on Fridays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_saturdays",
                "description": "Whether prompts are generated on Saturdays",
                "type": 5,
                "required": False
            },
            {
                "name": "run_sundays",
                "description": "Whether prompts are generated on Sundays",
                "type": 5,
                "required": False
            },
        ],
    }
    existsCheck(j, url, post)

    post = {
        "name": "contributors",
        "description": "Toggle options related to contributors",
        "type": 1,
        "options": [
            {
                "name": "turn_length",
                "description": "How many minutes a contributor has to post to a prompt. default: 30",
                "type": 4,
                "required": False
            },
            {
                "name": "contributor_minimum",
                "description": "The minimum number of contributors required for a prompt to run. default: 2",
                "type": 4,
                "required": False
            },
            {
                "name": "contributor_maximum",
                "description": "The maximum number of contributors a prompt will accept. default: 10",
                "type": 4,
                "required": False
            },
        ],
    }
    existsCheck(j, url, post)                 

    post = {
        "name": "run",
        "description": "Run a prompt now."
    }
    existsCheck(j, url, post)

    post = {
        "name": "kick",
        "description": "Kicks a contributor from a prompt and prevents them from rejoining.",
        "options": [
            {
                "name": "user_alias",
                "description": "enter the ColorAnimal alias of the user to kick",
                "type": 3,
                "required": True
            },
        ]
    }
    existsCheck(j, url, post)
    
    post = {
        "name": "ban",
        "description": "Bans someone. They will be unable to join prompts on this server.",
        "options": [
            {
                "name": "user_alias",
                "description": "enter the ColorAnimal alias of the user to kick",
                "type": 3,
                "required": True
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "unban_all",
        "description": "Unbans all users banned from prompt participation.",
        "options": [
            {
                "name": "confirmation",
                "description": 'enter "unban" to confirm this command.',
                "type": 3,
                "required": True
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "pause",
        "description": "Pause or unpause the prompt in this channel"
    }
    existsCheck(j, url, post)

    post = {
        "name": "autorun",
        "description": "Configure and begin automatic prompt generation.",
        "options": [
            {
                "name": "interval",
                "description": 'The number of minutes between automatic prompt generation.',
                "type": 4,
                "required": True
            },
            {
                "name": "delay",
                "description": 'The number of minutes before the first automatic prompt generation.',
                "type": 4,
                "required": True
            }
        ]
    }
    existsCheck(j, url, post)
    
    post = {
        "name": "autorun_stop",
        "description": "Stops automatic prompt generation (but not the current prompt)."
    }
    existsCheck(j, url, post)

    post = {
        "name": "conclude",
        "description": "Concludes the active prompt in this channel"
    }
    existsCheck(j, url, post)

def createGlobalCommands():
    url = f"https://discord.com/api/v8/applications/{bot.user.id}/commands"
    g = requests.get(url, headers=headers)
    j = g.json()

    post = {
        "name": "join",
        "description": "Join the pool of round-robin contributors for a prompt",
        "options": [
            {
                "name": "prompt_code",
                "description": "enter the 4-digit code for the prompt",
                "type": 4,
                "required": True
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "drop",
        "description": "Drop from a pool of contributors from a prompt",
        "options": [
            {
                "name": "prompt_code",
                "description": "enter the code of the prompt this is for",
                "type": 4,
                "required": True
            }
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "post",
        "description": "Submit a post for your current prompt",
        "options": [
            {
                "name": "prompt_code",
                "description": "enter the code of the prompt this is for",
                "type": 4,
                "required": True
            },
            {
                "name": "text",
                "description": "enter text of your post",
                "type": 3,
                "required": True
            }
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "pass",
        "description": "End your turn for submitting posts",
        "options": [
            {
                "name": "prompt_code",
                "description": "enter the code of the prompt this is for",
                "type": 4,
                "required": True
            },
        ]    
    }
    existsCheck(j, url, post)

    post = {
        "name": "help",
        "description": "User guide, admin info, external links."
    }
    existsCheck(j, url, post)
    
    post = {
        "name": "generate",
        "description": "Generates a prompt (but does not run a story with it) in this channel."
    }
    existsCheck(j, url, post)    

    post = {
        "name": "reset",
        "description": "Resets channel-specific settings for this channel",
        "options": [
            {
                "name": "confirmation",
                "description": 'enter "reset" to confirm this command.',
                "type": 3,
                "required": True
            },
        ]    
    }
    existsCheck(j, url, post)


    post = {
        "name": "display_settings",
        "description": "Displaying this channel's settings (only you see it)"
    }
    existsCheck(j, url, post)

    post = {
        "name": "categories",
        "description": "Toggle categories for prompt generation",
        "type": 1,
        "options": [
            {
                "name": "environments",
                "description": "Whether prompts generate an environment",
                "type": 5,
                "required": False
            },
            {
                "name": "characters",
                "description": "Whether prompts generate characters",
                "type": 5,
                "required": False
            },
            {
                "name": "character_number",
                "description": "How many characters a prompt generates",
                "type": 4,
                "required": False,
            },
            {
                "name": "scenes",
                "description": "Whether prompts generate a starting scene",
                "type": 5,
                "required": False
            },
            {
                "name": "play",
                "description": "Whether prompts generate play type suggestions",
                "type": 5,
                "required": False
            },
            {
                "name": "play_number",
                "description": "How many characters a prompt generates",
                "type": 4,
                "required": False,
            },
        ],
    }
    existsCheck(j, url, post)

    post = {
        "name": "environments",
        "description": "Toggle environment groups to generate from",
        "type": 1,
        "options": [
            {
                "name": "japan",
                "description": "Whether prompts generate from the Japanese environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "europe",
                "description": "Whether prompts generate from the European environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "america",
                "description": "Whether prompts generate from the American environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "historical",
                "description": "Whether prompts generate from the historical environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "modern",
                "description": "Whether prompts generate from the modern environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "futuristic",
                "description": "Whether prompts generate from the futuristic environments pool",
                "type": 5,
                "required": False
            },
            {
                "name": "fantasy",
                "description": "Whether prompts generate from the fantasy environments pool",
                "type": 5,
                "required": False
            },
        ],
    }
    existsCheck(j, url, post)

    post = {
        "name": "character_types",
        "description": "Settings for character gender, number, and pairings",
        "type": 1,
        "options": [
            {
                "name": "cis_men",
                "description": "Whether prompts generate men who were assigned male at birth",
                "type": 5,
                "required": False
            },
            {
                "name": "cis_women",
                "description": "Whether prompts generate women who were assigned female at birth",
                "type": 5,
                "required": False
            },
            {
                "name": "nonbinary",
                "description": "Whether prompts generate people who fall outside the man-woman gender bimode",
                "type": 5,
                "required": False
            },                          
            {
                "name": "trans_men",
                "description": "Whether prompts generates men who were not assigned male at birth",
                "type": 5,
                "required": False
            },
            {
                "name": "trans_women",
                "description": "Whether prompts generates women who were not assigned female at birth",
                "type": 5,
                "required": False
            },
            {
                "name": "futanari",
                "description": "Whether prompts generate futanari",
                "type": 5,
                "required": False
            }
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "species_anthros",
        "description": "Set what antrhopomorphic animal types are generated",
        "type": 1,
        "required": False,
        "options": [
            {
                "name": "mammals",
                "description": "cats, dogs, wolves, foxes, bears, cows, etc.",
                "required": False,
                "type": 5
            },
            {
                "name": "reptiles",
                "description": "lizards, dragons, snakes",
                "required": False,
                "type": 5
            },
            {
                "name": "fish",
                "description": "fish, sharks, squid, octopi",
                "required": False,
                "type": 5
            },
            {
                "name": "birds",
                "description": "crows, parrots, hawks... robins :)",
                "required": False,
                "type": 5
            },
            {
                "name": "insects",
                "description": "ants, bees, wasps, mantis",
                "required": False,
                "type": 5
            },
            {
                "name": "arachnids",
                "description": "spiders and scorpions",
                "required": False,
                "type": 5
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "species_fantasy",
        "description": "Set what humanoid fantasy species are generated",
        "type": 1,
        "required": False,
        "options": [
            {
                "name": "humans",
                "description": "the classic", 
                "required": False,
                "type": 5
            },
            {
                "name": "elves",
                "description": "high elves, wood elves, drow, half-elves", 
                "required": False,
                "type": 5
            },
            {
                "name": "dwarves",
                "description": "the true folk",
                "required": False,
                "type": 5
            },
            {
                "name": "halflings",
                "description": "shortstacks",
                "required": False,
                "type": 5
            },
            {
                "name": "gnomes",
                "description": "annoying jerks",
                "required": False,
                "type": 5
            },
            {
                "name": "tieflings",
                "description": "part demon",
                "required": False,
                "type": 5
            },
            {
                "name": "merfolk",
                "description": "is person, is fish",
                "required": False,
                "type": 5
            },
            {
                "name": "orcs",
                "description": "full and half-orcs",
                "required": False,
                "type": 5
            },
            {
                "name": "goliaths",
                "description": "half-giants",
                "required": False,
                "type": 5
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "species_monster",
        "description": "Set what \"monstrous species\" are generated",
        "type": 1,
        "required": False,
        "options": [
            {
                "name": "goblinoids",
                "description": "goblins, hobgoblins, bugbears",
                "required": False,
                "type": 5
            },                                
            {
                "name": "ilithids",
                "description": "mindflayers", 
                "required": False,
                "type": 5
            },
            {
                "name": "slimes",
                "description": "slimes, oozes, jellies", 
                "required": False,
                "type": 5
            },
            {
                "name": "tentacles",
                "description": "tentacle monsters, humanoids with tentacles",
                "required": False,
                "type": 5
            },
            {
                "name": "dryads",
                "description": "plant and tree spirits",
                "required": False,
                "type": 5
            },
            {
                "name": "harpies",
                "description": "large anthropomorphic raptors", 
                "required": False,
                "type": 5
            },
            {
                "name": "lamia",
                "description": "half-human, half-snake",
                "required": False,
                "type": 5
            },
            {
                "name": "centaurs",
                "description": "half-human, half-horse",
                "required": False,
                "type": 5
            },
            {
                "name": "minotaurs",
                "description": "big and bull-headed",
                "required": False,
                "type": 5
            },
            {
                "name": "giants",
                "description": "ogres, trolls, giants",
                "required": False,
                "type": 5
            },
            {
                "name": "werebeasts",
                "description": "werewolves, weretigers, werebears, weresharks",
                "required": False,
                "type": 5
            },
            {
                "name": "vampires",
                "description": "hunters of the night",
                "required": False,
                "type": 5
            },
            {
                "name": "undead",
                "description": "liches, mummies, ghosts, zombies",
                "required": False,
                "type": 5
            },
            {
                "name": "demons",
                "description": "half-demons, demons, devils, succubi, incubi",
                "required": False,
                "type": 5
            },
            {
                "name": "angels",
                "description": "half-angels, angels, and other celestials",
                "required": False,
                "type": 5
            },
            {
                "name": "faeries",
                "description": "fair folk, big and small",
                "required": False,
                "type": 5
            }
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "species_futuristic",
        "description": "Set what sci-fi species are generated",
        "type": 1,
        "required": False,
        "options": [
            {
                "name": "cyborgs",
                "description": "half-biological, half-machine", 
                "required": False,
                "type": 5
            },
            {
                "name": "androids",
                "description": "human-like robots",
                "required": False,
                "type": 5
            },
            {
                "name": "robots",
                "description": "machines that aren't meant to present as humans",
                "required": False,
                "type": 5
            },
            {
                "name": "humanoid_aliens",
                "description": "people from distant worlds who vaguely conform to human shape",
                "required": False,
                "type": 5
            },
            {
                "name": "aliens",
                "description": "bizarre and varied in form",
                "required": False,
                "type": 5
            },
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "play_vanilla",
        "description": "Set generatable types of non-kink play",
        "type": 1,
        "options": [
            {
                "name": "romance",
                "description": "grand gestures, affectionate conversation, dating, etc.", 
                "required": False,
                "type": 5
            },
            {
                "name": "kissing",
                "description": "gentle and firm, lips on various body parts",
                "required": False,
                "type": 5
            },
            {
                "name": "cuddling",
                "description": "close body contact",
                "required": False,
                "type": 5
            },
            {
                "name": "petting",
                "description": "stroking, caressing, touching, without direct genital contact",
                "required": False,
                "type": 5
            },
            {
                "name": "grinding",
                "description": "rubbing bodies together without penetration",
                "required": False,
                "type": 5
            },
            {
                "name": "titjobs",
                "description": "phallus thrust between breasts",
                "required": False,
                "type": 5
            },
            {
                "name": "ass_play",
                "description": "rimming, anal fingering",
                "required": False,
                "type": 5
            },
            {
                "name": "anal_sex",
                "description": "phallic penetration of the anus",
                "required": False,
                "type": 5
            },
            {
                "name": "manual_sex",
                "description": "direct hand-on-genital contact",
                "required": False,
                "type": 5
            },
            {
                "name": "oral_sex",
                "description": "direct mouth-on-genital contact",
                "required": False,
                "type": 5
            },
            {
                "name": "intercrural_sex",
                "description": "phallus thrust between thighs",
                "required": False,
                "type": 5
            },
            {
                "name": "penetrative_sex",
                "description": "phallic penetration of an orifice",
                "required": False,
                "type": 5                                    
            },
            {
                "name": "basic_toys",
                "description": "dildos, strapons, fleshlights, vibrators, hitachi",
                "required": False,
                "type": 5                                    
            }
        ]
    }
    existsCheck(j, url, post)

    post = {
        "name": "play_bdsm",
        "description": "Set generatable types of realistic kinky play",
        "type": 1,
        "options": [
            {
                "name": "age_play",
                "description": "one or more participants pretend to be a different age (often younger)", 
                "required": False,
                "type": 5
            },
            {
                "name": "bondage",
                "description": "ropes, handcuffs, shackles; restricted movement",
                "required": False,
                "type": 5
            },
            {
                "name": "biting",
                "description": "hard enough to leave a mark... or draw blood",
                "required": False,
                "type": 5
            },
            {
                "name": "breast_play",
                "description": "teasing or painful stimulation of breasts",
                "required": False,
                "type": 5
            },
            {
                "name": "impact_play",
                "description": "slapping, spanking, caning, paddling, flogging, whipping",
                "required": False,
                "type": 5
            },
            {
                "name": "orgasm_control",
                "description": "restricting when one or more participants are allowed to orgasm",
                "required": False,
                "type": 5
            },
            {
                "name": "genitorture",
                "description": "painful manipulation of the genitals, includes CBT",
                "required": False,
                "type": 5
            },
            {
                "name": "cuckoldry",
                "description": "an adulterer cheating on their partner, who is present",
                "required": False,
                "type": 5
            },
            {
                "name": "cupping",
                "description": "using heated cups applied to skin to create suction",
                "required": False,
                "type": 5
            },
            {
                "name": "dom_and_sub",
                "description": "having participants who are explicitly dominants or submissives",
                "required": False,
                "type": 5
            },
            {
                "name": "knife_play",
                "description": "knives traced along skin",
                "required": False,
                "type": 5                                    
            },
            {
                "name": "electro_play",
                "description": "electrostim units, violet wands, electrified surfaces", 
                "required": False,
                "type": 5
            },
            {
                "name": "food_play",
                "description": "eating, feeding, spreading, inserting",
                "required": False,
                "type": 5
            },
            {
                "name": "temperature_play",
                "description": "wax, heated or cooled ojbects, ice cubes",
                "required": False,
                "type": 5
            },
            {
                "name": "fire_play",
                "description": "lighters, candles, fire cupping, flamable liquid",
                "required": False,
                "type": 5
            },
            {
                "name": "fisting",
                "description": "vaginal or anal penetration using the entire hand",
                "required": False,
                "type": 5
            },
            {
                "name": "foot_play",
                "description": "licking, worshipping, feet-on-genitalia",
                "required": False,
                "type": 5
            },
            {
                "name": "degradation",
                "description": "insults, humiliation, demeaning acts",
                "required": False,
                "type": 5
            },
            {
                "name": "exhibition",
                "description": "public play, filmed play, play with an audience",
                "required": False,
                "type": 5
            },
            {
                "name": "pet_play",
                "description": "role-play as owner and animal pet",
                "required": False,
                "type": 5
            },
            {
                "name": "piss_play",
                "description": "play involving intentional urination",
                "required": False,
                "type": 5
            },
            {
                "name": "consensual_nonconsent",
                "description": "role-play involving the recreation of non-consensual sex",
                "required": False,
                "type": 5                                    
            },
            {
                "name": "sensory_deprivation",
                "description": "blindfolds, earplugs",
                "required": False,
                "type": 5
            },
            {
                "name": "sounding",
                "description": "insertion of a metal rod into the urethra",
                "required": False,
                "type": 5
            },
            {
                "name": "intoxicants",
                "description": "play involving consensual use of mind-altering substances",
                "required": False,
                "type": 5                                    
            }
        ]                
    }
    existsCheck(j, url, post)
    
    post = {
        "name": "play_surreal",
        "description": "Set generatable types of fiction-only play",
        "type": 1,
        "options": [
            {
                "name": "incest",
                "description": "sex between family members", 
                "required": False,
                "type": 5
            },
            {
                "name": "bestiality",
                "description": "sex with non-humanoid animals", 
                "required": False,
                "type": 5
            },
            {
                "name": "size_play",
                "description": "tiny characters, giant characters, growth, shrinking", 
                "required": False,
                "type": 5
            },
            {
                "name": "partial_growth",
                "description": "body part growth, muscle growth",
                "required": False,
                "type": 5
            },
            {
                "name": "extreme_insertions",
                "description": "large objects, bulging, all the way through",
                "required": False,
                "type": 5
            },
            {
                "name": "inflation",
                "description": "inflation, cum inflation",
                "required": False,
                "type": 5
            },
            {
                "name": "transformation",
                "description": "sex change, mutation, bodily change",
                "required": False,
                "type": 5
            },
            {
                "name": "impregnation",
                "description": "accelerated pregnancy, male pregnancy, enhanced fertility",
                "required": False,
                "type": 5
            },
            {
                "name": "oviposition",
                "description": "internal implantation of eggs, possibly including their hatching",
                "required": False,
                "type": 5
            },
            {
                "name": "dubious_consent",
                "description": "alcohol, mild coersion, power imbalance",
                "required": False,
                "type": 5
            },
            {
                "name": "nonconsent",
                "description": "drugging, mind control, blackmail, sleep play, rape",
                "required": False,
                "type": 5
            },
            {
                "name": "torture",
                "description": "extreme and pain and non-disfiguring bodily harm",
                "required": False,
                "type": 5
            },
            {
                "name": "gore",
                "description": "disfiguring harm, amputation, extreme violence",
                "required": False,
                "type": 5
            },
            {
                "name": "soft_vore",
                "description": "swallowed whole, nonlethal consumption, unrealistic vore",
                "required": False,
                "type": 5
            },
            {
                "name": "hard_vore",
                "description": "eaten part by part, lethal consumption, realistic vore",
                "required": False,
                "type": 5
            },
            {
                "name": "snuff",
                "description": "murder (of partners or otherwise) in sex",
                "required": False,
                "type": 5                                    
            },
            {
                "name": "necrophilia",
                "description": "sex with dead bodies or body parts", 
                "required": False,
                "type": 5
            },
        ]                
    }
    existsCheck(j, url, post)

def addChannel(guildID, channelID):
    config = configparser.ConfigParser()
    configPath = ap(f'{serverConfigs}\{guildID}.ini')
    config.read(configPath)
    if f'{channelID}' not in config.sections():
            config.add_section(f'{channelID}')  
            with open(configPath, 'w') as configfile:
                config.write(configfile)

def iReply(interactionID, interactionToken, message):
    url = f"https://discord.com/api/v8/interactions/{interactionID}/{interactionToken}/callback"
    post = {
        "type": 4,
        "data": {
            "content": f"{message}"
        }
    }
    r = requests.post(url, json=post)

def iHReply(interactionID, interactionToken, message):
    url = f"https://discord.com/api/v8/interactions/{interactionID}/{interactionToken}/callback"
    post = {
        "type": 4,
        "data": {
            "content": f"{message}",
            "flags": 64
        }
    }
    r = requests.post(url, json=post)

def iHFollowup(interactionToken, message):
    url = f"https://discord.com/api/v8/webhooks/{bot.user.id}/{interactionToken}"
    post = {
        "content": f"{message}",
        "flags": 64
    }
    r = requests.post(url, json = post)

def commandConfigSetter(options, guildID, channel):
    if len(options) > 0:
        optionNames = []
        for opt in range(0, len(options)):
            try:
                addConfig(guildID, channel.id, options[opt]["name"], options[opt]["value"])
                optionNames.append(options[opt]["name"].replace("_", " "))
            except:
                pass
        optionNames = ", ".join(optionNames)
    return f"The following channel-specific settings have been set for {channel.name}: {optionNames}.\nThese settings will override the corresponding default settings, but only for prompts generated in {channel.name}."

def commandDMConfigSetter(options, userID):
    if len(options) > 0:
        optionNames = []
        if f"{userID}" not in DMConfig:
            DMConfig[f"{userID}"] = {}
        for opt in range(0, len(options)):
            DMConfig[f"{userID}"][f"{options[opt]['name']}"] = options[opt]["value"]
            optionNames.append(options[opt]["name"].replace("_", " "))
        optionNames = ", ".join(optionNames)
    return f"The following settings have been set for private generation: {optionNames}.\nThese settings will override the corresponding default settings, but only for prompts generated in your DMs."

def getAlias(guildID, channelID, userID):
    for key, value in contributors[f"{guildID}"][f"{channelID}"].items():
         if value == userID:
             return key

def kickUser(guildID, channelID, userID):
    try:
        conChannel = contributors[f"{guildID}"][f"{channelID}"]
    except:
        return False
    try:
        pos = conChannel["pool"].index(userID)
        if conChannel["turn"] > pos:
            conChannel["turn"] -= 1
    except:
        pass
    try:
        conChannel["pool"].remove(userID)
        conChannel["kicked"].append(userID)
    except:
        return False
    return True

def dropUser(guildID, channelID, userID):
    try:
        conChannel = contributors[f"{guildID}"][f"{channelID}"]
    except:
        return False
    try:
        pos = conChannel["pool"].index(userID)
        if conChannel["turn"] > pos:
            conChannel["turn"] -= 1
    except:
        pass
    try:
        conChannel["pool"].remove(userID)
    except:
        return False
    return True

def createTimer(time, action, guildID, channelID, promptCode, userID, contributions):
    timers[f"{time}"] = {
                            "time": time, 
                            "action": f"{action}", 
                            "guildID": guildID, 
                            "channelID": channelID,
                            "promptCode": promptCode, 
                            "userID": userID, 
                            "contributions": contributions 
                        }

def createTempTimer(time, action, guildID, channelID, promptCode, userID, contributions):
    tempTimers[f"{time}"] = {
                            "time": time, 
                            "action": f"{action}", 
                            "guildID": guildID, 
                            "channelID": channelID,
                            "promptCode": promptCode, 
                            "userID": userID, 
                            "contributions": contributions 
                        }

def nextTurn(guildID, channelID):
    conChannel = contributors[f"{guildID}"][f"{channelID}"]    
    conChannel["multipost"] = False
    conChannel["turn"] += 1
    if conChannel["turn"] >= len(conChannel["pool"]):
        conChannel["turn"] = 0

def codeChecker(promptCode):    
    for guildID in guildIDList:
        try:
            config = configparser.ConfigParser()
            configPath = ap(f'{serverConfigs}\{guildID}.ini')
            config.read(configPath)
            sections = config.sections()
            for section in sections:
                if "promptcode" in config[section]:
                    if config[section]["promptcode"] == promptCode:
                        return [int(guildID), int(section)]                            
        except:
            continue
    else:
        return False

def displaySettings(guildID, channelID, channelName):
    settingsListGen = ['start_time', 'interval', 'runs', 'run_mondays', 'run_tuesdays', 'run_wednsdays', 'run_thursdays', 'run_fridays', 'run_saturdays', 'run_sundays', 'environments', 'characters', 'scenes', 'play', 'turn_length', 'contributor_minimum', 'contributor_maximum', 'character_number', 'play_number']
    displayGen = f">>> **LewdRobin General Settings for {channelName}**"
    for setting in settingsListGen:
        data = getConfigDisplay(guildID, channelID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displayGen += f"\n{setting}: {data[0]} *(default)*"
        else:
            displayGen += f"\n{setting}: {data[0]}"
    settingsListEnv = ['japan', 'europe', 'america', 'historical', 'modern', 'futuristic', 'fantasy', 'cis_men', 'cis_women', 'nonbinary', 'trans_men', 'trans_women', 'futanari']
    displayEnv = f">>> **LewdRobin Environment and Character Type Settings for {channelName}**"
    for setting in settingsListEnv:
        data = getConfigDisplay(guildID, channelID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displayEnv += f"\n{setting}: {data[0].title()} *(default)*"
        else:
            displayEnv += f"\n{setting}: {data[0].title()}"
    settingsListSpecies = ['mammals', 'reptiles', 'fish', 'birds', 'insects', 'arachnids', 'humans', 'elves', 'dwarves', 'halflings', 'gnomes', 'tieflings', 'merfolk', 'orcs', 'goliaths', 'goblinoids', 'ilithids', 'slimes', 'tentacles', 'dryads', 'harpies', 'lamia', 'centaurs', 'minotaurs', 'giants', 'werebeasts', 'vampires', 'undead', 'demons', 'angels', 'faeries', 'cyborgs', 'androids', 'robots', 'humanoid_aliens', 'aliens']
    displaySpecies = f">>> **LewdRobin Character Species Settings for {channelName}**"
    for setting in settingsListSpecies:
        data = getConfigDisplay(guildID, channelID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displaySpecies += f"\n{setting}: {data[0].title()} *(default)*"
        else:
            displaySpecies += f"\n{setting}: {data[0].title()}"
    settingsListPlay = ['romance', 'kissing', 'cuddling', 'petting', 'grinding', 'titjobs', 'ass_play', 'anal_sex', 'manual_sex', 'oral_sex', 'intercrural_sex', 'penetrative_sex', 'basic_toys', 'age_play', 'bondage', 'biting', 'breast_play', 'impact_play', 'orgasm_control', 'genitorture', 'cuckoldry', 'cupping', 'dom_and_sub', 'knife_play', 'electro_play', 'food_play', 'temperature_play', 'fire_play', 'fisting', 'foot_play', 'degradation', 'exhibition', 'pet_play', 'piss_play', 'consensual_nonconsent', 'sensory_deprivation', 'sounding', 'intoxicants', 'incest', 'bestiality', 'size_play', 'partial_growth', 'extreme_insertions', 'inflation', 'transformation', 'impregnation', 'oviposition', 'dubious_consent', 'nonconsent', 'torture', 'gore', 'soft_vore', 'hard_vore', 'snuff', 'necrophilia']
    displayPlay = f">>> **LewdRobin Play Settings for {channelName}**"
    for setting in settingsListPlay:
        data = getConfigDisplay(guildID, channelID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displayPlay += f"\n{setting}: {data[0].title()} *(default)*"
        else:
            displayPlay += f"\n{setting}: {data[0].title()}"
    return [displayGen, displayEnv, displaySpecies, displayPlay]

def displayDMSettings(userID):
    settingsListGen = ['environments', 'characters', 'scenes', 'play', 'character_number', 'play_number', 'japan', 'europe', 'america', 'historical', 'modern', 'futuristic', 'fantasy', 'cis_men', 'cis_women', 'nonbinary', 'trans_men', 'trans_women', 'futanari']
    displayGen = f">>> **LewdRobin General Settings for Personal Generation**"
    for setting in settingsListGen:
        data = getConfigDMDisplay(userID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displayGen += f"\n{setting}: {data[0]} *(default)*"
        else:
            displayGen += f"\n{setting}: {data[0]}"
    settingsListSpecies = ['mammals', 'reptiles', 'fish', 'birds', 'insects', 'arachnids', 'humans', 'elves', 'dwarves', 'halflings', 'gnomes', 'tieflings', 'merfolk', 'orcs', 'goliaths', 'goblinoids', 'ilithids', 'slimes', 'tentacles', 'dryads', 'harpies', 'lamia', 'centaurs', 'minotaurs', 'giants', 'werebeasts', 'vampires', 'undead', 'demons', 'angels', 'faeries', 'cyborgs', 'androids', 'robots', 'humanoid_aliens', 'aliens']
    displaySpecies = f">>> **LewdRobin Character Species Settings for Personal Generation**"
    for setting in settingsListSpecies:
        data = getConfigDMDisplay(userID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displaySpecies += f"\n{setting}: {data[0]} *(default)*"
        else:
            displaySpecies += f"\n{setting}: {data[0]}"
    settingsListPlay = ['romance', 'kissing', 'cuddling', 'petting', 'grinding', 'titjobs', 'ass_play', 'anal_sex', 'manual_sex', 'oral_sex', 'intercrural_sex', 'penetrative_sex', 'basic_toys', 'age_play', 'bondage', 'biting', 'breast_play', 'impact_play', 'orgasm_control', 'genitorture', 'cuckoldry', 'cupping', 'dom_and_sub', 'knife_play', 'electro_play', 'food_play', 'temperature_play', 'fire_play', 'fisting', 'foot_play', 'degradation', 'exhibition', 'pet_play', 'piss_play', 'consensual_nonconsent', 'sensory_deprivation', 'sounding', 'intoxicants', 'incest', 'bestiality', 'size_play', 'partial_growth', 'extreme_insertions', 'inflation', 'transformation', 'impregnation', 'oviposition', 'dubious_consent', 'nonconsent', 'torture', 'gore', 'soft_vore', 'hard_vore', 'snuff', 'necrophilia']
    displayPlay = f">>> **LewdRobin Play Settings for Personal Generation**"
    for setting in settingsListPlay:
        data = getConfigDMDisplay(userID, setting)
        setting = setting.replace("_", " ").title()
        if data[1]:
            displayPlay += f"\n{setting}: {data[0]} *(default)*"
        else:
            displayPlay += f"\n{setting}: {data[0]}"
    return [displayGen, displaySpecies, displayPlay]

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def logUpdater(guildID, channelID, promptCode, text):
    fpath = f"{promptLogs}\{promptCode}.txt"
    try:
        with open(f"{fpath}", "x") as f:
            promptText = getConfig(guildID, channelID, "prompttext")
            f.write(f"{promptText}\n\n**Story:**")
    except:
        pass
    with open(fpath, "a") as f:
        f.write(f"\n{text}")

#asyncio (async/await) functions
@bot.event
async def on_ready():
    if not initialize["on_ready"]:
        Interaction(bot)
        listPopulator()
        try:
            with open("reactables.txt", "x") as f:
                f.write("")
        except:
            pass
        async for guild in bot.fetch_guilds():
            if not os.path.isfile(f'{serverConfigs}\{guild.id}.ini'):               
                createGuildConfig(guild.id)
            contributors[f"{guild.id}"] = {}
            contributors[f"{guild.id}"]["banned"] = []
            config = configparser.ConfigParser()
            configPath = ap(f'{serverConfigs}\{guild.id}.ini')
            config.read(configPath)
            for section in range(1, len(config.sections())):
                channelID = config.sections()[section]
                contributorsConfig(guild.id, channelID)
        if initialize["deleteGlobalCommands"]:
            url = f"https://discord.com/api/v8/applications/{bot.user.id}/commands"
            p = requests.put(url, headers=headers, json={}) 
        if initialize["deleteGuildCommands"]:
            async for guild in bot.fetch_guilds():
                url = f"https://discord.com/api/v8/applications/{bot.user.id}/guilds/{guild.id}/commands"
                p = requests.put(url, headers=headers, json={})       
        if initialize["globalCommands"]:
            createGlobalCommands()
            print("Initializing global commands")
            initialize["globalCommands"] = False
        if initialize["guildCommands"]:
            print("Initializing guild commands")
            async for guild in bot.fetch_guilds():
                createGuildCommands(guild.id)
            else:
                initialize["guildCommands"] = False
        async for guild in bot.fetch_guilds():
            guildIDList.append(guild.id)
        initialize["on_ready"] = True
        print(f'We have logged in as {bot.user}!')

@bot.event
async def on_guild_join(guild):
    print("Initializing guild commands.")
    if initialize["guildCommands"]:
        createGuildCommands(guild.id)
    if not os.path.isfile(f'{serverConfigs}\{guild.id}.ini'):
        createGuildConfig(guild.id)
    contributors[f"{guild.id}"] = {}
    contributors[f"{guild.id}"]["banned"] = []
    guildIDList.append(guild.id)
    print(f"Joined {guild.name}.")

async def can_message(user):
  try:
    await user.send()
  except discord.errors.HTTPException as e:
    if e.code == 50006:
      return True
    elif e.code == 50007:
      return False
    else:
      raise

async def promptUpdater(guildID, channelID, promptCode):
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    conMin = getConfig(guildID, channelID, "contributor_minimum")
    conMax = getConfig(guildID, channelID, "contributor_maximum")
    conCurr = len(conChannel["pool"])
    contributions = getConfigInt(guildID, channelID, "promptcontributions")
    promptText = getConfig(guildID, channelID, "promptText")
    promptCodeLine = f"\n**Prompt Code:** {promptCode}"
    promptConLine = f"\n**Contributors:** {conCurr}/{conMax} ({conMin} required)"
    promptConConcludeLine= f"\n**Contributions:** {contributions}"
    promptPauseLine = "\n**PROMPT PAUSED**\n" if conChannel["paused"] else ""
    channel = await bot.fetch_channel(channelID)
    prompt = await channel.fetch_message(getConfigInt(guildID, channelID, "promptid"))
    if f"{promptCode}" in getConfig(guildID, channelID, "concluded"):
        content = "**PROMPT CONCLUDED**\n" + promptHeaderCondluded + promptText + promptCodeLine + promptConConcludeLine + promptReminderConcluded + promptPauseLine + "\n**PROMPT CONCLUDED**"
        await prompt.clear_reaction("✅")
        await prompt.clear_reaction("❌")   
        await prompt.clear_reaction("⏯")
        await prompt.clear_reaction("🔄")
    elif getConfigInt(guildID, channelID, "promptcontributions") > 0:
        content = promptPauseLine + promptHeaderActive + promptText + promptCodeLine + promptConLine + promptReminderActive + promptPauseLine
        await prompt.add_reaction("📜")
    else:
        content = promptPauseLine + promptHeader + promptText + promptCodeLine + promptConLine + promptReminder + promptPauseLine
    await prompt.edit(content=content)

async def promptConcluder(guildID, channelID, channel, promptCode):
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    contributions = getConfigInt(guildID, channelID, "promptcontributions")
    try:
        oldID = getConfigInt(guildID, channelID, "promptID")
        oldPin = await channel.fetch_message(oldID)
        await oldPin.unpin()
        if not contributions:
            oldMsg = await channel.fetch_message(oldID)
            await oldMsg.delete()        
    except:
        pass
    if contributions:
        concluded = getConfig(guildID, channelID, "concluded")
        concluded += f" {promptCode}"
        addConfig(guildID, channelID, "concluded", concluded)
        for post in conChannel["posts"]:
            await post.delete()
        for userID in conChannel["pool"]:
            user = await bot.fetch_user(userID)
            await user.send(f"Prompt {promptCode} has ended. Related posts have been deleted and archived; you can read the story by reacting to its prompt with :scroll:") 
        await promptUpdater(guildID, channelID, promptCode)

async def logDisplay(user, promptCode):
    fpath = f"{promptLogs}\{promptCode}.txt"
    file = discord.File(fpath, f"Story_Log_{promptCode}.txt")
    await user.send(f"**Story Log for Prompt {promptCode}**", file=file)

async def replyOrSend(user, iID, iToken, isInteraction, message):
    if isInteraction:
        iHReply(iID, iToken, message)
    else:
        await user.send(message)

async def sendNext(guildID, channelID, promptCode, turnLength):
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    pool = conChannel["pool"]
    nextUID = pool[conChannel["turn"]]
    nextUser = await bot.fetch_user(nextUID)
    msg = await nextUser.send(f"For the next {turnLength} minutes, it is your turn to /post ▶️ contributions to prompt {promptCode}. /pass ⏩ to end your turn early; 📝 to display the prompt; 📚 to display the prompt's three most recent posts; /drop ❌ to leave the prompt.")
    try:
        removeReactable(conChannel["postReactible"].id)
    except:
        pass
    try:
        await conChannel["postReactible"].unpin()
    except:
        pass
    addReactable(msg.id)
    conChannel["postReactible"] = msg
    await msg.add_reaction("▶️")
    await msg.add_reaction("⏩")
    await msg.add_reaction("📝")
    await msg.add_reaction("📚")
    await msg.add_reaction("❌")
    try:
        await msg.pin()
    except:
        pass

async def action_run(guildID, channelID, channel, iID, iToken, isInteraction):
    try:
        promptCode = getConfigInt(guildID, channelID, "promptcode")
        await promptConcluder(guildID, channelID, channel, promptCode)
    except:
        pass
    if isInteraction:
        iHReply(iID, iToken, "Generating a prompt. Give me a moment.")
    generation = promptGenerator(guildID, channelID, None, addText=True)
    text = generation[0]
    msg = await channel.send(text)
    addReactable(msg.id)
    addConfig(guildID, channelID, "promptID", msg.id)
    if generation[1]:
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")   
        await msg.add_reaction("⏯")
        try:
            await msg.pin()
        except:
            pass
    await msg.add_reaction("🔄")
    await msg.add_reaction("❓")    

async def action_generate(guildID, channelID, userID, channel, iID, iToken, isInteraction):
    if guildID:
        genID = getConfigInt(guildID, channelID, "genid")
        if genID:
            addReactable(genID)
    else:
        if f"{userID}" in DMConfig:
            if "genID" in DMConfig[f"{userID}"]:
                genID = DMConfig[f"{userID}"]["genID"]
                removeReactable(genID)
        else:
            DMConfig[f"{userID}"] = {}   
    if isInteraction:
        iHReply(iID, iToken, "Generating a prompt using this channel's settings. This prompt will only be shown, not run. To create a story contributors can join, use /run.")
    msg = promptGenerator(guildID, channelID, userID, addText=False)[0]
    if guildID:
        message = await channel.send(msg)
    else:
        user = await bot.fetch_user(userID)
        message = await user.send(msg)
    addReactable(message.id)
    if guildID:
        addConfig(guildID, channelID, "genid", f"{message.id}")
    else:
        DMConfig[f"{userID}"]["genID"] = message.id
    await message.add_reaction("🔃")    

async def action_join(userID, promptCode, iID, iToken, isInteraction):
    user = await bot.fetch_user(userID)
    data = codeChecker(promptCode)
    if not data:
        return
    guildID = data[0]
    channelID = data[1]
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    if userID in contributors[f"{guildID}"]["banned"]:
        task(replyOrSend(user, iID, iToken, isInteraction, "You have been banned, and can no longer join or contribute to prompts in this server."))
        return
    if userID in conChannel["kicked"]:
        task(replyOrSend(user, iID, iToken, isInteraction, f"You have been kicked from prompt {promptCode} and can no longer join or contribute to it. This is only temporary. You will be able to rejoin prompts in this server / channel when a new one is created."))
        return
    pool = conChannel["pool"]
    turn = conChannel["turn"]
    turnLength = getConfigInt(guildID, channelID, "turn_length")
    contributions = getConfigInt(guildID, channelID, "promptcontributions")
    if len(pool) < getConfigInt(guildID, channelID, "contributor_maximum"):
        if userID in pool:
            if isInteraction:
                iHReply(iID, iToken, f"You are already in the pool of contributors for prompt {promptCode}.")
        else:
            animal = ['Aardvark', 'Albatross', 'Alligator', 'Alpaca', 'Anole', 'Ant', 'Anteater', 'Antelope', 'Ape', 'Armadillo', 'Ass', 'Baboon', 'Badger', 'Barracuda', 'Bat', 'Bear', 'Beaver', 'Bee', 'Binturong', 'Bird', 'Aves', 'Bison', 'Bluebird', 'Boar', 'Pig', 'Bobcat', 'Budgerigar', 'Budgie', 'Buffalo', 'Butterfly', 'Camel', 'Capybara', 'Caracal', 'Caribou', 'Cassowary', 'Cat', 'Caterpillar', 'Cattle', 'Chamois', 'Cheetah', 'Chicken', 'Chimpanzee', 'Chinchilla', 'Chough', 'Coati', 'Cobra', 'Cockroach', 'Cod', 'Cormorant', 'Cougar', 'Coyote', 'Crab', 'Crane', 'Cricket', 'Crocodile', 'Crow', 'Cuckoo', 'Curlew', 'Deer', 'Dhole', 'Dingo', 'Dinosaur', 'Dog', 'Dogfish', 'Shark', 'Spiny', 'Dolphin', 'Donkey', 'Ass', 'Dove', 'Dragonfly', 'Duck', 'Mallard', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant', 'Elephant', 'Elk', 'Emu', 'Falcon', 'Ferret', 'Finch', 'Fish', 'Fisher', 'Flamingo', 'Fly', 'Flycatcher', 'Fox', 'Frog', 'Gaur', 'Gazelle', 'Gecko', 'Genet', 'Gerbil', 'Giant', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goosander', 'Goose', 'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Guinea', 'Guinea', 'Gull', 'Hamster', 'Hare', 'Hawk', 'Soaring', 'Hedgehog', 'Hermit', 'Heron', 'Herring', 'Hippopotamus', 'Hoatzin', 'Hoopoe', 'Hornet', 'Horse', 'Human', 'Hummingbird', 'Hyena', 'Ibex', 'Ibis', 'Iguana', 'Impala', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Jerboa', 'Kangaroo', 'Kingbird', 'Kingfisher', 'Kinkajou', 'Kite', 'Koala', 'Kodkod', 'Komodo', 'Kookaburra', 'Kouprey', 'Kudu', 'Langur', 'Lapwing', 'Lark', 'Lechwe', 'Lemur', 'Leopard', 'Lion', 'Lizard', 'Llama', 'Lobster', 'Locust', 'Loris', 'Louse', 'Lynx', 'Lyrebird', 'Macaque', 'Macaw', 'Magpie', 'Mallard', 'Duck', 'Mammoth', 'Manatee', 'Mandrill', 'Margay', 'Marmoset', 'Marmot', 'Meerkat', 'Mink', 'Mole', 'Mongoose', 'Monkey', 'Moose', 'Mosquito', 'Mouse', 'Myna', 'Narwhal', 'Newt', 'Nightingale', 'Nilgai', 'Ocelot', 'Octopus', 'Okapi', 'Oncilla', 'Opossum', 'Orangutan', 'Oryx', 'Ostrich', 'Otter', 'Ox', 'Cattle', 'Owl', 'Oyster', 'Panther', 'Parrot', 'Panda', 'Giant', 'Partridge', 'Peafowl', 'Penguin', 'Pheasant', 'Pig', 'Boar', 'Pigeon', 'Columbine', 'Pika', 'Polar', 'Pony', 'Horse', 'Porcupine', 'Porpoise', 'Prairie', 'Pug', 'Quail', 'Quelea', 'Quetzal', 'Rabbit', 'Raccoon', 'Ram', 'Sheep', 'Rat', 'Raven', 'Red', 'Red', 'Reindeer', 'Rhea', 'Rhinoceros', 'Rook', 'Saki', 'Salamander', 'Salmon', 'Sand', 'Sandpiper', 'Sardine', 'Sassaby', 'Sea', 'Seahorse', 'Seal', 'Serval', 'Shark', 'AUS', 'Sheep', 'Ram', 'Shrew', 'Shrike', 'Siamang', 'Skink', 'Skipper', 'Skunk', 'Sloth', 'Snail', 'Snake', 'Spider', 'Spoonbill', 'Squid', 'Teuthidane', 'Squirrel', 'Starling', 'Stilt', 'Swan', 'Tamarin', 'Tapir', 'Tarsier', 'Termite', 'Thrush', 'Tiger', 'Toad', 'Topi', 'Toucan', 'Turaco', 'Turkey', 'Turtle', 'Vicuna', 'Vinegaroon', 'Viper', 'Vulture', 'Wallaby', 'Walrus', 'Wasp', 'Water', 'Waxwing', 'Weasel', 'Whale', 'Wobbegong', 'Wolf', 'Wolverine', 'Wombat', 'Woodpecker', 'Worm', 'Wren', 'Yak', 'Zebra']
            color = ['Aero', 'Alabaster', 'Almond', 'Amaranth', 'Amazon', 'Amber', 'Amethyst', 'Apricot', 'Aqua', 'Aquamarine', 'Artichoke', 'Asparagus', 'Auburn', 'Aureolin', 'Avocado', 'Azure', 'Beaver', 'Beige', 'Bisque', 'Bistre', 'Bittersweet', 'Black', 'Blond', 'Blue', 'Bluetiful', 'Blush', 'Bole', 'Bone', 'Brandy', 'Bronze', 'Brown', 'Buff', 'Burgundy', 'Burlywood', 'Byzantine', 'Byzantium', 'Cadet', 'Camel', 'Canary', 'Capri', 'Cardinal', 'Carmine', 'Carnelian', 'Catawba', 'Celadon', 'Celeste', 'Cerise', 'Cerulean', 'Champagne', 'Charcoal', 'Chestnut', 'Cinereous', 'Cinnabar', 'Citrine', 'Citron', 'Claret', 'Coffee', 'Copper', 'Coquelicot', 'Coral', 'Cordovan', 'Corn', 'Cornsilk', 'Cream', 'Crimson', 'Crystal', 'Cultured', 'Cyan', 'Cyclamen', 'Denim', 'Desert', 'Drab', 'Ebony', 'Ecru', 'Eggplant', 'Eggshell', 'Eigengrau', 'Emerald', 'Eminence', 'Erin', 'Fallow', 'Fandango', 'Fawn', 'Feldgrau', 'Firebrick', 'Flame', 'Flax', 'Flirt', 'Frostbite', 'Fuchsia', 'Fulvous', 'Gainsboro', 'Gamboge', 'Glaucous', 'Gold', 'Goldenrod', 'Green', 'Grullo', 'Gunmetal', 'Harlequin', 'Heliotrope', 'Honeydew', 'Iceberg', 'Icterine', 'Inchworm', 'Independence', 'Indigo', 'Iris', 'Irresistible', 'Isabelline', 'Ivory', 'Jade', 'Jasmine', 'Jet', 'Jonquil', 'Keppel', 'Kobe', 'Kobi', 'Kobicha', 'Lava', 'Lemon', 'Liberty', 'Lilac', 'Linen', 'Lion', 'Liver', 'Livid', 'Magenta', 'Magnolia', 'Mahogany', 'Maize', 'Malachite', 'Manatee', 'Mandarin', 'Mango', 'Mantis', 'Marigold', 'Mauve', 'Mauvelous', 'Melon', 'Midnight', 'Mindaro', 'Ming', 'Mint', 'Mulberry', 'Mustard', 'Mystic', 'Nickel', 'Nyanza', 'Ochre', 'Olive', 'Olivine', 'Onyx', 'Opal', 'Orange', 'Orchid', 'Oxblood', 'Parchment', 'Patriarch', 'Peach', 'Pear', 'Periwinkle', 'Persimmon', 'Phlox', 'Pink', 'Pistachio', 'Platinum', 'Plum', 'Popstar', 'Prune', 'Puce', 'Pumpkin', 'Purple', 'Purpureus', 'Rajah', 'Raspberry', 'Razzmatazz', 'Red', 'Redwood', 'Rhythm', 'Rose', 'Rosewood', 'Ruber', 'Ruby', 'Rufous', 'Russet', 'Rust', 'Saffron', 'Sage', 'Salmon', 'Sand', 'Sapphire', 'Scarlet', 'Seashell', 'Sepia', 'Shadow', 'Sienna', 'Silver', 'Sinopia', 'Skobeloff', 'Smitten', 'Snow', 'Straw', 'Strawberry', 'Sunglow', 'Sunray', 'Sunset', 'Tan', 'Tangerine', 'Taupe', 'Teal', 'Telemagenta', 'Thistle', 'Timberwolf', 'Tomato', 'Tumbleweed', 'Turquoise', 'Tuscan', 'Tuscany', 'Ultramarine', 'Umber', 'Vanilla', 'Verdigris', 'Vermilion', 'Vermilion', 'Veronica', 'Violet', 'Viridian', 'Volt', 'Wheat', 'White', 'Wine', 'Wisteria', 'Xanadu', 'Xanthic', 'Xanthous', 'Yellow', 'Zaffre', 'Zomp']
            alias = f"{random.choice(color)}{random.choice(animal)}"
            conChannel[f"{userID}"] = {"alias": alias, "currentPrompt": None}
            conChannel["pool"].append(userID)
            pool = conChannel["pool"]
            position = pool.index(userID)
            rPosition = position + 1
            task(promptUpdater(guildID, channelID, promptCode))
            if position >= turn:
                wait = position - turn
            else:
                wait = len(pool) - (turn - position) - 1
            waitTime = wait*turnLength
            conMin = getConfigInt(guildID, channelID, 'contributor_minimum')
            if conChannel["paused"]:
                task(replyOrSend(user, iID, iToken, isInteraction, f"You have joined the pool of contributors for prompt {promptCode} under the alias {alias}. The prompt is currently paused. I will message you when it unpauses."))
                return
            if conChannel["promptStarted"]:
                if len(pool) > conMin:
                    task(replyOrSend(user, iID, iToken, isInteraction, f"You have joined the pool of contributors for prompt {promptCode} under the alias {alias}. You are contributor #{rPosition}. It will be your turn in {wait} turns. Your next turn will begin in at most {waitTime} minutes."))
                    return
                if(len(pool)) < conMin:
                    task(replyOrSend(user, iID, iToken, isInteraction, f"You have joined the pool of contributors for prompt {promptCode} under the alias {alias}. I will message you when enough contributors have joined to begin the prompt."))
                    return
            if len(pool) == conMin:
                conChannel["promptStarted"] = True  
                task(replyOrSend(user, iID, iToken, isInteraction, f"You have joined the pool of contributors for prompt {promptCode} under the alias {alias}. The prompt now has the minimum required number of contributors and will begin. You are contributor #{rPosition}. Your next turn will start in at most {waitTime} minutes."))
                await sendNext(guildID, channelID, promptCode, turnLength)
                for con in range(0, len(pool)):
                    pUserID = pool[con]
                    pUser = await bot.fetch_user(pUserID)
                    if con == 0:
                        nextTime = ns() + nsMinute*turnLength
                        contributors[f"{guildID}"][f"{channelID}"]["timer"] = nextTime
                        createTimer(nextTime, "autopass", guildID, channelID, promptCode, pUserID, contributions)
                    else:
                        await pUser.send(f"Prompt {promptCode} is starting. You are contributor #{rPosition}. Your next turn will start in at most {waitTime} minutes.")
            else:
                task(replyOrSend(user, iID, iToken, isInteraction, f"You have joined the pool of contributors for prompt {promptCode} under the alias {alias}. I will message you when enough contributors have joined to begin the prompt."))
    else:
        task(replyOrSend(user, iID, iToken, isInteraction, f"Prompt {promptCode} has already reached its maximum contributors. You cannot join at the moment. Sorry :("))

async def action_post(userID, promptCode, text, iID, iToken, isInteraction, isPostMode):
    user = await bot.fetch_user(userID)
    data = codeChecker(promptCode)
    if not data:
        return
    guildID = data[0]
    channelID = data[1]
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    if userID in contributors[f"{guildID}"]["banned"]:
        task(replyOrSend(user, iID, iToken, isInteraction, "You have been banned, and can no longer join or contribute to prompts in this server."))
        return
    if userID in conChannel["kicked"]:
        task(replyOrSend(user, iID, iToken, isInteraction, f"You have been kicked from prompt {promptCode} and can no longer join or contribute to it. This is only temporary. You will be able to rejoin prompts in this server / channel when a new one is created."))
        return
    pool = conChannel["pool"]
    turn = conChannel["turn"]
    multipost = conChannel["multipost"]
    position = pool.index(userID)    
    channel = bot.get_channel(channelID)
    if userID in pool:
        if turn == position:
            if conChannel["paused"]:
                task(replyOrSend(user, iID, iToken, isInteraction, f"Prompt {promptCode} is currently paused and all actions except dropping and joining are disabled until it resumes. I will message you when it unpauses."))
                return
            alias = conChannel[f"{userID}"]["alias"]
            if isInteraction or isPostMode:
                contributions = getConfigInt(guildID, channelID, "promptcontributions")
                contributions += 1
                addConfig(guildID, channelID, "promptcontributions", contributions)
                if contributions == 1:
                    task(promptUpdater(guildID, channelID, promptCode))
                conChannel["context"].pop(0)
                conChannel["context"].append(f">>> *from {alias}:*\n{text}")
                if multipost:
                    msg = await channel.send(text)
                else:
                    text = f"*from {alias}:*\n{text}"
                    msg = await channel.send(text)
                    conChannel["multipost"] = True
                if isInteraction:
                    iHReply(iID, iToken, f"The text you submitted has been posted to prompt {promptCode} under the alias {alias}. You may continue to /post until your turn ends. /pass to end your turn early.")
                conChannel["posts"].append(msg)
                logUpdater(guildID, channelID, promptCode, text)
                return
            else:
                await user.send(f"You have entered Post Mode. Any messages you send me here will be posted to prompt {promptCode} under the alias {alias}. Your turn will still end at its normal time. /pass to end Post Mode (and your turn) early.")
                contributors["postMode"][f"{userID}"] = promptCode
        else:
            turnLength = getConfigInt(guildID, channelID, "turn_length")
            if position >= turn:
                wait = position - turn
            else:
                wait = len(pool) - (turn - position) - 1
            waitTime = wait*turnLength 
            task(replyOrSend(user, iID, iToken, isInteraction, f"It is not your turn to contribute to prompt {promptCode}. It will be your turn in {wait} turns. Your next turn will begin in at most {waitTime} minutes."))
    elif isInteraction:
        iHReply(iID, iToken, f"You are not part of the contributor pool for prompt {promptCode}. You need to /join it before you can take a turn.")

async def action_pass(userID, promptCode, iID, iToken, isInteraction, isDrop, isAutopass):
    user = await bot.fetch_user(userID)
    data = codeChecker(promptCode)
    if not data:
        return
    guildID = data[0]
    channelID = data[1]
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    if userID in contributors[f"{guildID}"]["banned"]:
        task(replyOrSend(user, iID, iToken, isInteraction, "You have been banned, and can no longer join or contribute to prompts in this server."))
        return
    if userID in conChannel["kicked"]:
        task(replyOrSend(user, iID, iToken, isInteraction, f"You have been kicked from prompt {promptCode} and can no longer join or contribute to it. This is only temporary. You will be able to rejoin prompts in this server / channel when a new one is created."))
        return
    pool = conChannel["pool"]
    getConfigInt(guildID, channelID, "promptcontributions")
    turn = conChannel["turn"]
    turnLength = getConfigInt(guildID, channelID, "turn_length")  
    promptStarted = conChannel["promptStarted"]
    try:
        position = pool.index(userID)
        if position > turn:
            wait = position - turn
        else:
            wait = len(pool) - (turn - position) - 1
        waitTime = wait*turnLength
    except:
        pass
    if userID in pool:
        if conChannel["paused"]:
            if isDrop:
                nextTurn(guildID, channelID)
            else:
                task(replyOrSend(user, iID, iToken, isInteraction, f"Prompt {promptCode} is currently paused and all actions except dropping and joining are disabled until it resumes. I will message you when it unpauses."))
            return
        if promptStarted and len(pool) >= getConfigInt(guildID, channelID, "contributor_minimum"):
            if turn == position:
                timers.pop(f'{conChannel["timer"]}', None)
                nextTurn(guildID, channelID)
                nextTime = ns() + nsMinute*turnLength
                nextUID = pool[conChannel["turn"]]
                if not isDrop and not isAutopass:
                    task(replyOrSend(user, iID, iToken, isInteraction, f"You have ended your turn for prompt {promptCode}. It will be your turn in {wait} turns. Your next turn will begin in at most {waitTime} minutes."))               
                if not isDrop and isAutopass:
                    await user.send(f"Your turn for prompt {promptCode} has automatically ended. It will be your turn in {wait} turns. Your next turn will begin in at most {waitTime} minutes.")
                contributions = getConfigInt(guildID, channelID, "promptcontributions")
                contributors[f"{guildID}"][f"{channelID}"]["timer"] = nextTime
                createTimer(nextTime, "autopass", guildID, channelID, promptCode, nextUID, contributions)
                contributors["postMode"].pop(f"{userID}", None)
                removeReactable(conChannel["postReactible"].id)
                await conChannel["postReactible"].unpin()
                if len(pool) >= getConfigInt(guildID, channelID, 'contributor_minimum'):
                    task(sendNext(guildID, channelID, promptCode, turnLength))
            elif not isAutopass:
                task(replyOrSend(user, iID, iToken, isInteraction, f"It is not your turn to contribute to prompt {promptCode}. It will be your turn in {wait} turns. Your next turn will begin in at most {waitTime} minutes."))
        elif isInteraction:
            iHReply(iID, iToken, f"Prompt {promptCode} does not have enough contributors to start. When it does, you will have turn #{position} and may have to wait up to {waitTime} minutes before it is your turn.")   
    elif isInteraction:
        iHReply(iID, iToken, f"You are not part of the contributor pool for prompt {promptCode}. You need to /join it before you can take a turn.")        

async def action_drop(userID, promptCode, iID, iToken, alias, isInteraction, isKick, isBan, isAutopass):
    user = await bot.fetch_user(userID)
    data = codeChecker(promptCode)
    if not data:
        return
    guildID = data[0]
    channelID = data[1]    
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    turn = conChannel["turn"]
    pool = conChannel["pool"]
    try:
        pos = pool.index(userID)
        conChannel["pool"].remove(userID)
        if turn == pos:
            await action_pass(userID, promptCode, None, None, isInteraction=False, isDrop=True, isAutopass=isAutopass)
            turn = conChannel["turn"]
        if turn > pos:
            conChannel["turn"] -= 1
        if len(pool) < getConfigInt(guildID, channelID, "contributor_minimum"):
            for id in pool:
                u = await bot.fetch_user(id)
                await u.send(f"Prompt {promptCode} has dropped below the minimum required contributors and has paused. It will resume when sufficient contributors have joined.")
        task(promptUpdater(guildID, channelID, promptCode))
        if isKick:
            iHReply(iID, iToken, f'Contributor "{alias}" has been kicked from prompt {promptCode}.')
            await user.send(f"You have been kicked from prompt {promptCode}. You cannot rejoin that prompt, but can join other prompts and new ones as they are generated.")
        elif isBan:
            iHReply(iID, iToken, f'Contributor "{alias}" has been banned from all current and future prompts on this server.')
            guild = await bot.fetch_guild(guildID)
            await user.send(f"You have been permanently banned from contributing to all prompts in {guild.name}")
        elif isAutopass:
            await user.send(f"You have been dropped from the contributor pool of prompt {promptCode} for inactivity.")
        else:
            task(replyOrSend(user, iID, iToken, isInteraction, f"You have dropped out of the contributor pool for prompt {promptCode}. You may /join it again at any time."))
    except:
        if isInteraction:
            if not isKick and not isBan:
                iHReply(iID, iToken, f"You are not in the contributor pool for prompt {promptCode}.")
            else:
                iHReply(iID, iToken, f'Contributor "{alias}" could not be found.')

async def action_pause(guildID, channelID, iID, iToken, isInteraction):
    conChannel = contributors[f"{guildID}"][f"{channelID}"]
    paused = conChannel["paused"]
    pool = conChannel["pool"]
    turn = conChannel["turn"]
    promptCode = getConfig(guildID, channelID, "promptcode")
    if promptCode:
        if paused:
            conChannel["paused"] = False
            task(promptUpdater(guildID, channelID, promptCode))
            if len(pool) >= getConfigInt(guildID, channelID, "contributor_minimum"):
                turnLength = getConfigInt(guildID, channelID, "turn_length")
                task(sendNext(guildID, channelID, promptCode, turnLength))
                for pos in range(0, len(pool)):
                    if pos == turn and turn == 0 and not conChannel["promptStarted"]:
                        nextTime = ns() + nsMinute*turnLength
                        contributions = getConfigInt(guildID, channelID, "promptcontributions")
                        contributors[f"{guildID}"][f"{channelID}"]["timer"] = nextTime
                        createTimer(nextTime, "autopass", guildID, channelID, promptCode, pool[pos], contributions)
                    elif pos != turn:
                        u = await bot.fetch_user(pool[pos])
                        rPosition = pos + 1
                        if pos > turn:
                            wait = pos - turn
                        else:
                            wait = len(pool) - (turn - pos) - 1
                        waitTime = wait*turnLength
                        await u.send(f"Prompt {promptCode} is starting. You are contributor #{rPosition}. Your next turn will start in at most {waitTime} minutes.")
                conChannel["promptStarted"] = True
            if isInteraction:
                iHReply(iID, iToken, f"Prompt {promptCode} has resumed. Use this command again to pause it.")
        else:
            conChannel["paused"] = True
            task(promptUpdater(guildID, channelID, promptCode))
            postMode = contributors["postMode"]
            try:
                timers.pop(f'{conChannel["timer"]}', None)
            except:
                pass
            forDeletion = None
            for id in postMode:
                if postMode[id] == promptCode:
                    forDeletion = id
                    break
            contributors["postMode"].pop(forDeletion, None)
            if conChannel["promptStarted"]:
                for id in pool:
                    user = await bot.fetch_user(id)
                    await user.send(f"Prompt {promptCode} has been paused. I will message you again when it resumes.")
            if isInteraction:
                iHReply(iID, iToken, f"Prompt {promptCode} has been paused. Use this command again to resume it.")
    elif isInteraction:
        iHReply(iID, iToken, "A prompt has not yet been generated in this channel.")

async def action_help(userID):
    user = await bot.fetch_user(userID)
    msg = await user.send("**Help Menu** (React to Select)\n  🪶 – About & User Guide\n  🎊 – Admin Startup\n  📊 – Prompt Configuration\n  🤖 – Automation\n  💸 – Github & Tip the Author")
    addReactable(msg.id)
    await msg.add_reaction("🪶")
    await msg.add_reaction("🎊")
    await msg.add_reaction("📊")
    await msg.add_reaction("🤖")
    await msg.add_reaction("💸")

@bot.event
async def on_interaction(data):
    iID = int(data["id"])
    iToken = data["token"]
    iName = data["data"]["name"]
    try:
        roles = [str(x) for x in data["member"]["roles"]]
    except:
        roles = []
    try:
        userID = int(data["user"]["id"])
    except:
        userID = int(data["member"]["user"]["id"])
    channelID = int(data["channel_id"])
    iChannel = bot.get_channel(channelID)
    if "guild_id" in data:
        guildID = int(data["guild_id"])
        iGuild = bot.get_guild(guildID)
        member = await iGuild.fetch_member(userID)
        if member.guild_permissions.administrator:
            serverAdmin = True
        else:
            serverAdmin = False
    else:
        serverAdmin = False
        guildID = None
        iGuild = None
        member = None
    try:
        iOpt = data["data"]["options"]
    except:
        iOpt = None
    admin = getConfig(guildID, channelID, "admin")
    moderator = getConfig(guildID, channelID, "moderator")
    if admin == "none":
        admin = None
    if moderator == "none":
        moderator = None
    if admin:
        adminName = iGuild.get_role(int(admin)).name
    else:
        adminName = "LewdRobin Admin"
    if moderator:
        moderatorName = iGuild.get_role(int(moderator)).name
    else:
        moderatorName = "LewdRobin Moderator"
    admin = True if admin in roles or serverAdmin else False
    moderator = True if moderator in roles or serverAdmin else False
    if iName == "roles":
        if serverAdmin:
            guild = await bot.fetch_guild(guildID)
            exceptions = 0
            msg = ""
            try:
                for opt in range(0, len(iOpt)):
                    if iOpt[opt]["name"] == "admin":
                        admRole = guild.get_role(int(iOpt[opt]["value"]))
                        if admRole:
                            addConfig(guildID, "default", "admin", iOpt[opt]["value"])
                            msg += f"You have assigned LewdRobin admin priveledges to the {admRole.name} role."
                        else:
                            msg = "Something seems to have gone wrong with assigning the admin role."
            except:
                exceptions += 1
            try:
                for opt in range(0, len(iOpt)):
                    if iOpt[opt]["name"] == "moderator":                
                        modRole = guild.get_role(int(iOpt[opt]["value"]))
                        if modRole:
                            addConfig(guildID, "default", "moderator", iOpt[opt]["value"])
                            msg += f"\nYou have assigned LewdRobin moderator priveledges to the {modRole.name} role."
                        else:
                            msg = "Something seems to have gone wrong with assigning the moderator role."
            except:
                exceptions += 1
            if exceptions == 2:
                msg = "Something seems to have gone wrong with this command."
            iHReply(iID, iToken, msg)
        else:
            iHReply(iID, iToken, "You need to be a server admin to use this command.")
        return
    elif iName == "run":
        if moderator:
            task(action_run(guildID, channelID, iChannel, iID, iToken, isInteraction = True))
        else:
            iHReply(iID, iToken, f"You need the {moderatorName} role to use this command.")
        return
    elif iName == "autorun":
        if moderator:
            period = iOpt[0]["value"]
            delay = iOpt[1]["value"]
            addConfig(guildID, channelID, "autoperiod", period)
            firstTime = ns() + nsMinute*delay
            contributors[f"{guildID}"][f"{channelID}"]["autoTime"] = firstTime
            createTimer(firstTime, "autorun", guildID, channelID, None, None, None)
            iHReply(iID, iToken, f"Prompts will run automatically in this channel every {period} minutes, starting after a {delay}-minute delay.")
        else:
            iHReply(iID, iToken, f"You need the {moderatorName} role to use this command.")
        return
    elif iName == "autorun_stop":
        if moderator:
            timers.pop(f'{contributors[f"{guildID}"][f"{channelID}"]["autoTime"]}', None)
            iHReply(iID, iToken, f"Prompts will no longer autorun in this channel.")
        else:
            iHReply(iID, iToken, f"You need the {moderatorName} role to use this command.")
        return
    elif iName == "generate":
        if guildID:
            if moderator:
                task(action_generate(guildID, channelID, userID, iChannel, iID, iToken, isInteraction=True))
            else:
                iHReply(iID, iToken, f"You need the {moderatorName} role to use this command.")                
        else:
            task(action_generate(guildID, channelID, userID, iChannel, iID, iToken, isInteraction=True))            
        return
    elif iName in ["time", "categories", "character_types", "contributors", "environments", "play_bdsm", "play_surreal", "play_vanilla", "species_anthros", "species_fantasy", "species_futuristic", "species_monster"]:
        if guildID:
            if admin:  
                reply = commandConfigSetter(iOpt, guildID, iChannel)
                iHReply(iID, iToken, reply)
            else:
                iHReply(iID, iToken, f"You need the {adminName} role to use this command.")
        else:            
            reply = commandDMConfigSetter(iOpt, userID)
            iHReply(iID, iToken, reply)
        return
    elif iName == "reset":
        if guildID:
            if admin:
                if iOpt[0]["value"] == "reset":
                    config = configparser.ConfigParser()
                    configPath = ap(f'{serverConfigs}\{guildID}.ini')
                    config.read(configPath)
                    config[f'{channelID}'] = {}
                    with open(configPath, 'w') as configfile:
                        config.write(configfile)
                    iHReply(iID, iToken, f"Channel specific settings for{iChannel.name} have been reset. Using server defaults instead.")
                else:
                    iHReply(iID, iToken, f'You failed to properly confirm this command. Type "reset" in the confirmation if you really want to reset all configs in this channel.') 
            else:
                iHReply(iID, iToken, f"You need the {adminName} role to use this command.")
        else:
            if iOpt[0]["value"] == "reset":
                DMConfig[f"{userID}"] = {}
                iHReply(iID, iToken, "You have reset the settings for DM prompt generation to default")
            else:
                iHReply(iID, iToken, f'You failed to properly confirm this command. Type "reset" in the confirmation if you really want to reset all configs in this channel.')
        return
    elif iName in ["join", "post", "pass", "drop"]:
        user = await bot.fetch_user(userID)
        if not await can_message(user):
            iHReply(iID, iToken, "To participate in LewdRobin prompts, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
            return
        promptCode = str(iOpt[0]["value"]).zfill(4)
        pData = codeChecker(promptCode)
        if not pData:
            iHReply(iID, iToken, f"Something went wrong with your command. Make sure your prompt code is correct.")
        else:
            if iName == "join":
                task(action_join(userID, promptCode, iID, iToken, isInteraction=True))
            elif iName == "post":
                text = iOpt[1]["value"]
                task(action_post(userID, promptCode, text, iID, iToken, isInteraction=True, isPostMode=False))
            elif iName == "pass":
                task(action_pass(userID, promptCode, iID, iToken, isInteraction=True, isDrop=False, isAutopass=False))
            elif iName == "drop":
                task(action_drop(userID, promptCode, iID, iToken, None, isInteraction=True, isKick=False, isBan=False, isAutopass=False))
        return
    elif iName == "kick":
        if moderator:
            alias = iOpt[0]["value"]
            try:
                conChannel = contributors[f"{guildID}"][f"{channelID}"]
                keys = conChannel.keys()
                kickID = None
                for key in keys:
                    try:
                        if conChannel[f"{key}"]["alias"] == alias:
                            kickID = int(key)
                            break
                    except:
                        pass
                if kickID:
                    conChannel["kicked"].append(kickID)
                    promptCode = getConfig(guildID, channelID, "promptcode")
                    task(action_drop(kickID, promptCode, iID, iToken, alias, isInteraction=True, isKick=True, isBan=False, isAutopass=False))
                else:
                    iHReply(iID, iToken, f'Could not find a contributor to kick with alias "{alias}". Make sure to use this command in the channel this alias was used in.')
            except:
                iHReply(iID, iToken, f'Could not find a contributor to kick with alias "{alias}". Make sure to use this command in the channel this alias was used in.') 
        else:
            iHReply(iID, iToken, f"You need the {moderatorName} role to kick contributors from LewdRobin prompts in this server.")
        return
    elif iName == "ban":
        if admin:
            alias = iOpt[0]["value"]
            try:
                conChannel = contributors[f"{guildID}"][f"{channelID}"]
                keys = conChannel.keys()
                banID = None
                for key in keys:
                    try:
                        if conChannel[f"{key}"]["alias"] == alias:
                            banID = int(key)
                            break
                    except:
                        pass
                if banID:
                    contributors[f"{guildID}"]["banned"].append(banID)
                    promptCode = getConfig(guildID, channelID, "promptcode")
                    task(action_drop(banID, promptCode, iID, iToken, alias, isInteraction=True, isKick=False, isBan=True, isAutopass=False))
                else:
                    iHReply(iID, iToken, f'Could not find a contributor to ban with alias "{alias}". Make sure to use this command in the channel this alias was used in.')
            except:
                iHReply(iID, iToken, f'Could not find a contributor to ban with alias "{alias}". Make sure to use this command in the channel this alias was used in.') 
        else:
            iHReply(iID, iToken, f"You need the {adminName} role to kick contributors from LewdRobin prompts in this server.")
        return
    elif iName == "display_settings":
        if guildID:
            display = displaySettings(guildID, channelID, iChannel.name)
            iHReply(iID, iToken, display[0])
            iHFollowup(iToken, display[1])
            iHFollowup(iToken, display[2])
            iHFollowup(iToken, display[3])
        else:
            display = displayDMSettings(userID)
            iHReply(iID, iToken, display[0])
            iHFollowup(iToken, display[1])
            iHFollowup(iToken, display[2])          
        return
    elif iName == "pause":
        if moderator:
            task(action_pause(guildID, channelID, iID, iToken, isInteraction=True))
        else:
            iHReply(iID, iToken, "You do not have permission to pause/unpause prompts on this server")
        return
    elif iName == "help":
        user = await bot.fetch_user(userID)
        if not await can_message(user):
            iHReply(iID, iToken, "To view LewdRobin's help menu, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
            return
        iHReply(iID, iToken, "Check your DMs for the help menu.")
        task(action_help(userID))
        return
    elif iName == "unban_all":
        if admin:
            if iOpt[0]["value"] == "unban":
                contributors[f"{guildID}"]["banned"] = []
                iHReply(iID, iToken, f"The banned contributor list for this server has been reset")
            else:
                iHReply(iID, iToken, f'You failed to properly confirm this command. Type "unban" in the confirmation if you really want to reset all configs in this channel.')
        else:
            iHReply(iID, iToken, f"You need the {adminName} role to use this command.")
        return
    elif iName == "conclude":
        if moderator:
            try:
                promptCode = getConfig(guildID, channelID, "promptcode")
                if int(promptCode):
                    channel = await bot.fetch_channel(channelID)
                    await promptConcluder(guildID, channelID, channel, promptCode)
                    contributorsConfig(guildID, channelID)
                    addConfig(guildID, channelID, "promptCode", 0)
                    addConfig(guildID, channelID, "promptID", 0)
                    addConfig(guildID, channelID, "promptContributions", 0)
                    addConfig(guildID, channelID, "promptText", "")
                    contributorsConfig(guildID, channelID)
                    iHReply(iID, iToken, f"Prompt {promptCode} has been concluded.")
                else:
                    iHReply(iID, iToken, f"No active prompt found in this channel.")
            except:
                iHReply(iID, iToken, f"No active prompt found in this channel.")
        else:
            iHReply(iID, iToken, f"You need the {moderatorName} role to use this command.")
        return      

@bot.event
async def on_message(message):
    userID = message.author.id
    if userID == bot.user.id:
        if message.is_system():
            await message.delete()
    elif isinstance(message.channel, discord.channel.DMChannel):
        postMode = contributors["postMode"]
        if f"{userID}" in postMode.keys():
            data = codeChecker(postMode[f'{userID}'])
            guildID = data[0]
            channelID = data[1]
            text = message.content
            promptCode = getConfig(guildID, channelID, "promptcode")
            task(action_post(userID, promptCode, text, None, None, isInteraction=False, isPostMode=True))

@bot.event
async def on_raw_reaction_add(payload):
    botID = bot.user.id  
    messageID = payload.message_id
    userID = payload.user_id
    if messageID in getReactables() and userID != botID:
        emoji = payload.emoji.name
        user = await bot.fetch_user(userID)
        channelID = payload.channel_id
        channel = bot.get_channel(channelID)
        message = await channel.fetch_message(messageID)
        guildID = payload.guild_id
        if guildID:
            guild = bot.get_guild(guildID)
            member = await guild.fetch_member(userID)
            roles = [str(x.id) for x in member.roles]
            if member.guild_permissions.administrator:
                serverAdmin = True
            else:
                serverAdmin = False
        else:
            roles = []
            serverAdmin = False
            guild = None
            member = None 
        moderator = getConfig(guildID, channelID, "moderator")
        if moderator == "none":
            moderator = None
        if moderator:
            moderatorName = guild.get_role(int(moderator)).name
        else:
            moderatorName = "LewdRobin Moderator"
        moderator = True if moderator in roles or serverAdmin else False
        try:
            promptCode = getConfig(guildID, channelID, "promptcode")
            promptCode = promptCode if promptCode else re.findall("rompt (\d\d\d\d)", message.content)[0]
        except:
            pass
        if not guildID:
            if emoji == "▶️":
                task(action_post(userID, promptCode, None, None, None, isInteraction=False, isPostMode=False))
                return
            if emoji == "⏩":
                task(action_pass(userID, promptCode, None, None, isInteraction=False, isDrop=False, isAutopass=False))
                return
            if emoji == "📝":
                data = codeChecker(promptCode)
                await user.send(getConfig(data[0], data[1], "prompttext"))
                return
            if emoji == "📚":
                data = codeChecker(promptCode)
                for ctx in contributors[f"{data[0]}"][f"{data[1]}"]["context"]:
                    if ctx:
                        await user.send(ctx)
                return
            if emoji == "🪶":
                await user.send("**About**\nI am a bot that facilitates anonymous collaborative erotic writing.\nI generate writing prompts from a configurable pool of environments, characters, scenes, and play types. Contributors then join my prompts anonymously and are assigned temporary aliases which their writing will be posted under.\nWith my prompt as a starting point, contributors take turns adding to the story. Each contributor gets a configurable amount of time to write before the turn passes to the next person in line.")
                await user.send("**User Guide**\nAll of my user-facing features can be accessed either through slash commands or reactions. I'll list both ways in this guide.\n*Contributing to a prompt, step-by-step*\n**1.**  Make sure your server admins have invited me to their server, configured a channel for my prompts to play out in, and generated a prompt.\n**2.**  You can join my prompt by reacting to it with ✅ or by using the /join command along with the prompt's 4-digit code either in the server or in my DMs. Once you've joined, I'll DM you with the alias your contributions will be made under. However, the prompt may not immediately begin if it has fewer than the minimum required contributors (this count updates on the prompt message).\n**3.**  Contributing is turn-based, and each player gets 30 minutes (default) to contribute. I'll DM you when it's your turn. That DM will get pinned, and has a set of reacitons you can use to control your turn. If you need a refresher on the prompt, react with 📝 and I'll DM it to you. If you'd like some context, react with 📚 and I'll DM you the three most recent contributions to the prompt.\n**4.**  Now it's your turn to start contributing. You can do this in two ways. You can use the /post slash command with the prompt number and the text you'd like to post, either in the relevant server or my DMs. The easier way, however, is to react with ▶️ to enter Play Mode. Play Mode lasts the rest of your turn, and while you're in it, anything you DM me (except slash commands) will get posted as a contribution to the prompt.\n**5.**  Your turn will end automatically after its designated duration is over. You can end it early with ⏩ or /pass. You can also drop from the prompt at any time with ❌ (on the DM I sent you when your turn started or the prompt itself) or /drop. If you don't post a contribution or pass your turn within the time limit, you will be dropped from the prompt for inactivity.\n If you'd like to toy with prompt generation, you can use /generate in my DMs and set up generation settings in our private channel.")
                return
            if emoji == "🎊":
                await user.send("**Admin Startup**\n*step-by-step guide to get me set up on your server*\n**1.**  Use this link to add me to your server:\n[temporarily disabled until Lewd Robin has a stable host server]\nOnce you've added me to your server, I'll need a minute or two to set up slash commands.\n**2.**  Make a channel for my prompts to run in. I will need the `View Channel, Send Message, Add Reactions, Manage Messages, and Read Message History` permissions here. Potential contributors to the prompts I generate here should have the `View Channel, Add Reactions, Read Message History, and Use Slash Commands` permissions here. They should *not* have the `Send Messages` persmission in this channel.\n**3.**  Create LewdRobin Admin and Moderator roles. By default, only server admins can configure my settings or run prompts. If you want other members of your server to be able to do so, you will have to create roles for them. These will control who can use which slash and reaction commands in this server. These roles can be called anything, and don't need to grant any actual Discord permissions. Once you've created these roles, you will need to copy their IDs. To do this enable developer mode (User Settings -> Advanced -> Developer Mode) and right click on the roles in the role interface. Use the /roles command and paste in the role IDs for the IDs you want to be LewdRobin Admins and Moderators.\n*Admins* can configure, /display and /reset settings, /ban and /unban_all contributors.\n*Moderators* can /run prompts, /pause and resume prompts, and /kick contributors.\n**4.**  Configure settings. I use default settings to start with, but they can be fine-tuned for each channel I run prompts in. See 📊 Prompt Configuration for more info.")
                return
            if emoji == "📊":
                await user.send("**Prompt Configuration**\nThis will cover prompt settings configurable by people with the LewdRobin Admin role for your server. All settings have a server-wide default which is not (currently) modifiable. Any adjustments to settings are made on a channel-by-channel basis. Use /display_settings in a channel to create a message displaying its current settings. Modify settings with the commands listed below.\n**/Contributors**\n  turn_length – length in minutes of each contributor's turn\n  contributor_minimum – the minimum number of contributors a prompt needs before it can start\n  contributor_maximum – the most contributors a prompt can have at once\n**/categories**\n  [category]_on – whether prompts will generate this type of thing. At least one category must be turned on.\n  character_number – how many randomly generated characters will be created per prompt\n  play_number – how many play types will be generated per prompt\n**/environments**\nEnvironments and scenes both use these tags to determine the pool for generation. If any of an environment's tags are excluded here, it will be excluded; scenes are then drawn from a pool that matches the environment's tags.\n  [america/europe/japan] - environments set in this specific region\n  historical – environments set before 1980\n  modern – environments set between 1980 and 2030\n  futuristic – environments set after 2030\n  fantasy – environments with magical or fantasy-related elements\n**/character_types**\n  [type] – toggles whether this type of character is generated. If at least one of cis_men or cis_women are enabled, they will be given a weighted bias in the generation pool.\n**/species**\nIf humans are enabled, they will be given a weighted bias.\n  [species] – whether characters from this species group will be generated. May include multiple similar species.\n**/play**\n  [play type] – whether play recommendations from this activity group will be included. May include multiple similar activities.")
                return
            if emoji == "🤖":
                await user.send("**Automation**\nThe full automation feature is still under development, and the related /time command doesn't do anything (yet). However, basic automation can be started with /autorun and stopped with /autorun_stop. It will let you generate new prompts in a channel at a regular period.")
                return
            if emoji == "💸":
                await user.send(f"**Github**\nMy code is open source and free for anyone to use or modify. Find it at:\n<https://github.com/FaraCreations/LewdRobin>\n\n**Tip the Author**\nFara spent a lot of time lovingly coding to make me work. If you'd like to send her a tip, you can do so via:\n<https://paypal.me/FaraCreations>")
                return
        if emoji == "🔄":
            if moderator:
                user = await bot.fetch_user(userID)
                task(action_run(guildID, channelID, channel, None, None, isInteraction = False))
            else:
                msg = await channel.send(f"To run prompts in this channel, you need the {moderatorName} role.")
                await msg.delete(delay = 15)
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "🔄":
                        await reaction.remove(user)
            return
        if emoji == "❓":
            user = await bot.fetch_user(userID)
            if not await can_message(user):
                msg = await channel.send("To view LewdRobin's help menu, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
                await msg.delete(delay = 15)
                if guildID:
                    for reaction in message.reactions:
                        if reaction.emoji == "❓":
                            await reaction.remove(user)
                return
            task(action_help(userID))
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "❓":
                        await reaction.remove(user)
            return
        if emoji == "✅":
            if not await can_message(user):
                msg = await channel.send("To participate in LewdRobin prompts, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
                await msg.delete(delay = 15)
                if guildID:
                    for reaction in message.reactions:
                        if reaction.emoji == "✅":
                            await reaction.remove(user)
                return
            task(action_join(userID, promptCode, None, None, isInteraction=False))
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "✅":
                        await reaction.remove(user)
            return
        if emoji == "❌":
            if not await can_message(user):
                msg = await channel.send("To participate in LewdRobin prompts, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
                await msg.delete(delay = 15)
                if guildID:
                    for reaction in message.reactions:
                        if reaction.emoji == "❌":
                            await reaction.remove(user)
                return
            task(action_drop(userID, promptCode, None, None, None, isInteraction=False, isKick=False, isBan=False, isAutopass=False))
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "❌":
                        await reaction.remove(user)
            return
        if emoji == "📜":
            if not await can_message(user):
                msg = await channel.send("To recieve LewdRobin story logs, you need to enable direct messages from server members (User Settings -> Privacy & Safety)")
                await msg.delete(delay = 15)
                if guildID:
                    for reaction in message.reactions:
                        if reaction.emoji == "📜":
                            await reaction.remove(user)
                return
            promptCode = re.findall("(?<=\*\*Prompt\sCode:\*\*\s)(\d\d\d\d)", message.content)[0]
            task(logDisplay(user, promptCode))
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "📜":
                        await reaction.remove(user)
            return   
        if emoji == "⏯":
            if moderator:
                task(action_pause(guildID, channelID, None, None, isInteraction=False))
            else:
                msg = await channel.send(f"To pause/resume prompts in this channel, you need a {moderatorName} role.")
                await msg.delete(delay = 15)
            if guildID:
                for reaction in message.reactions:
                    if reaction.emoji == "⏯":
                        await reaction.remove(user)
            return
        if emoji == "🔃":
            if guildID:
                if moderator:
                    task(action_generate(guildID, channelID, userID, channel, None, None, isInteraction=False))
                else:
                    msg = await channel.send(f"To generate prompts here, you need the {moderatorName} role. You can generate prompts privately by DMing me /generate, though!")
                    await msg.delete(delay = 15)
                for reaction in message.reactions:
                        if reaction.emoji == "🔃":
                            await reaction.remove(user)
            else:
                task(action_generate(guildID, channelID, userID, channel, None, None, isInteraction=False))
            return
        if guildID:
            for reaction in message.reactions:
                await reaction.remove(user)

async def timer_loop():
    while True:
        await asyncio.sleep(60)
        now = ns()
        if is_connected():
            for timer in timers:
                time = timers[timer]["time"]
                action = timers[timer]["action"]
                guildID = timers[timer]["guildID"]
                channelID = timers[timer]["channelID"]
                promptCode = timers[timer]["promptCode"]
                userID = timers[timer]["userID"]
                contributions = getConfigInt(guildID, channelID, "promptcontributions")
                contributionsTimer = timers[timer]["contributions"]
                if now > time:
                    if action == "autopass":
                        if contributionsTimer == contributions:
                            task(action_drop(userID, promptCode, None, None, None, isInteraction=False, isKick=False, isBan=False, isAutopass=True))
                        if contributionsTimer != contributions:
                            task(action_pass(userID, promptCode, None, None, isInteraction=False, isDrop=False, isAutopass=True))
                    if action == "autorun":
                        period = getConfigInt(guildID, channelID, "autoperiod")                         
                        nextTime = ns() + nsMinute*period
                        createTempTimer(nextTime, "autorun", guildID, channelID, None, None, None)
                        channel = await bot.fetch_channel(channelID)
                        await action_run(guildID, channelID, channel, None, None, isInteraction=False)
                        contributors[f"{guildID}"][f"{channelID}"]["autoTime"] = nextTime
                    timers[timer] = None
            forDeletion = [timer for timer in timers if timers[timer] == None]
            for timer in forDeletion:
                del timers[timer]
            global tempTimers
            timers.update(tempTimers)
            tempTimers = {}

         
task(timer_loop())
bot.run(botToken)
