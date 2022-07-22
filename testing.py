import pandas as pd
from script_reworked import RunBallots, MakeRankings

#TODO: Fix all comments

#TODO: Archive all web pages to the github repo

#TODO: add a testing unit with pytests

#TODO: just accept files as arguments to a command line script

#TODO: Archive old code so that anyone who wants can read it to see the comments, an intersiting little history

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

def MakeAmbigiousTestCase():
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

print(RunBallots(MakeTennesseeBallots()))
print(MakeRankings(MakeTennesseeBallots()))

print(RunBallots(MakeAmbigiousTestCase(), debug=True))
print(MakeRankings(MakeAmbigiousTestCase()))

print(RunBallots(MakeTieTestCase(), debug=True))
print(MakeRankings(MakeTieTestCase()))