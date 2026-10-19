#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param ballNum int整型 彩球数量
# @param relationNum int整型 魔力彩球影响关系数量
# @param initialColor int整型一维数组 彩球的初始颜色
# @param relation int整型二维数组 魔力彩球的影响关系内容
# @return int整型一维数组
#
class Solution:
    def WinPhoneCompetition(
        self,
        ballNum: int,
        relationNum: int,
        initialColor: list[int],
        relation: list[list[int]],
    ) -> list[int]:
        rows = [1 << i for i in range(ballNum)]
        for a, b in relation:
            rows[b - 1] |= 1 << (a - 1)

        for final_color in (0, 1):
            matrix = [
                row | ((initialColor[i] ^ final_color) << ballNum)
                for i, row in enumerate(rows)
            ]
            pivot_columns = []
            pivot_row = 0

            for column in range(ballNum):
                selected = next(
                    (
                        r
                        for r in range(pivot_row, ballNum)
                        if (matrix[r] >> column) & 1
                    ),
                    None,
                )
                if selected is None:
                    continue

                matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
                for r in range(pivot_row + 1, ballNum):
                    if (matrix[r] >> column) & 1:
                        matrix[r] ^= matrix[pivot_row]

                pivot_columns.append(column)
                pivot_row += 1

            coefficient_mask = (1 << ballNum) - 1
            if any(
                (matrix[r] & coefficient_mask) == 0
                and ((matrix[r] >> ballNum) & 1)
                for r in range(pivot_row, ballNum)
            ):
                continue

            touches = 0
            for r in range(pivot_row - 1, -1, -1):
                column = pivot_columns[r]
                rhs = (matrix[r] >> ballNum) & 1
                parity = (matrix[r] & touches).bit_count() & 1
                if rhs ^ parity:
                    touches |= 1 << column

            return [i + 1 for i in range(ballNum) if (touches >> i) & 1]

        return []