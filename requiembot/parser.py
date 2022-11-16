# Parser for tokenized expressions.
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

from . import lexer
from .exprs import *
from .lexer import Token


class ParseError(Exception):
    pass


def parse(expr: str) -> Expr:
    """
    Parses a dice expression, based on the following context-free grammar:

    exp →       term;
    term →      factor (("+" | "-") factor)*;
    factor →    dice (("*" | "/") dice)*;
    dice →      primary ("d" ("f"|primary) dicemod*)?;
    dicemod →   ("kl"|"k"|"!") primary?;
    primary →   ("-"? INTEGER) | "(" exp ")";
    """
    tokens = lexer.tokenize(expr)
    current = 0

    def error(msg: str):
        return ParseError(msg + f" before `{tokens[current][1]}`")

    def peek():
        return tokens[current]

    def previous():
        return tokens[current - 1]

    def advance():
        nonlocal current
        current += 1
        return previous()

    def check(type: Token):
        return peek()[0] == type

    def match(*args: Token):
        for i in args:
            if check(i):
                advance()
                return True
        return False

    def expression() -> Expr:
        return term()

    def term() -> Expr:
        expr = factor()
        while match(Token.TIMES, Token.SLASH):
            op = previous()
            right = factor()
            expr = BinaryExpr(expr, op[1], right)
        return expr

    def factor() -> Expr:
        expr = dice()
        while match(Token.MINUS, Token.PLUS):
            op = previous()
            right = dice()
            expr = BinaryExpr(expr, op[1], right)
        return expr

    def dice() -> Expr:
        if check(Token.DICE):
            count = IntegerExpr(1)
        else:
            count = primary()

        if match(Token.FUDGE):
            raise error("Unexpected `f`")

        if match(Token.DICE):
            if not isinstance(count, IntegerExpr) or count.value < 1:
                raise ParseError("Positive integer expected before `d`")

            if match(Token.FUDGE):
                size = 0
            elif match(Token.INTEGER):
                size = int(previous()[1])
            else:
                raise ParseError("Positive integer or `f` expected after `d`")

            mods = []

            while match(Token.KEEP_HIGHEST, Token.KEEP_LOWEST, Token.EXPLODE):
                if check(Token.INTEGER):
                    mods.append((previous()[1], int(peek()[1])))
                    advance()
                else:
                    mods.append((previous()[1], None))

            return DiceExpr(count.value, size, mods)

        return count

    def primary() -> Expr:
        if match(Token.MINUS):
            if match(Token.INTEGER):
                return IntegerExpr(-int(previous()[1]))

        if match(Token.INTEGER):
            return IntegerExpr(int(previous()[1]))

        if match(Token.LPAREN):
            expr = expression()
            if not match(Token.RPAREN):
                raise error("`)` expected")
            return GroupingExpr(expr)

        raise error("Integer or parentheses expected")

    return expression()


if __name__ == "__main__":
    while True:
        val, stri = parse(input("Expression to parse: ")).evaluate()
        print(f"{stri} = {val}")
