"""
完全背包：
每种物品可以重复放入多次。
"""

# 直接在代码中给出数据，不需要用户输入
capacity = 10
items = [
    (2, 3),  # 体积 2，价值 3，可以重复选择
    (3, 4),  # 体积 3，价值 4，可以重复选择
]


def solve(items, capacity):
    # key：已经装入物品的总体积
    # value：达到该体积时能够获得的最大价值
    dp = {0: 0}

    for volume, value in items:
        # 从小到大检查体积。
        # 本轮新产生的状态可以继续使用，
        # 因此当前物品能够被重复选择。
        for current_volume in range(volume, capacity + 1):
            previous_volume = current_volume - volume

            if previous_volume in dp:
                new_value = dp[previous_volume] + value
                dp[current_volume] = max(
                    dp.get(current_volume, 0),
                    new_value,
                )

    return dp


dp = solve(items, capacity)

# 问题一：不要求恰好装满
answer1 = max(dp.values())

# 问题二：必须恰好装满；不能恰好装满时返回 0
answer2 = dp.get(capacity, 0)

print("不要求装满时的最大价值：", answer1)
print("恰好装满时的最大价值：", answer2)
