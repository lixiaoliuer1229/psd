#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
# 计算所有货物完成运输的总耗时
# @param priorities int整型一维数组 到达货物的优先级
# @return int整型
#
class Solution:
    def calculateTotalTime(self, priorities: list[int]) -> int:
        import heapq
        from collections import deque

        queue = deque(priorities)
        remaining_priorities = [-priority for priority in priorities]
        heapq.heapify(remaining_priorities)
        total_time = 0

        while queue:
            priority = queue.popleft()
            total_time += 1

            if priority == -remaining_priorities[0]:
                heapq.heappop(remaining_priorities)
                total_time += priority
            else:
                queue.append(priority)

        return total_time

t = Solution().calculateTotalTime([3])
print(t)