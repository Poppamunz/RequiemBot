# RequiemBot
This is a Discord bot for rolling dice (such as in tabletop RPGs) and optionally doing math on the results. Written in Python using [discord.py](https://discordpy.readthedocs.io/en/stable/).

## Usage
### Invite to your server:
Once I've found somewhere to host RequiemBot, a link to invite it to your Discord server will be here.
### Run locally:
1. Clone this repository using Git, and cd into the resulting directory
2. Create a copy of `.env-example` and rename it to `.env`
3. In `.env`, replace `[YOUR TOKEN HERE]` with your Discord bot token
4. Run `pip install -e .` which will install this project as a PyPI package
5. Run `python -m requiembot`

## Features
### Commands
- `/help`: Display a simple help message with examples and a link to the GitHub repo.
- `/roll`: Roll dice and/or do math. Options include:
  - `secret`: If set to "true", the result of your roll will only be visible to you.
  - `repeat`: Amount of times to roll the given input. Defaults to 1.
### Dice and Math Examples
- `1d20`, `4d5`, `100d2` You can roll practically any amount of dice with any number of sides
- `(2d20 + 3) - 5 * 4 / 2` Basic math operations and parentheses (follows order of operations)
- `4dF` Fudge/FATE dice (whose results range from -1 to 1)
- Roll modifiers:
  - `4d6k3` Roll four six-sided dice and keep the highest three, like a 5E stat.
  - `2d20kl1` Roll two twenty-sided dice and keep the lowest.
  - (If no number is specified after `k` or `kl`, the default is 1.)
  - `2d6!5` If any dice roll 5 or higher, then roll an additional die and add to the total for each one, aka "exploding." Useful for Savage Worlds or Open D6.
  - (If no number is specified after `!`, the default is the highest possible value on the die.)