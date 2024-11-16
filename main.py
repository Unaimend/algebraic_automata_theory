from src import automate
import argparse
import pandas as pd

# Create the parser
parser = argparse.ArgumentParser(description="A program that converts a given statemachine to a semigroup")

# Add arguments
parser.add_argument(
    "-d", "--dot", 
    type=str,
    help = "Specyfing this flag will generate a .dot file of the automata, pelase specify a filename",
    required=False  # Makes this argument mandatory
)


parser.add_argument(
    "-n", "--no-print-semig", 
    action="store_true",
    help = "Specyfing this flag will prevent the program from printing the semigroup",
    required=False 
)


parser.add_argument(
    "-t", "--table", 
    action="store_false",
    help = "Specyfing this flag will prevent the program from printing the table",
    required=False 
)


parser.add_argument(
    "-a", "--aut", 
    type=str,
    help = "Path to the an automate file (a comma seperated file with states, transitions and final states)",
    required=False # Makes this argument mandatory
)


parser.add_argument(
    "-N",  
    type=int,
    help = "The length on the longest workd-1 that will be simulated",
    default = 3,
    required=False # Makes this argument mandatory
)


# Parse the arguments
args = parser.parse_args()


if __name__ == "__main__":

  automaton = {}

  if args.aut:
    print(f'Loading automaton from {args.aut}')
    df = pd.read_csv(args.aut, header = None)
    automaton = {(row[0], row[1]) : row[2] for row in df.values }
  else: 
    print(f'Loading automaton from examples/lecture_1.csv')
    df = pd.read_csv("examples/lecture_1.csv", header = None)
    automaton = {(row[0], row[1]) : row[2] for row in df.values }
    
  eqv_classes = automate.create_table(automaton, ['a','b','c'], N = args.N)
  
  if args.table:
    print(f'Printing eqv. classes')
    eqv_with_rep = automate.add_representatives(automaton, eqv_classes)
    print(eqv_with_rep[1])
    print("\n\n\n")
    print("Are are eqv. of length n duplicate?\nIf one of the last columns entries are true your specied work length is long enough.")
    print(eqv_with_rep[2])
    print("\n\n\n")

  if args.dot:
    automate.plot(automaton, args.dot)

  if not args.no_print_semig:
    print(f'Printing semigroup')
    u, class_, _ = automate.add_representatives(automaton, eqv_classes)
    r = automate.eqv_class_to_semigroup(automaton,['a','b','c'], u)
    print(automate.format_semitable(r))
