# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 17:48:45 2026

@author: CYBORG
"""
# ============================================================
# کلاس ۱: Team (نماینده یک تیم ملی)
# مسئولیت: ذخیره اطلاعات تیم، آمار مسابقات، شبیه‌سازی یک بازی
# ============================================================

import math
import random


class Team:
    def __init__(self, name, attack, defense, rank):
        """
        سازنده کلاس Team
         name: نام تیم 
        attack: قدرت حمله 
        defense: قدرت دفاع 
        rank: رتبه فیفا
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None

    def goal_difference(self):
        """محاسبه تفاضل گل (گل زده منهای گل خورده)"""
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """بازنشانی آمار تیم (برای شروع دوباره شبیه‌سازی)"""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def poisson_random(self, lam):
        """
        تولید یک عدد تصادفی با توزیع پواسون به روش تجمعی 
         lam: میانگین گل مورد انتظار
        :return: تعداد گل (عدد صحیح)
        """
        if lam <= 0:
            return 0
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        return k - 1

    def simulate_match(self, opponent, is_knockout=False):
        """
        شبیه‌سازی یک مسابقه کامل بین دو تیم (۹۰ دقیقه + وقت اضافه + پنالتی در صورت نیاز)
         opponent: تیم حریف (شیء Team)
         is_knockout: True اگر بازی مرحله حذفی است، False اگر مرحله گروهی است
        :return: (گل تیم خودی، گل تیم حریف، تیم برنده یا None در صورت تساوی در گروهی)
        """
        # محاسبه لامبدا (میانگین گل) برای هر تیم بر اساس حمله خودی و دفاع حریف
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        # تولید تعداد گل برای ۹۰ دقیقه
        goals_self = self.poisson_random(lambda_self)
        goals_opponent = self.poisson_random(lambda_opponent)

        # ==========================================
        # بخش ۱: مرحله گروهی (بدون وقت اضافه و پنالتی)
        # ==========================================
        if not is_knockout:
            # به‌روزرسانی آمار گل‌ها
            self.goals_for += goals_self
            self.goals_against += goals_opponent
            opponent.goals_for += goals_opponent
            opponent.goals_against += goals_self

            # محاسبه امتیاز
            if goals_self > goals_opponent:
                self.points += 3
            elif goals_self < goals_opponent:
                opponent.points += 3
            else:
                self.points += 1
                opponent.points += 1

            return goals_self, goals_opponent, None

        # ==========================================
        # بخش ۲: مرحله حذفی (بررسی نتیجه ۹۰ دقیقه)
        # ==========================================
        if goals_self != goals_opponent:
            if goals_self > goals_opponent:
                return goals_self, goals_opponent, self
            else:
                return goals_self, goals_opponent, opponent

        # ==========================================
        # بخش ۳: وقت اضافه ۳۰ دقیقه‌ای (ضریب ۰.۳۳)
        # ==========================================
        extra_lambda_self = lambda_self * 0.33
        extra_lambda_opponent = lambda_opponent * 0.33

        goals_self += self.poisson_random(extra_lambda_self)
        goals_opponent += self.poisson_random(extra_lambda_opponent)

        if goals_self != goals_opponent:
            if goals_self > goals_opponent:
                return goals_self, goals_opponent, self
            else:
                return goals_self, goals_opponent, opponent

        # ==========================================
        # بخش ۴: ضربات پنالتی
        # ==========================================
        return self.penalty_shootout(opponent, goals_self, goals_opponent)

    def penalty_shootout(self, opponent, goals_self, goals_opponent):
        """
        شبیه‌سازی ضربات پنالتی (۵ ضربه اول + ناگهانی در صورت تساوی)
        :param opponent: تیم حریف
        :param goals_self: گل‌های تیم خودی در وقت عادی و اضافه
        :param goals_opponent: گل‌های تیم حریف در وقت عادی و اضافه
        :return: (گل نهایی خودی، گل نهایی حریف، تیم برنده)
        """
        # محاسبه احتمال گل برای هر تیم بر اساس حمله خودی و دفاع حریف
        prob_self = 0.75 + (self.attack - opponent.defense) / 250
        prob_opponent = 0.75 + (opponent.attack - self.defense) / 250

        # محدود کردن احتمال بین ۰.۶ و ۰.۹ 
        prob_self = max(0.6, min(0.9, prob_self))
        prob_opponent = max(0.6, min(0.9, prob_opponent))

        pen_self = 0
        pen_opponent = 0

        # ۵ پنالتی اول
        for _ in range(5):
            if random.random() < prob_self:
                pen_self += 1
            if random.random() < prob_opponent:
                pen_opponent += 1

        # پنالتی ناگهانی (تا زمانی که یکی جلو بیفتد)
        while pen_self == pen_opponent:
            if random.random() < prob_self:
                pen_self += 1
            if random.random() < prob_opponent:
                pen_opponent += 1

        # مشخص کردن برنده
        if pen_self > pen_opponent:
            return goals_self, goals_opponent, self
        else:
            return goals_self, goals_opponent, opponent
