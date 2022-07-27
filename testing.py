import pandas as pd
from script_reworked import RunBallots, MakeRankings

#TODO: Fix all comments

#TODO: Archive all web pages to the github repo

#TODO: add a testing unit with pytests

#TODO: just accept files as arguments to a command line script

#TODO: Check create cycle code

# Makes example ballots accoring to the Tennessee example in the Ranked
# Pairs wikipedia page, assuming 100 votes
# https://en.wikipedia.org/wiki/Ranked_pairs

def MakeTennesseeBallots():
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
    for i in range(42):
        data.append(memphis)
    for i in range(26):
        data.append(nashville)
    for i in range(15):
        data.append(chattanooga)
    for i in range(17):
        data.append(knoxville)
    return pd.DataFrame(data, columns=['memphis','nashville','chattanooga','knoxville'])

def MakeNarrowWinnerTestCase():
    # 1 = A
    # 2 = B
    # 3 = C

    voter_one = [1, 2, 3] # Order: A, B, C
    voter_two = [2, 3, 1] # Order: C, A, B
    voter_three = [3, 1, 2] #Order: B, C, A
    data = []
    for i in range(35):
        data.append(voter_one)
    for i in range(33):
        data.append(voter_two)
    for i in range(32):
        data.append(voter_three)
    return pd.DataFrame(data, columns=["A", "B", "C"])

def MakeTieTestCase():
    # 1 = A
    # 2 = B
    # 3 = C
    
    voter_one = [1, 2, 3] # Order: A, B, C
    voter_two = [2, 3, 1] # Order: C, A, B
    voter_three = [3, 1, 2] #Order: B, C, A
    data = []
    for i in range(33):
        data.append(voter_one)
    for i in range(33):
        data.append(voter_two)
    for i in range(33):
        data.append(voter_three)
    return pd.DataFrame(data, columns=["A", "B", "C"])

def MakeMiddleTwoTieTestCase():
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
    return pd.DataFrame(data, columns=["A", "B", "C", "D"])

def MakeMiddleThreeTieTestCase():
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
    return pd.DataFrame(data, columns=["A", "B", "C", "D", "E"])

def MakeMultipleTieTestCase():
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
    return pd.DataFrame(data, columns=["A", "B", "C", "D"])

print(MakeRankings(MakeTennesseeBallots()))

print(MakeRankings(MakeNarrowWinnerTestCase()))

print(MakeRankings(MakeTieTestCase()))

print(MakeRankings(MakeMiddleTwoTieTestCase()))

print(MakeRankings(MakeMiddleThreeTieTestCase()))

print(MakeRankings(MakeMultipleTieTestCase()))