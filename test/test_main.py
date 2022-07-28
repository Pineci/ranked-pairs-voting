import pandas as pd

print(__name__)
print(__package__)

from src.main import FindRankings
from itertools import permutations

import pytest

#TODO: Fill in README

#TODO: just accept files as arguments to a command line script

# Makes example ballots accoring to the Tennessee example in the Ranked
# Pairs wikipedia page, assuming 100 votes
# https://en.wikipedia.org/wiki/Ranked_pairs

def test_tennessee_ballots():
    # This order the preferences of each type of voter
    # rankings are given under the heading of the following column order.
    # 1 = memphis
    # 2 = nashville
    # 3 = chattanooga
    # 4 = knoxville

    memphis = [1, 2, 3, 4]
    nashville = [4, 1, 2, 3]
    chattanooga= [4, 3, 1, 2]
    knoxville = [4, 3, 2, 1]
    data = []
    for _ in range(42):
        data.append(memphis)
    for _ in range(26):
        data.append(nashville)
    for _ in range(15):
        data.append(chattanooga)
    for _ in range(17):
        data.append(knoxville)
    df = pd.DataFrame(data, columns=['memphis','nashville','chattanooga','knoxville'])

    rankings = FindRankings(df)
    assert rankings == ['nashville', 'chattanooga', 'knoxville', 'memphis']

def test_narrow_winner():
    # 1 = A
    # 2 = B
    # 3 = C

    voter_one = [1, 2, 3] # Order: A, B, C
    voter_two = [2, 3, 1] # Order: C, A, B
    voter_three = [3, 1, 2] #Order: B, C, A
    data = []
    for _ in range(35):
        data.append(voter_one)
    for _ in range(33):
        data.append(voter_two)
    for _ in range(32):
        data.append(voter_three)
    df = pd.DataFrame(data, columns=["A", "B", "C"])
    
    rankings = FindRankings(df)
    assert rankings == ["A", "B", "C"]

def test_tie():
    # 1 = A
    # 2 = B
    # 3 = C
    
    voter_one = [1, 2, 3] # Order: A, B, C
    voter_two = [2, 3, 1] # Order: C, A, B
    voter_three = [3, 1, 2] #Order: B, C, A
    data = []
    for _ in range(33):
        data.append(voter_one)
    for _ in range(33):
        data.append(voter_two)
    for _ in range(33):
        data.append(voter_three)
    df = pd.DataFrame(data, columns=["A", "B", "C"])

    rankings = FindRankings(df)
    assert rankings in list(map(lambda x: [x], permutations(["A", "B", "C"])))

def test_middle_two_tie():
    # 1 = A
    # 2 = B
    # 3 = C
    # 4 = D

    # Want to have A win, B, C tie, D last
    
    voter_one = [1, 2, 3, 4] # Order: A, B, C, D
    voter_two = [1, 3, 2, 4] # Order: A, C, B, D
    data = []
    for i in range(50):
        data.append(voter_one)
    for i in range(50):
        data.append(voter_two)
    df = pd.DataFrame(data, columns=["A", "B", "C", "D"])

    rankings = FindRankings(df)
    assert rankings in [["A", ("B", "C"), "D"], ["A", ("C", "B"), "D"]]

def test_middle_three_tie():
    # 1 = A
    # 2 = B
    # 3 = C
    # 4 = D
    # 5 = E

    # Want to have A win, B, C, D tie, E last
    
    voter_one = [1, 2, 3, 4, 5] # Order: A, B, C, D, E
    voter_two = [1, 4, 2, 3, 5] # Order: A, D, B, C, E
    voter_three = [1, 3, 4, 2, 5] # Order: A, C, D, B, E
    data = []
    for i in range(33):
        data.append(voter_one)
    for i in range(33):
        data.append(voter_two)
    for i in range(33):
        data.append(voter_three)
    df = pd.DataFrame(data, columns=["A", "B", "C", "D", "E"])

    rankings = FindRankings(df)
    assert rankings in list(map(lambda x: ["A"] + [x] + ["E"], permutations(["B", "C", "D"])))

def test_multiple_ties():
    # 1 = A
    # 2 = B
    # 3 = C
    # 4 = D

    # Want to have A, B tie, then C, D tie
    
    voter_one = [1, 2, 3, 4] # Order: A, B, C, D
    voter_two = [2, 1, 3, 4] # Order: B, A, C, D
    voter_three = [1, 2, 4, 3] # Order: A, B, D, C
    voter_four = [2, 1, 4, 3] # Order: B, A, D, C
    data = []
    for i in range(25):
        data.append(voter_one)
    for i in range(25):
        data.append(voter_two)
    for i in range(25):
        data.append(voter_three)
    for i in range(25):
        data.append(voter_four)
    df = pd.DataFrame(data, columns=["A", "B", "C", "D"])
    
    rankings = FindRankings(df)
    assert rankings in [[("A", "B"), ("C", "D")],
                        [("B", "A"), ("C", "D")],
                        [("A", "B"), ("D", "C")],
                        [("B", "A"), ("D", "C")]]