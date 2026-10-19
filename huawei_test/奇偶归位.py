# @param nums list[int] — 待排序数组
# @return list[int]
class Solution:
    def sortArr(self, nums: list[int]) -> list[int]:
        sort_nums = sorted(nums)
        result = []

        z_list = [] #偶数列
        l_list = [] #奇数列
        for i in sort_nums:
            if i % 2>0:
                l_list.append(i)
            else:
                z_list.append(i)

        for index,num in enumerate(z_list):
            result.append(num)
            result.append(l_list[index])

        return result

Solution().sortArr([3, 1, 2, 4, 5, 6])