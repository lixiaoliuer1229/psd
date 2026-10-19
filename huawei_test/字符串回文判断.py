
class Solution:
    def palindromeDeletionIndices(self, s: str) -> list[int]:
        result = []
        if len(s) > 2:
            for t in s:
                ss = s.replace(t, "")
                if ss == ss[::-1]:
                    result.append(s.rindex(t))
                print(result)
        return result


Solution().palindromeDeletionIndices("abca")