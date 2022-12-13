import traceback
import discord, sqlite3, os, random, asyncio, requests, datetime, json, time
from Setting import *
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

admin_id = [관리자]
hz_on=0
hz_h = []
hz_z = []
doing_bet = []
t=0

def getinfo(id):
    url = f"https://discordapp.com/api/users/{id}"
    he = {
        "Authorization":f"Bot {봇토큰}"
    }
    res = requests.get(url,headers=he)
    r = res.json()
    return r

if not (os.path.isfile("./database/database.db ")):
    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE users (id INTEGER, money INTEGER, boggle_bet_pick TEXT, boggle_bet_money INTEGER, is_bet INTEGER, ban INTEGER, ladder_bet_pick TEXT, ladder_bet_money INTEGER, wllet_bet_pick TEXT, wllet_bet_money INTEGER, owrun_bet_pick TEXT, owrun_bet_money INTEGER, eos1_bet_pcik TEXT, eos1_bet_money INTEGER, pwball_bet_pick TEXT, pwball_bet_money INTEGER, eos5_bet_pcik TEXT, eos5_bet_money INTEGER, powerladder_bet_pick TEXT, powerladder_bet_money INTEGER, ad_bet_pick TEXT, ad_bet_money INTEGER, rotoball_bet_pick TEXT, rotoball_bet_money INTEGER, rotoladder_bet_pick TEXT, rotoladder_bet_money INTEGER, hz_bet_pick TEXT, hz_bet_money INTEGER)")
    con.commit()
    con.close()


