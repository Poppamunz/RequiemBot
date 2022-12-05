# RequiemBot
This is a Discord bot for rolling dice (such as in tabletop RPGs) and optionally doing math on the results. Written in Python using [discord.py](https://discordpy.readthedocs.io/en/stable/).

## Usage
### Invite to your server:
I am currently testing the bot with a small group of people, and will make an invite link publicly available when I've received enough feedback.
### Run locally:
(Requires Python ≥ 3.10. The `GUILD_MEMBERS` privileged intent is required for `/stats` to work properly.)
1. Install from PyPI using `pip install requiembot`
2. Set environment variable `TOKEN` to your Discord bot token
3. Run `python -m requiembot`

## Details
### Commands
- `/help`: Display a simple help message with examples and a link to this GitHub repo.
- `/roll`: Roll dice and/or do math, as described below. Options include:
  - `secret`: If set to "true", the result of your roll will only be visible to you.
  - `repeat`: Amount of times to roll the given input. Defaults to 1.
- `/stats`: Display the number of Discord servers the bot is on, and the number of non-bot members across those servers.
### Example Dice Rolls
- d20 ability check: `1d20 + 3` or simply `d20+3`
- D&D 5E attribute: `4d6k3` or `4d6d1` (or simply `4d6d`)
- Advantage: `2d20k1`
- Disadvantage: `2d20kl1`
- Fudge/Fate: `4df`
- Wild Die (Savage Worlds or Open D6): `1d6!`
### Details
- Dice are expressed in the form `XdY` where X and Y are positive integers representing die count and size.
  - X is optional; if it is not present, the default is 1
  - Y can instead be `f` to use Fudge/FATE dice which range from -1 to 1
- Dice can be followed by modifiers. These consist of a one- or two- character symbol, and optionally a positive integer X as described below (otherwise using the default listed):
  - `dX`: Drop the lowest X dice. (Defaults to 1.)
  - `dhX`: Drop the highest X dice. (Defaults to 1.)
  - `kX`: Keep the highest X dice, and drop the rest. (Defaults to 1.)
  - `klX`: Keep the lowest X dice, and drop the rest. (Defaults to 1.)
  - `!X`: "Exploding" dice; for every dice resulting in X or above, add another die of the same type, and repeat for every added die resulting in X or above. (Defaults to the highest possible value on the die.)
    - (To avoid infinite loops, this is capped at 10 repeats.)
- The following math features are supported:
  - addition `+`, subtraction `-`
  - multiplication `*`, division `/`
    - Note: The bot uses integer division. Results are rounded down and remainders are disregarded.
  - `(` grouping `)`
- Whitespace (spaces etc.) is completely ignored between symbols. For example, `(5d6kl3!k3dh1+2)*5` and `( 5 d 6 kl 3 ! k 3 dh 1 +  2)  *  5` will be interpreted as exactly the same.

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