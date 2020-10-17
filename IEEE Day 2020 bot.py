import discord
from discord.ext import commands

IEEE_Client = commands.Bot(command_prefix = '!')

TOKEN = "NzY1Njk3OTg1MTYxMzMwNzI5.X4Yl0Q.qy8WwQTUNkTeRALpsQbmiVXVJDU"

Workshop_channels = {766007764970766336:{"role":766662068975304727, "move_channel":766006185051553813}, #room 1 channel
                     766007917148635158:{"role":766671973521817620, "move_channel":766006320813572134}, #room 2 channel
                     766007984748625952:{"role":766673121255620638, "move_channel":766006371455467542}, #room 3 channel
                     766008042079780874:{"role":766688860062482456, "move_channel":766007399659470858}, #room 4 channel
                     766008082102091777:{"role":766690060505841675, "move_channel":766007548255010858}} #room 5 channel

Previous_channels_roles = {766006185051553813:766662068975304727,
                           766006320813572134:766671973521817620,
                           766006371455467542:766673121255620638,
                           766007399659470858:766688860062482456,
                           766007548255010858:766690060505841675}

Game_channels = {766009923116728364:{"limit":12, "channel":[766010379083317298, 766010397768810536, 766010413661814784], "Room#":3, "category":766006438668533790}, #Scribble channels
                 766010049075216384:{"limit":4,  "channel":[766010494154440715, 766010513184260127, 766010530338701363, 766010548575010866], "Room#":4, "category":766006583976132648}, #Tarneeb channels
                 766010191576694784:{"limit":4,  "channel":[766010576719183922, 766010592586104883, 766010611623657482, 766010634399252530], "Room#":4, "category":766006817850654750}, #Chkoba channels
                 766010303531974676:{"limit":10, "channel":[766010676438368357, 766010695429914734, 766010711653482496, 766010800334438423, 766010921892970516], "Room#":5, "category":766006971714764802}} #amongus channels

async def removeRoles(member, before):
    try:
        await member.remove_roles(discord.utils.get(member.guild.roles, id=Previous_channels_roles[before.channel.id]))
    except KeyError:
        return
    except AttributeError:
        return

@IEEE_Client.event
async def on_ready():
    print("IEEE Bot is Ready!")
    # embed=discord.Embed(title="Choose your country:", color=discord.Colour(0x0059ff))
    # embed.set_author(name="IEEE Day 2020")
    # embed.add_field(name="Jordan", value=":flag_jo:", inline=True)
    # embed.add_field(name="Tunisia", value=":flag_tn:", inline=True)
    # channel = IEEE_Client.get_channel(764134656781189151) #Welcome text channel 
    # embed_msg = await channel.send(embed=embed)
    # await embed_msg.add_reaction("🇯🇴")
    # await embed_msg.add_reaction("🇹🇳")
    # await channel.send(embed=discord.Embed(description="[Click here to see the rules](https://discord.com/channels/765698106405945344/766430294973612032/766430306092843029)"))

@IEEE_Client.event
async def on_voice_state_update(member, before, after):
    if(after.channel != before.channel):
        if(after.channel != None):
            if(after.channel.category_id == 766007248656138240):   
                    try:
                        await member.add_roles(discord.utils.get(member.guild.roles, id=Workshop_channels[after.channel.id]["role"])) #add workshop room # role
                        await member.edit(mute=True, voice_channel=IEEE_Client.get_channel(Workshop_channels[after.channel.id]["move_channel"])) #mute member and move him to workshop room # voice channel
                        await removeRoles(member, before)
                    except KeyError:
                        return
            else:
                try:
                    for channel in Game_channels[after.channel.id]["channel"]:
                        await member.edit(mute=False)
                        await removeRoles(member, before)
                        if(len(list(IEEE_Client.get_channel(channel).members)) < Game_channels[after.channel.id]["limit"]):
                            await member.edit(voice_channel=IEEE_Client.get_channel(channel))
                            return
                    new_channel = await IEEE_Client.get_guild(ctx.message.guild.id).create_voice_channel(
                                            f"Room {Game_channels[after.channel.id]['Room#']+1}", 
                                            category=discord.utils.get(IEEE_Client.get_guild(ctx.message.guild.id).categories, id=Game_channels[after.channel.id]['category']),
                                            user_limit=Game_channels[after.channel.id]['limit'])
                    Game_channels[after.channel.id]["Room#"] += 1
                    Game_channels[after.channel.id]["channel"].append(new_channel.id)
                    await member.edit(voice_channel=IEEE_Client.get_channel(new_channel.id))
                except KeyError:
                    return
        else:
            await removeRoles(member, before)

@IEEE_Client.event
async def on_reaction_add(reaction, member):
    if(member == IEEE_Client.user):
        return
    elif(str(reaction) == "🇯🇴"):
        try:
            await member.edit(nick=f"{member.name} 🇯🇴") if(member.nick == None) else await member.edit(nick=f"{member.nick} 🇯🇴")
            await member.add_roles(discord.utils.get(member.guild.roles, id=766440500994506792)) #country was choosen role
            await member.add_roles(discord.utils.get(member.guild.roles, id=767016555871469629)) #add jordan role
        except discord.errors.Forbidden:
            await member.send(f"You are organizer please change your nickname to '{member.name if(member.nick == None) else member.nick} 🇯🇴' manually.")
    elif(str(reaction) == "🇹🇳"):
        try:
            await member.edit(nick=f"{member.name} 🇹🇳") if(member.nick == None) else await member.edit(nick=f"{member.nick} 🇹🇳")
            await member.add_roles(discord.utils.get(member.guild.roles, id=766440500994506792)) #country was choosen role
            await member.add_roles(discord.utils.get(member.guild.roles, id=767016646510379058)) #add tunisia role
        except discord.errors.Forbidden:
            await member.send(f"You are organizer please change your nickname to '{member.name if(member.nick == None) else member.nick} 🇹🇳' manually.")

@IEEE_Client.command()
@commands.has_role("Moderators")
async def split(ctx):
    for member in list(IEEE_Client.get_channel(764134656781189152).members): #split members from main room
        if(member.nick[-2:] == "🇯🇴"):
            await member.edit(voice_channel=IEEE_Client.get_channel(766011995786444820), mute=False) #Jordan Room
        elif(member.nick[-2:] == "🇹🇳"):
            await member.edit(voice_channel=IEEE_Client.get_channel(766012069136695348), mute=False) #Tunisia Room

@IEEE_Client.command()
@commands.has_role("Moderators")
async def gather(ctx):
    for member in list(IEEE_Client.get_channel(766011995786444820).members):
        await member.edit(voice_channel=IEEE_Client.get_channel(764134656781189152), mute=False)
    for member in list(IEEE_Client.get_channel(766012069136695348).members):
        await member.edit(voice_channel=IEEE_Client.get_channel(764134656781189152), mute=False)

@split.error
@gather.error
async def split_error(ctx, error):
    if isinstance(error, commands.errors.MissingRole):
        await ctx.send(f"Nice Try {ctx.author.nick[0:len(ctx.author.nick)-2] if(ctx.author.nick != None) else ctx.author.name}, That wont work you are not a Moderator.")

IEEE_Client.run(TOKEN)