import discord, json, os

class Stats:
    def __init__(self):
        pass
    
    def load_stats(self):
        stats_file = 'stats.json'
        if not os.path.exists(stats_file) or os.path.getsize(stats_file) == 0:
            return {}
        with open(stats_file, 'r') as file:
            return json.load(file)

    def update_stats(self, player_name, result):
        stats = self.load_stats()
        if player_name not in stats:
            stats[player_name] = {'wins': 0, 'losses': 0}
        stats[player_name][result] += 1
        with open('stats.json', 'w') as file:
            json.dump(stats, file)

    def save_stats(self, stats):
        with open("stats.json", "w") as file:
            json.dump(stats, file, indent=4)   
    
    def display_stats(self):
        stats = self.load_stats(); embed = discord.Embed(title="Player Statistics", color=discord.Color.blue())
        for player, data in stats.items():
            player_rank = "🥇" if data["wins"] > data["losses"] else "🥈" if data["wins"] < data["losses"] else "🥉"
            win_ratio = data["wins"] / (data["wins"] + data["losses"]) if (data["wins"] + data["losses"]) > 0 else 0
            embed.add_field(name=player, value=f"Rank: {player_rank}, Wins: {data['wins']}, Losses: {data['losses']}, Win Ratio: {win_ratio:.2f}", inline=False)
        return embed