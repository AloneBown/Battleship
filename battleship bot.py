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
# - AI ADMIRALS NAMES + RANDOMISER FOR THEM
# - BETTER EMBEDS (GRAPHICS MB?)
# - OPTIMISE THE CODE
# - CHAOS MODE (AI SHIPS RANDOMLY MOVING, ETC)

import discord, yaml, random, json, asyncio

intents = discord.Intents.default(); intents.members = True; bot = discord.Bot(intents=intents)

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)
TOKEN = config["token"]

board_size = 10; empty_cell = "O"; ship_cell = "P"; hit_cell = "U"; miss_cell = "X"; ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def create_board():
    return [[empty_cell for _ in range(board_size)] for _ in range(board_size)]

player_board = create_board(); computer_board = create_board(); player_hits = 0; ai_hits = 0; game_started = False; player_ships = {}; computer_ships = {}

def load_stats():
    try:
        with open("stats.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_stats(stats):
    with open("stats.json", "w") as file:
        json.dump(stats, file, indent=4)

def update_stats(player, result):
    stats = load_stats()
    if player not in stats:
        stats[player] = {"wins": 0, "losses": 0}
    stats[player][result + "s"] += 1
    save_stats(stats)

def display_stats():
    stats = load_stats(); embed = discord.Embed(title="Player Statistics", color=discord.Color.blue())
    for player, data in stats.items():
        win_ratio = data["wins"] / (data["wins"] + data["losses"]) if (data["wins"] + data["losses"]) > 0 else 0
        embed.add_field(name=player, value=f"Wins: {data['wins']}, Losses: {data['losses']}, Win Ratio: {win_ratio:.2f}", inline=False)
    return embed

def is_valid_position(board, x, y, length, horizontal):
    def is_within_bounds(nx, ny):
        return 0 <= nx < board_size and 0 <= ny < board_size

    def is_surrounding_cells_empty(nx, ny):
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            adj_x, adj_y = nx + dx, ny + dy
            if is_within_bounds(adj_x, adj_y) and board[adj_x][adj_y] == ship_cell:
                return False
        return True

    for i in range(length):
        nx, ny = (x, y + i) if horizontal else (x + i, y)
        if not is_within_bounds(nx, ny) or board[nx][ny] != empty_cell or not is_surrounding_cells_empty(nx, ny):
            return False
    return True

def place_ships(board, ships_dict):
    def place_ship(x, y, length, horizontal):
        ship_positions = []
        for i in range(length):
            nx, ny = (x, y + i) if horizontal else (x + i, y)
            board[nx][ny] = ship_cell
            ship_positions.append((nx, ny))
        return ship_positions

    for index, length in enumerate(ships):
        placed = False
        while not placed:
            x, y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
            horizontal = random.choice([True, False])
            if is_valid_position(board, x, y, length, horizontal):
                ships_dict[f"{length}_{index}"] = place_ship(x, y, length, horizontal)
                placed = True
                print(f'All ships positioned: {ships_dict}')

def convert_coordinates(coord):
    letter_to_index = lambda c: ord(c.lower()) - ord('a'); x = letter_to_index(coord[0]); y = int(coord[1:]) - 1
    return x, y

def print_board(board):
    header = "  " + " ".join([str(i + 1) for i in range(board_size)]); rows = []
    for i, row in enumerate(board):
        rows.append(chr(65 + i) + " " + " ".join(row))
    return header + "\n" + "\n".join(rows)

def print_computer_board():
    display_board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    for x in range(board_size):
        for y in range(board_size):
            if computer_board[x][y] in [hit_cell, miss_cell]:
                display_board[x][y] = computer_board[x][y]
    header = "  " + " ".join([str(i + 1) for i in range(board_size)]); rows = []
    for i, row in enumerate(display_board):
        rows.append(chr(65 + i) + " " + " ".join(row))
    return header + "\n" + "\n".join(rows)

def all_ships_destroyed(ships, board):
    for positions in ships.values():
        if not is_ship_sunk(positions, board):
            return False
    return True

def is_ship_sunk(ship_positions, board):
    return all(board[x][y] == hit_cell for x, y in ship_positions)

def mark_surrounding_cells_as_miss(ship_positions, board):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for x, y in ship_positions:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < board_size and 0 <= ny < board_size and board[nx][ny] == empty_cell:
                board[nx][ny] = miss_cell

def hit_cells(board, x, y, ships):
    if board[x][y] == ship_cell:
        board[x][y] = hit_cell
        for ship, positions in ships.items():
            if (x, y) in positions:
                if is_ship_sunk(positions, board):
                    mark_surrounding_cells_as_miss(positions, board)
                break
        return True
    elif board[x][y] == empty_cell:
        board[x][y] = miss_cell
        return False
    return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="start", description="Start a new game of Battleship")
async def start(ctx):
    global player_board, computer_board, ai_last_hit, player_hits, ai_hits, ships, ai_hits_positions, game_started, player_moves, ai_moves
    player_board = create_board(); computer_board = create_board(); ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]; ai_moves = set()
    ai_last_hit = None; player_hits = 0; ai_hits = 0; ai_hits_positions = []; game_started = True; player_moves = set()
    place_ships(computer_board, computer_ships)
    await ctx.respond("Game started! Place your ships using /place_ship command.", ephemeral=True)

