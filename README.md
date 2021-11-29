# tidal-dl discord bot
 A discord bot to download high quality music from streaming services.
 
 #### This bot was designed to work on Ubuntu
 Edit the commands in [music.py](https://github.com/parnexcodes/tidal-dl-discord-bot/blob/main/cogs/music.py) if you're using another operating system.
 
 ## Note
 Make a channel for requests channel.
 
 The bot performs tasks **synchronously** (one task at a time) , so the channel needs to be locked after each request.
 
 If you have a better solution , open a PR.
 
 I have restricted Qobuz , Youtube , Soundcloud and Artist Profile/Playlists. Edit these [lines](https://github.com/parnexcodes/tidal-dl-discord-bot/blob/f3abf3a9c05455b88df999a7653ac26c7fbccbe0/cogs/music.py#L50-L63) if you want to allow them.

## Install the following packages before proceeding.
```python```

```pip```

```pip3 install git+https://github.com/uwulily/streamrip.git```

```rclone```

```7zip```

```pip install -r requirements.txt```

Keep rclone and 7zip in the bot folder if you are using Windows.

## Setting up the bot is pretty straight forward.
Run ```rip config --open``` , it will show you the file location of streamrip's config. Open it with a text editor and change
```folder = "/Users/nathan/StreamripDownloads"``` to ```folder = "Your bot folder/download/Temp/"```

Set ```[database]
enabled = true``` to **false**.

Open the config.json file and edit it.

[This line](https://github.com/parnexcodes/tidal-dl-discord-bot/blob/f3abf3a9c05455b88df999a7653ac26c7fbccbe0/config.json#L5) Should have a ```/``` at the end.

Put the channel id in [line](https://github.com/parnexcodes/tidal-dl-discord-bot/blob/f3abf3a9c05455b88df999a7653ac26c7fbccbe0/config.json#L6) 6.

## Run Bot
```python3 bot.py```

When you run the $dl <link> command for the first time , check your terminal and follow the steps to login to tidal/qobuz.

Your token is saved so you don't have to do it everytime.

## Thanks
[Streamrip](https://github.com/nathom/streamrip) by nathom

[Discord.py Bot Template](https://github.com/kkrypt0nn/Python-Discord-Bot-Template) by kkrypt0nn


## Discord
<https://discord.gg/z6prF5C>
