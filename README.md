# The Donations Dilemma
An Analog Spin on the Prisoner's Dilemma.
By Fiona Shyne and Logan Walker

Evolutionary Computation at Union College - 2021

In this project, we explore a new approach to the well-explored Prisoner's Dilemma.
Taking inspiration from the video game series "Jackbox", we used the donations
minigame from Murder Trivia Party 2 within Jackbox Party Pack 6 as the main
source to represent and portray our analog interpretation.

The goal of this project is to determine whether or not there is a
strategy within this 'Donations Dilemma' that proves to be more superior
than random choice. To accomplish this goal, a variety of different experiments
and comparisons have been devised. Utilizing human designed strategies as well
as a baseline agent of random choice, agents are created and evolved using a GP
package, Deap. With fitness and trends acquired and visualized, we can make
comparisons between the general success of evolved agents versus those
belonging to randomness or human design.


## Preemptive Requirements (For Windows, should be similar for Linex?)

### Download Deap package

To install the Deap package, open the command prompt and run:

```
pip install deap
```

### Download networkx package

With the command prompt already open
Install the networkx package by running:

```
pip install networkx
```

### Download matplotlib package

Install the matplotlib package by running:

```
pip install matplotlib
```

### Download Sci-Kit Learn

'''
pip install -U scikit-learn
'''

## How to start/run the experiments

# Run a new GA session 
The file GA.py has an example for how to evolve agents for the prisoner's dilemma, and test agents against both human designed strageties and random stragies. Donations in the GA can be changed to true to evolve donations dilemma agents instead. 

# Test Previously Evolved Agents 
The pickle objects Pisoners.p and Ten10gens.p (NOTE: rename these) contain agents evolved for one thousand generations for prisoner's and donation dilemmas repectively. The file pickleResults.py test these agents agaisn't human and random agents in a similar fashion to GA.py and prints the results. 

# Stragety Analysis 
To look into what strageties emerged, the evolved agents were fed sample inputs and the results (either a decision or donation) were recorded. The list of results was fed into a cluster anaylsis algorithm affinity propagation (from scikit learn). These tests were done in Analysis.py for the donations dillema and PrisonerAnalysis.py for the prisoner's dillema.  

## Where are the generated graphs located?
Graphs are located in the images folder
