import json
import os
import platform
import random
import sys
import subprocess
import asyncio
import aiohttp
import discord
import base64
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import time
import base64
from datetime import timedelta
from time import gmtime, strftime

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

download_folder = config['bot_folder']
request_channel = config['request_channel']

# status = False

# Here we name the cog and create a new class for the cog.
class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="dl")
    # @commands.max_concurrency(1, per=BucketType.guild, wait=False)
    # @commands.cooldown(1, 300.0, commands.BucketType.guild)
    # @commands.has_any_role("Admin", "Super Moderator", "Mod", "Uploader", "Server Booster", "VIP", "beta tester")  
    async def dl(self, ctx, link):
        """
        Downloads music.
        """

        req_channel = self.bot.get_channel(request_channel)
        # global status

        rclone_drives = ["tidal"]
        random_rclone_drives = random.choice(rclone_drives)

        if ctx.channel.id == request_channel:                    
            if link.find("artist") != -1 and link.find("tidal") != -1:
                await ctx.send(f"Downloading **Artist Profile** and **Playlists** not allowed.\n{ctx.author.mention}")
            elif link.find("playlist") != -1 and link.find("tidal") != -1:
                await ctx.send(f"Downloading **Artist Profile** and **Playlists** not allowed.\n{ctx.author.mention}")
            if link.find("interpreter") != -1 and link.find("qobuz") != -1:
                await ctx.send(f"Downloading **Artist Profile** and **Playlists** not allowed.\n{ctx.author.mention}")                
            elif link.find("youtube") != -1:
                await ctx.send(f"**YouTube Music** can't be downloaded.\n{ctx.author.mention}")
            elif link.find("youtu.be") != -1:
                await ctx.send(f"**YouTube Music** can't be downloaded.\n{ctx.author.mention}")
            # elif link.find("tidal") != -1:
            #     await ctx.send(f"**Tidal** is down for maintainence.\n{ctx.author.mention}")
            # elif link.find("qobuz") != -1:
            #     await ctx.send(f"**qobuz** is down for maintainence.\n{ctx.author.mention}")            
            elif link.find("soundcloud") != -1:
                await ctx.send(f"**Soundcloud** can't be downloaded.\n{ctx.author.mention}")
            elif link.find("spotify") != -1:
                await ctx.send(f"**Spotify** can't be downloaded.\n{ctx.author.mention}")
            elif link.find("deezer") != -1:
                await ctx.send(f"**Deezer** can't be downloaded.\n{ctx.author.mention}")                               
            elif not link.find(".com") != -1:
                await ctx.send(f"**Invalid** Link.\n{ctx.author.mention}")  
            elif not link.find("https") != -1:
            	await ctx.send(f"Add **https://** to Link.\n{ctx.author.mention}")                            
            else:
                await req_channel.set_permissions(ctx.guild.default_role, send_messages=False)                
                await ctx.send(f"{ctx.author.mention} Please wait while your request is being downloaded.\nChannel will be unlocked after completing the request.")            
                # while True:
                #     if status == True:
                #         await asyncio.sleep(3)
                #     else: break
                # status = True                
                download_start_time = time.time()
                try:
                    with open('rip_log.txt', 'wb') as f:
                        process = subprocess.Popen(["rip", 'url', f'{link}', '-i'], stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            f.write(line)

                    download_end_time = time.time() - download_start_time                        
                    download_time = timedelta(seconds=round(download_end_time))

                    search_path = f'{download_folder}download/Temp'
                    root, dirs, files = next(os.walk(search_path), ([],[],[]))
                    try:
                        folder_name = dirs[0]
                    except:
                        file_name = files[0]

                    zipping_start_time = time.time()        

                    time_format_file_name = strftime("%Y-%m-%d_%H%M%S", gmtime())

                    try:
                        zip_file = f"{folder_name}_{time_format_file_name}.zip"
                    except:
                        zip_file = f"{file_name}_{time_format_file_name}.zip"                                       

                    subprocess.run(["7z", "a", "-mx0", "-tzip", f"{download_folder}download/Temp/{zip_file}", f'{download_folder}download/Temp/'])

                    zipping_end_time = time.time() - zipping_start_time        
                    zipping_time = timedelta(seconds=round(zipping_end_time))

                    upload_start_time = time.time()

                    with open('upload_log.txt', 'wb') as f:
                        process = subprocess.Popen(["python3", "krakenupload.py", f"{search_path}/{zip_file}"], stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            kf = line
                            f.write(line)

                    upload_end_time = time.time() - upload_start_time                            
                    upload_time = timedelta(seconds=round(upload_end_time))

                    subprocess.run(["rm", "-rf", f'{download_folder}download/Temp'])              

                    all_done = discord.Embed(
                        name="**Music DL**",
                        description="**Uploaded**\nAll Done.",
                        color=0x20e84f
                    )                
                    request_link = link
                    kf_link = kf.decode("utf-8")
                    b64link = base64.b64encode(bytes(kf_link, "utf-8")).decode()
                    encoded_link = f'https://links.gamesdrive.net/#/link/{b64link}.U2xhdiBNdXNpYyBCb3Q='
                    all_done.add_field(name="Name", value=zip_file, inline=False)
                    all_done.add_field(name="Request Link", value=request_link, inline=False)
                    all_done.add_field(name="Link", value=encoded_link, inline=False)
                    all_done.add_field(name="Download Time", value=download_time, inline=False)
                    all_done.add_field(name="Zip Time", value=zipping_time, inline=False)
                    all_done.add_field(name="Upload Time", value=upload_time, inline=False)            


                    all_done.set_footer(text=f"Requested by {ctx.message.author}\nBot Developed by parnex#2368") 

                    try:
                        await ctx.author.send(embed=all_done)
                        await ctx.send(f"It's uploaded, Slide into my dms. {ctx.author.mention}")
                        await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                        # status = False
                    except discord.Forbidden:
                        await ctx.send(f"Why do you have your dm's disabled ? Sorry I can't message you. {ctx.author.mention}")
                        # status = False
                        await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                except:
                    await ctx.send("The following Song/Album isn't available to download because of Geo Restriction or Internal Error from Streaming Platform.")
                    # status = False
                    await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)

        else:
            await ctx.send(f"This command can only be used in <#{request_channel}>")                                         
        

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Music(bot))