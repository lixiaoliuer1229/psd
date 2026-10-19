# @param n — 关卡数量，等于 scores 长度
# @param scores — 各关卡分数，包含起点和终点，可为负数
# @return — 合法路线的最大积分，不能因为分数为负而跳过终点
class Solution:
    def maxMountainScore(self, n: int, scores: list[int]) -> int:
        max_num = 0
        if n > 1:
            for i in range(n):
                print(i, scores[i])
                if scores[i]>0:
                    max_num += scores[i]
                    print("max_num", max_num)
                else:
                    if i+2 < n:
                        if scores[i+2] < 0:
                            return max_num
                    else:
                        return max_num
            return max_num
        else:
            return scores[0]


result = Solution().maxMountainScore(5, [1, 2, -3, 4, 5])
print(result)