"""
使用字典实现一维动态规划。

字典中的 key 表示位置，value 表示该位置对应的动态规划结果。
"""


# 一只青蛙一次可以跳 1 级或 2 级台阶，
# 求跳上 n 级台阶共有多少种跳法。
def frog_jump(n):
    # dp[i]：跳上第 i 级台阶的方法数
    dp = {
        0: 1,
        1: 1,
    }

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


# 找出具有最大和的连续子数组，返回最大和。
def max_subarray(nums):
    # dp[i]：以 nums[i] 结尾的连续子数组的最大和
    dp = {0: nums[0]}

    for i in range(1, len(nums)):
        dp[i] = max(
            nums[i],                 # 从当前位置重新开始
            dp[i - 1] + nums[i],     # 接在前面的连续子数组后面
        )

    return max(dp.values())


# 找出具有最大和的连续子数组，返回最大和及该子数组。
def max_subarray_nums(nums):
    # dp[i]：以 nums[i] 结尾的连续子数组的最大和
    dp = {0: nums[0]}

    # start_positions[i]：dp[i] 对应的连续子数组从哪里开始
    start_positions = {0: 0}

    for i in range(1, len(nums)):
        if dp[i - 1] > 0:
            # 前面的和大于 0，接在前面会让结果更大
            dp[i] = dp[i - 1] + nums[i]
            start_positions[i] = start_positions[i - 1]
        else:
            # 前面的和不大于 0，从当前位置重新开始
            dp[i] = nums[i]
            start_positions[i] = i

    # 找到最大和对应的结束位置
    end = max(dp, key=dp.get)
    start = start_positions[end]

    return dp[end], nums[start:end + 1]


if __name__ == "__main__":
    # 示例一：青蛙跳台阶
    print(frog_jump(5))

    # 示例二：最大连续子数组之和
    nums1 = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(max_subarray(nums1))

    # 示例三：最大连续子数组之和，以及该子数组
    nums2 = [-2, 1, -3, 4, -1, 2, 1, -5, 4, -2, -7, -8]
    print(max_subarray_nums(nums2))
