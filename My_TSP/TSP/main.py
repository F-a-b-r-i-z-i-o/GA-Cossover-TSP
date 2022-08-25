###################################################
# Libraries used are:
# numpy -  To generate random integers as indices
# matplotlib - To plot a graph
# hydra - Create a hierarchical configuration
# loguru - library which aims to bring enjoyable logging in Python.
###################################################

from Ga_algo import *
import matplotlib.pyplot as plt
import numpy as np
import os
import hydra
from loguru import logger


logger.add('../Result/result.log')
file_name = ('../Test/dantzig42.txt')


# File Class which implements the GA algorithm which takes as input the parameters tsp_len, pop_size, distance matrix, iterations, elitism flag, crossover_type


class File:

    def __init__(self):

        # Inizialize tsp_len
        self.tsp_len = None

        # Inizialize iterations
        self.iterations = None

        # Inizialize elitism
        self.elitism = None

        # Inizialize pop_size
        self.pop_size = None

        # Inizialize file_name
        self.file_name = None

        # Inizialize crossover
        self.crossover = None

    """
        Read configuration of algoritm by the file.yaml
        Plot the path of algoritm
        Writes the best path and the best solution in the log file
    """

    # Pass data of configuration algoritm

    @hydra.main(config_name="config.yaml")
    def configsetters(cfg):
        # List of init value
        init_values = []

        # List of final value
        final_values = []

        # List of ans value
        ans_values = []

        """
            Read the configuration by the file.yaml
        """

        tsp_len = cfg.main.tsp_len
        iterations = cfg.main.iterations
        elitism = cfg.main.elitism
        pop_size = cfg.main.pop_size
        best_n = cfg.main.pop_size
        file_name = cfg.main.file_name
        crossover = cfg.main.crossover
        logger.info(cfg.main)

        cwd = os.getcwd()

        with open(file_name, 'r') as fp:
            data = fp.readlines()
        data = [[int(j) for j in i.replace("\n", "").split(',')] for i in data]

        # Create original data
        original_points = data

        pop_size = len(data)

        # Create the weights matrix
        weights = np.zeros((pop_size, pop_size), dtype=np.float64)

        # Calc eucliedean distance of data
        for i in range(pop_size):
            for j in range(pop_size):
                weights[i][j] = (original_points[i][0] - original_points[j]
                                 [0])**2 + (original_points[i][1] - original_points[j][1])**2
                weights[i][j] = weights[i][j]**0.5

         # Application of GA_ALGORITM
        obj = GAalgo(tsp_len, pop_size, weights,
                     iterations, elitism, crossover, best_n)

        # Find init value
        init_values.append(1/obj.cost(obj.population[0]))

        val, ans = obj.run_algo()

        # Print best value select
        print(val)

        # Fetching cicle
        ans_values.append(ans)

        # Fetching final value
        final_values.append(val)

        # Save log of cycle
        logger.info(ans_values)

        # Save log of best value
        logger.info(final_values)

        # Plot cost graph
        obj.graph()

        # Fetching the best solution
        pts = np.array(original_points)
        pts = pts[ans_values[0]]
        joining_pts = np.zeros((2, 2))
        joining_pts[0] = pts[-1]
        joining_pts[1] = pts[0]

        # Plot graph of city path

        plt.title("Best Solution Tour using select Crossover")

        plt.plot(pts[0][0], pts[0][1], color='orange', marker='o',
                 linestyle='dashed', label="Starting city")
        plt.plot(pts[1:, 0], pts[1:, 1], color='green',
                 marker='o', linestyle='dashed')
        plt.plot(pts[-1][0], pts[-1][1], color='blue', marker='o',
                 linestyle='dashed', label="Ending city")
        plt.plot(joining_pts[:, 0], joining_pts[:, 1],
                 color='orange', linestyle='dashed')
        plt.legend()
        plt.show()


# Running experiments
if __name__ == "__main__":
    File.configsetters()
