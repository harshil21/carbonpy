# Carbonpy
A module which names straight/branched chain organic compounds, suggests conversions from one type to another, etc.

[![Downloads](https://pepy.tech/badge/carbonpy)](https://pepy.tech/project/carbonpy) [![Downloads](https://pepy.tech/badge/carbonpy/month)](https://pepy.tech/project/carbonpy/month) [![Downloads](https://pepy.tech/badge/carbonpy/week)](https://pepy.tech/project/carbonpy/week) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/harshil21/carbonpy?color=orange)
## Installation

- You can install or upgrade carbonpy with:
``` 
$ pip install carbonpy --upgrade
```
- Building from source:
```
$ git clone https://github.com/harshil21/carbonpy --recursive
$ cd carbonpy
$ python setup.py install
```
## Usage

### Syntax for representing bonds:  

Single bond: -  
Double bond: =  
Triple bond: ~  

Examples: `CH3-CH3`, `CH2=CH2`, `CH~CH`

### Naming compounds:

Instantiate the class `Namer()` , which takes a string which contains the hydrocarbon (condensed form) and then call it with a method named `analyser()` to get the IUPAC name of the compound.

Example:
``` python
from carbonpy import Namer

compound = Namer('CH~CH')
print(compound.analyser())

>>> 'Eth-1-yne'
```

You can also get the molecular formula of a compound:
```python
compound = Namer('CH~C-C~C-CH=C=C=CH2')
print(compound.molecular_formula())
>>> 'C₈H₄'
```

Or get the number of carbons/hydrogens in the compound by using the attributes:
```python
compound = Namer('CH4')
carbs = compound.carbons
hydros = compound.hydrogens

print(f"Carbons: {carbs}, Hydrogens: {hydros}")

>>> 'Carbons: 1, Hydrogens: 4'
```

Once branches are supported, 2-Methylpropane would be expressed as:
```
a = Namer('CH3-CH(CH3)-CH3').analyser()
>>> 2-Methylpropane
```

Will support naming with functional groups in the future.
