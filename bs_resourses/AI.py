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

import discord, random, asyncio, json

class AI:
    def __init__(self, board_size, empty_cell, ship_cell, hit_cell, miss_cell, player_board, ships, player_ships, computer_ships):
        self.board_size = board_size; self.ships = ships; self.player_ships = player_ships; self.computer_ships = computer_ships
        self.hit_cell = hit_cell; self.miss_cell = miss_cell; self.ship_cell = ship_cell; self.empty_cell = empty_cell
        self.player_board = player_board; self.ai_hits_positions = []; self.ai_moves = set(); self.ai_hits = 0
    
    def is_valid_position(self, board, x, y, length, horizontal):
        def is_within_bounds(nx, ny):
            return 0 <= nx < self.board_size and 0 <= ny < self.board_size

        def is_surrounding_cells_empty(nx, ny):
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                adj_x, adj_y = nx + dx, ny + dy
                if is_within_bounds(adj_x, adj_y) and board[adj_x][adj_y] == self.ship_cell:
                    return False
            return True

        for i in range(length):
            nx, ny = (x, y + i) if horizontal else (x + i, y)
            if not is_within_bounds(nx, ny) or board[nx][ny] != self.empty_cell or not is_surrounding_cells_empty(nx, ny):
                return False
        return True

    def place_ships(self, board, ships_dict):
        def place_ship(x, y, length, horizontal):
            ship_positions = []
            for i in range(length):
                nx, ny = (x, y + i) if horizontal else (x + i, y)
                board[nx][ny] = self.ship_cell
                ship_positions.append((nx, ny))
            return ship_positions

        for index, length in enumerate(self.ships):
            placed = False
            while not placed:
                x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
                horizontal = random.choice([True, False])
                if self.is_valid_position(board, x, y, length, horizontal):
                    ships_dict[f"{length}_{index}"] = place_ship(x, y, length, horizontal)
                    placed = True
                    print(f'All ships positioned: {ships_dict}')
    
    def print_board(self, board):
        header = "  " + " ".join([str(i + 1) for i in range(self.board_size)])
        rows = []
        for i, row in enumerate(board):
            rows.append(chr(65 + i) + " " + " ".join(row))
        return header + "\n" + "\n" + "\n".join(rows)

    def print_computer_board(self, computer_board):
        display_board = [[self.empty_cell for _ in range(self.board_size)] for _ in range(self.board_size)]
        for x in range(self.board_size):
            for y in range(self.board_size):
                if computer_board[x][y] in [self.hit_cell, self.miss_cell]:
                    display_board[x][y] = computer_board[x][y]
        header = "  " + " ".join([str(i + 1) for i in range(self.board_size)])
        rows = []
        for i, row in enumerate(display_board):
            rows.append(chr(65 + i) + " " + " ".join(row))
        return header + "\n" + "\n" + "\n".join(rows)

    def all_ships_destroyed(self, ships, board):
        for positions in ships.values():
            if not self.is_ship_sunk(positions, board):
                return False
        return True

    def is_ship_sunk(self, ship_positions, board):
        return all(board[x][y] == self.hit_cell for x, y in ship_positions)

    def mark_surrounding_cells_as_miss(self, ship_positions, board):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for x, y in ship_positions:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and board[nx][ny] == self.empty_cell:
                    board[nx][ny] = self.miss_cell

    async def ai_move(self, ctx, result, player_name, player_board, player_ships, board_size, hit_cell, miss_cell, ship_cell, empty_cell, computer_ships, computer_board):
        embed = discord.Embed(title="AI is thinking...", color=discord.Color.purple())
        await ctx.send(embed=embed)
        while True:
            await asyncio.sleep(random.uniform(1, 3))
            if self.ai_hits_positions:
                await asyncio.sleep(random.uniform(1, 3))
                ai_x, ai_y = self.ai_hits_positions[-1]
                possible_moves = [(ai_x + dx, ai_y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                possible_moves = [(x, y) for x, y in possible_moves if 0 <= x < board_size and 0 <= y < board_size and player_board[x][y] not in [hit_cell, miss_cell] and (x, y) not in self.ai_moves]
                if possible_moves:
                    ai_x, ai_y = random.choice(possible_moves)
                    print(f"AI move: {ai_x}, {ai_y}")
                else:
                    self.ai_hits_positions.pop()
                    print(f"AI move: {ai_x}, {ai_y}")
                    continue
            else:
                ai_x, ai_y = random.randint(0, board_size - 1), random.randint(0, board_size - 1)
                print(f"AI move: {ai_x}, {ai_y}")
            if (ai_x, ai_y) not in self.ai_moves and player_board[ai_x][ai_y] not in [hit_cell, miss_cell]:
                self.ai_moves.add((ai_x, ai_y))
                if player_board[ai_x][ai_y] == ship_cell:
                    player_board[ai_x][ai_y] = hit_cell
                    self.ai_hits += 1
                    self.ai_hits_positions.append((ai_x, ai_y))
                    ai_result = f"AI hit your ship! (AI hits: {self.ai_hits})"
                    embed = discord.Embed(title="AI hit your ship!", color=discord.Color.orange()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{self.print_board(player_board)}\n```")
                    await ctx.send(embed=embed)
                    for ship, positions in player_ships.items():
                        if (ai_x, ai_y) in positions and self.is_ship_sunk(positions, player_board):
                            self.mark_surrounding_cells_as_miss(positions, player_board)
                            embed = discord.Embed(title="AI destroyed your ship!", color=discord.Color.red()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{self.print_board(player_board)}\n```")
                            await ctx.send(embed=embed)
                            if self.all_ships_destroyed(player_ships, player_board):
                                self.update_stats(player_name, "lose")
                                embed = discord.Embed(title="AI wins!", color=discord.Color.dark_red()); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{self.print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{self.print_computer_board()}\n```")
                                await ctx.send(embed=embed)
                                self.ai_moves.clear(); self.ai_hits = 0; self.player_hits = 0
                                player_ships.clear(); computer_ships.clear()
                                return
                            else:
                                break
                    continue
                else:
                    player_board[ai_x][ai_y] = miss_cell
                    ai_result = f"AI missed! (AI hits: {self.ai_hits})"
                    self.ai_hits = 0
                    embed = discord.Embed(title="We and the enemy finish our turns", color=discord.Color.blue()); embed.add_field(name="Your move", value=result); embed.add_field(name="AI move", value=ai_result); embed.add_field(name="Your board", value=f"```json\n{self.print_board(player_board)}\n```"); embed.add_field(name="AI board", value=f"```json\n{self.print_computer_board(computer_board)}\n```")
                    await ctx.send(embed=embed)
                    break
            else:
                continue

    def update_stats(self, player, result):
        stats = self.load_stats()
        if player not in stats:
            stats[player] = {"wins": 0, "losses": 0}
        stats[player][result + "s"] += 1
        self.save_stats(stats)

    def load_stats(self):
        try:
            with open("stats.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_stats(self, stats):
        with open("stats.json", "w") as file:
            json.dump(stats, file, indent=4)   
        

        