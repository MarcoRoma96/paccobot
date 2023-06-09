import requests
import json
import os
import datetime
import pandas as pd


path_to_score = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'score.json')

def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.

    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()


def get_scores(path):
    if os.path.isfile(path):
        with open(path) as scorefile:
            score_dict = json.load(scorefile)
        return pd.DataFrame(score_dict)
        #print(score_df)
    else:
        return pd.DataFrame()


def error_answer(bot, message):
    text = "You donkey, fucking idiot, whats wrong with you?? What the hell are you trying to do??"
    bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    

def get_championship(championship: str, bot, message) -> dict:
    """Get ranking of the specified championship.

    Keyword arguments:
    ------------------

    championship: str - Championship identifier
    """
    score_df = get_scores(path_to_score)
    print(score_df)
    score_df = score_df.loc[score_df["championship"] == championship]

    if len(score_df) == 0:
        error_answer(bot, message)
    pivoted  = score_df.pivot_table(index = ['player'],
                                    values=['points'],
                                    aggfunc=sum,
                                    fill_value=0,
                                    )
    pivoted = pivoted.sort_values(by='points', ascending=False).reset_index()
    pivoted.index = list(range(1, len(pivoted) + 1))
    print(pivoted)
    return pivoted


def push_championship(championship:str, player:str, points:int, reason:str = '') -> dict:
    """Add points to the specified player for a championship.

    Keyword arguments:
    ------------------

    - championship: str    - the championship the player joins
    - player: str          - the name of the player
    - points: int          - how many points to add to the score
    - reason: str          - a possible motivation of this points
    - Return: dict         - JSON data
    """

    new_record = pd.DataFrame({
                    "championship"  : [championship],
                    "player"        : [player],
                    "points"        : [points],
                    "reason"        : [reason],
                    "time"          : [datetime.datetime.now().strftime("%d-%m-%Y, %H:%M")]
                })

    score_df = get_scores(path_to_score)
    print(score_df)
    score_df = pd.concat([score_df, new_record]).reset_index(drop=True)
    score_df.to_json(path_to_score, indent=4)

    score_df = score_df.loc[score_df["championship"] == championship]
    
    return score_df