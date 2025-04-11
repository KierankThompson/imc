import numpy as np

minRewards = 10000
crates = [(89,8), (73,4), (20,2), (50,4), (90,10), (17, 1), (31,2), (10,1), (37,3), (80,6)]
rewards = []
for crate in crates:
    rewards.append((crate, minRewards * crate[0] / crate[1]))
rewards.sort(key=lambda x: x[1],reverse=True)
percentRewards = []
for reward in rewards:
    #print(f"Multiplier {reward[0][0]} Inhabitants: {reward[0][1]} Rewards: {reward[1]}")
    percentRewards.append((reward[0],reward[1],(minRewards*reward[0][0] / 50000 - reward[0][1])))
print()


percentRewards.sort(key=lambda x: x[2], reverse=True)
for reward in percentRewards:
    #print(f"Multiplier {reward[0][0]} Inhabitants: {reward[0][1]} Rewards: {reward[1]} Percent to Lose With Penalty {reward[2]}%")
    continue

print()
percentage = []
justRewards = [r[1] for r in rewards]
#100,000 loops
for i in range(100000):

    percentage = [0 for _ in rewards]
    s = sum(justRewards)

    #Weight probability by highest rewards
    weightedProb = [max(0,j/s) for j in justRewards]

    #Get 1000 choices
    prob = np.random.choice([i for i in range(len(justRewards))], 1000,  p=weightedProb)

    #Calculate percentage
    for p in prob:
        percentage[p] += 1
    percentage = [p / 1000 for p in percentage]
    #Check each crates reward given new prob. 0 is equal to negative reward
    for j, _ in enumerate(justRewards):
        justRewards[j] = max(0,minRewards*crates[j][0] / (crates[j][1]+(100*percentage[j])) - 500)

#Sort based on reward and print
sorted_rewards = sorted(enumerate(justRewards), key=lambda x: x[1], reverse=True)

for idx, reward in sorted_rewards:
    print(f"Multiplier {crates[idx][0]}, Inhabitants {crates[idx][1]}, Reward {reward:.4f}, Percentage {percentage[idx]:.4f}")
    

    

    
        




