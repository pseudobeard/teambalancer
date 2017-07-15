import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "overwatch_team_balancer_and_discord_bot",
    version = "0.1.0",
    author = "KarQ Community",
    author_email = "",
    description = ("A team balancer and bot."),
    license = "",
    keywords = "",
    url = "",
    packages=['requests', 'pyscreenshot', 'pytesseract'],
    long_description="A team balancer and bot.",
    classifiers=[ ],
)