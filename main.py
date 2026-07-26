# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 18:08:58 2026

@author: CYBORG
"""

from simulator import WorldCupSimulator
# ============================================================
# منوی اصلی برنامه 
# ============================================================
def main():
    simulator = WorldCupSimulator()

    while True:
        print("\n" + "="*40)
        print("⚽ World Cup 2026 Simulator")
        print("="*40)
        print("1. Load teams from CSV")
        print("2. Draw groups")
        print("3. Run group stage & show tables")
        print("4. Run full tournament & show champion")
        print("5. Simulate 1000 times & show percentages")
        print("6. Show knockout bracket")
        print("7. Exit")
        print("-"*40)

        choice = input("Your choice: ").strip()

        if choice == '1':
            filename = input("CSV filename (default: worldcup_2026_teams.csv): ").strip()
            if not filename:
                filename = "worldcup_2026_teams.csv"
            simulator.load_teams_from_csv(filename)

        elif choice == '2':
            if not simulator.teams:
                print("❌ Load teams first!")
            else:
                simulator.seed_and_draw_groups()  # پیش‌فرض silent=False

        elif choice == '3':
            if not simulator.groups:
                print("❌ Draw groups first!")
            else:
                simulator.reset_all_stats()
                simulator.run_group_stage()

        elif choice == '4':
            if not simulator.teams:
                print("❌ Load teams first!")
            else:
                simulator.run_full_simulation()

        elif choice == '5':
            if not simulator.teams:
                print("❌ Load teams first!")
            else:
                try:
                    num = input("Number of simulations (default 1000): ").strip()
                    if num == "":
                        num = 1000
                    else:
                        num = int(num)
                    simulator.most_likely_champion(num)
                except ValueError:
                    print("❌ Enter a valid number!")

        elif choice == '6':
            simulator.display_bracket()

        elif choice == '7':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()