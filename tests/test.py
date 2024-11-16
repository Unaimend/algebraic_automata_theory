import unittest
from src.automate import *

import unittest

class TestAutomatonToState(unittest.TestCase):

  one_state_one_trans = {
    ('q0', 'a'): 'q0',
  }

  one_state_two_trans = {
    ('q0', 'a'): 'q0',
    ('q0', 'b'): 'q1',
  }


  def test_get_states(self):
    self.assertEqual(get_states(TestAutomatonToState.one_state_one_trans), {"q0"})

    self.assertEqual(get_states(TestAutomatonToState.one_state_two_trans), {"q0", "q1"})


  def test_simulate_fsm(self):
    self.assertEqual(simulate_fsm("q0", "a", TestAutomatonToState.one_state_one_trans),
                     "q0")

    self.assertEqual(simulate_fsm("q0", "a", TestAutomatonToState.one_state_two_trans),
                     "q0")

    self.assertEqual(simulate_fsm("q0", "b", TestAutomatonToState.one_state_two_trans),
                     "q1")

    self.assertEqual(simulate_fsm("q1", "a", TestAutomatonToState.one_state_two_trans),
                     "_")

  def test_empty_machine(self):
      # Currently not possible to write a machine without transition but states
      self.assertEqual(True, True)
      
  def test_one_state_machine_table(self):
    r = create_table(TestAutomatonToState.one_state_one_trans, ['a'], N = 3)
    self.assertEqual(r.iloc[0, 0], "q0")
    self.assertEqual(r.iloc[1, 0], "q0")
    self.assertEqual(len(r), 2)

  def test_two_state_machine_table(self):
    r = create_table(TestAutomatonToState.one_state_two_trans, ['a', 'b'], N = 3)
    self.assertEqual(r.loc["a", "q0"], "q0")
    self.assertEqual(r.loc["b", "q1"], "_")
    self.assertEqual(r.loc["ab", "q0"], "q1")
    self.assertEqual(len(r), 6)


  def test_one_state_machine_representative(self):
    r = create_table(TestAutomatonToState.one_state_one_trans, ['a'], N = 3)
    _, t, _ = add_representatives(TestAutomatonToState.one_state_one_trans, r)
    self.assertEqual(list(t["eqv_class"]), ["a", "a"])


  def test_two_state_machine_representative(self):
    r = create_table(TestAutomatonToState.one_state_two_trans, ['a', "b"], N = 3)
    _, t, _ = add_representatives(TestAutomatonToState.one_state_two_trans, r)
    self.assertEqual(list(t["eqv_class"]), ["a", "a", "b", "b", "ba", "ba"])
