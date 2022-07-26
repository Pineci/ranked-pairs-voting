import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Union
from functools import cmp_to_key
from itertools import permutations

# Loads ballots from a csv file. Assumes file is formated using output from a google sheets form.
def LoadBallots(filename: str) -> pd.DataFrame:
    ballots = pd.read_csv(filename)
    return ballots.drop(columns=["Timestamp"])

# Returns a new ballots dataframe and removes a specific candidate from consideration.
def RemoveCandidate(ballots: pd.DataFrame, candidate: Union[str, List[str]]) -> pd.DataFrame:
    if isinstance(candidate, list):
        return ballots.drop(columns=candidate)
    else:
        return ballots.drop(columns=[candidate])

# Take in a dataframe and return a square maatrix with results from the ballots.
# The entry in row i, column j indicates how many people preferred candidate i to
# candidate j. In the event that two candidates are ranked the same, the voter is
# split equally between them. The diagonal of the matrix holds no meaning. 
def TallyBallots(ballots: pd.DataFrame) -> pd.DataFrame:
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

# Returns a list of pairs of candidates where one candidate was more preferred
# than the other. In the event that two candidates are tied when faced head to
# head, the pair is not considered.
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
# Ordering is determined first by largest size of winning majority, then by smallest size of opposing minority.
def CompareMajorities(majority1: tuple[str, str], majority2: tuple[str, str], tally: pd.DataFrame) -> int:
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
    
# Sort majorities in order of descending priority
def SortMajorities(majorities: List[tuple[str, str]], tally: pd.DataFrame) -> List[tuple[str, str]]:
    return sorted(majorities, key=cmp_to_key(lambda m1, m2: CompareMajorities(m1, m2, tally)), reverse=True)

# Returns a list of tuples where each tuple is of the form (start, end) where elements at indices
# starting at start and up until but not including end are all equal according the comparing
# function. 
def FindContinuousIndices(majorities: List[tuple[str, str]], tally: pd.DataFrame) -> List[tuple[int, int]]:
    start_idx = 0
    prev_majority = None
    continuous_indices = []
    for idx, current_majority in enumerate(majorities):
        if prev_majority and CompareMajorities(prev_majority, current_majority, tally) != 0:
            if idx - start_idx > 0:
                continuous_indices.append((start_idx, idx))
            start_idx = idx
        prev_majority = current_majority
    if len(majorities) - start_idx > 0:
        continuous_indices.append((start_idx, len(majorities)))
    return continuous_indices
    
# Need to test all possible sorted lists of majorities by permuting adjacement elements which are
# equivalent in the ordering. This function produces a list of all possible sorted majorities
def PermuteSortedMajorities(sorted_majorities: List[tuple[str, str]], tally: pd.DataFrame) -> List[List[tuple[str, str]]]:
    continuous_sections = FindContinuousIndices(sorted_majorities, tally)
    permuted_indices = [[]]
    current_idx = 0

    # Generate all possible permuted lists given the sections that need to be permuted
    for continuous_section in continuous_sections:
        start, end = continuous_section
        new_section_start = list(range(current_idx, start)) # Extends unpermuted section from previous step
        new_sections = [new_section_start + list(permutation) for permutation in permutations(list(range(start, end)))]

        new_permuted_indices = []
        for section in permuted_indices:
            for new_section in new_sections:
                new_permuted_indices.append(section + new_section)
        permuted_indices = new_permuted_indices

        current_idx = end

    # Add tail if necessary
    if current_idx < len(sorted_majorities):
        for i in range(len(permuted_indices)):
            tail = list(range(current_idx, len(sorted_majorities)))
            permuted_indices[i] = permuted_indices[i] + tail

    # Finally index the original list by the permuted indices
    permuted_sorted_majorities = []
    for permuted_index in permuted_indices:
        permuted_sorted_majorities.append([sorted_majorities[i] for i in permuted_index])

    return permuted_sorted_majorities

# Creates a graph given a list of sorted majorities. Sorted majorities in the form [(a, b), (c, d), ...]
# create edges from a to b, from c to d, et cetera. The graph is stored in a dictionary, where the key is
# a vertex and the value is a list of vertices which have edges pointing to them from the key vertex.
def LockGraph(sorted_majorities: List[tuple[str, str]], tally: pd.DataFrame) -> Dict[str, List[str]]:
    graph = {k: [] for k in tally.columns}
    for majority in sorted_majorities:
        c1, c2 = majority
        graph[c1].append(c2)
        if InCycle(graph, c1):
            graph[c1].pop(-1)
    return graph

