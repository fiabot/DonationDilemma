import GA
import Graph
import matplotlib.pyplot as plt
import pickle

ga = GA.GA(100, 0.3, 0.3, 10, rand_agents = 50, human_agents= 50, donation = False)
pop, log, toolbox = ga.run(10, True)


#get top half
random = [toolbox.random() for i in range(int(len(pop)/2))]
human = [toolbox.human() for i in range(int(len(pop)/2))]
GA.pop_v_pop(pop, random + random, 50, donation = False)
top_half = toolbox.top_half(pop)
best_agent = toolbox.get_best(pop)[0]

#pickle population
pop_trees = [agent.tree for agent in pop]
#pickle.dump(pop_trees, open("Prisoners_2.p", "wb")) #<-- uncomment out to save agents

print()
print("-------------------FINAL EVALUATIONS -------------------")
print()

#run random trials
avg_agent, avg_rand = GA.pop_v_pop(top_half, random, 50, donation = False)
print("Agent Average:", avg_agent, "Random Average:", avg_rand)
avg_agent, avg_human = GA.pop_v_pop(top_half, human, 50, donation = False)
print("Agent Average:", avg_agent, "Human Average:", avg_human)

avg_rand, avg_human = GA.pop_v_pop(random, human, 50, donation = False)
print("Random Average:", avg_rand, "Human Average:", avg_human)

#display results
plt.plot(log.select("gen"), log.select("rand") , label = "Random Ratios")
plt.plot(log.select("gen"), log.select("hum"), label = "Human Ratios")
plt.title("Evolved Agents Fitness Ratios over Time")
plt.ylabel("Ratio of Evolved Fitness over combined")
plt.xlabel("Generation")
plt.legend()
plt.show()
#plt.savefig('PrisonersFitness1k_2.png') #<-- uncomment out to save (must remove line 41 thought)

#display an agent

print("Best Agent: ", best_agent.tree)
Graph.graphAgent(best_agent, title = "Top Prisoner Agent", save=False) #<- set save to true to save graph