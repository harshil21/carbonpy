# Carbonpy
A module which names straight/branched chain organic compounds, suggests conversions from one type to another, etc.

## Usage-

### Naming compounds-
Instantiate the class `Namer()` , which takes a string which contains the hydrocarbon (condensed form) and then call it with a method named `analyser()` to get the IUPAC name of the compound.

Example:
```
a = Namer('CH~CH')
a.analyser()
>>> Ethyne
```

Due to limitations in expressing a hydrocarbon easily, we have selected this path  
Single bond:- -  
Double bond:- =  
Triple bond:- ~  
Branches:- -([compound](more branches...))([another branch from same carbon])- and so on  

Will support naming with functional groups in the future soon.
