import GA
import matplotlib as plt
import Graph
import pickle
import Agent
import PrisonerAgent
prisonerGA = GA.GA(100, 0.3, 0.3, 10, rand_agents = 50, human_agents= 50, donation = False)
prisonToolbox = prisonerGA.toolbox

donationGA = GA.GA(100, 0.3, 0.3, 10, rand_agents = 50, human_agents= 50, donation = True)
donationToolbox = donationGA.toolbox

#Donation Agents
trees = pickle.load(open("Ten10Gens.p", "rb"))
donationAgents = [Agent.Agent(tree=tree) for tree in trees]


donRandom = [donationToolbox.random() for i in range(int(len(donationAgents) / 2))]
donHuman = [donationToolbox.human() for i in range(int(len(donationAgents) / 2))]

#evaulate agents
GA.pop_v_pop(donationAgents, donRandom + donRandom, 50, donation = True)

#get top half
donTopHalf = donationToolbox.top_half(donationAgents, fit_attr = "savings")

GA.reset(donationAgents + donRandom + donHuman)

print()
print("-------------------Donation Results -------------------")
print()

#run random trials
avg_agent, avg_rand = GA.pop_v_pop(donTopHalf, donRandom, 50, donation = True)
print("Agent Average:", avg_agent, "Random Average:", avg_rand)
avg_agent, avg_human = GA.pop_v_pop(donTopHalf, donHuman, 50, donation = True)
print("Agent Average:", avg_agent, "Human Average:", avg_human)


#display an agent
don_best = donationToolbox.get_best(donTopHalf, fit_attr = "savings")
print(don_best[0].tree)
Graph.graphAgent(don_best[0], title = "Top Donation Agent", save = True)



# ----------- PRISONER --------------------
#------------------------------------------

trees = pickle.load(open("Prisoners.p", "rb"))
prisonAgents = [PrisonerAgent.PrisonerAgent(tree=tree) for tree in trees]


prisRandom = [prisonToolbox.random() for i in range(int(len(prisonAgents) / 2))]
prisHuman = [prisonToolbox.human() for i in range(int(len(prisonAgents) / 2))]

#evaulate agents
GA.pop_v_pop(prisonAgents, prisRandom + prisRandom, 50, donation = False)

#get top half
prisTopHalf = donationToolbox.top_half(prisonAgents, fit_attr = "savings")

GA.reset(prisonAgents + prisRandom + prisHuman)

print()
print("------------------- Prisoner Results -------------------")
print()

#run random trials
avg_agent, avg_rand = GA.pop_v_pop(prisTopHalf, prisRandom, 50, donation = False)
print("Agent Average:", avg_agent, "Random Average:", avg_rand)
avg_agent, avg_human = GA.pop_v_pop(prisTopHalf, prisHuman, 50, donation = False)
print("Agent Average:", avg_agent, "Human Average:", avg_human)


#display an agent
pris_best = prisonToolbox.get_best(prisTopHalf, fit_attr = "savings")
print("Best Tree:" , pris_best[0].tree)
Graph.graphAgent(pris_best[0], title = "Top Prisoner Agent", save = True)
