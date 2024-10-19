# Cog Stuff
import logging

import discord
# AA-Discordbot
from aadiscordbot.app_settings import get_all_servers
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
from django.utils import timezone

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
                discord_string = f"[{main.character_name}](https://evewho.com/character/{main.character_id}) [[{main.corporation_name} [{main.corporation_ticker}]](https://zkillboard.com/corporation/{main.corporation_id}/)]"

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

    @commands.slash_command(name='ghost', guild_ids=get_all_servers())
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
                         'ghosttools.access_ghost_tools'],
                         guild=ctx.guild)
            return await ctx.respond(embed=self.ghost_embed(character))
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)

    @commands.slash_command(name='ghosts_processed', guild_ids=get_all_servers())
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
                         'ghosttools.access_ghost_tools'],
                         guild=ctx.guild)
            await ctx.respond("Ok!", ephemeral=True)
            return await ctx.send("All Ghost applications processed!\nPlease log in your ghost and accept the invite!\nIf you were rejected please check the reason before you re-apply!")
        except commands.MissingPermissions as e:
            return await ctx.respond(e.missing_permissions[0], ephemeral=True)

    async def open_ticket(
        self,
        ctx: discord.Interaction,
        member: discord.Member
    ):
        sup_channel = settings.RECRUIT_CHANNEL_ID
        ch = ctx.guild.get_channel(sup_channel)
        th = await ch.create_thread(
            name=f"{member.display_name} | {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            auto_archive_duration=10080,
            type=discord.ChannelType.private_thread,
            reason=None
        )
        msg = (f"<@{member.id}> is hunting for a recruiter!\n\n"
               f"Someone from <@&{settings.RECRUITER_GROUP_ID}> will get in touch soon!")
        embd = Embed(title="Private Thread Guide",
                     description="To add a person to this thread simply `@ping` them. This works with `@groups` as well to bulk add people to the channel. Use wisely, abuse will not be tolerated.\n\nThis is a beta feature if you experience issues please contact the admins. :heart:")
        await th.send(msg, embed=embd)
        await ctx.response.send_message(content="Recruitment thread created!", view=None, ephemeral=True)

    @commands.slash_command(
        name='recruit_me',
        guild_ids=get_all_servers()
    )
    async def slash_halp(
        self,
        ctx,
    ):
        """
            Get hold of a recruiter
        """
        await self.open_ticket(ctx, ctx.user)

    @commands.message_command(
        name="Create Recruitment Thread",
        guild_ids=get_all_servers()
    )
    async def reverse_recruit_msg(
        self,
        ctx,
        message
    ):
        """
            Help a new guy get recruiter
        """
        await self.open_ticket(ctx, message.author)

    @commands.user_command(
        name="Recruit Member",
        guild_ids=[int(settings.DISCORD_GUILD_ID)]+settings.DISCORD_GUILD_IDS
    )
    async def reverse_recruit_user(
        self, ctx, user
    ):
        """
            Help a new guy get recruiter
        """
        await self.open_ticket(ctx, user)


def setup(bot):
    bot.add_cog(Ghosts(bot))
