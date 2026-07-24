capacity = 5

items = [
    (2, 10),
    (4, 5),
    (1, 4),
]


def solve(items, capacity):
    # key：已经选择物品的总体积
    # value：该体积下能够获得的最大价值
    dp = {0: 0}

    for volume, value in items:
        # 必须复制一份旧状态。
        # 本轮只能根据处理当前物品之前的状态产生新状态，
        # 这样每件物品才不会被重复选择。
        old_dp = dp.copy()

        for old_volume, old_value in old_dp.items():
            new_volume = old_volume + volume
            new_value = old_value + value

            if new_volume <= capacity:
                dp[new_volume] = max(
                    dp.get(new_volume, 0),
                    new_value
                )

    return dp


dp = solve(items, capacity)

# 问题一：体积不超过 capacity 即可
answer1 = max(dp.values())

# 问题二：体积必须恰好等于 capacity
answer2 = dp.get(capacity, 0)

print(answer1)
print(answer2)