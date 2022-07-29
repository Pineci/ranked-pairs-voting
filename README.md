# Ranked Pairs Voting

This repository implements the ranked pairs voting system. The outline of how the scheme works and several examples of results from the voting system can be inspected in the references folder of this repo.

## Environment Setup

Included in this repository is a `environment.yml` file which can be used to construct a python environment using [Anaconda](https://www.anaconda.com/products/distribution). Briefly, the command line tool `conda` manages multiple python environments and allows the user to easily switch between different installations of python and whatever modules are installed in those environments. If this software is new to you, it may be helpful to look at the [conda cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf).

To create an environment for this repository, please run the command `conda env create --file environment.yml` from the root directory of this repository. This will create a conda environment called `voting`, which can be activated using the command `conda activate voting`. Please ensure that this environment is activated anytime code is run from the repository from the command line or in a jupyter notebook.

## Usage

There are two ways the voting code may be used. First, there is a command line tool which can be used by running the `run.py` file. For help with its input arguments, please run `python run.py -h` for a full description. To see the code in action, a test ballot has been provided in the ballots directory. Running the command `python run.py tennessee_ballots.csv` should report the correct winner, nashville.

Alternatively, the code can be run from a jupyter notebook. The provided notebook `run.ipynb` contains two methods of finding the winner from a file. One uses a single function, while the other runs through some more detailed code which allows for more user specificity.

### Input Format

Please inspect the sample ballot file located at `ballots/tennessee_ballots.csv` to see the desired input format. Ballot files are assumed to have been created from a google form sheet. If a different input format is desired, please modify the `LoadBallots` function as necessary and create a pull request/contact me directly to incorporate any changes into this repository.

## Testing

This repository includes a testing module. The test file can be found in the test directory. To run the tests, run the `run-tests.sh` file.

## Modifications to Ranked Pairs

As a brief outline, ranked pairs involves three crucial steps: **tally**, **sort**, and **lock**. The **tally** step is simple and just creates a matrix of how many voters chose noe candidate over another. From this matrix, winning majorities are found and then **sorted** first according to the largest size of the winning majority, then by according to the smallest size of the opposing minority. Finally these sorted majorities are used to **lock** directed graph where vertices are candidates and edges indicate when one candidate beats another, while skipping edges which would create cycles in the already existing graph. The winner is the candidate/vertex with in-degree 0. More details can be found in the references. 

This sorting scheme creates an amibguity when two majorities have equal winning majorities and equal opposing minorities. I have created several examples in the test file which create this ambiguity. To avoid choosing one candidate over the other, I have made a modification to the voting system where we create all possible valid sorted majorities by permuting adjacent majorities which are equal under the comparison metric. The lock step is then run for every one of these valid sorted majorities. If every one of these lock steps results in the same winner, then this candidate is reported as the winner. If any of these orderings produces different winning candidates, a tie is declared. Another way for a tie to occur is when two vertices have in-degree 0 in the lock step. This is also declared as a tie.

## Authors

This repository was created by Anthony Pineci (CS/Ma '22). I rewrote most of the previously existing voting code, but several functions were modified or included directly into this repository. The  original voting code can be found in the jupyter notebook included in the archive directory. The original code credits the following individuals:

Written by Jacob "Coby" Abrahams, Secretary 2016-2017 with help from other skurves.
Updated for python 3 and debugged by Alejandro López, Secretary 2018-2019, with help from Alison Dugas, Secretary 2017-2018, Umesh Padia, Webmaster 2017-2019, Jack Briones (CS class of 2020) and Coby Abrahams