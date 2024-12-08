## Battleship Bot

### Project Description

This project is a **Battleship game bot** implementation where the bot plays against a user. The bot makes moves, detects hits and misses, and keeps track of the game board's state.

### Key Features

1. **AI Moves**:  
   - The bot analyzes the game board and makes strategic moves to find and sink ships.
   - After a hit, the bot continues targeting adjacent cells until the ship is destroyed.

2. **Game Status Updates**:  
   - Displays the results of each move (hit, miss, or ship destroyed).
   - Checks for victory conditions and ends the game accordingly.

3. **Statisctics**:  
   - Bot records player wins and loses to .json file, from which it can be shown to the player with command

### Requirements

- **Python 3.x**
- **discord.py** and **pycord** library's for Discord bot interaction.