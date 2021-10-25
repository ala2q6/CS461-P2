# CS461P2 by Alex Arbuckle #


# Import <
import numpy as np
import pandas as pd

# >


def funcInitialization(size: int, file: str) -> list:

    '''  '''

    # Declaration <
    df = np.array(pd.read_csv(file, sep = '\t', header = None))
    numItem = (int(len(df) / 20))

    # >

    # Population <
    population = []
    while (len(population) < size):

        chromosome = []
        weightIndex = np.random.choice(len(df), numItem, replace = False)
        for i in range(len(df)):

            # if (Selected) else (Not Selected) <
            if (i in weightIndex): chromosome.append(['1', df[i][0], df[i][1]])
            else: chromosome.append(['0', df[i][0], df[i][1]])

            # >

        # if (New) <
        if (chromosome not in population): population.append(chromosome)

        # >

    return population

    # >


def funcFitness(size: int, load: int, population: list) -> (list, np.ndarray):
    '''  '''

    # get Utility & Weight per Chromosome <
    uListA, wList = [], []
    for c in population:

        chromosome = [[g[1], g[2]] for g in c if (g[0] == '1')]
        u, w = np.sum(chromosome, axis = 0)
        uListA.append(u)
        wList.append(w)

    # >

    # L2 Normalization <
    uListB = [(u ** 2) if (w < load) else (1) for u, w in zip(uListA, wList)]
    uListC = [(u / np.sum(uListB)) for u in uListB]

    # >

    # Sort <
    df = pd.DataFrame({'chromosome' : population, 'utility': uListC})
    ucList = df.sort_values(by = 'utility', ascending = False)

    # >

    return uListA, np.array(ucList[:size])


def funcSelection(population: np.ndarray) -> np.ndarray:
    '''  '''

    selection = np.random.choice(p = [u for c, u in population],
                                 a = len(population),
                                 replace = False,
                                 size = 2)

    return np.array([c for c, u in [population[s] for s in selection]])


def funcCrossover(selection: np.ndarray) -> list:
    '''  '''

    a, b = selection
    k = np.random.randint(0, len(selection[0]))

    return [np.concatenate([a[k:], b[:k]]), np.concatenate([b[k:], a[:k]])]


def funcMutation(selection: list) -> list:
    '''  '''

    # for gene in selection <
    output, size = [], len(selection[0])
    for c in [c for s in selection for c in s]:

        # if (1 in 10 000) <
        if (np.random.randint(0, 100) == 1):

            # Flip <
            c = ['1' if (c[0] == '0') else ('0'), c[1], c[2]]

            # >

        # >

        output.append(list(c))

    # >

    return [output[size:], output[:size]]


# Main <
if (__name__ == '__main__'):

    # Declaration <
    load, condition = 500, 0.10
    size, file = 100, 'CS461P2.txt'
    listAverage, listMaximum = [], []

    # >

    # (I -> F) <
    population = funcInitialization(size, file)
    uList, population = funcFitness(size, load, population)

    # >

    generation, notImproving = 0, False
    while (notImproving is False):

        # (S -> C -> M) <
        selection = funcSelection(population)
        crossover = funcCrossover(selection)
        offspring = funcMutation(crossover)

        # >

        # (F) <
        population = [c for c, u in population] + [o for o in offspring]
        for i in population:

            print(i)

        print()

        for i in offspring:

            print(i)

        print(len(offspring))
        print(len(offspring[0]))


        input('; ') # remove

        # >

        # Update <
        if (((generation % size) == 0) and (generation > 0)):

            listAverage.append(np.average(uList))
            listMaximum.append(np.max(uList))

        # >

        # Condition <
        if ((len(listAverage) > 10)):

            index, outcome = (len(listAverage) - 11), []
            for i in range(10):

                result = (listAverage[index + i] / listAverage[index + (i + 1)])

                # if (valid) else (not valid) <
                if ((result < 1) and (result > condition)): outcome.append(1)
                else: outcome.append(0)

                # >

            # if (not improving) <
            if (outcome.count(1) != 10): break

            # >

        # >

    # >

    # Output <


    # >

# >
