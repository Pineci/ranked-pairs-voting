# Ranked Pairs Voting

This repository implements the ranked pairs voting system. The outline of how the scheme works and several examples of results from the voting system can be inspected in the references folder of this repo.

## Usage

TODO: Fill this in.

## Testing

This repository includes a testing module. The test file can be found in the test directory. To run the tests, run the `run-tests.sh` file.

## Modifications to Ranked Pairs

As a brief outline, ranked pairs involves three crucial steps: **tally**, **sort**, and **lock**. The **tally** step is simple and just creates a matrix of how many voters chose noe candidate over another. From this matrix, winning majorities are found and then **sorted** first according to the largest size of the winning majority, then by according to the smallest size of the opposing minority. Finally these sorted majorities are used to **lock** directed graph where vertices are candidates and edges indicate when one candidate beats another, while skipping edges which would create cycles in the already existing graph. The winner is the candidate/vertex with in-degree 0. More details can be found in the references. 

This sorting scheme creates an amibguity when two majorities have equal winning majorities and equal opposing minorities. I have created several examples in the test file which create this ambiguity. To avoid choosing one candidate over the other, I have made a modification to the voting system where we create all possible valid sorted majorities by permuting adjacent majorities which are equal under the comparison metric. The lock step is then run for every one of these valid sorted majorities. If every one of these lock steps results in the same winner, then this candidate is reported as the winner. If any of these orderings produces different winning candidates, a tie is declared. Another way for a tie to occur is when two vertices have in-degree 0 in the lock step. This is also declared as a tie.

## Authors

This repository was created by Anthony Pineci (CS '22). I rewrote most of the previously existing voting code, but several functions were modified or included directly into this repository. This  original voting code can be found in the jupyter notebook included in the archive directory. The original code credits the following individuals:

Written by Jacob "Coby" Abrahams, Secretary 2016-2017 with help from other skurves.
Updated for python 3 and debugged by Alejandro López, Secretary 2018-2019, with help from Alison Dugas, Secretary 2017-2018, Umesh Padia, Webmaster 2017-2019, Jack Briones (CS class of 2020) and Coby Abrahams