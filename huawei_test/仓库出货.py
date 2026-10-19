# 借助一个栈式临时区，使货物按编号严格升序出库，求最少双向暂存次数。
# 主库和临时区都只能操作栈顶，允许双向转移；
# 不要修改 goods。
class Solution:
    def minimumStorageMoves(self, n: int, goods: list[int]) -> int:
        main, temporary = list(goods), []
        moves = 0
        for target in sorted(goods):
            print(target)

            if target in temporary:
                temporary.pop()
                moves += 1

        return moves


tt = Solution().minimumStorageMoves(6, [6,5,2,4,3,1])
print(tt)