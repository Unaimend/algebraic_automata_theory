

## Installing

```
git clone https://github.com/PyCQA/bandit
conda install --f environment.yml
conda activate aat
```

## Testing
Running the tests will ensure that everything is working properly.

```
python3 -m unittest discover tests/
```


## Running the program on a given automaton
You can specify an input automaton with the `--aut` flag.
DISCLAIMER: Currently we do not ensure that eqv. classes of necessary length are tested, please provide a big enough word length to ensure that all classes are tested. This can be done with the `-N` flag. This will be fixed in future versions

```
python3 main.py --aut examples/lecture_1.csv -N 5
```

This will print the $\delta_w$ table and the corresponding semigroup
