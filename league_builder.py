import os
import csv
import random
import datetime

def get_players():
        """Opens the player csv and returns the player as a list"""
        with open("./csv/soccer_players.csv") as file:
                reader = csv.DictReader(file)
                players = list(reader)
        return players

def create_dir(path):
        try:
                os.makedirs(path)
        except OSError:
                pass

def sort_height(current):
        """Sorting comparitor"""
        return int(current["Height (inches)"])
	
def sort_players(players):
        """Sorts players into two lists, experienced and not experienced,
        and then sorts each of those lists by height"""
        some_exp = []
        no_exp = []
        for player in players:
                if player["Soccer Experience"] == "YES":
                        some_exp.append(dict(player))
                else:
                        no_exp.append(dict(player))
        some_exp.sort(key=sort_height)
        no_exp.sort(key=sort_height)
        return some_exp, no_exp

def shift(teams):
        """Shifts list up by one, creating a queue-like structure"""
        return teams[1:] + [teams[0]]

def create_teams(players, count):
        """Creates even teams based on a player list and a desired
        number of teams"""
        some_exp, no_exp = sort_players(players)
        teams = [[] for x in range(count)]
        total_players = len(some_exp) + len(no_exp)
        for index in range(total_players):
                # Reinsert to get indeterminate, balanced teams
                # if not index == 0 and not index % 3:
                #         random.shuffle(teams)
                pick = some_exp if index % 2 else no_exp
                teams[0].append(pick.pop())
                teams = shift(teams)
        return teams

def print_team(team):
        """Creates a string for each team roster"""
        string = "{}\n".format(team[0].title())
        for player in team[1]:
                string += "{Name}, {Soccer Experience}, {Guardian Name(s)}\n".format(**player)
        string += "="*10 + "\n"
        return string 

def print_league(league):
        """Creates a string for the league roster"""
        printout = ""
        for team in league.items():
                printout += print_team(team)
        return printout

def save_league(printout):
        """Writes league to a teams text file"""
        create_dir("./league")
        with open("./league/teams.txt", "w") as league:
                league.write(printout)

def create_letter(**kwargs):
        """Creates a string for a parent/guardian letter"""
        string = """Dear {Guardian Name(s)},

I regret to inform you that {Name} will be playing with
the {team} this year. They really didn't seem like they 
wanted to be at tryouts in the first place. God knows I
didn't. Are you sure {Name} is the "sports type"? One too
many Tolken books if you ask me. Anyway, the {team} ain't
winning any Heisman's this year, I'm sure {Name} can sit 
bench and carry balls with the best of them. You should be 
so proud blah blah blah...just remember to pick the weasel
up on time, 'aight?

Coach Biff

First practice is a week from now, {date} at 4pm
""".format(**kwargs)
        return string

def mail_letters(league):
        """Creates and saves parental letters for the entire league"""
        date = datetime.date.today()+ datetime.timedelta(days=7)
        create_dir("./league/letters")
        for team, players in league.items():
                for player in players:
                        letter = create_letter(team=team,date=date, **player)
                        with open("./league/letters/{}.txt".format(player["Name"].replace(" ", "_")), "w") as file:
                                file.write(letter)

def get_team_count(players):
        """User input for team creation"""
        print("How many teams are in the league?")
        while True:
                try:
                        team_count = int(input("> "))
                except ValueError:
                        print("Enter a valid number of teams...")
                else:
                        return create_teams(players, team_count)

def name_teams(teams):
        """User input for team naming"""
        league = {}
        for index, team in enumerate(teams):
                print("Enter name for team {} out of {}:".format(index + 1,len(teams)))
                team_name = input("> ")
                league[team_name] = team
        return league

	
if __name__ == "__main__":
        players = get_players()
        # Comment out these next two lines and uncomment the third
        # to let user insert infinite number of teams
        first, second, third = create_teams(players, 3)
        league = { "sharks": first, "dragons": second, "raptors": third }
        #league = name_teams(get_team_count(players))
        printout = print_league(league)
        save_league(printout)
        mail_letters(league)	
