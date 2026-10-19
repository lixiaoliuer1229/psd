from collections import deque


class Solution:
    def countPaths(self, n: int, edges: list[list[int]], s: int, t: int) -> int:
        graph = [[] for _ in range(n)]
        indegree = [0] * n

        for u, v in edges:
            u -= 1
            v -= 1
            graph[u].append(v)
            indegree[v] += 1

        paths = [0] * n
        paths[s - 1] = 1

        queue = deque(i for i in range(n) if indegree[i] == 0)
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                paths[v] += paths[u]
                indegree[v] -= 1
                if indegree[v] == 0:
                    queue.append(v)

        return paths[t - 1]