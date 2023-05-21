from discord.ext import commands
from discord.ext.commands.core import command
from yt_dlp import YoutubeDL
from requests import get
import ctypes.util
import ctypes
import discord
import asyncio
import re

findOpus = ctypes.util.find_library('opus')
discord.opus.load_opus(findOpus)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.nowPlayingLink = ''
        self.nowPlayingTitle = ''
        self.queueLink = []
        self.queueTitle = []
        self.queueEmpty = True
        self.leave = False
        self.skipSong = False
        self.titleString = ''''''

    def searchSong(self, arg):
        ydl_opts = {
            'format': 'bestaudio/best',
        }
        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'noplaylist': 'true'
        # }
        print(arg)
        with YoutubeDL(ydl_opts) as ydl:
            try:
                get(arg)
            except:
                print(f"Getting entry from: {arg} in except")
                linkExtract = ydl.extract_info(
                    f"ytsearch:{arg}", download=False)
                # print(video['entries'][0]['url'])
                urlExtract = linkExtract['entries'][0]['url']
                titleExtract = linkExtract['entries'][0]['title']
                linkDict = {
                    'url': f'{urlExtract}',
                    'title': f'{titleExtract}'
                }
            else:
                print(f"Getting entry from: {arg} in else")
                linkExtract = ydl.extract_info(arg, download=False)
                urlExtract = linkExtract['formats'][6]['url']
                titleExtract = linkExtract['title']
                linkDict = {
                    'url': f'{urlExtract}',
                    'title': f'{titleExtract}'
                }
        return linkDict

    def checkPlaylist(self, link):
        linkStr = str(link)
        check = re.findall(r"playlist\b", linkStr)
        if check:
            return True
        else:
            return False

    def playPlaylist(self, link):
        print(f"Get playlist: {link}")
        # if 'entries' in linkExtract:
        #     print("Get playlist")
        #     playlistTitles = linkExtract['title']
        #     playlistSongLength = len(linkExtract['entries'])
        #     linkDict = {
        #         'url': [],
        #         'title': []
        #     }
        #     for song in linkExtract['entries']:
        #         linkDict['url'].append(song['formats'][6]['url'])
        #         linkDict['title'].append(song['title'])
        #     linkDict['playlistTitle'] = playlistTitles
        #     linkDict['playlistLength'] = playlistSongLength

    def addQueue(self, link):
        if len(link) > 0:
            linkStr = ''
            for i in link:
                linkStr += i
                linkStr += ' '
        else:
            linkStr = link
        vidExtract = self.searchSong(linkStr)
        # vidExtract = self.searchSong('https://www.youtube.com/playlist?list=PL9vgwW6Zi5bcNuYWplDHXBvQTxUrdHzTh')
        if 'playlistLength' in vidExtract:
            for i in range(vidExtract['playlistLength']):
                print(vidExtract['title'][i])
                # if self.nowPlayingLink == '':
                #     self.nowPlayingLink = vidExtract['url'][i]
                #     self.nowPlayingTitle = vidExtract['title'][i]
                # else:
                #     self.queueLink.append(vidExtract['url'][i])
                #     self.queueTitle.append(vidExtract['title'][i])

            self.queueEmpty = False
            return vidExtract['playlistTitle']
        else:
            if self.nowPlayingLink == '':
                self.nowPlayingLink = vidExtract['url']
                self.nowPlayingTitle = vidExtract['title']
            else:
                self.queueLink.append(vidExtract['url'])
                self.queueTitle.append(vidExtract['title'])
            self.queueEmpty = False

            return vidExtract['title']

    def nextSong(self):
        print(f"Deleting played Title - [{self.nowPlayingTitle}]")
        self.nowPlayingTitle = ''
        self.nowPlayingLink = ''
        if len(self.queueLink) > 0:
            self.nowPlayingTitle = self.queueTitle[0]
            self.nowPlayingLink = self.queueLink[0]
            self.queueLink.remove(self.queueLink[0])
            self.queueTitle.remove(self.queueTitle[0])

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Anda tidak berada dalam Voice Channel")
        voiceChannel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voiceChannel.connect()
        else:
            await ctx.voice_client.move_to(voiceChannel)

    @commands.command()
    async def leave(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Anda tidak berada dalam Voice Channel")
        elif ctx.voice_client is None:
            await ctx.send("Bot tidak berada pada voice channel")
        else:
            self.nowPlayingTitle = ''
            self.nowPlayingLink = ''
            self.queueLink.clear()
            self.queueTitle.clear()
            self.queueEmpty = True
            self.leave = True
            await ctx.send("Leaving voice channel.")
            await ctx.voice_client.disconnect()

    @commands.command(brief="Buat play lagu", description='buat ngeplay lagu lah apalagi', aliases=['p'])
    async def play(self, ctx, *url):
        if 'pantek' in url:
            await ctx.send("JANGAN DIPLAY ANJING")
        else:
            if len(url) > 0:
                FFMPEG_OPTIONS = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }

                # authorChannel = ctx.author.voice
                # botChannel = ctx.voice_client
                # voiceChannel = authorChannel.channel
                # Cek bot di channel atau tidak
                if ctx.author.voice is None:
                    await ctx.send("Anda tidak berada dalam Voice Channel")
                voiceChannel = ctx.author.voice.channel
                if ctx.voice_client is None:
                    await voiceChannel.connect()
                
                #Jika terdapat playlist
                isPlaylist = self.checkPlaylist(url)
                if(isPlaylist and len(url) == 1):
                    self.playPlaylist(url)
                    embed = discord.Embed(title="Play", description="Can't Play Playlist right now.")
                    await ctx.send(embed=embed)
                else:
                    # if ctx.voice_client is not None and ctx.author.voice.channel != ctx.voice_client:
                    #     await ctx.send("Anda harus berada dalam Voice Channel yang sama.")

                    # Tambahkan lagu pada Queue
                    print(url)
                    print(type(url))
                    judul = self.addQueue(url)
                    embed = discord.Embed(
                        title="Add Queue", description=judul)
                    await ctx.send(embed=embed)

                    # Play lagu
                    # Cek bot sudah play musik apa belum
                    vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                    checkPlay = vc.is_playing()
                    while checkPlay == False and self.queueEmpty == False:
                        print("Bot is not used, playing song")
                        if len(self.queueLink) > 0 and self.skipSong != True or self.nowPlayingLink != '':
                            source = await discord.FFmpegOpusAudio.from_probe(self.nowPlayingLink, **FFMPEG_OPTIONS)
                            embed = discord.Embed(
                                title="Playing", description=self.nowPlayingTitle)
                            await ctx.send(embed=embed)
                            vc.play(source)

                        while vc.is_playing():
                            await asyncio.sleep(1)
                        else:
                            print("Checking for next song...")
                            self.skipSong = False
                            if self.nowPlayingTitle != '':
                                print("Song entry found, play song")
                                ctx.voice_client.stop()
                                self.nextSong()
                                # source = await discord.FFmpegOpusAudio.from_probe(self.queueLink[0], **FFMPEG_OPTIONS)
                                # vc.play(source)
                            else:
                                if self.skipSong == False or len(self.queueLink) == 0:
                                    if self.leave == False:
                                        print("No song entry, leaving channel")
                                        embed = discord.Embed(
                                            title="Play", description="Queue Empty. Leaving voice channel")
                                        await ctx.send(embed=embed)
                                        self.queueEmpty = True
                                        await vc.disconnect()
                                    else:
                                        self.leave = False
            else:
                embed = discord.Embed(
                    title="Play", description="Cara penggunaan:\n$p [link/judul lagu]")
                await ctx.send(embed=embed)

    @commands.command(brief ="Ngebug, jangan digunakan")
    async def stop(self, ctx):
        # await ctx.voice_client.stop()
        pass

    @commands.command(brief="Ngebug, jangan digunakan")
    async def pause(self, ctx):
        # await ctx.voice_client.pause()
        pass

    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Anda tidak berada dalam Voice Channel")
        elif ctx.voice_client is None:
            await ctx.send("Bot tidak berada pada voice channel")
        print(f"Skipping current song: {self.nowPlayingTitle}")
        self.skipSong = True
        ctx.voice_client.stop()
        embed = discord.Embed(title="Skip", description=f"Skipping {self.nowPlayingTitle}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['mv'])
    async def move(self, ctx, *nomor):
        if len(nomor) == 2:
            num1 = int(nomor[0])
            num2 = int(nomor[1])
            if num1 > len(self.queueLink) or num2 > len(self.queueLink):
                embed = discord.Embed(
                    title="Move", description=f"Nomor urutan melebihi total queue")
                await ctx.send(embed=embed)
            else:
                if num1 > 0:
                    num1 -= 1
                if num2 > 0:
                    num2 -= 1
                tempLink = self.queueLink[num1]
                tempTitle = self.queueTitle[num1]
                self.queueLink.remove(self.queueLink[num1])
                self.queueTitle.remove(self.queueTitle[num1])
                self.queueLink.insert(num2, tempLink)
                self.queueTitle.insert(num2, tempTitle)
                embed = discord.Embed(
                    title="Move", description=f"{tempTitle} dipindah ke nomor {num2+1}")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Move", description=f"Cara penggunaan:\n$move [urutan1][urutan2]\nContoh: $move 2 1")
            await ctx.send(embed=embed)

    @commands.command(aliases=['rm'])
    async def remove(self, ctx, num):
        num = int(num)
        if len(self.queueLink) > 0:
            if num > 0:
                num -= 1
            embed = discord.Embed(
                title="Remove", description=f"{self.queueTitle[num]} removed")
            await ctx.send(embed=embed)
            self.queueLink.remove(self.queueLink[num])
            self.queueTitle.remove(self.queueTitle[num])
        else:
            embed = discord.Embed(
                title="Remove", description=f"Queue kosong.")
            await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        if len(self.queueLink) > 0 or self.nowPlayingLink != '':
            self.queueLink.clear()
            self.queueTitle.clear()
            embed = discord.Embed(
                title="Queue", description="Semua queue telah dihapus.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Queue", description="Queue kosong.")
            await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if self.nowPlayingTitle == '':
            embed = discord.Embed(title="Queue", description='Queue Kosong.')
            await ctx.send(embed=embed)
        else:
            titleString = ''''''
            titleString += f'Now Playing: {self.nowPlayingTitle}\n'
            i = 0
            for i in range(len(self.queueTitle)):
                titleString += f'{i+1}. {self.queueTitle[i]}\n'
            embed = discord.Embed(title="Queue", description=titleString)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Music(client))