@client.event
async def on_ready():
    DiscordComponents(client)
    print(f"")
    print(f"─────────────────────────────────────────────────────")
    print(
        f"메인시스템을 실행 합니다.: {client.user}\n봇 초대 링크 : https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
    print(f"─────────────────────────────────────────────────────")
    print(f"사용 중인 서버 : {len(client.guilds)}개 관리 중")
    print(f"SFT#8770")


@client.event
async def on_message(message):
    global hz_on
    global hz_h
    global hz_z
    global doing_bet
    global t
    global hz_round
    global result # 결과값 연동 

    if message.author.bot:
        return

    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
    user_info = cur.fetchone()

    if (user_info == None):
        cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None))
        con.commit()
        con.close()
    con.close()

    if message.content.startswith('?순위'):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()
        try:
            args = message.content.split(" ")[1]
        except:
            args = ""

        amsg = await message.channel.send("잠시만 기다려주세요..")
        if (len(args) == 2):
            int(args).pop(0)
            counts = int(args[0])
            conn = sqlite3.connect("./database/database.db")
            c = conn.cursor()
            list_all = list(c.execute("SELECT * FROM users"))
            list_all.sort(key=lambda x: -x[1])
            print()
            res_text = "=======순위=======\n\n"
            idx = 1
            for ii in list_all[0:counts]:
                res_text += str(idx) + ". " + str(await client.fetch_user(ii[0])) + " - " + str(ii[1]) + "원 \n"
                idx += 1
            conn.close()
            # await amsg.edit(res_text)
            res_text = discord.Embed(title=f'유저 {counts}명의 순위입니다.',
                                     description=f'{res_text}',
                                     color=0x2f3136)
            await amsg.edit("", embed=res_text)


        else:
            conn = sqlite3.connect("./database/database.db")
            c = conn.cursor()
            list_all = list(c.execute("SELECT * FROM users"))
            list_all.sort(key=lambda x: -x[1])
            print()
            res_text = "=======순위=======\n\n"
            idx = 1
            for ii in list_all[0:10]:
                res_text += str(idx) + ". " + str(await client.fetch_user(ii[0])) + " - " + str(ii[1]) + "원 \n"
                idx += 1
            conn.close()
            res_text = discord.Embed(title='유저 10명의 순위입니다.',
                                     description=f'{res_text}',
                                     color=0x2f3136)
            await amsg.edit("", embed=res_text)
    if message.content == "?홀짝":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(홀짝회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0
            bet_msg=await client.get_channel(홀짝채널).send(f"start")
            if hz_on == 0:
                await message.channel.send(f"<#{홀짝채널}> 에 게임이 시작됩니다.")
                hz_on = 1
                hz_round = 0
                while True:
                    text=''
                    hz_round += 1
                    hz_h = []
                    hz_z = []
                    result="홀" if random.randint(0, 1) == 1 else '짝'
                    t = 60
                    hz_ch = client.get_channel(홀짝채널)
                    bet_embed = discord.Embed(title=f"{hz_round}회차 배팅가능시간입니다.",
                                              description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`", color=0x2f3136)
                    bet_embed.set_footer(text='킹볼 게임랜드')
                    await bet_msg.edit(content="",embed=bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        t -= 5
                        bet_embed = discord.Embed(title=f"{hz_round}회차 배팅가능시간입니다.",
                                                  description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`",
                                                  color=0x2f3136)
                        bet_embed.set_footer(text='킹볼 게임랜드')
                        await bet_msg.edit(embed=bet_embed)
                        if t==0:
                            break
                    if result == "홀":
                        for i in hz_h:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = int(f'{(user_info[27] * 1.95):.0f}')
                            text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1]+new_money, i))
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                        for i in hz_z:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = 0
                            text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    else:
                        for i in hz_h:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = 0
                            text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                        for i in hz_z:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = int(f'{(user_info[27] * 1.95):.0f}')
                            text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + new_money, i))
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    if text == '':
                        close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                    description=f"{hz_round}회차 결과 : `{result}`\n\n```아무도 참여하지 않았습니다.```",
                                                    color=0x2f3136)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    else:
                        close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                    description=f"{hz_round}회차 결과 : `{result}`\n\n```{text}```",
                                                    color=0x2f3136)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    await bet_msg.edit(content="@everyone",embed=close_embed, components="")
                    await asyncio.sleep(10)
                    doing_bet = []
                    if result == "홀":
                        if text!='':
                            result = f"{result} :one: "
                        else:
                            result = f"{result} :one: "
                    else:
                        if text != '':
                            result = f"{result} :two: "
                        else:
                            result = f"{result} :two: "
                    leng += 1
                    if leng >= 50:
                        round_rs = "**🎨결과값 초기화🎨**"
                        leng = 0
                    round_rs += f"\n\n`{hz_round}회차` -- **{result}**"
                    ch = client.get_channel(배팅내역)
                    await ch.send(f"`{hz_round}회차`\n\n{text}")
                    await pe_rs.edit(content=f"{round_rs}")
    if message.content.startswith('?주작'): # .주작 홀 / 짝
        if message.author.id in admin_id:  #관리자만 반응
            if message.content.split(" ")[1] == "홀" or message.content.split(" ")[1] == "짝":
                result=message.content.split(" ")[1]
                await message.reply(f"> **{hz_round}회차 결과가 `{result}` 으로 변경되었습니다.**") #바뀌는 로직
    if message.content.startswith('?홀짝 '):
        if hz_on != 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if not user_info[5] == 3:
                if message.content.split(" ")[2] == "올인":
                    if (int(user_info[1]) >= 1000):
                        amount = int(user_info[1])
                    else:
                        con.close()
                        await message.channel.send("**```보유금액이 부족합니다.```**")
                else:
                    amount = int(message.content.split(" ")[2])
                if not amount < 1000:
                    if user_info[1] >= amount:
                        if t > 10:
                            if not message.author.id in doing_bet:
                                doing_bet.append(message.author.id)

                                choice=message.content.split(" ")[1]
                                if user_info[1] >= 1000:
                                    if choice == "홀":
                                        hz_h.append(message.author.id)
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, message.author.id))
                                        cur.execute("UPDATE users SET hz_bet_pick = ? WHERE id == ?;",
                                                    (choice, message.author.id))
                                        cur.execute("UPDATE users SET hz_bet_money = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        await message.channel.send(f"**> {hz_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1]-amount}**")
                                    elif choice == "짝":
                                        hz_z.append(message.author.id)
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, message.author.id))
                                        cur.execute("UPDATE users SET hz_bet_pick = ? WHERE id == ?;",
                                                    (choice, message.author.id))
                                        cur.execute("UPDATE users SET hz_bet_money = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        await message.channel.send(f"**> {hz_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1]-amount}**")
                                    else:
                                        con.close()
                                        await message.channel.send("**```홀/짝 중에서만 배팅해주세요.```**")
                                else:
                                    con.close()
                                    await message.channel.send("**```보유금액이 부족합니다.```**")
                            else:
                                con.close()
                                await message.channel.send("**```중복베팅은 불가능합니다.```**")
                        else:
                            con.close()
                            await message.channel.send("**```배팅이 마감되었습니다.```**")
                    else:
                        con.close()
                        await message.channel.send("**```보유금액이 부족합니다.```**")
                else:
                    con.close()
                    await message.channel.send("**```1000원이상부터 배팅이 가능합니다.```**")
            else:
                con.close()
                await message.channel.send("**```당신은 차단된유저입니다.```**")
        else:
            await message.channel.send("**```게임이 진행되고있지않습니다.```**")

    if message.content.startswith('?정보'):
        try:
            m = message.content.split(" ")[1]
            m = m.split('@')[1]
            m = m.split('>')[0]
            id = int(m)
        except Exception as e:
            id = message.author.id
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            con.close()
            if user_info[5] == 1:
                is_ban = True
            else:
                is_ban = False
            await message.channel.send(f"```py\n보유하신 머니 : {str(user_info[1])}원```")
        else:
            con.close()
            await message.channel.send("**```가입되있지않은 유저입니다.```**")

    if message.content.startswith('?강제충전 '):
        log_id = 입출금채널
        log_ch = client.get_channel(int(log_id))
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.channel.send("**```누구를 충전할건데요?ㅋ.```**")
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

                con.commit()
                await message.channel.send(
                    f"```py\n{str(amount)}원 강제충전 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] + amount)}원```")
                await log_ch.send(f"<@{message.mentions[0].id}>님이 {amount}원을 충전하셨습니다")
            else:
                con.close()
                await message.channel.send("**```가입되있지않은 유저입니다.```**")

    if message.content.startswith('?강제차감 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.channel.send("**```누구 돈을뺄건지 멘션좀ㅋ.```**")
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, user_id))
                con.commit()
                await message.channel.send(
                    f"```py\n{str(amount)}원 강제차감 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] - amount)}원```")
                res = getinfo(user_id)
                webhook = DiscordWebhook(
                    url=f'{입출금로그}',
                    username='환전로그',
                    avatar_url=f"https://cdn.discordapp.com/avatars/{user_id}/{res['avatar']}.webp?size=80",
                    content=f'<@{user_id}> 님이 {amount}원을 환전하셨습니다.')
                webhook.execute()
            else:
                con.close()
                await message.channel.send("**```가입되있지않은 유저입니다.```**")

    if message.content.startswith('?블랙리스트 '):
        if message.author.id in admin_id:
            user_id = message.mentions[0].id

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (3, user_id))
                con.commit()
                con.close()
                await message.channel.send("**```성공적으로 블랙리스트 추가를 완료하였습니다!```**")
            else:
                con.close()
                await message.channel.send("**```가입되있지않은 유저입니다.```**")

    if message.content.startswith('?화이트리스트 '):
        if message.author.id in admin_id:
            user_id = message.mentions[0].id

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (0, user_id))
                con.commit()
                con.close()
                await message.channel.send("**```성공적으로 화이트리스트 추가를 완료하였습니다!```**")
            else:
                con.close()
                await message.channel.send("**```가입되있지않은 유저입니다.```**")
    if (message.content == '?충전'):
        await message.delete()
        if message.author.id in admin_id:
            charge_embed=discord.Embed(title="계좌 충전",description="```yaml\n계좌 충전버튼을 눌러주세요```",color=0x2f3136)
            account = Button(label="계좌충전", custom_id="계좌충전", style=ButtonStyle.blue)

            await client.get_channel(충전채널).send(embed=charge_embed, components=
                        ActionRow(
                            [account],
                        )
                                                    )
