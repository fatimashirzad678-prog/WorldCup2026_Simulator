# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:55:44 2026

@author: CYBORG
"""

from team import Team


# ============================================================
# کلاس ۲: Match (نماینده یک مسابقه)
# مسئولیت: نگهداری اطلاعات دو تیم و اجرای مسابقه
# ============================================================
class Match:
    def __init__(self, team1, team2, is_knockout=False):
        """
        سازنده کلاس Match
         team1: تیم اول
         team2: تیم دوم
         is_knockout: True اگر بازی حذفی است
        """
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.is_knockout = is_knockout
        self.winner = None

    def play(self):
        """
        اجرای مسابقه با فراخوانی simulate_match از تیم اول
        :return: (گل تیم اول، گل تیم دوم، تیم برنده)
        """
        self.goals1, self.goals2, self.winner = self.team1.simulate_match(
            self.team2, self.is_knockout
        )
        return self.goals1, self.goals2, self.winner

