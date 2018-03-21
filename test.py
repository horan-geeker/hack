class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        dic = {}
        for k,v in enumerate(nums):
            if target-v in dic:
                return [dic[target-v], k]
            else:
                dic[v] = k

if __name__ == '__main__':
    i,j = Solution.twoSum(Solution(), [3,2,4], 6)
    print(i, j)