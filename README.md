# Carbonpy
A module which names straight/branched chain organic compounds, suggests conversions from one type to another, etc.
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

### Naming compounds:
Instantiate the class `Namer()` , which takes a string which contains the hydrocarbon (condensed form) and then call it with a method named `analyser()` to get the IUPAC name of the compound.

Example:
```
from carbonpy import Namer

a = Namer('CH~CH')
a.analyser()

>>> Eth-1-yne
```

Due to limitations in expressing a hydrocarbon easily, we have selected this path  
Single bond:- -  
Double bond:- =  
Triple bond:- ~  
Branches:- -([compound] (more branches...))([another branch from same carbon])- and so on  
(Branches support coming soon)

You can also get the molecular formula of the compound:
```
compound = Namer('CH~C-C~C-CH=C=C=CH2')
compound.molecular_formula()
>>> C₈H₄
```
Example- 2-Methylpropane would be expressed as (once branches are supported):
```
a = Namer('CH3-CH(CH3)-CH3').analyser()
>>> 2-Methylpropane
```

Will support naming with functional groups in the future.
