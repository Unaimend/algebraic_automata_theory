import pandas as pd
from graphviz import Digraph
from itertools import product
from typing import Dict, Tuple, List
from tabulate import tabulate

State = str
Letter = str
StateMachine = Dict[Tuple[State, Letter], State]

EqvTable = pd.DataFrame
Semigroup = pd.DataFrame


def get_states(transitions):
  a = []
  for((start_state, _), end_state) in transitions.items():
    a.append(start_state)
    a.append(end_state)
  return set(a)


def get_alphabet(transitions):
  a: List[Letter] = []
  for((_, letter), _) in transitions.items():
    a.append(letter)
  return list(set(a))

def simulate_fsm(start_state, input_string: str, transitions: StateMachine) -> str:
  current_state = start_state  # Start state
  #print(f"Initial State: {current_state}")
  for symbol in input_string:
      if (current_state, symbol) in transitions:
          next_state = transitions[(current_state, symbol)]
          #print(f"On input '{symbol}', transition from {current_state} to {next_state}")
          current_state = next_state
      else:
          #print(f"No transition defined for input '{symbol}' from state {current_state}.")
          return "_"# Reject if there's no valid transition
  
  #print(f"Final State: {current_state}")
  return current_state 


def create_table(transitions: StateMachine, input_alphabet: List[Letter], N: int = 5) -> EqvTable:
  """
  Creates the eqv. classes (based on \\delta_w) for a given state machine.
  Only eqv. classes of length < N are being calculated

  Args:
    transitions StateMachine:
    input_alphabet (List[Letter]):
    N (int):
  """
  real_res = {}
  # Generate all possible concatenations
  all_concatenations = []
  for length in range(1, N):
      for combination in product(input_alphabet, repeat=length):
          all_concatenations.append(''.join(combination))
  # Display permutations
  for s in get_states(transitions):
    #print(f"Starting from {s}")
    res = {}
    for i, perm in enumerate(all_concatenations):
      res[perm] = simulate_fsm(s, perm, transitions)
      #print(perm)
      if(i < len(all_concatenations) - 1 and  len(all_concatenations[i]) + 1 == len(all_concatenations[i+1])):
        pass
        #print("----------------")
    real_res[s] = res
  return pd.DataFrame.from_dict(real_res)


# Create a directed graph
def plot(transitions: StateMachine, filename: str):
  dot = Digraph()
  
  # Add nodes and edges from the transition dictionary
  for (start_state, symbol), end_state in transitions.items():
      dot.node(start_state)  # add starting state node
      dot.node(end_state)    # add ending state node
      dot.edge(start_state, end_state, label=symbol)  # add transition edge
  
  # Save or render the graph
  dot.render(filename, format='png', cleanup=False)  # Saves as 'fsm_graph.png'



# Define the transitions
l1 = {
    ('q0', 'a'): 'q0',
    ('q0', 'b'): 'q1',
    ('q1', 'b'): 'q0',
    ('q1', 'c'): 'q2',
    ('q2', 'b'): 'q0'
}

#plot(transitions)


# TODO Test first and last element of tuple return
def add_representatives(transitions: StateMachine, res2: EqvTable):
  """
  Adds the smallest representative of the eqv. to the input words
  """
  is_duplicate = res2.duplicated(keep='first')
  res2['is_duplicate'] = is_duplicate
  res2['length'] = res2.index.str.len()

  # Tells us if table is really complete
  result = res2.groupby('length')['is_duplicate'].all().reset_index()

  def assign_custom_value(group):
      group['eqv_class'] = group.index[0]
      return group
  
  # Group by specific columns and apply the custom function
  res3 = res2.groupby(list(get_states(transitions))).apply(assign_custom_value, include_groups=False)
  for s in get_states(transitions):
    res3 = res3.droplevel(s)
  
  res3_sorted = res3.sort_values(by='eqv_class')
  #print(res3_sorted)
  u = res3_sorted['eqv_class'].unique()
  return (u, res3_sorted, result)


def eqv_class_to_semigroup(transitions, input_alphabet, eqv_classes) -> Semigroup:
    result = [s1 + s2 for s1 in eqv_classes for s2 in eqv_classes]
    result2 = [(s1, s2, s1 + s2) for s1 in eqv_classes for s2 in eqv_classes]
    longest_class = len(max(result, key=len))
    
    result3 = []

    eqv_classes_to_longes = create_table(transitions, input_alphabet, N = longest_class + 1)
    # TODO Check for the third tuple argument otherwise we might not have all eqv. classes
    u, class_, _= add_representatives(transitions, eqv_classes_to_longes)

    for a, b, ab in result2:
      c = class_.loc[ab]
      result3.append((a,b, c["eqv_class"]))

    df = pd.DataFrame(result3, columns=['Row', 'Column', 'Value'])
    
    # Pivot the DataFrame
    result = df.pivot(index='Row', columns='Column', values='Value')
      
    return result

def format_semitable(s: Semigroup):
  s = s.map(lambda x: f"[{x}]")
  s.index = [f"[{i}]" for i in s.index]
  s.columns = [f"[{col}]" for col in s.columns]
  return tabulate(s, headers="keys", tablefmt="grid")

#res2 = create_table(l1, ['a','b','c'], N = 5)
#u, class_, _ = add_representatives(l1, res2)
#
##print(u)
##
#r = eqv_class_to_semigroup(l1,['a','b','c'], u)
