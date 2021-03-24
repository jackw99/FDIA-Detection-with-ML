# -*- coding: utf-8 -*-
"""FDIA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gm-1v2Ni_W6SA2nVlWa-qGThd38gf6CX

# False Data Injection Attack Detection

A false data injection attack is when an external entity will insert false readings into networks collecting data from sensors. Machine Learning can be used to identify the attacks within the data.
Stages:
- Generate large data set of some kind with standard un-compromised readings
- Overwrite some readings with compromised, false readings
- Throw ML at the data
- Produce a large deep learning architecture to identify FDIA

## Data Set

- Data set is a 14 bus smart grid network. 11 consumer lines taking readings (What we are concerned with). 8 lines where energy is being produced (Wind, Solar, Coal and Gas).
- Consumers take readings of 'LoadMinPower' which is the minimum power needed for a power supply to correctly function. Otherwise, the power supply will flicker, and may go off and on rapidly.
- FDIA may inject incorrect data that damages power supplies by falsifying how much power is needed to maintain power supply health. This would cause damage to power supplies, economic damage repairing supplies and from potential network downtime while repairing. 
- Injection of false data into the acquired LoadMinPower data set from https://zenodo.org/record/1220935 to mimic FDI attack
"""

#importing library for data
import pandas as pd
import numpy as np

#read csv into dataframe
df = pd.read_csv(r'LoadMinPower.csv', sep=',', header=0)
df.head(5)

#Mean of each column
col_means = [np.array(df.get([f'{i}'])).mean() for i in range(1, 12)]
print(f" Means for all columns in the data set: \n{col_means}")

#Variance of each column
col_vars = [np.array(df.get([f'{i}'])).var() for i in range(1, 12)]
print(f" Variance for all columns in the data set: \n{col_vars}")

"""## False Data Injection
- Injecting False data into the data set to mimic a FDIA
- Then convert to appropriate format for ML
- Also need to generate labels. (1 for compromised sensor, 0 for uncompromised).
- Choose random sensors to compromise each time (np.random.choice(1,12)*5) and append a 1 for a compromised sensor, 0 for non
- Do not need to append normal noises as the data set is real, not artificially generated
- Experiment with injecting different L2 norm distances of data and seeing classification accuracy differences
- maybe negate small amounts to mimic an attacker trying to get less power than what is needed, to damage the power supplies
- assume attacker doesn't know mean and variance, so injects tiny decrements in between 0 and 1 to each target

Example of False Data Injection:
"""

#example reading at a timestep
reading = np.array([2.2, 23, 4, 0.51, 1.6, 3.2, 0.73, 0.12, 0.41, 0.19, 2.354, 1.197])
#choosing how many target values to inject into
sensors_to_attack = np.random.randint(2,6)
#getting indices of targets
targets = np.random.choice((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), sensors_to_attack, replace = False)
print(f"Targets = {targets}")
#getting values to add to targets
values_to_inject = np.random.random(sensors_to_attack)*3
print(f"Values to inject: {values_to_inject}")
#Negating from reading (Injecting)
print(f"Initial Reading: {reading}")
reading[targets] -= values_to_inject
print(f"After Injection: {reading}")

"""Creation of Labels:"""

#Creation of labels for row (0 if not injected, 1 if injected)
labels = [0 if i not in targets else 1 for i in range(11)]
labels

"""To Do:
- Loop through all rows injecting data 
- creating labels as it goes and appending to a np array
"""

