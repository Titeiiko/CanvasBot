from PIL import Image
import discord
from discord.ext import commands
import urllib.request

#CONFIG
#====== EDIT YOUR VARS HERE!
adminChan = insert admin channel id here #add discord id to admins channel
prefix = "insert command prefix" #Prefix of the discord bot
botid = "insert bot id here"
#=====

bot = commands.Bot(command_prefix=str(prefix))
image = Image.open("Canvas.png")

#Variable Gathering
width, height = image.size
ImageWidth = width
ImageHeight = height #Gathers The Width and Height
RGBimage = image.convert('RGB') #Gathers the RGB version of it
print('bot is awake!')

@bot.command()
async def assist(ctx):
    embed = discord.Embed(title="Help Assistance!", description="```c!canvas```", color=0x7be5c2)
    embed.add_field(name="Canvas Prefix", value=str(prefix), inline=True)
    embed.add_field(name="Commands", value="canvas - Shows canvas. \n art (x) (y) (discord url) - place artwork onto it.", inline=True)
    embed.add_field(name="Github", value="https://github.com/Titeiiko/CanvasBot", inline=True)
    await ctx.send(embed=embed)



@bot.command()
async def place(ctx, xcoord: int, ycoord: int):
    if xcoord > ImageWidth:
        await ctx.send("Woah! I can't place a pixel right there!")
        stop
    if ycoord > ImageWidth:
        await ctx.send("Woah! I can't place a pixel right there!")
        stop
    if ycoord < 0:
        await ctx.send("Your placing a pixel in an illegal spot.")
        stop
    if xcoord < 0:
        await ctx.send("Your placing a pixel in an illegal spot.")
        stop

    RGBimage.putpixel((xcoord, ycoord), (155, 155, 55, 255))
    RGBimage.save('Canvas.png')

@bot.command()
async def art(ctx, xcoord: int, ycoord: int, url: str):
    if xcoord > ImageWidth:
        await ctx.send("Woah! I can't place a pixel right there!")
        stop
    if ycoord > ImageWidth:
        await ctx.send("Woah! I can't place a pixel right there!")
        stop
    if ycoord < 0:
        await ctx.send("Your placing a pixel in an illegal spot.")
        stop
    if xcoord < 0:
        await ctx.send("Your placing a pixel in an illegal spot.")
        stop
    #This does a quick check if everything is working smoothly, if it fits all rules!

    req = urllib.request.Request(str(url), headers={'User-Agent': 'Mozilla/5.0'}) #This allows the bot to use a header to grab a discord image.
    with open("temporarily.png", "wb") as f:
        with urllib.request.urlopen(req) as r:
            f.write(r.read())


    tempimage = Image.open("temporarily.png") #After image is grabbed, it starts it's process of placing it onto the canvas
    tempimage = tempimage.convert('RGB')  # Gathers the RGB version of it
    width, height = image.size
    tempwidth = width
    tempheight = height

    if tempheight > ImageHeight or tempwidth > ImageWidth:
        await ctx.send("The image you wanna place onto the canvas is a little bit too large. Give me a size that can fit a canvas under x: " + str(ImageWidth) +
        " and y: " + str(tempheight))
        stop
    RGBimage.paste(tempimage, (xcoord, ycoord))
    RGBimage.save('Canvas.png')

    author = ctx.message.author

    file = discord.File("temporarily.png", filename="temporarily.png")
    channel = bot.get_channel(int(adminChan))
    embed = discord.Embed(title="Canvas Update", description="User: " + str(author) + " has updated the canvas with this artwork.")
    embed.set_image(url='attachment://temporarily.png')
    await channel.send(file = file, embed=embed)

    await ctx.send("Your image has been successfully placed! To see it, do: **" + str(prefix) + "canvas**")


@bot.command()
async def canvas(ctx):
    curimage = Image.open("Canvas.png") #Grabs the image AFTER edited (or if it was)

    expandh = height * 2
    expandw = width * 2
    tempimg = curimage.resize((expandw, expandh), Image.ANTIALIAS) #Resize, this would mostly play a role for small canvases
    tempimg.save('resized_image.png')
    file = discord.File("resized_image.png", filename="resized_image.png")

    embed = discord.Embed(title="Canvas", description="", color = 222222)  #,color=Hex code
    embed.set_image(url = 'attachment://resized_image.png')
    await ctx.send(file = file, embed=embed)

#===
#Events
#===

async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Event Handlers'))
    print("the bot is online!")

bot.run(str(botid))

