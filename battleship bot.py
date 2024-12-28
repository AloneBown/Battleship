# Copyrighting (C) 2024 by AloneBown
#
# <-This code is free software; 
# you can redistribute it and/or modify it under the terms of the license
# This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.->
#  
# See GNU General Public License v3.0 for more information.
# You should receive a copy of it with code or visit https://www.gnu.org/licenses/gpl-3.0.html
# (do not remove this notice)

#TO DO LIST
# - DO AN AI TACTICS TO MAKE IT MORE UNPREDICTEBLE (CHESSBOARD HITTS, DIAGONAL HITTS, ETC)
# - BETTER EMBEDS (GRAPHICS MB?)
# - OPTIMISE THE CODE (+-)
# - CHAOS MODE (AI SHIPS RANDOMLY MOVING, ETC)

import discord, yaml
from bs_resourses.AI import AI
from bs_resourses.lists import Lists

intents = discord.Intents.default(); intents.members = True; bot = discord.Bot(intents=intents)

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
TOKEN = config["token"]

board_size = 10; empty_cell = "O"; ship_cell = "P"; hit_cell = "U"; miss_cell = "X"; ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def create_board():
    return [[empty_cell for _ in range(board_size)] for _ in range(board_size)]

player_board = create_board(); computer_board = create_board(); player_hits = 0; ai_hits = 0; game_started = False; player_ships = {}; computer_ships = {}

ai = AI(board_size, empty_cell, ship_cell, hit_cell, miss_cell, player_board, ships=ships, player_ships=player_ships, computer_ships=computer_ships)
lists = Lists()

def convert_coordinates(coord):
    letter_to_index = lambda c: ord(c.lower()) - ord('a'); x = letter_to_index(coord[0]); y = int(coord[1:]) - 1
    return x, y

    
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="start", description="Start a new game of Battleship")
async def start(ctx):
    global player_board, computer_board, ai_last_hit, player_hits, ai_hits, ships, ai_hits_positions, game_started, player_moves, ai_moves
    player_board = create_board(); computer_board = create_board(); ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]; ai_moves = set()
    ai_last_hit = None; player_hits = 0; ai_hits = 0; ai_hits_positions = []; game_started = True; player_moves = set()
    ai.place_ships(computer_board, computer_ships); admiral=lists.ai_admirals_randomiser()
    embed = discord.Embed(title="Enemy fleet on a horizon!", color=discord.Color.yellow()); embed.add_field(name=f"We are approaching the enemy fleet under the command of {admiral.r} {admiral.n} {admiral.s} from {admiral.c}", value=f"Prepare our ships! (use ``/place_ship`` command)")
    await ctx.send(embed=embed)

@bot.slash_command(name="place_ship", description="Place a ship on the board")
async def place_ship(ctx, mode: str = discord.Option(str, "Choose placement mode", choices=["manual", "random"]), start: str = None, end: str = None):
    global ships, game_started
    if not game_started:
        await ctx.respond("You need to start a game first using /start command.", ephemeral=True)
        return
    if mode == "random":
        ai.place_ships(player_board, player_ships)
        ships = []
        embed = discord.Embed(title="All ships placed randomly", color=discord.Color.green()); embed.add_field(name="Your board", value=f"```json\n{ai.print_board(player_board)}\n```")
        await ctx.send(embed=embed)
        return
    if not start or not end:
        await ctx.respond("You need to provide start and end positions for the ship.", ephemeral=True)
        return
    start_x, start_y = map(int, start.split(","))
    end_x, end_y = map(int, end.split(","))
    length = max(abs(end_x - start_x), abs(end_y - start_y)) + 1
    if length not in ships:
        await ctx.respond(f"Invalid ship length. Available lengths: {ships}", ephemeral=True)
        return
    horizontal = start_x == end_x
    if not ai.is_valid_position(player_board, start_x, start_y, length, horizontal):
        await ctx.respond("Invalid position for the ship. It overlaps with another ship or is out of bounds.", ephemeral=True)
        return
    ship_positions = []
    if horizontal:
        for i in range(length):
            player_board[start_x][start_y + i] = ship_cell
            ship_positions.append((start_x, start_y + i))
    else:
        for i in range(length):
            player_board[start_x + i][start_y] = ship_cell
            ship_positions.append((start_x + i, start_y))

    player_ships[f"{length}_{len(player_ships)}"] = ship_positions
    ships.remove(length)
    if not ships:
        embed = discord.Embed(title="All ships placed", color=discord.Color.green()); embed.add_field(name="Your board", value=f"```json\n{ai.print_board(player_board)}\n```")
        await ctx.send(embed=embed)
    else:
        await ctx.respond(f"Ship placed from {start} to {end}.\nYour board:\n```json\n{ai.print_board(player_board)}\n```", ephemeral=True)

@bot.slash_command(name="move", description="Make a move in Battleship")
async def move(ctx, coord: str):
    global ai_last_hit, player_hits, ai_hits, ai_hits_positions, player_moves, ai_moves
    player_name = str(ctx.author.name)
    x, y = convert_coordinates(coord)
    if not (0 <= x < board_size and 0 <= y < board_size):
        await ctx.respond("Out of range, admiral.", ephemeral=True)
        return
    if computer_board[x][y] in [hit_cell, miss_cell]:
        await ctx.respond("Can't do that. We already hit that zone, high command will be furious if we will be wasting shells.", ephemeral=True)
        return
    player_moves.add((x, y))    
    if computer_board[x][y] == ship_cell:
        computer_board[x][y] = hit_cell
        player_hits += 1
        result = f"Hit! (Player hits: {player_hits})"
        await ctx.respond('Fire!', ephemeral=True)
        for ship, positions in computer_ships.items():
            if (x, y) in positions:
                if ai.is_ship_sunk(positions, computer_board):
                    ai.mark_surrounding_cells_as_miss(positions, computer_board)
                    embed = discord.Embed(title="You destroyed a ship!", color=discord.Color.red()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI board", value=f"```json\n{ai.print_computer_board()}\n```")
                    await ctx.send(embed=embed)
                    if ai.all_ships_destroyed(computer_ships, computer_board):
                        ai.update_stats(player_name, "win")
                        embed = discord.Embed(title="You win!", color=discord.Color.dark_green()); embed.add_field(name="Your move", value=result); embed.add_field(name="Your board", value=f"```json\n{ai.print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{ai.print_computer_board()}\n```")
                        await ctx.send(embed=embed)
                        ai_hits_positions.clear()
                        ai_moves.clear()
                        ai_hits = 0
                        player_hits = 0
                        player_ships.clear()
                        computer_ships.clear()
                        return
                else:
                    embed = discord.Embed(title="You hit a ship!", color=discord.Color.orange()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI board", value=f"```json\n{ai.print_computer_board()}\n```")
                    await ctx.send(embed=embed)
                break
    else:
        computer_board[x][y] = miss_cell
        result = f"Miss! (Player hits: {player_hits})"
        await ctx.respond('Fire!', ephemeral=True)
        player_hits = 0
        await ai.ai_move(ctx, result, player_name, player_board, player_ships, board_size, hit_cell, miss_cell, ship_cell, empty_cell, computer_ships, computer_board)

@bot.slash_command(name="stats", description="Display statistics")
async def stats(ctx):
    embed = ai.display_stats()
    await ctx.send(embed=embed)

bot.run(TOKEN)