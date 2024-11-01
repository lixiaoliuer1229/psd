
#一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法。
def frog_jump(n):
    


# 给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组(子数组最少包含一个元素)，返回其最大和。
def max_subarray(nums):
    for i in range(1, len(nums)):
        nums[i] = nums[i] + max(nums[i - 1], 0)
    return max(nums)

# 给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组(子数组最少包含一个元素)，返回其最大和及该子数组
def max_subarray_nums(nums):
    start = end = 0
    new_nums = nums.copy()
    for i in range(1, len(new_nums)):
        new_nums[i] = new_nums[i] + max(new_nums[i - 1], 0)
        if new_nums[i] == max(new_nums):
            end = i
        if max(new_nums[i - 1], 0) == 0 and new_nums[i] == max(new_nums):
            start = i

    return max(new_nums),nums[start:end+1]


if __name__ == '__main__':
    # 示例
    # print(frog_jump(5))  # 输出 8

    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(max_subarray(nums))  # 输出 6

    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4,-2,-7,-8]
    print(max_subarray_nums(nums))  # 输出 6 (6, [4, -1, 2, 1])