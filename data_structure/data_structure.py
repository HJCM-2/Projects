# From June 1, 2020 to June 20, 2020, a total of 34 articles were released, and the number of readings was 4690+.
# Attach the Python code for LeetCode.

class CQueue1(object):
    def __init__(self):
        self.items1 = []
        self.items2 = []


    def appendTail(self, value):
        """
        :type value: int
        :rtype: None
        """
        
        self.items1.append(value)


    def deleteHead(self):
        """
        :rtype: int
        """
        if self.items1:
            while self.items1:
                self.items2.append(self.items1.pop())
            x = self.items2.pop()
            while self.items2:    
                self.items1.append(self.items2.pop())
            return x
        else:
            return -1


class CQueue2(object):
    def __init__(self):
        self.items1 = []
        self.items2 = []


    def appendTail(self, value):
        """
        :type value: int
        :rtype: None
        """
        
        self.items1.append(value)


    def deleteHead(self):
        """
        :rtype: int
        """
        if self.items2: 
            return self.items2.pop()
        
        if not self.items1:
            return -1
        
        while self.items1:
            self.items2.append(self.items1.pop())
        return self.items2.pop()


# ----------------------------

class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        q1 = "([{"
        q2 = ")]}"
        p = []
        ok = True
        num = 0
        
        while num<len(s) and ok:          
            if s[num] in "([{":
                p.append(s[num])
            else:
                if not p:
                    ok = False
                else:
                    if q2.index(s[num]) != q1.index(p.pop()):
                        ok = False
            num = num + 1
        if p:
            ok = False
        return ok


class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        q = {'{':'}','[':']','(':')','?':'?'}
        p = ['?']
        
        for si in s:
            if si in q:
                p.append(si)
            elif q[p.pop()] != si:
                return False
        return len(p) == 1

# ----------------------------

class Solution(object):

    def removeDuplicates(self, S):
        """
        :type S: str
        :rtype: str
        """
        p = []
        for si in S:
            if not p:
                p.append(si)
            else:
                if si != p[len(p)-1]:
                    p.append(si)
                else:
                    p.pop()
        return "".join(p)


class Solution(object):

      def removeDuplicates(self, S):
        """
        :type S: str
        :rtype: str
        """
        p = []
        for si in S:
            if p and si == p[-1]:
                p.pop()
            else:
                p.append(si)
        return "".join(p)


# ----------------------------


class MyQueue(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.items1 = []
        self.items2 = []


    def push(self, x):
        """
        Push element x to the back of queue.
        :type x: int
        :rtype: None
        """
        self.items1.append(x)


    def pop(self):
        """
        Removes the element from in front of queue and returns that element.
        :rtype: int
        """
        if self.items2:
            return self.items2.pop()
        if not self.items1:
            return [].pop()
        while self.items1:
            self.items2.append(self.items1.pop())
        return  self.items2.pop()


    def peek(self):
        """
        Get the front element.
        :rtype: int
        """
        if self.items2:
            return self.items2[-1]
        if not self.items1:
            return [][-1]
        while self.items1:
            self.items2.append(self.items1.pop())
        return self.items2[-1]
   

    def empty(self):
        """
        Returns whether the queue is empty.
        :rtype: bool
        """
        if (not self.items1) and (not self.items2):
            return True
        else:
            return False

# ----------------------------


class Solution(object):
    def calPoints(self, ops):
        """
        :type ops: List[str]
        :rtype: int
        """
        p2 = []
        p3 = [0]
    
        for s in ops:
            if s == '+':
                p2.append(p2[-1] + p2[-2])
                p3.append(p3[-1] + p2[-1])
            elif s == 'D':
                p2.append(p2[-1] * 2)
                p3.append(p3[-1] + p2[-1])
            elif s == 'C':
                p2.pop()
                p3.pop()
            else:
                p2.append(int(s))
                p3.append(p3[-1] + p2[-1]) 
                
        return p3.pop()


# ----------------------------


class Solution(object):
    def calPoints(self, ops):
        """
        :type ops: List[str]
        :rtype: int
        """
        p2 = []
    
        for s in ops:
            if s == '+':
                p2.append(p2[-1] + p2[-2])
            elif s == 'D':
                p2.append(2 * p2[-1])
            elif s == 'C':
                p2.pop()
            else:
                p2.append(int(s)) 
                
        return sum(p2)
    

# ----------------------------

class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.minstack = []


    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if not self.stack or self.minstack[-1] >= x:
            self.minstack.append(x)
            
        self.stack.append(x)



    def pop(self):
        """
        :rtype: None
        """
        if self.stack[-1] == self.minstack[-1]:
            self.minstack.pop()
        self.stack.pop()


    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1]


    def getMin(self):
        """
        :rtype: int
        """
        return self.minstack[-1]



