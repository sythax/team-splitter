#!/usr/bin/env python

import yaml
from random import shuffle

class Player():
    def __init__(self, name, power):
        self.name = name
        self.power = power
    
    def __repr__(self) -> str:
        return f"<{self.name}: {self.power}>"


class Team():
    def __init__(self, players):
        self.members = players
        self.power = sum([member.power for member in self.members])
    
    def __repr__(self) -> str:
        return str(self.members)


def read_players():
    """
    Reads a yaml dict of players where the dictionary is in the form:
    { 
        name : power_level,
     }
    """
    roster = []
    with open("players.yml", "r") as stream:
        try:
            players = yaml.safe_load(stream)
            roster.extend([Player(name, power) for name, power in players.items()]) 
        except yaml.YAMLError as exc:
            print(exc)
    return roster


def generate_opposing_teams(roster, team_size=5, permutations=100):
    """
    Given a list of players and a team size, randomly generates teams, continually
    trying to find the pair of teams with the smallest difference in combined power level."""

    if 2 * team_size > len(roster):
        return None


    def get_teams(roster, team_size):
        all_players = shuffle(roster)
        return Team(roster[:team_size]), Team(roster[team_size:2*team_size])

    closest_teams = None
    mismatch = 1000

    for perm in range(permutations):
        team_a, team_b = get_teams(roster, team_size)
        power_difference = abs(team_a.power - team_b.power)
        if power_difference < mismatch:
            closest_teams = (team_a, team_b)
            mismatch = power_difference
    
    
    print(f"After {permutations}, generated two teams with power difference {mismatch}")
    return(closest_teams)


if __name__ == '__main__':
    players = read_players()
    teams = generate_opposing_teams(players)
    print(teams[0])
    print(teams[1])
