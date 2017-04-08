import csv
import datetime

def get_players():
	with open("soccer_players.csv") as file:
		reader = csv.DictReader(file)
		players = list(reader)
	return players

def sort_height(current):
	return int(current["Height (inches)"])
	
def sort_players(players):
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

def create_teams(players):
	some_exp, no_exp = sort_players(players)
	draft, second, third = ([], [], []) 
	total_players = len(some_exp) + len(no_exp)
	for index in range(total_players):
		pick = some_exp if index % 2 else no_exp
		draft.append(pick.pop())
		third, draft, second = draft, second, third
	return draft, second, third

def print_team(team):
	string = "{}\n".format(team[0].title())
	for player in team[1]:
		string += "{Name}, {Soccer Experience}, {Guardian Name(s)}\n".format(**player)
	string += "="*10 + "\n"
	return string 

def print_league(league):
	printout = ""
        for team in league.items():
                printout += print_team(team)
	return printout

def save_league(printout):
	with open("teams.txt", "w") as league:
		league.write(printout)

def create_letter(**kwargs):
	#letter = { "date" : date, **letter1 }
	string = """
Dear {Guardian Name(s)},

I regret to inform you that {Name} will be playing with
the {team} this year. They really didn't seem like they 
wanted to be at tryouts in the first place. God knows I
didn't. Are you sure {Name} is the "sports type"? One too
many Tolken books if you ask me.Anyway, the {team} ain't
winning any Heisman's this year, I'm sure {Name} can sit 
bench and carry balls with the best of them. You should be 
so proud blah blah blah...just remember to pick the weasel
up on time, 'aight?

Coach Biff

First practice on {date} at 4pm
""".format(**kwargs)
	return string

def mail_letters(league):
	date = datetime.date.today()+ datetime.timedelta(days=7)
	for team, players in league.items():
		for player in players:
			letter = create_letter(team=team,date=date, **player)
			with open("{}.txt".format(player["Name"].replace(" ", "_")), "w") as file:
				file.write(letter)

	
if __name__ == "__main__":
	players = get_players()
	first, second, third = create_teams(players)
	league = { "sharks": first, "dragons": second, "raptors": third }
	printout = print_league(league)
	save_league(printout)
	mail_letters(league)	
