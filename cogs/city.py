import discord
from discord.ext import commands


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
                    city_members.insert(0, [m])

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
                        cat.pop(cat.index(m))  # TODO: owner will stay
                        break
                continue

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


def setup(bot):
    bot.add_cog(City(bot))
