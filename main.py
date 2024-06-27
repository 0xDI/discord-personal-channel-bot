import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Mentoring"))
    print(f'{bot.user.name} started Working!')

@bot.event
async def on_member_update(before, after):
    verified_role_id = 1196578683943665777 # REPLACE IT
    if any(role.id == verified_role_id for role in after.roles) and not any(role.id == verified_role_id for role in before.roles):
        await on_verified(after)

async def on_verified(member):
    guild = member.guild
    category_id = 1201815658791444490 # REPLACE IT
    category = discord.utils.get(guild.categories, id=category_id)
    verified_role_id = 1196578683943665777 # REPLACE IT
    role = discord.utils.get(guild.roles, id=verified_role_id)
    staff_role_id = 1196584599560671353  # REPLACE IT
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await category.create_text_channel(f"mentoring-{member.name}", overwrites=overwrites)
    user_mention = member.mention
    role_mention = f"<@&{staff_role_id}>"

    message_content = f"||{user_mention} {role_mention}||"
    await channel.send(message_content)

    embed = discord.Embed(title="__**Welcome to Ecom Funds**__",
                          description=f"Hey, {user_mention}. This is a channel created just for you, so you can get to know our team & also get help with anything you might need.\n An {role_mention} will be with you ASAP.\n **Make sure you:** \n > **1.** Check out our **Free Resources**\n > **2.** Consider an <#1197917745782722640> to Funded Plan\n > **3.** Check out <#1197917045715640331> from our customers\n > **4.** Hook yourself with some <#1196578686032412757> \n > **5.** Read our <#1196578685331968054>\n > **6.** Have a look at [**our website**](https://ecomfunds.click) \n\n Don't hesitate to **tag any of our Team** if our Mentors take too long to respond.\n\nReact with ❌ to close (The bot will DM you).",
                          color=discord.Color.darker_grey())
    embed.set_image(url="https://media.discordapp.net/attachments/1083053135741849762/1197218428906381404/welcome.gif?ex=65c3b20c&is=65b13d0c&hm=32697c53497513c02f79309590ac4186a961e616cb524afeb164349dbfd017a1&width=956&height=212&")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1197617796654321694/1200197543221530756/IMG_3534.gif?ex=65c54e10&is=65b2d910&hm=aa0a1939f3b654c610578bf2e02efb9c4a6ad472dc31aca0e121325e0e9d3fdb&")
    message = await channel.send(embed=embed)
    await message.add_reaction("❌")


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == "❌":
        channel = reaction.message.channel
        if channel.name.startswith("mentoring-"):
            dm_channel = await user.create_dm()
            embed = discord.Embed(
                title="Are you sure you want to delete this mentoring channel?",
                description="\n__You might not have this chance again!__\nReact with ✅ to confirm or ❌ to cancel.",
                color=discord.Color.red()
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1113081965525094452/1150093735040913428/blue.gif?ex=65c79942&is=65b52442&hm=d9de1455abaac5d3ca32903f63aac40172adce153613ba01fdbdf91017e6f4a0&")
            embed.set_footer(text="By Ecom Funds Mentoring")
            message = await dm_channel.send(embed=embed)

            # Add reactions for confirmation
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            # Listen for reaction in DMs
            def check(reaction, reacted_user):
                return reacted_user == user and str(reaction.emoji) in ["✅", "❌"] and reaction.message == message

            try:
                reaction, _ = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await dm_channel.send("You took too long to respond. Channel deletion cancelled.")
            else:
                if str(reaction.emoji) == "✅":
                    await channel.delete()
                    await dm_channel.send("Mentoring Channel Closed.")
                else:
                    await dm_channel.send("Mentoring Closing Cancelled.")


bot.run('tokenhere')