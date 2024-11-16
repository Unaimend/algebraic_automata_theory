Discainers: The semigroup output still needs to be tested

## Installing

```
git clone https://github.com/Unaimend/algebraic_automata_theory.git
conda install --f environment.yml
conda activate aat
pip install graphviz
```

## Testing
Running the tests will ensure that everything is working properly.

```
python3 -m unittest discover tests/
```


## Running the program on a given automaton
You can specify an input automaton with the `--aut` flag.
DISCLAIMER: Currently we do not ensure that eqv. classes of necessary length are tested, please provide a big enough word length to ensure that all classes are tested. This can be done with the `-N` flag. This will be fixed in future versions.

```
python2 main.py --aut examples/lecture_1.csv -N 5
```

This will print the $\delta_w$ table and the corresponding semigroup.




### Plotting the automata
You can plot, layout and export the automata with the `--dot` flag.

```
python3 main.py --aut examples/lecture_1.csv -N 5 --dot test.png
```


## Automate format
To sepcify an automate via csv use the following format

```
start_state_1,letter,end_state_1
        ...
start_state_n,letter,end_state_1
```

Be careful to not include ANY whitespace.
