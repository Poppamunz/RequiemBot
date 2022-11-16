# Setup script used for Pip and PyPI.
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

from setuptools import setup, find_packages
from requiembot import __version__

setup(name="RequiemBot",
      version=__version__,
      description="A simple TTRPG dice bot for Discord",
      author="Michael Munzer",
      packages=find_packages(),
      requires=["discord.py", "python_dotenv"],
      classifiers=[
          "Private :: Do Not Upload",
          "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
          "Operating System :: OS Independent"
      ])
