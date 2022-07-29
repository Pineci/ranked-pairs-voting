from src.voting import RunFile
import argparse

parser = argparse.ArgumentParser(description="Use ranked pairs voting to find winners given a ballot of voters' preferences.")
parser.add_argument("files", metavar="file", type=str, nargs="+", help="One or more ballot files to be processed")
parser.add_argument("--rankings", dest="mode", action="store_const", const="rankings", 
                    default="winner", help="Ranks all candidates on the ballot. By default, the program finds the winner")
parser.add_argument("--dir", dest="folder", action="store", default=["ballots"], nargs=1, type=str, help="Directory where ballot files are contained. Defaults to 'ballots'")

args = parser.parse_args()

print("")
for file in args.files:
    filename = f"{args.folder[0]}/{file}"
    result = RunFile(filename, mode=args.mode)
    print(f"The {args.mode} for the ballots located in the file {file}:\t{result}")
print("")