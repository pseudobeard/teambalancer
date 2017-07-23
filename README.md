# teambalancer

This is a quick and dirty hack in the form of a Discord bot for
balancing scrim teams in Overwatch.

## Initial Setup (Windows)

Edit SETUP.bat (Right click -> Edit) to provide the correct path to python pip - This is usually located in `C:\Users\USER\AppData\Local\Programs\Python36\Scripts` or `C:\Python34\Scripts`. Ensure this directory contains pip.exe.

The bat file should look like the following:
`C:\Users\USER\AppData\Local\Programs\Python36\Scripts\pip install -r requirements.txt`

Save changes and close SETUP.bat.

Run SETUP.bat and leave to install required modules.

## How to Use - Standalone Code

You will need Python 3.

Edit players.txt with BattleNet IDs, e.g., `ASnackyBeard#1234`,
one per line.

Run `python balance.py`. When prompted, enter number of teams to generate.

A prompt will be displayed to import from Stream Elements. Either enter "y" to import players from Stream Elements, or "n" to import from players.txt

Players will be imported from the selected location.

A prompt will be displayed to add aditional players who have not been loaded yet - enter battletags or type continue to finish and balance teams

Balanced teams and a random map will be generated and displayed.

A prompt will be displayed to auto-invite players to a custom game (Windows only). Type "y" to perform this functionality. You should have Overwatch open and a custom game lobby ready. After typing "y" then enter when prompted, you will have 10 seconds to tab into Overwatch until auto-invite will start. Do not touch the keyboard or mouse until completed.

## How to Use - Discord Bot

You will need Python 3.5 or greater.

Run `python scrimbot.py` and allow the bot to startup. Use the folling commands in discord:

  `listplayers {all}` - List active players. Add "all" argument to include inactive players.
  
  `update {players}` - Update players stats. For example `update ASnackyBeard#1234 ExamplePlayer#9876`
  
  `activate {players}` - Set listed players as active. For example `activate ASnackyBeard#1234 ExamplePlayer#9876`
  
  `retire {players}` - Set listed players as inactive. For example `retire ASnackyBeard#1234 ExamplePlayer#9876`
  
  `retireall` - Retire all active players (set all players as inactive)
  
  `playerstats {player}` - Show stats for specified player
  
  `updatesr {player} {new SR}` - Manually update SR for specified player. For example `updatesr ASnackyBeard#1234 3000`
  
  `autobalance {weight}`- Generate two balanced teams from active players. For example `autobalance flat`
  
  `tourney {weight}` - Generate balanced teams of 6 from active players. For example `tourney curve`
  
  `randomMap {--no2CP}` - Generate a random map. Using `--no2CP` will prevent a 2CP map being picked.
  
  


## TODOs

- Weight teams by role