class MinStack(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.minstack = [float('inf')]


    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
            
        self.stack.append(x)
        self.minstack.append(min(x, self.minstack[-1]))



    def pop(self):
        """
        :rtype: None
        """
        self.minstack.pop()
        self.stack.pop()


    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1]


    def getMin(self):
        """
        :rtype: int
        """
        return self.minstack[-1]

# ----------------------------

class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        nums3 = []
        nums = []
        
        for j in range(len(nums2)-1):
            for z in range(j+1, len(nums2)):
                if nums2[j] < nums2[z]:
                    nums3.append(nums2[z])
                    break
            else:
                nums3.append(-1)
        nums3.append(-1)
        
        for i in range(len(nums1)):
            for k in range(len(nums2)):
                 if nums1[i] == nums2[k]:
                    nums.append(nums3[k])
                    break
        return nums          


                    
class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        nums3 = []
        nums = []
        a = {}
        if nums2:
            for j in range(len(nums2)-1):
                for z in range(j+1, len(nums2)):
                    if nums2[j] < nums2[z]:
                        nums3.append(nums2[z])
                        a[nums2[j]] = nums2[z]
                        break
                else:
                    nums3.append(-1)
                    a[nums2[j]] = -1
                    
            nums3.append(-1)
            a[nums2[-1]] = -1
            
                    
            for i in nums1:
                nums.append(a[i])
            return nums
        else:
            return []          


                    
                    
