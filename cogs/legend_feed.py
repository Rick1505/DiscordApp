import discord
import asyncio

from discord.ext    import commands, tasks
from discord        import app_commands
from classes.player import Player
from typing         import List
from classes.emojis import Emoji



class LegendFeed(commands.GroupCog, name="legend"):
    """Uses all information to create a legend feed"""
    def __init__(self, bot) -> None:
        self.bot = bot
        self.db = bot.dbconn
        self.emoji = Emoji()
    
        
    async def creates_embed_player_overview(self, player_name:str, player_tag: str, group_name: str) -> discord.Embed:
        """Creates a discord embed for a legend_overview of a player"""       
        data = self.db.get_all_mutations_per_day(account_tag=player_tag)
        
        offense = data["offense"]
        defense = data["defense"]
        
        field1 = "\n".join(str(attack) for attack in offense)
        field2 = "\n".join(str(defend) for defend in defense)
        
        description = f"""
        __*Overview*__ \n
        Total Offense: {sum(offense)}\n
        Total Defense: {sum(defense)}
        """
        custom_embed = discord.Embed(
            title=player_name,
            description= description,
            colour=discord.Colour.from_rgb(0, 150, 255)
        )
        custom_embed.add_field(name="**Offense**", value=field1, inline=True)
        custom_embed.add_field(name="**Defense**", value=field2, inline=False)
        
        custom_embed.set_footer(text=group_name)
        return custom_embed


    async def create_embed_paging(self, embeds: List, channel:discord.TextChannel):
        current_page = 0         
        
        message = await channel.send(embed=embeds[current_page])
        for emoji in ['◀️', '▶️']:
            await message.add_reaction(emoji)
            
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0)

                if str(reaction.emoji) == "▶️":
                    current_page = (current_page + 1) % len(embeds)
                elif str(reaction.emoji) == "◀️":
                    current_page = (current_page - 1) % len(embeds)

                await message.edit(embed=embeds[current_page])
                await message.remove_reaction(reaction, user)

            except TimeoutError:
                await message.clear_reactions()
                break   
   
    #THIS WILL POST LEGEND HITS EVERY 60 SECONDS
    @tasks.loop(seconds=60) 
    async def legend_feed(self, channel, guild_id: int):
      
        # Get tags from all groups
        player_group = self.db.get_all_groups(guild_id=guild_id)
        
        #store every tag in a list
        tags_to_check = [record.tag for record in player_group]
        
        #Create list of mutations and embeds
        mutations = []
        embed_embeds = []
        
        #Check every individual tag for changes
        for tag in tags_to_check:
            info = {}
            player = Player(tag)
            player_info = player.get_all_player_info()
            
            #Calculating trophies
            new_trophies = player_info["trophies"]
            current_trophies = player.get_db_trophies()
            #CHANGE TO DELTA
            delta_trophies = current_trophies
                            
            #TODO add all changes to a list in a list as a string with: emoji, cups, name
            #TODO make an embed with multiple pages, every page shows Title: name; Description: overview, total begin total now +/- and details with every attack. footer is group_name
            if delta_trophies != 0:
                #adds mutation to database
                self.db.add_mutation(account_tag=tag, current_trophies=current_trophies, new_trophies=new_trophies)

                #adds information to info
                info["name"] = player_info["name"]
                info["group_name"] = self.db.get_player_from_group(guild_id=guild_id, account_tag=tag).group
                info["delta_trophies"] = delta_trophies
                
                embed_embeds.append(await self.creates_embed_player_overview(info["name"], tag, info["group_name"]))
                
                #add information of mutation to list mutations
                mutations.append(info)
                
        #Check amount of mutations
        if len(mutations) > 1:    
            
            #create list of embeds
            embeds = []
            counter = 1
            description = ""
                
            for mutation in mutations:

                if mutation["delta_trophies"] > 0:
                    #Add positive mutation to description
                    description =  description + (f"{counter} {self.bot.get_emoji(self.emoji.get_emoji("plus_trophy"))} {mutation["delta_trophies"]} {mutation["name"]}\n")
                    counter += 1
                    
                else:
                    #Add negative mutation to description
                    description = description +  (f"{counter} {self.bot.get_emoji(self.emoji.get_emoji("min_trophy"))} {mutation["delta_trophies"]} {mutation["name"]} \n")
                    counter += 1
                    
            #Create embed with lists of mutations
            custom_embed = discord.Embed(
                    description = description,
                    colour=discord.Colour.from_rgb(0, 150, 255)
            )
            
            #add custom_embed to list of embeds
            embeds.append(custom_embed)
            embeds = embeds + embed_embeds
            
            #check if there are any embeds
            if len(embeds) > 0:
                
                await self.create_embed_paging(embeds=embeds, channel=channel)
            
        elif len(mutations) == 1:
            embeds = []       
            mutation = mutations[0]
            
            if mutation["delta_trophies"] > 0:
                
                custom_embed = discord.Embed(
                    title=mutation["name"],
                    color= discord.Color.from_rgb(0, 200, 0),
                    description= f"{self.bot.get_emoji(self.emoji.get_emoji(emoji="plus_trophy"))} {mutation["delta_trophies"]}"
                ) 
                custom_embed.set_footer(text=tag)
                embeds.append(custom_embed)
                
            else:
                custom_embed = discord.Embed(
                    title=mutation["name"],
                    colour= discord.Colour.from_rgb(254, 0,0),
                    description= f"{self.bot.get_emoji(self.emoji.get_emoji(emoji="min_trophy"))} {mutation["delta_trophies"]}"
                ) 
                custom_embed.set_footer(text=tag)
                embeds.append(custom_embed)
            
            embeds = embeds + embed_embeds

                        
            if len(embeds) > 0:
                await self.create_embed_paging()
        else:
            pass

    #ACTIVATES THE LEGEND_FEED   
    @app_commands.command(name = "set_feed", description = "This will set the correct channel for the legend feed.")
    @app_commands.rename(channel = "channel")
    @app_commands.describe(channel = "The channel you want the bot to post all hits in")
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.legend_feed.start(channel, interaction.guild.id)
        
        await interaction.response.send_message(f"The channel has successfully been set {channel}")
        
        
async def setup(bot:commands.Bot) -> None:
  await bot.add_cog(LegendFeed(bot))