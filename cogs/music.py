import json
import os
import platform
import random
import sys
import subprocess

import aiohttp
import discord
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
upload_channel = config['upload_channel']

# Here we name the cog and create a new class for the cog.
class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="dl")
    # @commands.max_concurrency(1, per=BucketType.guild, wait=False)
    # @commands.cooldown(1, 300.0, commands.BucketType.guild)
    # @commands.has_any_role("Admin", "Super Moderator", "Mod", "Uploader", "Server Booster", "VIP", "beta tester")  
    async def dl(self, ctx, *, link):
        """
        Downloads music.
        """

        req_channel = self.bot.get_channel(request_channel)
        up_channel = self.bot.get_channel(upload_channel)

        rclone_drives = ["drive", "drive1", "drive2"] # Change it to your rclone remote
        random_rclone_drives = random.choice(rclone_drives)

        if ctx.channel.id == request_channel:                    
            if link.find("artist") != -1:
                await ctx.send(f"Downloading **Artist Profile** and **Playlists** not allowed.\n{ctx.author.mention}")
            elif link.find("playlist") != -1:
                await ctx.send(f"Downloading **Artist Profile** and **Playlists** not allowed.\n{ctx.author.mention}")
            elif link.find("qobuz") != -1:
                await ctx.send(f"**Qobuz** Module can't be run atm.\n{ctx.author.mention}")
            elif link.find("youtube") != -1:
                await ctx.send(f"**YouTube** Module can't be run atm.\n{ctx.author.mention}")
            elif link.find("youtu.be") != -1:
                await ctx.send(f"**YouTube** Module can't be run atm.\n{ctx.author.mention}")
            elif link.find("soundcloud") != -1:
                await ctx.send(f"**Soundcloud** Module can't be run atm.\n{ctx.author.mention}")
            elif not link.find(".com") != -1:
                await ctx.send(f"**Invalid** Link.\n{ctx.author.mention}")                        
            else:
                await req_channel.set_permissions(ctx.guild.default_role, send_messages=False)                
                await ctx.send(f"{ctx.author.mention} Please wait while your request is being downloaded <#{upload_channel}>\nChannel will be unlocked after completing the request.")            

                download_start_time = time.time()
                try:
                    with open('rip_log.txt', 'wb') as f:
                        process = subprocess.Popen(["rip", "--no-db", '-u', f'{link}'], stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            f.write(line)

                    download_end_time = time.time() - download_start_time                        
                    download_time = timedelta(seconds=round(download_end_time))

                    upload_start_time = time.time()

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

                    with open('upload_log.txt', 'wb') as f:
                        process = subprocess.Popen(["rclone", "copy", f'{download_folder}download/Temp/{zip_file}', f"{random_rclone_drives}:", "--progress", "--transfers", "16", "--drive-chunk-size", "32M"], stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            f.write(line)

                    upload_end_time = time.time() - upload_start_time                            
                    upload_time = timedelta(seconds=round(upload_end_time))

                    try:
                        subprocess.run(["rm", "-rf", f'{download_folder}download/Temp/{folder_name}'])
                        subprocess.run(["rm", "-rf", f'{download_folder}download/Temp/{zip_file}'])
                    except:
                        subprocess.run(["rm", "-rf", f'{download_folder}download/Temp/{file_name}'])
                        subprocess.run(["rm", "-rf", f'{download_folder}download/Temp/{zip_file}'])                       

                    all_done = discord.Embed(
                        name="**Music DL**",
                        description="**Uploaded**\nAll Done.",
                        color=0x20e84f
                    )                

                    link_process = subprocess.run(["rclone", "link", f"{random_rclone_drives}:"f'{zip_file}', "--retries", "15"], stdout=subprocess.PIPE, encoding='utf-8')
                    gdrive_link = link_process.stdout        

                    request_link = link

                    all_done.add_field(name="Name", value=zip_file, inline=False)
                    all_done.add_field(name="Request Link", value=request_link, inline=False)
                    all_done.add_field(name="Link", value=gdrive_link, inline=False)
                    all_done.add_field(name="Download Time", value=download_time, inline=False)
                    all_done.add_field(name="Zip Time", value=zipping_time, inline=False)
                    all_done.add_field(name="Upload Time", value=upload_time, inline=False)            


                    all_done.set_footer(text=f"Requested by {ctx.message.author}\nBot Developed by parnex#2368") 

                    await up_channel.send(embed=all_done)
                    await up_channel.send(f"{ctx.author.mention}")
                    await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                except:
                    await ctx.send("The following Song/Album isn't available to download because of Geo Restriction or Internal Error from Streaming Platform.")
                    await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)

        else:
            await ctx.send(f"This command can only be used in <#{request_channel}>")                                         
        

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Music(bot))
