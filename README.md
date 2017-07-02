# teambalancer

This is a quick and dirty hack in the form of a Discord bot for
balancing scrim teams in Overwatch.

## How to Use - Standalone Code

You will need Python 3.

Edit players.txt with BattleNet IDs, e.g., `ASnackyBeard#1234`,
one per line.

Run `python balance.py` and enter number of teams desired. The program will generate the requested number of balanced teams.

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
  
  


## TODOs

- Weight teams by role
