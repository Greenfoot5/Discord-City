import discord
from discord.ext import commands
import cairocffi as cairo
from io import BytesIO
import random
import math


def PolarToCartesian(coord):
    angle = coord[0]
    magnitude = coord[1]    
    x = magnitude*math.cos(angle)+512
    y = magnitude*math.sin(angle)+512
    return [x,y]

def createCity(memberList, houseSize):
    #memberList format should be, for example, [(r,g,b)*x,(r1,g1,b1)*y...]
    #houseSize should be between 5-20
    #castle formation process:
    #street formation process;
    streetNum = random.randint(5,8)
    streets =[]
    temp = random.randint(0,int(360/streetNum))
    streets.append(temp)
    shapeArray=[]
    
    for i in range(0,streetNum-1):
        temp1 = streets[i]
        temp2 = random.randint(0,int(360/streetNum))
        streets.append(temp1+temp2)
    streets.append(360)
    memberCount=0
    r=0
    rAppend=20
    band=0
    while memberCount<len(memberList):
        r+=rAppend
        band+=1
        if band % 3 != 2:
            for i in range(1, streetNum):
                temp1 = (streets[i] - streets[i-1])/360*2*math.pi*r
                angle = streets[i-1]/360*2*math.pi
                houseAngle = houseSize/r
                temp2=0
                while True:
                    if temp1>=houseSize:
                        temp1-=houseSize
                        temp2+=1
                        coord0=PolarToCartesian([angle+houseAngle*temp2,r])
                        coord3=PolarToCartesian([angle+houseAngle*temp2,r+rAppend])
                        if temp1-houseSize>=0:
                            coord1=PolarToCartesian([angle+houseAngle*(temp2+1),r])
                            coord2=PolarToCartesian([angle+houseAngle*(temp2+1),r+rAppend])
                        else:
                            coord1=PolarToCartesian([streets[i]/360*2*math.pi,r])
                            coord2=PolarToCartesian([streets[i]/360*2*math.pi,r+rAppend])
                        if memberCount==len(memberList):
                            break
                        shapeArray.append([coord0,coord1,coord2,coord3,memberList[memberCount]])
                        memberCount+=1
                    else:
                        break

    return shapeArray


def ListToImage(thislist):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 1024)
    with open("paper.png", "rb") as f:
        surface = cairo.ImageSurface.create_from_png(f)
    ctx = cairo.Context(surface)
    ctx.scale(1,1)
    for i in range(0, len(thislist)):
        ctx.move_to(thislist[i][0][0],thislist[i][0][1])
        for j in range(1, len(thislist[i])-1):
            x=thislist[i][j][0]
            y=thislist[i][j][1]
            ctx.line_to(x,y)
            k=j+1
        ctx.close_path()
        r=thislist[i][k][0]/255
        g=thislist[i][k][1]/255
        b=thislist[i][k][2]/255
        ctx.set_source_rgb(r,g,b)
        ctx.stroke()
    buff = BytesIO()
    surface.write_to_png(buff)
    buff.seek(0)

    return buff

def do_city(colors):
    city = createCity(colors, 10)
    img = ListToImage(city)
    return img


def flatten(list_):
    out = []
    for elem in list_:
        for elem2 in elem:
            out.append(elem2)
    return out


class City(commands.Cog):
    """
    The commands related about generating the city.
    """

    def __init__(self, bot):
        self.bot = bot

    def any_offline(self, city_members):
        for cat in city_members:
            for m in cat:
                if m.status == discord.Status.offline:
                    return True
        return False

    def get_city_members(self, guild, max_members):
        added = []
        city_members = []

        # roles are now in descending order
        for role in sorted(guild.roles, reverse=True):
            mem = role.members
            if mem == []:  # empty role
                continue

            cat = []
            for m in mem:
                if m.display_name.startswith("!") and m.top_role == guild.default_role:
                    added.append(m)  # hoister

                if m == guild.owner:
                    added.append(m)
                    owner = [[m]]

                if m in added:
                    continue

                added.append(m)
                cat.append(m)

            city_members.append(
                sorted(cat.copy(),
                       key=lambda m_: str(m_))
            )
            cat.clear()

        while len(flatten(city_members)) > max_members and self.any_offline(city_members):
            for cat in reversed(city_members):
                for m in cat:
                    if m.status == discord.Status.offline:
                        cat.pop(cat.index(m))
                        break
                continue

        city_members = owner + city_members
        if len(flatten(city_members)) > max_members:
            while len(flatten(city_members)) > max_members:
                for cat in reversed(city_members):
                    if cat == []:
                        city_members.pop()
                        break
                    cat.pop()
                    break

        return city_members

    # debug command
    @commands.command()
    async def show_members(self, ctx):
        members = self.get_city_members(ctx.guild, 5)  # debug, will change
        #                                                once image gen is set up
        out = []
        for cat in members:
            out.append(" | ".join([str(m) for m in cat]))

        await ctx.send("\n".join(out))

    @commands.command()
    async def city(self, ctx):
        """
        Generates a city out of the current server.
        """
        async with ctx.typing():
            colors = [m.color.to_rgb() for m in ctx.guild.members]

            out = await self.bot.loop.run_in_executor(None, do_city, colors)

            await ctx.send(file=discord.File(out, "out.png"))



def setup(bot):
    bot.add_cog(City(bot))
