# Converts input expression strings into a list of tokens.
# Copyright (C) 2022 Michael Munzer
# This file is part of RequiemBot.
#
# RequiemBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# RequiemBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
from enum import Enum, auto


# define token types
class Token(Enum):
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    SLASH = auto()
    POWER = auto()
    DICE = auto()
    KEEP_HIGHEST = auto()
    KEEP_LOWEST = auto()
    EXPLODE = auto()  # dice modifiers such as k, kl, !, etc
    LPAREN = auto()
    RPAREN = auto()
    FUDGE = auto()
    EOS = auto()


exprs = [
    (r"\s+", None),
    (r"(?i)kl", Token.KEEP_LOWEST),
    (r"(?i)k", Token.KEEP_HIGHEST),
    (r"!", Token.EXPLODE),
    (r"(?i)f", Token.FUDGE),
    (r"(?i)d", Token.DICE),
    (r"\(", Token.LPAREN),
    (r"\)", Token.RPAREN),
    (r"\d+", Token.INTEGER),
    (r"\^", Token.POWER),
    (r"\+", Token.PLUS),
    (r"-", Token.MINUS),
    (r"\*", Token.TIMES),
    (r"/", Token.SLASH)
]


def tokenize(str):
    pos = 0
    tokens = []
    while pos < len(str):
        for exp, token in exprs:
            match = re.match(exp, str[pos:])
            if match:
                pos += match.end()

                if token is not None:
                    tokens.append((token, match.group()))
                break
        if match is None:
            raise ValueError(f"Invalid character `{str[pos]}`")
    tokens.append((Token.EOS, "end of string"))
    return tokens


if __name__ == "__main__":
    tokens = tokenize(input("Expression to lex: "))
    for i, j in tokens:
        print(f"{i} {j}")
