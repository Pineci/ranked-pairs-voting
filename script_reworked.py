import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from functools import cmp_to_key

#TODO: Fix all comments

def LoadBallots(filename : str) -> pd.DataFrame:
    ballots = pd.read_csv(filename)
    return ballots.drop(columns=["Timestamp"])

def RemoveCandidate(ballots : pd.DataFrame, candidate : str) -> pd.DataFrame:
    return ballots.drop(columns=[candidate])

def TallyBallots(ballots : pd.DataFrame):
    # Set up tally matrix
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
    return sorted(majorities, key=cmp_to_key(lambda m1, m2: CompareMajorities(m1, m2, tally)), reverse=True)

def LockGraph(sorted_majorities, tally):
    graph = {k: [] for k in tally.columns}
    for majority in sorted_majorities:
        c1, c2 = majority
        graph[c1].append(c2)
        if CreatesCycle(graph, c1, c1, 0):
            graph[c1].pop(-1)
    return graph

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
def DrawGraph(graph):
    g = nx.DiGraph(graph)
    nx.draw_circular(g)
    pos = nx.circular_layout(g)
    labels = {k: k for k in graph.keys()}
    nx.draw_networkx_labels(g,pos,labels)
    plt.show()

def GraphRoot(graph):
    in_degrees = {k: 0 for k in graph.keys()}
    for key in graph.keys():
        for target in graph[key]:
            in_degrees[target] += 1
    for key in in_degrees.keys():
        if in_degrees[key] == 0:
            return key

def RunBallots(ballots, draw_graph=False, debug=False):
    tally = TallyBallots(ballots)
    majorities = FindMajorities(tally)
    sorted_majorities = SortMajorities(majorities, tally)
    graph = LockGraph(sorted_majorities, tally)
    winner = GraphRoot(graph)

    if draw_graph:
        DrawGraph(graph)
    if debug:
        print(f"Tally:\n {tally}")
        print(f"Majorities: {majorities}")
        print(f"Sorted Majorities: {sorted_majorities}")
    return winner

def MakeRankings(ballots):
    candidates = ballots.columns
    ranking = []
    for i in range(len(candidates)):
        winner = RunBallots(ballots)
        ranking.append(winner)
        ballots = RemoveCandidate(ballots, winner)
    return ranking

def RunFile(filename, i=None):
    ballots = LoadBallots(filename)
    if i:
        ballots = RemoveCandidate(ballots,i)
    RunBallots(ballots)

#filename = "Historian - Sheet1.csv"

#RunFile(filename)