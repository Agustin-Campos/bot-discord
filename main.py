import logging
import random
import discord
from discord.ext import commands
import json


bot = commands.Bot(command_prefix='!', case_insensitive=True, intents= discord.Intents.all())


secret_file = json.load(open('secrets.json'))
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)


# Events
@bot.event
async def on_ready():
    print("I'm ready")


# deletes selected words
# words within the list must be in lower case letters
@bot.event
async def on_message(message):
    await bot.process_commands(message)

    words = ['stupid', 'idiot', 'bitch', 'b1tch', 'b!tch']

    for word in words:
        if message.content.lower() == word:
            await message.delete()

    # remove invitations to channels
    if message.content.startswith('https://discord.gg'):
        await message.delete()
        await message.channel.send(f'No invitation links please {message.author.mention}')

    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send(':partying_face: :zany_face: :smiling_face_with_3_hearts:')
        await bot.process_commands(message)


# commands
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title='Bot', description='These are all commands, always use the "!" prefix', color=0xffffff)
    embed.add_field(name='rules', value='The rules')
    embed.add_field(name='hi/hello/hola', value='The bot says hi')
    embed.add_field(name='link<site name>', value='Generates a link with the entered word')
    embed.add_field(name='pin_msg<message>', value='Pin a message')
    embed.add_field(name='info', value='send by md information')
    embed.add_field(name='delete_msg<number>', value='Deletes the indicated number of messages (max. 100)')
    embed.add_field(name='channel_text<channel name>', value='Creates a text channel')
    embed.add_field(name='channel_voice<channel name>', value='Creates a voice channel')
    embed.add_field(name='member_join<user name>', value='Date of entry of the indicated user')
    embed.add_field(name='repeat<message>', value='Repeat message')
    embed.add_field(name='reverse<message>', value='Reverses the message entered')
    embed.add_field(name='poll<message>', value='Survey to be answered by yes or no')
    embed.add_field(name='cat', value='The image of a cat')
    embed.add_field(name='dog', value='The image of a dog')
    embed.add_field(name='randomnum', value='A random number between 1 and 10(modifiable)')
    await ctx.send(content=None, embed=embed)


@bot.command()
async def rules(ctx):
    f = open('rules', 'r')
    rule = f.readlines()
    for rul in rule:
        await ctx.send(rul)


@bot.command()
async def repeat(ctx, *args):
    await ctx.send("{}".format(" ".join(args)))


@bot.command()
async def link(ctx, text: str):
    link1 = 'https:/'
    link2 = '.com'
    link = link1 + text + link2
    await ctx.send('Your link: ' + link)


@bot.command()
async def pin_msg(ctx):
    await ctx.message.pin()


@bot.command()
async def info(ctx):
    await ctx.author.send(file=discord.File('information'))


# maximum of 100 messages can be deleted at a time
@bot.command()
async def delete_msg(ctx, index: int):
    def not_pinned(msg):
        return not msg.pinned
    delete_messages = await ctx.channel.purge(limit=index, check=not_pinned)
    await ctx.send(f'{len(delete_messages)} messages have been successfully deleted.')


@bot.command()
async def channel_text(ctx, channel_name):
    await ctx.guild.create_text_channel(channel_name)
    await ctx.send(f'Text channel {channel_name} has been successfully created.')


@bot.command()
async def channel_voice(ctx, channel_name):
    await ctx.guild.create_voice_channel(channel_name)
    await ctx.send(f'The voice channel {channel_name} has been successfully created.')


@bot.command()
async def member_join(ctx, member: discord.Member):
    joined = member.joined_at.strftime('%b %d, %Y, %T')
    await ctx.send(f'{member.mention} joined at {joined}')


@bot.command(name='hi', aliases=['hello', 'hola'])
async def hi(ctx):
    await ctx.send(f'Hi {ctx.author.mention} :)')


@bot.command()
async def reverse(ctx, *, arg='gnihtyna deretne ton evah uoY'):
    await ctx.message.delete()
    await ctx.send(arg[::-1])


@bot.command()
async def poll(ctx, *, content: str):
    embed = discord.Embed(title=f'{content}', description='✅ for yes and ❌ for no.', color=0xffffff)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    message = await ctx.channel.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')


@bot.command()
async def cat(ctx):
    file = discord.File("images/cat.jpg")
    embed = discord.Embed(color=0xffffff)
    embed.set_image(url="attachment://cat.jpg")
    await ctx.send(file=file, embed=embed)


@bot.command()
async def dog(ctx):
    file = discord.File("images/dog.jpg")
    embed = discord.Embed(color=0xffffff)
    embed.set_image(url="attachment://dog.jpg")
    await ctx.send(file=file, embed=embed)


@bot.command(pass_context=True)
async def randomnum(ctx):
    embed = discord.Embed(title='The random number is', description=(random.randint(1, 10)), color=0xffffff)
    await ctx.send(embed=embed)


bot.run(bot.config_token)
