import pandas as pd
from graphviz import Digraph
from itertools import product
from typing import Dict, Tuple

def simulate_fsm(start_state, input_string: str, transitions: Dict[Tuple[str, str], str]) -> str:
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


# Creates the whole table until words of length N
def create_table(transitions, input_alphabet, N = 5):
  real_res = {}
  # Generate all possible concatenations
  all_concatenations = []
  for length in range(1, N):
      for combination in product(input_alphabet, repeat=length):
          all_concatenations.append(''.join(combination))
  # Display permutations
  for s in ["q0", "q1", "q2"]:
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
def plot(transitions):
  dot = Digraph()
  
  # Add nodes and edges from the transition dictionary
  for (start_state, symbol), end_state in transitions.items():
      dot.node(start_state)  # add starting state node
      dot.node(end_state)    # add ending state node
      dot.edge(start_state, end_state, label=symbol)  # add transition edge
  
  # Save or render the graph
  dot.render('fsm_graph', format='png', cleanup=False)  # Saves as 'fsm_graph.png'
  dot


def get_states(transitions):
  a = []
  for((start_state, _), end_state) in transitions.items():
    a.append(start_state)
    a.append(end_state)
  return list(set(a))

# Define the transitions
transitions = {
    ('q0', 'a'): 'q0',
    ('q0', 'b'): 'q1',
    ('q1', 'b'): 'q0',
    ('q1', 'c'): 'q2',
    ('q2', 'b'): 'q0'
}



#transitions = {
#    ('q0', 'a'): 'q0',
#    ('q1', 'a'): 'q1',
#    ('q0', 'b'): 'q1',
#    ('q1', 'c'): 'q0',
#}

#plot(transitions)




res2 = create_table(transitions, ['a','b','c'], N = 5)
print(res2)
is_duplicate = res2.duplicated(keep='first')
res2['is_duplicate'] = is_duplicate
res2['section'] = res2.index.str.len()
print(res2)
result = res2.groupby('section')['is_duplicate'].all().reset_index()

def assign_custom_value(group):
    group['eqv_class'] = group.index[0]
    return group

# Group by specific columns and apply the custom function
res3 = res2.groupby(get_states(transitions)).apply(assign_custom_value)
for s in get_states(transitions):
  res3 = res3.droplevel(s)

res3_sorted = res3.sort_values(by='eqv_class')
print(res3_sorted)
print(result)

u = res3_sorted['eqv_class'].unique()
print(u)
