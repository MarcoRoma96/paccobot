# paccobot
A ranking bot for generic purposes, allowing to keep points for different cathegories or championships.
You can find my running version of this bot and test it on telegram as `@ilpaccobot`, but consider that if you uses existing championship or player's names you are playing with some groups of friends somewere else in the world! Otherwise, you can create your own using this repository and simply obtaining a new Token by `@BotFather`.
You can find a good tutorial for beginners here: <https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python>

## Token
The file the bot reads to get the Token (and maybe in the future other informations) should be named `env.json`. `example_env.json` is an example of this file, you can set there your specific bot token and remember to rename it removing `example_`.

## Functions
At the moment, nothing special. The aim of this bot is to create different championships, identified by a unique name, and assign points to players, with a tag for each addition of points that specifies the reason. Here I'm going to explain better how to use it, describing function by function.
- `/help`: lists all the possibile functions
- `/points`: is the command you should use to add points to someone for a championship, the bot will guide you to different steps where you specify the name of the championship and the player you are adding points to, the number of points and the reason. If a championship or a player name does not exist it is simply created as new one. There is no sintax control, it is key-sensitive so be careful to use always the same nickname for a player, or you will have different players. Note also that if you use an already existing bot of this type and not your own, if you use the name of a championship or a player created by another user around the world, you will play at his his own championship. At the end of th eaddition of points a summary will be printed showing recent points of that player.
- `/ranking`: prints the table of the current ranking for the specified championship. answer with the championship's name when asked by the bot.
- `/horoscope`: without any reason, as you can guess, it is used to get the horoscope of any date for any sigh. It uses a remote server. 
- `/hello` or `/start`: reply with a simple message but actually does nothing.


## Good ideas for developer contributions:
- make buttons to select existing championship or players, or explicitly create a new one
- allow to delete points (actually, it can be managed by a negative point addition)
- allow to delete players and championships