# Checks if the provided graph contains a cycle which contains the relevant new edge
def InCycle(graph: Dict[str, List[str]], vertex: str) -> bool:
    def CreatesCycle(graph, currentkey, depth):
        if depth > len(graph.keys())+1:
            return False
        if currentkey in graph.keys():
            for key in graph[currentkey]:
                if key == vertex:
                    return True
                if CreatesCycle(graph, key, depth+1):
                    return True
        return False
    return CreatesCycle(graph, vertex, 0)

# Draws the graph.
def DrawGraph(graph: Dict[str, List[str]]) -> None:
    g = nx.DiGraph(graph)
    nx.draw_circular(g)
    pos = nx.circular_layout(g)
    labels = {k: k for k in graph.keys()}
    nx.draw_networkx_labels(g,pos,labels)
    plt.show()

# Finds all roots of the graph, i.e. vertices with in-degree 0
def GraphRoots(graph: Dict[str, List[str]]) -> List[str]:
    in_degrees = {k: 0 for k in graph.keys()}
    for key in graph.keys():
        for target in graph[key]:
            in_degrees[target] += 1
    roots = []
    for key in in_degrees.keys():
        if in_degrees[key] == 0:
            roots.append(key)
    return roots

# Runs the full ranked pairs algorithm to find a winner given a ballot. The process first tallies the ballots, then find the winning majorities, and
# sort these majorities by the ranked pairs ordering criterion. Then this sorted list is used to create a directed acyclic graph (DAG) and the winner
# is the unique vertex with in degree 0. If there is more than one vertex with degree 0, then the winner is ambiguous and the result is a tie.
# 
# Another way a tie can occur is due to ambiguous orderings of the sorted majorities. We check all possible sorted majorities where equivalent elements
# are permuted. If every majority has exactly one winner and this winner is the same across all possible sorts, then they are unambiguously the winner. 
# Otherwise, it is ruled as a tie and multiple winners are returned in a tuple. 
def FindWinner(ballots: pd.DataFrame, draw_graph: bool=False, debug: bool=False, alert_ties: bool=False) -> Union[str, tuple[str]]:
    tally = TallyBallots(ballots)
    majorities = FindMajorities(tally)
    first_sorted_majorities = SortMajorities(majorities, tally)
    permuted_majorities = PermuteSortedMajorities(first_sorted_majorities, tally)
    winners = {}
    for sorted_majorities in permuted_majorities:
        graph = LockGraph(sorted_majorities, tally)
        roots = GraphRoots(graph)

        # Split win between each root of the graph. In most real world cases, there will only be one root
        for root in roots:
            winners[root] = winners.get(root, 0) + 1/len(roots)

    if draw_graph:
        DrawGraph(graph)
    if debug:
        print(f"Tally:\n {tally}")
        print(f"Majorities: {majorities}")
        print(f"Sorted Majorities: {sorted_majorities}")
        print(f"Permuted Majorities:\n")
        for majority in permuted_majorities:
            print(majority)

    if len(winners.keys()) > 1:
        if alert_ties:
            print(f"A tie has occurred! Out of {len(permuted_majorities)} permutations, each candidate won the following:\n")
            for winner in winners.keys():
                print(f"{winner} {100*winners[winner]/len(permuted_majorities):.1f}%")
        return tuple(winners.keys())
    else:
        return list(winners.keys())[0]

# Find rankings for all the candidates given the ballots. To do so, the winner/winners are found given the ballots. The winner/winners
# are then removed from the ballots and a winner among the remaining candidates if found until no candidates remain. Results are returned
# in an ordered list of the winners, where tuples of candidates indicate ties.
def FindRankings(ballots: pd.DataFrame) -> List[Union[str, tuple[str]]]:
    candidates = ballots.columns
    ranking = []
    counted = 0
    while counted < len(candidates):
        winner = FindWinner(ballots)
        ranking.append(winner)
        if not isinstance(winner, tuple):
            winner = [winner]
        for w in winner:
            ballots = RemoveCandidate(ballots, w)
            counted += 1
    return ranking

# Loads ballots from a file and either finds the winner or rankings from the ballot. A specific candidate or list of candidates
# can optionally be removed from consideration. 
def RunFile(filename: str, mode: str='winner', removed_candidates: Union[str, List[str]]=None) -> Union[str, tuple[str], List[Union[str, tuple[str]]]]:
    ballots = LoadBallots(filename)
    if removed_candidates:
        ballots = RemoveCandidate(ballots, removed_candidates)
    if mode == 'winner':
        return FindWinner(ballots)
    if mode == 'rankings':
        return FindRankings(ballots)