@client.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "계좌충전":
        user_id = interaction.user.id

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                user_id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=discord.Embed(description=f"```입금자명을 입력해주세요.```", color=0x2f3136))
                await interaction.respond(content="**```DM을 확인해주세요```**")
            except:
                await interaction.respond(content="**```DM이 막혀있습니다```**")

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=discord.Embed(title="계좌 충전 실패", description="```시간 초과되었습니다```", color=0x2f3136))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=discord.Embed(description=f"```입금할 액수를 입력해주세요.```", color=0x2f3136))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                            interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                if int(money) <1000:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```최소충전금은 1000원입니다.```", color=0x2f3136))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```시간 초과되었습니다.```", color=0x2f3136))
                except:
                    pass
                return None
            if money.isdigit():
                await interaction.user.send(embed=discord.Embed(title="계좌 충전",
                                                                description=f"**```py\n입금 계좌 : {계좌}```**\n─────────────\n입금자명 : `{name}`\n입금 금액 : `{money}`원",
                                                                color=0x2f3136))
                await interaction.user.send(
                    f"{계좌}")
                screenshot = await interaction.user.send(
                    embed=discord.Embed(description=f"```충전후 스크린샷을 5분내에 보내주세요.```", color=0x2f3136))

                def check(file):
                    return (isinstance(file.channel, discord.channel.DMChannel) and (
                            interaction.user.id == file.author.id))

                try:
                    file = await client.wait_for("message", timeout=300, check=check)
                    await screenshot.delete()
                    try:
                        if file.attachments != []:
                            for attach in file.attachments:
                                sct=attach.url
                    except:
                        try:
                            await interaction.user.send(
                                embed=discord.Embed(title="계좌 충전 실패", description="```올바른 사진 형식이 아닙니다.```",
                                                    color=0x2f3136))
                        except:
                            pass
                        return None
                except asyncio.TimeoutError:
                    try:
                        await interaction.user.send(
                            embed=discord.Embed(title="계좌 충전 실패", description="```시간 초과되었습니다.```", color=0x2f3136))
                    except:
                        pass
                    return None

                access_embed = discord.Embed(title='계좌이체 충전 요청',
                                             description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금금액 : {money}',
                                             color=0x2f3136)
                try:
                    access_embed.set_image(url=sct)
                except:
                    try:
                        await interaction.user.send(
                            embed=discord.Embed(title="계좌 충전 실패", description="```올바른 사진 형식이 아닙니다.```",
                                                color=0x2f3136))
                    except:
                        pass
                    return None
                await interaction.user.send(
                            embed=discord.Embed(title="충전 요청 성공 ✅", description=f"```yaml\n관리자의 승인을 기다려주세요.```",
                                                color=0x2f3136))
                access = Button(label="✅ 승인하기", custom_id="승인", style=ButtonStyle.green)
                deny = Button(label="❌ 거부하기", custom_id="거부", style=ButtonStyle.red)
                a_m = await client.get_channel(요청채널).send(embed=access_embed, components=
                ActionRow(
                    [access, deny],
                )
                                                          )
                while True:
                    interaction = await client.wait_for("button_click",
                                                        check=lambda inter: inter.custom_id != "",
                                                        timeout=None)
                    if interaction.custom_id == '승인':
                        await a_m.delete()
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] + int(money), user_id))
                        con.commit()
                        con.close()
                        await client.get_user(user_id).send(embed=discord.Embed(title="계좌 충전 성공",
                                                                                description=f"{interaction.user} 관리자님께서 충전을 승인해주셨습니다. {money}원`",
                                                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(
                            embed=discord.Embed(title="계좌 충전 성공", description=f"<@{user_id}>님께 충전되었습니다. {money}원",
                                                color=0x2f3136))
                        log_id = 입출금채널
                        log_ch = client.get_channel(int(log_id))
                        await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다")
                    if interaction.custom_id == '거부':
                        await a_m.delete()
                        await client.get_user(user_id).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"<@{user_id}>님의 계좌 충전이 거부되었습니다.",
                                                color=0x2f3136))

            else:
                await interaction.user.send(
                    embed=discord.Embed(title="계좌 충전 실패", description=f"```올바른 액수를 입력해주세요.```", color=0x2f3136))
client.run(봇토큰)
