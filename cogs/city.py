import discord
from discord.ext import commands


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
                if m in added:
                    continue
                cat.append(m)
                added.append(m)

            city_members.append(
                sorted(cat.copy(),
                       key=lambda m_: str(m_))
            )
            cat.clear()

        while len(city_members) > max_members and self.any_offline(city_members):
            for cat in reversed(city_members):
                for m in cat:
                    if m.status == discord.Status.offline:
                        cat.pop(cat.index(m))
                        break
                continue

        if len(city_members) > max_members:
            while len(city_members) > max_members:
                for cat in reversed(city_members):
                    for m in cat:
                            cat.pop(cat.index(m))
                            break
                    continue

        return city_members

    # debug command
    @commands.command()
    async def show_members(self, ctx):
        members = self.get_city_members(ctx.guild, 5)  # debud, will change
                                                       # once image gen is set up
        out = []
        for cat in members:
            out.append(" | ".join([str(m) for m in cat]))

        await ctx.send("\n".join(out))


def setup(bot):
    bot.add_cog(City(bot))
