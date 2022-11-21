# Expression classes for the parser's use.
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

from dataclasses import dataclass
from random import randint
from typing import Protocol


class Expr(Protocol):
    def evaluate(self) -> tuple[int, str]:
        ...


class IntegerExpr:
    def __init__(self, value: int):
        self.value = value

    def evaluate(self):
        return self.value, str(self.value)


class BinaryExpr:
    def __init__(self, left: Expr, op: str, right: Expr):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.op == "+":
            value = left_val[0] + right_val[0]
        elif self.op == "-":
            value = left_val[0] - right_val[0]
        elif self.op == "*":
            value = left_val[0] * right_val[0]
        elif self.op == "/":
            value = left_val[0] // right_val[0]

        return value, f"{left_val[1]} {self.op} {right_val[1]}"


class GroupingExpr:
    def __init__(self, expr: Expr):
        self.expr = expr

    def evaluate(self):
        val, string = self.expr.evaluate()
        return val, f"({string})"


@dataclass(order=True)
class Die:
    value: int
    dropped: bool

    def __init__(self, val: int, exploded=False) -> None:
        self.value = val
        self.dropped = False
        self.exploded = exploded

    def __str__(self):
        output = str(self.value)
        if self.exploded:
            output = "*" + output + "*"
        if self.dropped:
            output = "~~" + output + "~~"
        return output


class DiceExpr:
    def __init__(self, count: int, size: int, mods: list[tuple[str, int]]):
        self.count = count
        self.size = size
        self.mods = mods
        self.dice = []

    def evaluate(self):
        self.dice = []

        for i in range(self.count):
            self.dice.append(self.roll())
        for i in self.mods:
            if i[0] == "k":
                self.keep(i[1])
            elif i[0] == "kl":
                self.keep(i[1], False)
            elif i[0] == "!":
                self.explode(i[1])

        return sum(die.value for die in self.dice if not die.dropped), "[" + ", ".join(str(die) for die in self.dice) + "]"

    def keep(self, count, highest=True):
        if count is None:
            count = 1
        if count >= sum((not die.dropped) for die in self.dice):
            return
        for i in range(len(list(die for die in self.dice if not die.dropped)) - count):
            if highest:
                min(d for d in self.dice if not d.dropped).dropped = True
            else:
                max(d for d in self.dice if not d.dropped).dropped = True

    def explode(self, min):
        if min is None:
            min = self.size if self.size > 0 else 1

        i = 0
        counter = 10
        while i < len(self.dice):
            if self.dice[i].dropped:
                i += 1
                continue
            if not self.dice[i].exploded:
                counter = 10
            if self.dice[i].value >= min and counter > 0:
                self.dice.insert(i + 1, self.roll())
                self.dice[i + 1].exploded = True
                counter -= 1
            i += 1

    def roll(self) -> int:
        if self.size == 0:
            return Die(randint(-1, 1))
        else:
            return Die(randint(1, self.size))
