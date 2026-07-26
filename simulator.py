# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:04:08 2026

@author: CYBORG
"""

import random
import csv
from team import Team
from group import Group
from knockout_stage import KnockoutStage
from match import Match

# ============================================================
# کلاس ۵: WorldCupSimulator (مدیریت کل جام جهانی)
# مسئولیت: هماهنگی تمام مراحل (گروه‌بندی، گروهی، حذفی، شبیه‌سازی‌های متعدد)
# ============================================================
class WorldCupSimulator:
    def __init__(self):
        """سازنده کلاس اصلی"""
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None
        self.last_bracket = []

    def load_teams_from_csv(self, filename):
        """
        خواندن تیم‌ها از فایل CSV
        filename: نام فایل CSV
        :return: True در صورت موفقیت، False در صورت خطا
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # رد کردن خط هدر
                self.teams = []
                for row in reader:
                    if len(row) >= 4:
                        name = row[0].strip()
                        attack = int(row[1].strip())
                        defense = int(row[2].strip())
                        rank = int(row[3].strip())
                        self.teams.append(Team(name, attack, defense, rank))
            print(f"✅ {len(self.teams)} teams loaded!")
            return True
        except FileNotFoundError:
            print(f"❌ File {filename} not found!")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def seed_and_draw_groups(self, silent=False):
        """
        قرعه‌کشی گروه‌ها بر اساس سیدبندی (رنکینگ فیفا)
        :param silent: اگر True باشد، پیام چاپ نمی‌شود
        :return: True در صورت موفقیت
        """
        if len(self.teams) != 32:
            print("❌ Need 32 teams!")
            return False

        # مرتب‌سازی بر اساس رنکینگ
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)

        # تقسیم به ۴ سید
        seed1 = sorted_teams[0:8]
        seed2 = sorted_teams[8:16]
        seed3 = sorted_teams[16:24]
        seed4 = sorted_teams[24:32]

        # شافل کردن هر سید
        random.shuffle(seed1)
        random.shuffle(seed2)
        random.shuffle(seed3)
        random.shuffle(seed4)

        # ساخت ۸ گروه
        group_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.groups = [Group(name) for name in group_names]

        # توزیع تیم‌ها در گروه‌ها (هر گروه یک تیم از هر سید)
        for i in range(8):
            self.groups[i].add_team(seed1[i])
            self.groups[i].add_team(seed2[i])
            self.groups[i].add_team(seed3[i])
            self.groups[i].add_team(seed4[i])

        if not silent:
            print("✅ Groups drawn!")
        return True

    def reset_all_stats(self):
        """بازنشانی آمار تمام تیم‌ها"""
        for team in self.teams:
            team.reset_stats()

    def run_group_stage(self):
        """
        اجرای کامل مرحله گروهی 
        و نمایش جدول هر گروه
        """
        if not self.groups:
            print("❌ Draw groups first!")
            return

        for group in self.groups:
            group.play_all_matches()
            group.display_table()

    def setup_knockout_bracket(self):
        """
        ساخت براکت حذفی بر اساس قانون فیفا
        A1 vs B2, C1 vs D2, E1 vs F2, G1 vs H2,
        B1 vs A2, D1 vs C2, F1 vs E2, H1 vs G2
        :return: لیستی از تاپل‌های (تیم اول، تیم دوم)
        """
        first_teams = []
        second_teams = []
        for group in self.groups:
            first, second = group.advance_teams()
            first_teams.append(first)
            second_teams.append(second)

        bracket = [
            (first_teams[0], second_teams[1]),  # A1 vs B2
            (first_teams[2], second_teams[3]),  # C1 vs D2
            (first_teams[4], second_teams[5]),  # E1 vs F2
            (first_teams[6], second_teams[7]),  # G1 vs H2
            (first_teams[1], second_teams[0]),  # B1 vs A2
            (first_teams[3], second_teams[2]),  # D1 vs C2
            (first_teams[5], second_teams[4]),  # F1 vs E2
            (first_teams[7], second_teams[6]),  # H1 vs G2
        ]
        return bracket

    def run_knockout_stage(self):
        """
        اجرای کامل مراحل حذفی (یک‌هشتم، یک‌چهارم، نیمه‌نهایی، فینال)
        :return: تیم قهرمان
        """
        if not self.groups:
            print("❌ Draw groups first!")
            return None

        # ساخت براکت
        bracket = self.setup_knockout_bracket()
        self.last_bracket = []

        # یک‌هشتم نهایی
        self.round_of_16 = KnockoutStage("Round of 16")
        for team1, team2 in bracket:
            match = Match(team1, team2, is_knockout=True)
            self.round_of_16.add_match(match)
        self.round_of_16.play_round()
        self.round_of_16.display_results()
        self.last_bracket.append(("Round of 16", self.round_of_16.matches))

        # یک‌چهارم نهایی
        winners = self.round_of_16.get_winners()
        qf_matches = []
        for i in range(0, 8, 2):
            qf_matches.append((winners[i], winners[i+1]))

        self.quarterfinals = KnockoutStage("Quarterfinals")
        for team1, team2 in qf_matches:
            match = Match(team1, team2, is_knockout=True)
            self.quarterfinals.add_match(match)
        self.quarterfinals.play_round()
        self.quarterfinals.display_results()
        self.last_bracket.append(("Quarterfinals", self.quarterfinals.matches))

        # نیمه‌نهایی
        winners = self.quarterfinals.get_winners()
        sf_matches = []
        for i in range(0, 4, 2):
            sf_matches.append((winners[i], winners[i+1]))

        self.semifinals = KnockoutStage("Semifinals")
        for team1, team2 in sf_matches:
            match = Match(team1, team2, is_knockout=True)
            self.semifinals.add_match(match)
        self.semifinals.play_round()
        self.semifinals.display_results()
        self.last_bracket.append(("Semifinals", self.semifinals.matches))

        # فینال
        winners = self.semifinals.get_winners()
        final_matches = [(winners[0], winners[1])]

        self.final = KnockoutStage("Final")
        for team1, team2 in final_matches:
            match = Match(team1, team2, is_knockout=True)
            self.final.add_match(match)
        self.final.play_round()
        self.final.display_results()
        self.last_bracket.append(("Final", self.final.matches))

        # قهرمان
        final_winners = self.final.get_winners()
        if final_winners:
            self.champion = final_winners[0]
            print(f"\n🏆 CHAMPION: {self.champion.name} 🏆")

        return self.champion

    def run_full_simulation(self):
        """
        اجرای کامل جام جهانی (مرحله گروهی + حذفی)
        :return: تیم قهرمان
        """
        self.reset_all_stats()
        if not self.groups:
            self.seed_and_draw_groups()
        self.run_group_stage()
        champion = self.run_knockout_stage()
        return champion

    def most_likely_champion(self, num_simulations=1000):
        """
        شبیه‌سازی چندباره (پیش‌فرض ۱۰۰۰ بار) و محاسبه درصد قهرمانی هر تیم
         num_simulations: تعداد شبیه‌سازی‌ها
        """
        if num_simulations <= 0:
            print("❌ Number must be > 0!")
            return

        counts = {}
        print(f"\n🔄 Simulating {num_simulations} times...")

        for i in range(num_simulations):
            if (i + 1) % 100 == 0:
                print(f"  {i+1} of {num_simulations} done...")

            self.reset_all_stats()
            self.seed_and_draw_groups(silent=True)  # <--- تغییر: بی‌صدا

            # مرحله گروهی
            for group in self.groups:
                group.play_all_matches()

            # مرحله حذفی (بی‌صدا)
            bracket = self.setup_knockout_bracket()

            self.round_of_16 = KnockoutStage("Round of 16")
            for team1, team2 in bracket:
                match = Match(team1, team2, is_knockout=True)
                self.round_of_16.add_match(match)
            self.round_of_16.play_round()

