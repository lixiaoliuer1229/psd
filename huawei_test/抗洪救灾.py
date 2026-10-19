
class Solution:
    def countDryRegions(
            self,
            waterLevel: int,
            rows: int,
            cols: int,
            heights: list[list[int]]
    ) -> int:

        results = []
        for rows_index ,list_rows in enumerate(heights):
            for row in list_rows:
                if row > waterLevel:
                    results.append([rows_index ,list_rows.index(row)])

        if len(results) <= 0:
            return len(results)

        item = {}
        begin_row = results[0][0]
        begin_col = results[0][1]
        for result in results:
            item[result[0]] = result[1]

        rows_nums = 1
        #只有一行
        for i in range(begin_row,rows):
            if begin_row + 1  in item:
                rows_nums += 1

        if rows_nums == 1:
            for col in range(begin_col,cols):





Solution().countDryRegions(3, 3, 3, [[4, 3, 2], [3, 2, 1], [2, 1, 0]])