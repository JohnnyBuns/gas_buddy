
import threading
import discord
from discord.ext.tasks import loop
import requests
import json
import gas_timer
import asyncio

client = discord.Client()
TOKEN = 'OTMyNTM5NjA5OTkxMjQ1ODI0.YeUdMA.d5DwKe98xFNdBLhTIHifLyvE2uc'
notify_list = {}
gas_updater = gas_timer.gas_updater()
embed_color =0xCFB408


async def notify_event():
    for user in notify_list:
        print('big change folks')
        channel = notify_list[user]
        print(channel)
        await channel.send(f'{user.mention} Base Gas changes drastically from {gas_updater.base_gas_average} to {gas_updater.suggested_gas_base}')


@loop(seconds=10)
async def get_gas():
    print('hmm')
    await gas_updater.gas_update(notify_event)
#     await get_gas.start()
#     # threading.Timer(6.0, notify_event_wrapped).start()


@client.event
async def on_ready():
    '''
    message on ready
    '''
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    message_args = message.content.split(' ')
    if message_args[0] == '!gas' and len(message_args) == 1:
        embedGasOracle = discord.Embed(title="⛽  Gas Fee's", description="*Current Gas fee's on the Ethereum chain*", color=embed_color)
        embedGasOracle.add_field(name="✨ Base Gas ✨", value=gas_updater.suggested_gas_base, inline=False)
        embedGasOracle.add_field(name="🛡 Safe Gas Price 🛡", value=gas_updater.safe_gas_price, inline=False)
        embedGasOracle.add_field(name="⚔ Fast Gas Price ⚔", value=gas_updater.fast_gas_price, inline=False)
        embedGasOracle.set_footer(text="Fetched from etherscan API")

        await message.channel.send(embed=embedGasOracle)
        # await message.channel.send(f'GASSS BUDDDY \nBase gas = {gas_updater.suggested_gas_base}')

    elif message_args[0] == '!gas' and message_args[1] == ('subscribe'):
        # await message.channel.send(f'Will notify {message.author.mention} when absolute change of gas changes by > 10%')
        await message.channel.send(f'Will notify {message.author.mention} gas fees under 90')
        notify_list[message.author] = message.channel
        print(message.author.mention)

    elif message_args[0] == '!gas' and message_args[1] == ('estimate'):
        embedGasEstimate = discord.Embed(title="⛽⏱  Gas Fee Time Estimator", description="*Current estimated transaction type based on current gas fee's*", color=embed_color)
        embedGasEstimate.add_field(name="✨ Base Gas Time Estimate✨\n", value=gas_updater.suggested_time_estimate, inline=False)
        embedGasEstimate.add_field(name="\n🛡 Safe Gas Time Estimate 🛡\n", value=gas_updater.safe_time_estimate, inline=False)
        embedGasEstimate.add_field(name="\n⚔ Fast Gas Time Estimate ⚔\n", value=gas_updater.fast_time_estimate, inline=False)
        embedGasEstimate.set_footer(text="Fetched from etherscan API")

        await message.channel.send(embed=embedGasEstimate)
        print(message.author.mention)


get_gas.start()
client.run(TOKEN)  
