import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from functools import cmp_to_key

#TODO: Fix all comments

# Loading the ballots, hard coded for the format that google sheets outputs to
# .csvs. Returns a list of lists, where the first entry defines which candidate
# that position in the ballots refer to, and the rest of the entries are the 
# ballots themselves.
def LoadBallots(filename : str) -> pd.DataFrame:
    ballots = pd.read_csv(filename)
    return ballots.drop(columns=["Timestamp"])

# Removes candidate i from all ballots in order to find a second place winner
def RemoveCandidate(ballots : pd.DataFrame, candidate : str) -> pd.DataFrame:
    return ballots.drop(columns=[candidate])

# Returns a matrix where entry (i,j) is the number of ballots on which 
# candidate i beats candidate j. If (i,j) = (j,i), both are set to zero
# to avoid problems later.
def TallyBallots(ballots : pd.DataFrame):
    # Set up count matrix
    candidates = ballots.columns
    tally = pd.DataFrame(np.zeros((len(candidates), len(candidates))), columns=candidates, index=candidates)

    # Iterate over all ballots
    for index, row in ballots.iterrows():
        for c1 in candidates:
            for c2 in candidates:
                if row[c1] < row[c2]:
                    tally.loc[c1][c2] += 1
                elif row[c1] == row[c2]:
                    tally.loc[c1][c2] += 0.5
    
    # TODO: At this point, the original code zeros out any values which are symmetric across the diagonal, says its to avoid problems later. What are these problems?

    return tally

def FindMajorities(tally: pd.DataFrame) -> List[tuple[str, str]]:
    candidates = tally.columns
    majorities = [] # Entries are in the form (c1, c2) where candidate c1 beat candidate c2
    for i1 in range(len(candidates)):
        for i2 in range(i1+1, len(candidates)):
            c1, c2 = candidates[i1], candidates[i2]
            v12, v21 = tally.loc[c1][c2], tally.loc[c2][c1]
            if v12 > v21:
                majorities.append((c1, c2))
            if v21 > v12:
                majorities.append((c2, c1))
    return majorities

# Returns positive values iff majority1 > majority2, negative values iff majority1 < majority2, and 0 for equality
def CompareMajorities(majority1 : tuple[str, str], majority2: tuple[str, str], tally: pd.DataFrame) -> int:
    c1, c2 = majority1
    d1, d2 = majority2
    s1, s2 = tally.loc[c1][c2], tally.loc[d1][d2]

    # First compare by size of winning majority
    if s1 > s2:
        return 1
    elif s1 < s2:
        return -1
    else:
        # If majorities are equal, majority with smaller opposition is ranked higher
        o1, o2 = tally.loc[c2][c1], tally.loc[d2][d1]
        if o2 > o1:
            return 1
        elif o2 < o1:
            return -1
        else:
            # If the majorities win by the same amount and have the same opposition, then they're tied
            return 0
    

def SortMajorities(majorities: List[tuple[str, str]], tally: pd.DataFrame):
    return sorted(majorities, key=cmp_to_key(lambda m1, m2: CompareMajorities(m1, m2, tally)))

def LockGraph(sorted_majorities, tally):
    graph = {k: [] for k in tally.columns}
    for majority in sorted_majorities:
        c1, c2 = majority
        graph[c1].append(c2)
        if CreatesCycle(graph, c1, c1, 0):
            graph[c1].pop(-1)
    return graph


# Returns tuple of indices (i,j) for the entry in the score matrix with the
# max value. If there is a tie, the tie is broken by which of the complementary
# locations, (j,i), indicating losing, is smallest. If there is still a tie, 
# both are returned, and a runoff election becomes a possibility.
def FindMax(scores):
    maxscore = None # this way if every entry in scores is 0, it doesn't update
    maxindex = None
    candidates = scores.columns
    for i1, c1 in enumerate(candidates):
        for i2, c2 in enumerate(candidates):
            score = scores.loc[c1][c2]
            if not maxscore or score > maxscore:
                maxscore = score
                maxindex = [(c1,c2)]
            elif score == maxscore:
                #TODO: Check algorithm to see why this tie breaking rule is necessary
                maxscore_transpose = scores.loc[maxindex[0][1]][maxindex[0][0]]
                if score < maxscore_transpose:
                    maxindex = [(c1,c2)]
                elif score == maxscore_transpose:
                    maxindex.append((c1,c2))
    if maxindex and len(maxindex) == 2 and maxindex[0][0] == maxindex[1][0]:
        if scores.loc[maxindex[0][1]][maxindex[1][1]] > scores.loc[maxindex[1][1]][maxindex[0][1]]:
            maxindex = [maxindex[0]]
        elif scores.loc[maxindex[0][1]][maxindex[1][1]] < scores.loc[maxindex[1][1]][maxindex[0][1]]:
            maxindex = [maxindex[1]]
    return maxindex, maxscore




# Checks if the provided graph contains a cycle which contains the relevant
# new edge.
def CreatesCycle(graph, currentkey, origin,depth):
    if depth > len(graph.keys())+1:
        return False
    if currentkey in graph.keys():
        for key in graph[currentkey]:
            if key == origin:
                return True
            if CreatesCycle(graph,key,origin,depth+1):
                return True
    return False

# Draws the graph.
def DrawGraph(graph,names):
    g = nx.DiGraph(graph)
    nx.draw_circular(g)
    pos = nx.circular_layout(g)
    labels = {k: k for k in graph.keys()}
    nx.draw_networkx_labels(g,pos,labels)
    plt.show()


def Run(filename,i=-1):
    ballots = LoadBallots(filename)
    if i != -1:
        ballots = RemoveCandidate(ballots,i)
    scores = TallyBallots(ballots)
    graph = ConstructGraph(scores)
    names = [i.rstrip() for i in ballots.columns]

    print("p sure the winner is " + max(graph.keys(), key=lambda k: len(graph[k])))
    DrawGraph(graph, names)



# This is the main function

# Identifies the largest value(s) in the scores matrix, adds that to a directed
# graph of candidates, where a->b means a beats b, and repeats. The graph is 
# stored in a dictionary where (key,value) is key->value. An edge is not
# drawn if it would complete a cycle. The source of the graph, if there is a
# single one, is the winner. If there is a cycle where everyone in the cycle
# beats everyone outside the cycle, a runoff is needed between the members of 
# the cycle. Note that a runoff will only work if people change their votes. 
def ConstructGraph(scores):
    graph = {k: [] for k in scores.columns}
    maxindex, maxscore = FindMax(scores)
    while(maxscore > 0):
        for c1, c2 in maxindex:
            graph[c1].append(c2)
            if len(maxindex) == 1 and CreatesCycle(graph, c1, c1, 0):
                graph[c1].pop(-1)
            scores.loc[c1][c2] = 0
            scores.loc[c2][c1] = 0
        maxindex, maxscore = FindMax(scores)
    return graph

filename = "Historian - Sheet1.csv"

#Run(filename)

ballots = LoadBallots(filename)
tally = TallyBallots(ballots)
majorities = FindMajorities(tally)
sorted_majorities = SortMajorities(majorities, tally)
print(majorities)
print(sorted_majorities)