class Solution(object):
    def nextGreaterElement(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        
        s = []
        a = {}
        x = []
        for i in range(len(nums2)):
            while s and nums2[i]>s[-1]:
                a[s.pop()] = nums2[i]
            s.append(nums2[i])
            
        while s:
            a[s.pop()] =  -1
        
        for j in nums1:
            x.append(a[j])

        return x

# ----------------------------

class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        s = []
        p = []
        if not nums or k == 0:
            return []
        for ki in range(k):
            while s and s[-1] < nums[ki]:
                s.pop()
            s.append(nums[ki])
        p.append(s[0])
        
        for i in range(k, len(nums)):
            if s[0] ==  nums[i-k]:
                s.pop(0)
            while s and s[-1] < nums[i]:
                s.pop()
            s.append(nums[i])
            p.append(s[0])
            
        return p



class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        s = collections.deque()
        p = []
        if not nums or k == 0:
            return []
        for ki in range(k):
            while s and s[-1] < nums[ki]:
                s.pop()
            s.append(nums[ki])
        p.append(s[0])
        
        for i in range(k, len(nums)):
            if s[0] ==  nums[i-k]:
                s.popleft()
            while s and s[-1] < nums[i]:
                s.pop()
            s.append(nums[i])
            p.append(s[0])
            
        return p



class Solution(object):
   def maxSlidingWindow(self, nums, k):
      """
      :type nums: List[int]
      :type k: int
      :rtype: List[int]
      """
      if not nums or k== 0:
          return []
      
      s = max(nums[:k])
      p = [s]
      i = 1
      j = k + 1
      
      while j <= len(nums):
          if s == nums[i-1]:
              s = max(nums[i:j])
          elif s < nums[j-1]:
              s = nums[j-1]
          p.append(s)
          i = i + 1
          j = j + 1
          
      return p

# ----------------------------


class Solution(object):
    def buildArray(self, target, n):
        """
        :type target: List[int]
        :type n: int
        :rtype: List[str]
        """
        s = []
        for i in range(1, int(target[-1])+1):
            if i in target:
                s.append("Push")
            else:
                s.append("Push")
                s.append("Pop")

        return s          
                



class Solution(object):
    def buildArray(self, target, n):
        """
        :type target: List[int]
        :type n: int
        :rtype: List[str]
        """
        s = []

        for i in range(1, n+1):
            if target:
                if i in target:
                    s.append("Push")
                    target.pop(0)
                else:
                    s.append("Push")
                    s.append("Pop")
            else:
                break
        
        return s          
                    

class Solution(object):
    def buildArray(self, target, n):
        """
        :type target: List[int]
        :type n: int
        :rtype: List[str]
        """
        from collections import deque
        s = []
        target = deque(target)

        for i in range(1, n+1):
            if target:
                if i in target:
                    s.append("Push")
                    target.popleft()
                else:
                    s.append("Push")
                    s.append("Pop")
            else:
                break
        
        return s            

# ----------------------------


class Solution(object):
    def backspaceCompare(self, S, T):
        """
        :type S: str
        :type T: str
        :rtype: bool
        """
        s = []
        p = []
        for i in S:
                if i != "#":
                    s.append(i)
                elif s:
                    s.pop()               

        for i in T:
            if i != "#":
                p.append(i)
            elif p:
                p.pop()
                
        if s == p:
            return True
        else:
            return False


class Solution(object):
    def backspaceCompare(self, S, T):
        def F(S):
            skip = 0
            for x in reversed(S):
                if x == '#':
                    skip += 1
                elif skip:
                    skip -= 1
                else:
                    yield x

        return all(x == y for x, y in itertools.izip_longest(F(S), F(T)))
        
# ----------------------------

class Solution(object):
    def removeOuterParentheses(self, S):
        """
        :type S: str
        :rtype: str
        """
        s = []
        p = []
        n = 0
        for i in range(len(S)):
            if S[i] == "(":
                s.append("(")
            else:
                while len(s) > 1:
                        p.append(s.pop())
                        n = n + 1
                if n > 0:
                    p.append(")")
                    n = n - 1
                else:
                    s.pop()
        return "".join(p)


class Solution(object):
    def removeOuterParentheses(self, S):
        """
        :type S: str
        :rtype: str
        """
        s = []
        p = ""
        n = 0
        for i in range(len(S)):
            if S[i] == "(":
                s.append(S[i])
            else:
                while len(s) > 1:
                        p = p + s.pop()
                        n = n + 1
                if n > 0:
                    p = p + S[i]
                    n = n - 1
                else:
                    s.pop()
        return p


class Solution(object):
    def removeOuterParentheses(self, S):
        """
        :type S: str
        :rtype: str
        """
        s = []
        p = ""
        for i in S:
            if i == "(":
                s.append(i)
                if len(s) > 1:
                    p = p + "("
            else:
                s.pop()
                if len(s) != 0:
                    p = p + ")"                      
        return p

# ----------------------------


class RecentCounter(object):

    def __init__(self):
        self.items = []
        self.n = 0
        

    def ping(self, t):
        """
        :type t: int
        :rtype: int
        """
        self.items.append(t)
        self.n = self.n + 1
        
        while self.items[0] < t-3000:
            self.items.pop(0)
            self.n = self.n - 1
  
        return self.n      


class RecentCounter(object):

    def __init__(self):
        self.items = collections.deque()
        

    def ping(self, t):
        """
        :type t: int
        :rtype: int
        """
        self.items.append(t)
        
        while self.items[0] < t-3000:
            self.items.popleft()
   
        return len(self.items)



class RecentCounter(object):

    def __init__(self):
        self.items = collections.deque()
        self.n = 0
        

    def ping(self, t):
        """
        :type t: int
        :rtype: int
        """
        self.items.append(t)
        self.n = self.n + 1
        
        while self.items[0] < t-3000:
            self.items.popleft()
            self.n = self.n - 1
  
        return self.n      

# ----------------------------

class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        votes = 0
        for num in nums:
            if votes == 0:
                x = num
            if num == x:
                votes = votes + 1
            else:
                votes = votes - 1
        return x


class Solution(object):
    def majorityElement(self, nums):
        votes = 0
        for num in nums:
            if votes == 0: x = num
            votes += 1 if num == x else -1
        return x


# ----------------------------

class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        for i in nums:
            if i >= 0:
                break
        else:
            return max(nums)
        
        max1 = 0
        save = 0
              
        for num in nums:
            if num + max1 > 0:
                max1 += num
            else:
                max1 = 0
                
            if max1 > save:
                save = max1
        
        return save


class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max1 = nums[0]
        for i in nums:
            if i >= 0:
                break
            elif max1 < i:
                max1 = i
        else:
            return max1
         
        max1 = 0
        save = 0

        for num in nums:
            if num + max1 > 0:
                max1 += num
            else:
                max1 = 0
                
            if max1 > save:
                save = max1
 
        return save


class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        max1 = float('-inf')
        save = float('-inf')
           
        for num in nums:
            max1 = max(num, num+max1)
            save = max(save, max1)              
           
        return save

# ----------------------------


class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        x1 = x2 = ListNode(0)
        while l1 and l2:
            if l1.val <= l2.val:
                x1.next, l1 = l1, l1.next
            else:
                x1.next, l2 = l2, l2.next
            x1 = x1.next
        x1.next = l1 if l1 else l2
            
        return x2.next

# ----------------------------


class Solution(object):
    def isSubsequence(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        if not s:
            return True
        
        i = 0
        j = 0
        while i < len(t):
            if s[j] == t[i]:
                j += 1
            i += 1
            if j == len(s):
                return True
        else:
            return False

# ----------------------------


class Solution(object):
    def minDeletionSize(self, A):
        n = 0
        for col in zip(*A):
            if any(col[i] > col[i+1] for i in xrange(len(col) - 1)):
                n += 1
        return n
                  

class Solution(object):
    def minDeletionSize(self, A):
        n = 0
        for col in zip(*A):
            for i in xrange(len(col) - 1):
                if col[i] > col[i+1]:
                    n += 1
                    break
        return n


# ----------------------------


class Solution(object):
    def minCostToMoveChips(self, chips):
        """
        :type chips: List[int]
        :rtype: int
        """
        x = 0
        y = 0
        for i in chips:
            if i % 2 == 1:
                x += 1
            else:
                y += 1
        return min(x, y)
                

# ----------------------------


class Solution(object):
    def minSubsequence(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        a =  sorted(nums,reverse=True)
        i = 0
        j = len(a)-1
        if not nums:
            return []

        left_sum = a[0]
        right_sum = a[len(a)-1]
        while i < j:
            if left_sum > right_sum:
                j -= 1
                right_sum += a[j]
            else:
                i += 1
                left_sum += a[i]
        return a[:j+1]
                
# ----------------------------

class Solution(object):
    def twoCitySchedCost(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """
        s = []
        n = 0
        for i in range(len(costs)):
            s.append(costs[i][0]-costs[i][1])
            
        a = sorted(range(len(s)), key=lambda k: s[k])           
        for j in range(len(a)//2):
            n += costs[a[j]][0]
        for j in range(len(a)//2,len(a)):
            n += costs[a[j]][1]
        return n


class Solution(object):
    def twoCitySchedCost(self, costs):
        """
        :type costs: List[List[int]]
        :rtype: int
        """
        n = 0
        costs.sort(key = lambda x : x[0] - x[1])
        len1 = len(costs)//2
        
        for i in range(len1):
            n += costs[i][0] +  costs[i+len1][1]
       
        return n

# ----------------------------


class Solution(object):
    def lemonadeChange(self, bills):
        """
        :type bills: List[int]
        :rtype: bool
        """
        if bills[0] != 5:
            return False
        i5 = 0
        i10 = 0
        
        for bill in bills:
            if bill == 5:
                i5 += 1
            elif bill == 10:
                i5 -= 1
                i10 += 1
            else:
                if i10:
                    i10 -= 1
                    i5 -= 1
                else:
                    i5 -= 3
            if i5 < 0:
                return False
        return True

# ----------------------------

class Solution(object):
    def robotSim(self, commands, obstacles):
        """
        :type commands: List[int]
        :type obstacles: List[List[int]]
        :rtype: int
        """
        x = 0
        y = 0
        n1 = 0
        max_distance = 0    
        for i in range(len(commands)):
            if commands[i] == -1:
                n1 += 1
                continue
            elif commands[i] == -2:
                n1 += 3
                continue
            else:
                n1 = n1 % 4
                if n1 == 0:
                    for j in range(commands[i]):
                        y += 1
                        if [x,y] in obstacles:
                            y -= 1
                            break
                elif n1 == 1:
                    for j in range(commands[i]):
                        x += 1
                        if [x,y] in obstacles:
                            x -= 1
                            break
                elif n1 == 2:
                    for j in range(commands[i]):
                        y -= 1
                        if [x,y] in obstacles:
                            y += 1
                            break
                else:
                    for j in range(commands[i]):
                        x -= 1
                        if [x,y] in obstacles:
                            x += 1
                            break
            max_distance = max(x**2+y**2,max_distance)
        return max_distance



class Solution(object):
    def robotSim(self, commands, obstacles):
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        x = y = di = 0
        obstacleSet = set(map(tuple, obstacles))
        ans = 0

        for cmd in commands:
            if cmd == -2:  #left
                di = (di - 1) % 4
            elif cmd == -1:  #right
                di = (di + 1) % 4
            else:
                for k in xrange(cmd):
                    if (x+dx[di], y+dy[di]) not in obstacleSet:
                        x += dx[di]
                        y += dy[di]
                        ans = max(ans, x*x + y*y)

        return ans


# ----------------------------

class Solution(object):
    def balancedStringSplit(self, s):
        """
        :type s: str
        :rtype: int
        """

        if not s:
            return 0
        
        n = 0
        x = s[0]
        num = 0
        
        for i in range(len(s)-1):
            if s[i] == x:
                n += 1
            else:
                n -= 1
                
            if n == 0:
                x = s[i+1]
                num += 1
            
        return num+1


class Solution(object):
    def balancedStringSplit(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = 0
        num = 0
        
        for i in s:
            if i == "L":
                n += 1
            else:
                n -= 1
                
            if n == 0:
                num += 1
            
        return num

# ----------------------------


class Solution(object):
    def lastStoneWeight(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """
        if not stones:
            return 0
        stones.sort(reverse=True)
        while len(stones) > 1:
            x = stones[0]-stones[1]
            stones.pop(0)
            stones.pop(0)
            for i in range(len(stones)):
                if x >stones[i]:
                    stones.insert(i,x)
                    break
            else:
                stones.append(x)
          
        return stones[0]


class Solution(object):
    def lastStoneWeight(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """
        if not stones:
            return 0
            
        stones.sort()
        while len(stones) > 1:
            x = stones.pop()-stones.pop()
            for i in range(len(stones)):
                if x <stones[i]:
                    stones.insert(i,x)
                    break
            else:
                stones.append(x)
          
        return stones[0]


# ----------------------------

class Solution(object):
    def findContentChildren(self, g, s):
        """
        :type g: List[int]
        :type s: List[int]
        :rtype: int
        """
        num = 0
        i = 0
        j = 0
        g.sort()
        s.sort()

        if s and g and s[0] > g[-1] and len(s)>=len(g):
            return len(g)
        else:
            while i < len(g) and j< len(s):
                if g[i] <= s[j]:
                    i += 1
                    j += 1
                    num += 1
                else:
                    j += 1
            return num

# ----------------------------


class Solution(object):
    def largestSumAfterKNegations(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        A.sort()

        while K > 0:
            if A[0] == 0:
                return sum(A)
            elif A[0] < 0:
                A.append(-A.pop(0))
                K -= 1
            else:
                if K % 2 == 0:
                    return sum(A)
                else:
                    return sum(A)-2*min(A)
        return sum(A)


class Solution(object):
    def largestSumAfterKNegations(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        A.sort()

        while K > 0:
            if A[0] < 0:
                A.append(-A.pop(0))
                K -= 1
            else:
                if K % 2 == 0:
                    return sum(A)
                else:
                    return sum(A)-2*min(A)
        return sum(A)


# ----------------------------

class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        prices.reverse()
        max_prices = 0
        num = 0
        for i in range(len(prices)):
            if prices[i] >= max_prices:
                max_prices = prices[i]
            else:
                num = max(max_prices - prices[i],num)
        return num



class Solution(object):
    def maxProfit(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        min_prices = int(1e9)
        num = 0
        for i in range(len(prices)):
            if prices[i] <= min_prices:
                min_prices = prices[i]
            else:
                num = max(prices[i]-min_prices, num)
        return num

# ----------------------------


class Solution(object):
    def divingBoard(self, shorter, longer, k):
        """
        :type shorter: int
        :type longer: int
        :type k: int
        :rtype: List[int]
        """
        if not k:
            return []
        if shorter == longer:
            return [shorter*k]
     
        return range(shorter * k, longer * k + 1, longer - shorter)      


# ----------------------------


class Solution(object):
    def tribonacci(self, n):
        """
        :type n: int
        :rtype: int
        """
        import collections
        d = collections.deque()
        d.append(0)
        d.append(1)
        d.append(1)
        d.append(2)
        x = 3
        if n < 4:
            return d[n]
        else:
            while x<n:
                d.popleft()
                d.append(sum(d))
                x += 1
                
        return d.pop()


# ----------------------------

class Solution(object):
    def fib(self, n):
        """
        :type n: int
        :rtype: int
        """
        import collections
        d = collections.deque()
        d.append(0)
        d.append(1)
        d.append(1)
        x = 2
        if n < 3:
            return d[n]
        else:
            while x<n:
                d.popleft()
                d.append(sum(d) % 1000000007)
                x += 1
        return d.pop()



class Solution(object):
    def fib(self, n):
        """
        :type n: int
        :rtype: int
        """
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a % 1000000007


# ----------------------------


class Solution(object):
    def hanota(self, A, B, C):
        """
        :type A: List[int]
        :type B: List[int]
        :type C: List[int]
        :rtype: None Do not return anything, modify C in-place instead.
        """
        n = len(A)
        self.move(n, A, B, C)
    def move(self,n, A, B, C):
        if n == 1:
            C.append(A.pop())
            return
        else:
            self.move(n-1,A,C,B)
            C.append(A.pop())
            self.move(n-1,B,A,C)


# ----------------------------


class Solution(object):
    def numWays(self, n):
        """
        :type n: int
        :rtype: int
        """
        a, b = 0, 1
        num = 1
        for _ in range(n-1):
            a, b = b , a+b
            num = (num + a) % 1000000007
        return num


# ----------------------------

class Solution(object):
    def isBalanced(self, root):        
        if root is None:
            return True
        if abs(self.check_height(root.left) - self.check_height(root.right))>1:
            return False
        return self.isBalanced(root.left) and self.isBalanced(root.right) 
        
    def check_height(self,root):
        if not root:
            return 0
        height = max(self.check_height(root.left), self.check_height(root.right))
        return height+1
        

class Solution(object):
  def __init__(self):
      self.flag = True
  
  def isb(self, root):
      if not root:
          return 0
      l = self.isb(root.left) + 1
      r = self.isb(root.right) + 1
      if abs(l-r)>1:
          self.flag = False
      return max(l,r)
      
  def isBalanced(self, root):
      """
      :type root: TreeNode
      :rtype: bool
      """
      self.isb(root)
      return self.flag


class Solution(object):
    def __init__(self):
        self.flag = True
        
    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        
        def isb(root):
            if not root:
                return 0
            l = isb(root.left) + 1
            r = isb(root.right) + 1
            if abs(l-r)>1:
                self.flag = False
            return max(l,r)
        isb(root)
        return self.flag

# ----------------------------

class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: int
        """
        if not root:
            return 0
        return self.dfs(root,sum) + self.pathSum(root.left, sum) + self.pathSum(root.right, sum)
        
    def dfs(self,root,path):
        if not root:
            return 0
        path -= root.val
        return (1 if path == 0 else 0) + self.dfs(root.left,path) + self.dfs(root.right,path)


class Solution(object):
    def pathSum(self, root, sum):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: int
        """
        def dfs(root,sumlist):
            if not root:
                return 0
            sumlist = [num+root.val for num in sumlist]
            sumlist.append(root.val)
            
            return sumlist.count(sum) + dfs(root.left,sumlist)+dfs(root.right,sumlist)
            
        return dfs(root,[])














