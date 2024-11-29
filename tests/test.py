import unittest
from src.automate import *
from typing import Optional

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



class TestSemigroupToAutomaton(unittest.TestCase):
  states = ["a", "b"]
  semigroup = pd.DataFrame( 
                           {"0":["0", "1"], 
                            "1": ["1", "0"]}
                           )
  semigroup.set_index(["0", "1"])
  
  @staticmethod
  def action1(s: State, sge: SemigroupElement) -> Optional[State]:
    if str(sge) == "0":
      return s
    elif str(sge) == "1":
      if s == "a":
        return "b"
      if s == "b":
        return "a"
    else:
      print(f"SemigroupElement {sge} with State {s}")
      raise Exception("Operation not defined")


  @staticmethod
  def action2(s: State, sge: SemigroupElement) -> Optional[State]:
    
    if str(sge) == "0":
      return s
    elif str(sge) == "1":
      if s == "a":
        return "b"
      if s == "b":
        return "b"
    else:
      print(f"SemigroupElement {sge} with State {s}")
      raise Exception("Operation not defined")


  def compatability(self):
    res = compatability(TestSemigroupToAutomaton.states, 
                        TestSemigroupToAutomaton.semigroup, 
                        TestSemigroupToAutomaton.action1)
    self.assertTrue(res)

    res = compatability(TestSemigroupToAutomaton.states, 
                        TestSemigroupToAutomaton.semigroup, 
                        TestSemigroupToAutomaton.action2)
    self.assertFalse(res)



  def semigroup_to_machine(self):
    """
    This semigroup toggles between a and b on 1 and says on a or b on 0.
    """
    #res = semigroup_to_machine((states, semigroup, action))



  def test_check_homom_single_state_2(self):
    sm1 = {
        ("q0", "a"): "q0",
      }

    sm2 = {
        ("q0'", "a"): "q0'",
      }
    data = {
      "alpha": str({"q0": "q0'"}),
      "beta": str({"a": "a"}),
      "is_homom": [True]
    }
    
    # Convert to DataFrame
    expected = pd.DataFrame(data)
    expected.sort_values(by=["alpha", "beta", "is_homom"], inplace = True, ignore_index=True)

    homoms =  try_full_homoms_beta_alpha(sm1, sm2)
    ret = homoms.equals(expected)

    self.assertTrue(ret)


  def test_check_homom_single_state_3(self):
    """
      Checks homoms from a one-state machine to a two-state machine.
      The two-state machine has two self loops with the same letter as the first. So there two homons, the first one maps q_0 to q0', the other one maps q_1 to q1'
    """
    sm1 = {
        ("q0", "a"): "q0",
      }

    sm2 = {
        ("q0'", "a"): "q0'",
        ("q1'", "a"): "q1'",
      }
    data = {
      "alpha": [str({"q0": "q0'"}), str({"q0": "q1'"})],
      "beta": [str({"a": "a"}), str({"a": "a"})],
      "is_homom": [True, True]
    }

    expected = pd.DataFrame(data)
    expected.sort_values(by=["alpha", "beta", "is_homom"], inplace = True, ignore_index=True)

    homoms =  try_full_homoms_beta_alpha(sm1, sm2)
    ret = homoms.equals(expected)

    self.assertTrue(ret)

  def test_check_homom_single_state_with_beta(self):
    """
      
    """
    sm1 = {
        ("q0", "a"): "q0",
      }

    sm2 = {
        ("q0'", "b"): "q0'",
      }
    data = {
      "alpha": ["{'q0': \"q0'\"}"],
      "beta": ["{'a': 'b'}"],
      "is_homom": [True]
    }

    ret = try_full_homoms_beta_alpha(sm1, sm2)
    expected = pd.DataFrame(data)
    expected.sort_values(by=["alpha", "beta", "is_homom"], inplace = True, ignore_index=True)

    homoms =  try_full_homoms_beta_alpha(sm1, sm2)
    ret = homoms.equals(expected)

    self.assertTrue(ret)


  def test_check_homom_single_state_4(self):
    """
      Checks homoms from a one-state machine to a three-state machine.
      The three-state machine has three self loops with the same letter as the first and one self loops with a different letter So there two homons (with beta as identity) and  the first one maps q_0 to q0', the other one maps q_1 to q1'. I guess you could also map a to b, this would result in one homo, but we need another function for that
      
    """
    sm1 = {
        ("q0", "a"): "q0",
      }

    sm2 = {
        ("q0'", "a"): "q0'",
        ("q1'", "a"): "q1'",
        ("q2'", "b"): "q2'",
      }
    data = {
      "alpha": ["{'q0': \"q0'\"}", "{'q0': \"q0'\"}", "{'q0': \"q1'\"}", "{'q0': \"q1'\"}", "{'q0': \"q2'\"}", "{'q0': \"q2'\"}"],
      "beta": ["{'a': 'a'}", "{'a': 'b'}", "{'a': 'a'}", "{'a': 'b'}", "{'a': 'a'}", "{'a': 'b'}"],
      "is_homom": [True, False, True, False, False, True]
    }

    expected = pd.DataFrame(data)
    expected.sort_values(by=["alpha", "beta", "is_homom"], inplace = True, ignore_index=True)
    homoms =  try_full_homoms_beta_alpha(sm1, sm2)
    ret = homoms.equals(expected)



  def test_check_homom_all_states_with_beta_1(self):
    """
      
    """
    sm1 = {
        ("q0", "a"): "q0",
        ("q1", "a"): "q1",
      }

    sm2 = {
        ("q0'", "a"): "q0'",
        ("q1'", "a"): "q1'",
        ("q2'", "b"): "q2'",
      }
    # Provided data as a dictionary
    data = {
        "alpha": [
            "{'q0': \"q0'\", 'q1': \"q0'\"}",
            "{'q0': \"q0'\", 'q1': \"q0'\"}",
            "{'q0': \"q0'\", 'q1': \"q1'\"}",
            "{'q0': \"q0'\", 'q1': \"q1'\"}",
            "{'q0': \"q0'\", 'q1': \"q2'\"}",
            "{'q0': \"q0'\", 'q1': \"q2'\"}",
            "{'q0': \"q1'\", 'q1': \"q0'\"}",
            "{'q0': \"q1'\", 'q1': \"q0'\"}",
            "{'q0': \"q1'\", 'q1': \"q1'\"}",
            "{'q0': \"q1'\", 'q1': \"q1'\"}",
            "{'q0': \"q1'\", 'q1': \"q2'\"}",
            "{'q0': \"q1'\", 'q1': \"q2'\"}",
            "{'q0': \"q2'\", 'q1': \"q0'\"}",
            "{'q0': \"q2'\", 'q1': \"q0'\"}",
            "{'q0': \"q2'\", 'q1': \"q1'\"}",
            "{'q0': \"q2'\", 'q1': \"q1'\"}",
            "{'q0': \"q2'\", 'q1': \"q2'\"}",
            "{'q0': \"q2'\", 'q1': \"q2'\"}"
        ],
        "beta": [
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}",
            "{'a': 'a'}",
            "{'a': 'b'}"
        ],
        "is_homom": [
            True, False, True, False, False, False, 
            True, False, True, False, False, False, 
            False, False, False, False, False, True
        ]
    }
    # Convert to DataFrame
    expected = pd.DataFrame(data)
    expected.sort_values(by=["alpha", "beta", "is_homom"], inplace = True, ignore_index=True)

    homoms = try_full_homoms_beta_alpha(sm1, sm2)
    print(homoms)
    self.assertTrue(homoms.equals(expected))


   
  #def test_check_homom_complex_1(self):
  #  sm1 = {
  #      ("q0", "a"): "q0",
  #      ("q0", "b"): "q1",
  #      ("q1", "a"): "q0",
  #      ("q1", "b"): "q2",
  #      ("q2", "a"): "q2",
  #    }

  #  sm2 = {
  #      ("q0'", "a"): "q0'",
  #      ("q0'", "b"): "q1'",
  #      ("q1'", "a"): "q0'",
  #      ("q1'", "b"): "q2'",
  #      ("q2'", "a"): "q0'",
  #      ("q2'", "c"): "q2'",
  #    }

  #  homoms = try_full_homoms_beta_alpha(sm1, sm2)
  #  print(homoms)
