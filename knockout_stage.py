# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:00:52 2026

@author: CYBORG
"""

from match import Match

# ============================================================
# کلاس ۴: KnockoutStage (نماینده یک دور حذفی)
# مسئولیت: مدیریت مسابقات یک دور حذفی (مثلاً یک‌هشتم نهایی)
# ============================================================
class KnockoutStage:
    def __init__(self, round_name):
        """
        سازنده کلاس KnockoutStage
        :param round_name: نام مرحله (Round of 16, Quarterfinals, ...)
        """
        self.round_name = round_name
        self.matches = []

    def add_match(self, match):
        """اضافه کردن یک مسابقه به این دور"""
        self.matches.append(match)

    def play_round(self):
        """اجرای تمام مسابقات این دور و برگرداندن نتایج"""
        results = []
        for match in self.matches:
            g1, g2, winner = match.play()
            results.append((match.team1, match.team2, g1, g2, winner))
        return results

    def get_winners(self):
        """برگرداندن لیست تیم‌های برنده این دور"""
        winners = []
        for match in self.matches:
            if match.winner:
                winners.append(match.winner)
        return winners

    def display_results(self):
        """چاپ نتایج مسابقات این دور در کنسول"""
        print(f"\n===== {self.round_name} =====")
        for match in self.matches:
            pen = ""
            if match.goals1 == match.goals2:
                pen = " (Penalty)"
            print(f"{match.team1.name} {match.goals1} - {match.goals2} {match.team2.name}{pen} -> {match.winner.name}")

