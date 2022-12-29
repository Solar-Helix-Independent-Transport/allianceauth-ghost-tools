# Cog Stuff
import logging

# AA-Discordbot
from aadiscordbot.cogs.utils.decorators import has_any_perm
from allianceauth.eveonline.models import EveCharacter
from discord import AutocompleteContext, option
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
# AA Contexts
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class Ghosts(commands.Cog):
    """
    All about Ghosts!
    """

    def __init__(self, bot):
        self.bot = bot

    def ghost_embed(self, input_name):
        embed = Embed(
            title="Ghost Lookup {character_name}".format(
                character_name=input_name)
        )

        try:
            char = EveCharacter.objects.get(character_name=input_name)

            main = char.character_ownership.user.profile.main_character
            state = char.character_ownership.user.profile.state.name
            ghosts = char.character_ownership.user.character_ownerships.all(
            ).select_related('character').filter(character__corporation_id=98534707)
            ghost = None

            if ghosts.exists():
                _g = []
                for g in ghosts:
                    _g.append(g.character.character_name)
                ghost = "**Ghosts:** {}".format(
                    ", ".join(_g)
                )
            else:
                ghost = "None Found"
            try:
                discord_string = "<@{}>".format(
                    char.character_ownership.user.discord.uid)

                user = get(self.bot.get_all_members(),
                           id=char.character_ownership.user.discord.uid)
                try:
                    if user:
                        #url = user.avatar.url
                        discord_string = f"**{user.display_name}** `{user.name}@{user.discriminator}` <@{user.id}>\n[[eveWho](https://evewho.com/character/{main.character_id})]  [[zKill](https://zkillboard.com/character/{main.character_id}/)]"
                except Exception as e:
                    logger.error(e)
            except Exception as e:
                logger.error(e)
                discord_string = "unknown"

            if state in ["Member", "s_vip"]:
                embed.color = Color.blue()
                embed.description = (
                    "**Accept** Application"
                )
            else:
                embed.color = Color.red()
                embed.description = (
                    f"**Reject/Kick** Application: `Main not a Member`"
                )

            embed.add_field(
                name="Main", value=discord_string, inline=False
            )
            if ghost:
                embed.add_field(
                    name="Existing Ghosts", value=ghost, inline=False
                )

            return embed

        except (EveCharacter.DoesNotExist, ObjectDoesNotExist):
            embed.colour = Color.red()

            embed.description = (
                "**Reject** Application `Ghost not in Auth`"
            )

            return embed

    async def search_characters(ctx: AutocompleteContext):
        """Returns a list of colors that begin with the characters entered so far."""
        return list(EveCharacter.objects.filter(character_name__icontains=ctx.value).values_list('character_name', flat=True)[:10])

    @commands.slash_command(name='ghost', guild_ids=[int(settings.DISCORD_GUILD_ID)])
    @option("character", description="Search for a Ghost!", autocomplete=search_characters)
    async def slash_ghost(
        self,
        ctx,
        character: str,
    ):
        """
        Gets Ghost data about a character
        """

        try:
            await ctx.defer()
            has_any_perm(ctx.author.id, [
                         'ghosttools.access_ghost_tools'])
            return await ctx.respond(embed=self.ghost_embed(character))
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)

    @commands.slash_command(name='ghosts_processed', guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def slash_ghosts_done(
        self,
        ctx
    ):
        """
        Say ghosts have been processed like a good ghost manager
        """

        try:
            await ctx.defer(ephemeral=True)
            has_any_perm(ctx.author.id, [
                         'ghosttools.access_ghost_tools'])
            await ctx.respond("Ok!", ephemeral=True)
            return await ctx.send("All Ghost applications processed!\nPlease log in your ghost and accept the invite!\nIf you were rejected please check the reason before you re-apply!")
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)


def setup(bot):
    bot.add_cog(Ghosts(bot))
