import GA
import pickle
import Agent as a
import Graph

if __name__ == "__main__":
    ga = GA.GA(1024, 0.3, 0.3, 1)
    pop, log, toolbox = ga.run(10000, True)
    #get top half
    best = toolbox.top_half(pop)
    random = [a.RandAgent() for i in range(len(best))]

    #pickle population
    pop_trees = [agent.tree for agent in pop]
    pickle.dump(pop_trees, open("LastGeneration2.p", "wb"))

    #run random trials
    avg_agent, avg_rand = GA.pop_v_pop(best, random, 30)
    print("Agent Average:", avg_agent, "Random Average:", avg_rand)


    #display an agent
    print(best[0].tree)
    Graph.graphAgent(best[0], title = "Top half of Agents")