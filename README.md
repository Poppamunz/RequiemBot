# RequiemBot
This is a Discord bot for rolling dice (such as in tabletop RPGs) and optionally doing math on the results. Written in Python using [discord.py](https://discordpy.readthedocs.io/en/stable/).

## Usage
### Invite to your server:
I am currently testing the bot with a small group of people, and will make an invite link publicly available when I've received enough feedback.
### Run locally:
(Requires Python ≥ 3.10)
1. Install from PyPI using `pip install requiembot`
2. Set environment variable `TOKEN` to your Discord bot token
3. Run `python -m requiembot`

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

## Planned Additions
(in no particular order)
- Optional "compact" rolls shortened to one line
- Count successes/failures, like World of Darkness
- Reroll on nat 1 (or some other number)
- Highest/lowest of multiple different expressions
- Proper code comments/documentation

## Copyright Notice
Copyright (C) 2022 Michael Munzer

RequiemBot is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

RequiemBot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.