@bot.slash_command(name="place_ship", description="Place a ship on the board")
async def place_ship(ctx, mode: str = discord.Option(str, "Choose placement mode", choices=["manual", "random"]), start: str = None, end: str = None):
    global ships, game_started
    if not game_started:
        await ctx.respond("You need to start a game first using /start command.", ephemeral=True)
        return
    if mode == "random":
        place_ships(player_board, player_ships)
        ships = []
        embed = discord.Embed(title="All ships placed randomly", color=discord.Color.green()); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```")
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
    if not is_valid_position(player_board, start_x, start_y, length, horizontal):
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
        embed = discord.Embed(title="All ships placed", color=discord.Color.green()); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```")
        await ctx.send(embed=embed)
    else:
        await ctx.respond(f"Ship placed from {start} to {end}.\nYour board:\n```json\n{print_board(player_board)}\n```", ephemeral=True)

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
                if is_ship_sunk(positions, computer_board):
                    mark_surrounding_cells_as_miss(positions, computer_board)
                    embed = discord.Embed(title="You destroyed a ship!", color=discord.Color.red()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI board", value=f"```json\n{print_computer_board()}\n```")
                    await ctx.send(embed=embed)
                    if all_ships_destroyed(computer_ships, computer_board):
                        update_stats(player_name, "win")
                        embed = discord.Embed(title="You win!", color=discord.Color.dark_green()); embed.add_field(name="Your move", value=result); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{print_computer_board()}\n```")
                        await ctx.send(embed=embed)
                        ai_hits_positions.clear()
                        ai_moves.clear()
                        ai_hits = 0
                        player_hits = 0
                        player_ships.clear()
                        computer_ships.clear()
                        return
                else:
                    embed = discord.Embed(title="You hit a ship!", color=discord.Color.orange()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI board", value=f"```json\n{print_computer_board()}\n```")
                    await ctx.send(embed=embed)
                break
    else:
        computer_board[x][y] = miss_cell
        result = f"Miss! (Player hits: {player_hits})"
        await ctx.respond('Fire!', ephemeral=True)
        player_hits = 0
        await ai_move(ctx, result, player_name)

async def ai_move(ctx, result, player_name):
    global ai_hits_positions, ai_moves, ai_hits, player_hits
    embed = discord.Embed(title="AI is thinking...", color=discord.Color.purple())
    await ctx.send(embed=embed)
    while True:
        await asyncio.sleep(random.uniform(1, 3))
        if ai_hits_positions:
            await asyncio.sleep(random.uniform(1, 3))
            ai_x, ai_y = ai_hits_positions[-1]
            possible_moves = [(ai_x + dx, ai_y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            possible_moves = [(x, y) for x, y in possible_moves if 0 <= x < board_size and 0 <= y < board_size and player_board[x][y] not in [hit_cell, miss_cell]]
            if possible_moves:
                ai_x, ai_y = random.choice(possible_moves)
                print(f"AI move: {ai_x}, {ai_y}")
            else:
                ai_hits_positions.pop()
                print(f"AI move: {ai_x}, {ai_y}")
                continue
        else:
            ai_x, ai_y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
            print(f"AI move: {ai_x}, {ai_y}")
        if (ai_x, ai_y) not in ai_moves and player_board[ai_x][ai_y] not in [hit_cell, miss_cell]:
            ai_moves.add((ai_x, ai_y))
            if player_board[ai_x][ai_y] == ship_cell:
                player_board[ai_x][ai_y] = hit_cell
                ai_hits += 1
                ai_hits_positions.append((ai_x, ai_y))
                ai_result = f"AI hit your ship! (AI hits: {ai_hits})"
                embed = discord.Embed(title="AI hit your ship!", color=discord.Color.orange()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```")
                await ctx.send(embed=embed)
                for ship, positions in player_ships.items():
                    if (ai_x, ai_y) in positions and is_ship_sunk(positions, player_board):
                        mark_surrounding_cells_as_miss(positions, player_board)
                        embed = discord.Embed(title="AI destroyed your ship!", color=discord.Color.red()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```")
                        await ctx.send(embed=embed)
                        if all_ships_destroyed(player_board):
                            update_stats(player_name, "lose")
                            embed = discord.Embed(title="AI wins!", color=discord.Color.dark_red()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{print_computer_board()}\n```")
                            await ctx.send(embed=embed)
                            ai_moves.clear()
                            ai_hits = 0
                            player_hits = 0
                            player_ships.clear()
                            computer_ships.clear()
                            return
                        else:
                            break
                continue
            else:
                player_board[ai_x][ai_y] = miss_cell
                ai_result = f"AI missed! (AI hits: {ai_hits})"
                ai_hits = 0
                embed = discord.Embed(title="We and the enemy finish our turns", color=discord.Color.blue()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{print_computer_board()}\n```")
                await ctx.send(embed=embed)
                break
        else:
            continue

@bot.slash_command(name="stats", description="Display statistics")
async def stats(ctx):
    embed = display_stats()
    await ctx.send(embed=embed)

bot.run(TOKEN)