# یک چهارم
            winners = self.round_of_16.get_winners()
            qf_matches = []
            for j in range(0, 8, 2):
                qf_matches.append((winners[j], winners[j+1]))

            self.quarterfinals = KnockoutStage("Quarterfinals")
            for team1, team2 in qf_matches:
                match = Match(team1, team2, is_knockout=True)
                self.quarterfinals.add_match(match)
            self.quarterfinals.play_round()
            
  # نیم نهایی
            winners = self.quarterfinals.get_winners()
            sf_matches = []
            for j in range(0, 4, 2):
                sf_matches.append((winners[j], winners[j+1]))

            self.semifinals = KnockoutStage("Semifinals")
            for team1, team2 in sf_matches:
                match = Match(team1, team2, is_knockout=True)
                self.semifinals.add_match(match)
            self.semifinals.play_round()

# فینال
            winners = self.semifinals.get_winners()
            final_matches = [(winners[0], winners[1])]

            self.final = KnockoutStage("Final")
            for team1, team2 in final_matches:
                match = Match(team1, team2, is_knockout=True)
                self.final.add_match(match)
            self.final.play_round()

            final_winners = self.final.get_winners()
            if final_winners:
                self.champion = final_winners[0]

            if self.champion:
                counts[self.champion.name] = counts.get(self.champion.name, 0) + 1

        print("\n" + "="*50)
        print("📊 Championship Percentages:")
        print("="*50)
        sorted_res = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for name, wins in sorted_res:
            percent = (wins / num_simulations) * 100
            print(f"{name:<20} : {percent:.1f}% ({wins} wins)")
        print("="*50)

    def display_bracket(self):
        """نمایش براکت حذفی آخرین شبیه‌سازی انجام شده"""
        if not self.last_bracket:
            print("❌ No matches yet!")
            return

        print("\n" + "="*50)
        print("🏆 Knockout Bracket")
        print("="*50)

        for round_name, matches in self.last_bracket:
            print(f"\n===== {round_name} =====")
            for match in matches:
                pen = ""
                if match.goals1 == match.goals2:
                    pen = " (Penalty)"
                print(f"{match.team1.name} {match.goals1} - {match.goals2} {match.team2.name}{pen} -> {match.winner.name}")

        if self.champion:
            print(f"\n🏆 Champion: {self.champion.name}")
