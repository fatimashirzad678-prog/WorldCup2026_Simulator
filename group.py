# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:57:48 2026

@author: CYBORG
"""


import random
from match import Match

# ============================================================
# کلاس ۳: Group (نماینده یک گروه)
# مسئولیت: مدیریت تیم‌های گروه، اجرای بازی‌ها، رتبه‌بندی
# ============================================================
class Group:
    def __init__(self, name):
        """
        سازنده کلاس Group
        :param name: نام گروه (A, B, C, ...)
        """
        self.name = name
        self.teams = []

    def add_team(self, team):
        """اضافه کردن یک تیم به گروه"""
        self.teams.append(team)
        team.group = self.name

    def play_all_matches(self):
        """اجرای تمام مسابقات گروه (هر تیم یک بار با بقیه)"""
        for i in range(4):
            for j in range(i + 1, 4):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()

    def get_ranking(self):
        """
        رتبه‌بندی تیم‌های گروه بر اساس:
        ۱- امتیاز بیشتر
        ۲- تفاضل گل بیشتر
        ۳- گل زده بیشتر
        ۴- قرعه‌کشی در صورت تساوی کامل
        :return: لیست رتبه‌بندی شده تیم‌ها
        """
        # مرتب‌سازی اولیه
        sorted_teams = sorted(self.teams,
                             key=lambda t: (t.points, t.goal_difference(), t.goals_for),
                             reverse=True)

        # مدیریت تساوی کامل (قرعه‌کشی)
        final = []
        i = 0
        while i < len(sorted_teams):
            same = [sorted_teams[i]]
            j = i + 1
            while j < len(sorted_teams):
                if (sorted_teams[i].points == sorted_teams[j].points and
                    sorted_teams[i].goal_difference() == sorted_teams[j].goal_difference() and
                    sorted_teams[i].goals_for == sorted_teams[j].goals_for):
                    same.append(sorted_teams[j])
                    j += 1
                else:
                    break

            if len(same) > 1:
                random.shuffle(same)

            final.extend(same)
            i = j

        return final

    def advance_teams(self):
        """برگرداندن دو تیم اول گروه برای صعود به مرحله حذفی"""
        ranking = self.get_ranking()
        return ranking[0], ranking[1]

    def display_table(self):
        """نمایش جدول گروه در خروجی کنسول"""
        print(f"\n===== Group {self.name} =====")
        print(f"{'Team':<20} {'Pts':<5} {'GD':<5} {'GF':<5} {'GA':<5}")
        print("-" * 45)
        ranking = self.get_ranking()
        for team in ranking:
            print(f"{team.name:<20} {team.points:<5} {team.goal_difference():<5} {team.goals_for:<5} {team.goals_against:<5}")


