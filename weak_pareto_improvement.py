
def result(valuations, allocation):
    result = []
    for i in range(len(valuations)):
        temp = []
        for j in range(len(valuations[i])):
            _val = valuations[i][j]
            _alloc = allocation[i][j]
            temp.append(_val * _alloc)
        result.append(temp)
    return result

def find_weak_pareto_improvement(valuations: list[list[float]], allocation: list[list[float]], cycle: list):
    # find the ratio of values for each edge
    # players
    player = []

    for i in range(0, len(cycle) - 1, 2):
        player.append(cycle[i])  # each player is an index at the matrix 'allocation'

    print(f"number of player = {len(player)}")

    min_ratio = []
    min_loss = 100
    index = 0

    """""
    The function looks for the player (x) whose ratio =< 1 because if the ratio > 1 then
    the transfer will not benefit.
    In addition, the function is looking for the player whose maximum he can transfer is the least (call the item 'y')
    """
    for p in range(len(player)):
        min_ratio.append(1000)
        for item in range(len(valuations[0])):
            alloc_item = allocation[player[p]][item]
            if alloc_item > 0:  # the player has the item
                valueOf_item = valuations[player[p]][item]
                try:
                    ratio = valueOf_item / valuations[player[p + 1]][item]
                except:
                    ratio = valueOf_item / valuations[player[0]][item]
                if ratio < min_ratio[p]:
                    min_ratio[p] = ratio
                    if min_ratio[p] <= 1 and valueOf_item * alloc_item < min_loss:
                        min_loss = valueOf_item * alloc_item  # the minimum that player can loss
                        index = p

    for ratio in min_ratio:
        print(f"min ratio of player is: {ratio}")

    print(f"min loss of the cycle is: {min_loss}\n")

    """"
    After we have found player x, he will transfer all the contents y first,
    and thanks to this we will get rid of the edge - then every player
    after him transfers exactly the amount he earned,
    as a result no player loses, and player x can also profit.
    """
    profit = min_loss
    for i in range(index*2, 0, -2):
        alloc_toPass = profit / valuations[cycle[i]][cycle[i - 1]]
        value = allocation[cycle[i]][cycle[i - 1]]
        before = value
        print(f'before = {before}')

        allocation[cycle[i]][cycle[i - 1]] = value - alloc_toPass
        after = allocation[cycle[i]][cycle[i - 1]]
        print(f'after = {after}\n')

        allocation[cycle[i-2]][cycle[i - 1]] += alloc_toPass

        profit = value*valuations[cycle[i-2]][cycle[i - 1]]



    for i in range(len(cycle)-1, index+1, -2):
        alloc_toPass = profit / valuations[cycle[i]][cycle[i - 1]]
        value = allocation[cycle[i]][cycle[i - 1]]
        before = value
        print(f'before = {before}')

        allocation[cycle[i]][cycle[i - 1]] = value - alloc_toPass
        after = allocation[cycle[i]][cycle[i - 1]]
        print(f'after = {after}\n')

        allocation[cycle[i - 2]][cycle[i - 1]] += alloc_toPass

        profit = value * valuations[cycle[i - 2]][cycle[i - 1]]

    return allocation




"""*** Parameters you can change****"""
valuations = [[40, 30, 15, 15], [30, 5, 25, 40]]
allocation = [[0.5, 0.6, 0, 0], [0.5, 0.4, 1, 1]]
cycle = [0, 1, 1, 0, 0]
"""*** Parameters you can change****"""

_result = result(valuations, allocation)

old = f'\nold allocation:\n{allocation}\nresults:\n{_result}'
ans = find_weak_pareto_improvement(valuations, allocation, cycle)

_result = result(valuations, allocation)

new = f'\nnew allocation:\n{allocation}\nresults:\n{_result}'

print(old)
print(new)

"""""
old allocation:
[[0.5, 0.6, 0, 0], [0.5, 0.4, 1, 1]]
results:
[[20.0, 18.0, 0, 0], [15.0, 2.0, 25, 40]]

new allocation:
[[0.2, 1.0, 0, 0], [0.8, 0.0, 1, 1]]
results:
[[8.0, 30.0, 0, 0], [24.0, 0.0, 25, 40]]
"""""