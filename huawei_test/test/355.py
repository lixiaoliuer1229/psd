#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 计算所有货物完成运输的总耗时
# @param priorities int整型一维数组 到达货物的优先级
# @return int整型
#
class Solution:
    def calculateTotalTime(self, priorities: list[int]) -> int:

        len_priorities = len(priorities)
        if len_priorities == 0:
            return -1

        if len_priorities == 1:
            return priorities[0] + 1

        count_times = 0
        change_priorities = priorities
        for i in range(len_priorities):

            # 优先级最高的物品
            max_good = max(change_priorities)
            max_good_index = change_priorities.index(max_good)

            count_times += max_good
            count_times += 1
            count_times += max_good_index

            if max_good_index == 0:
                change_priorities = change_priorities[1:]
            elif max_good_index == len(change_priorities) - 1:
                change_priorities = change_priorities[:-1]
            else:
                change_priorities = change_priorities[max_good_index + 1:] + change_priorities[:max_good_index]

        return count_times

result = Solution().calculateTotalTime([3, 1, 4, 2])
print(result)