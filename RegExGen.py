# ReGex generator
from difflib import SequenceMatcher

class GenRegEx:
    def __init__(self, strict=True):
        self.charRange = []
        self.uc = []
        self.inputList = None
        self.substrs = None
        self.strict = strict

    def LCS(self, X, Y, m, n):
        L = [[0 for x in range(n+1)] for x in range(m+1)]
        # Following steps build L[m+1][n+1] in bottom up fashion. Note
        # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1] 
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])
        # Following code is used to print LCS
        index = L[m][n]
        # Create a character array to store the lcs string
        lcs = [""] * (index+1)
        lcs[index] = ""
        # Start from the right-most-bottom-most corner and
        # one by one store characters in lcs[]
        i = m
        j = n
        while i > 0 and j > 0:
            # If current character in X[] and Y are same, then
            # current character is part of LCS
            if X[i-1] == Y[j-1]:
                lcs[index-1] = X[i-1]
                i-=1
                j-=1
                index-=1
            # If not same, then find the larger of two and
            # go in the direction of larger value
            elif L[i-1][j] > L[i][j-1]:
                i-=1
            else:
                j-=1
        return "".join(lcs)

    def callLCS(self, str1, str2):
        return self.LCS(str1, str2, len(str1), len(str2))

    def computeLCS(self):
        list_strs = self.inputList
        count = len(list_strs)
        lcs = self.callLCS(list_strs[0], list_strs[1])
        for i in range(1, count):
            lcs = self.callLCS(list_strs[i], lcs)
        return lcs

    def computeRegex(self):
        input_list = self.inputList
        cregex  = ""
        if self.lcs == "":
            # find lengths of shortest and longest strings in list
            sLen, lLen = 99999, 0
            for l in input_list:
                sLen = min(sLen, len(l))
                lLen = max(lLen, len(l))
            #RegEx="["+str(self.charRange(0)) + str(self.charRange(1)) + "].{" + str(sLen) + "," + str(lLen) + "}"
            cregex = "[{0}-{1}].{{{2}, {3}}}".format(str(self.charRange[0]), str(self.charRange[1]), str(sLen), str(lLen))
        else:
            subStrs = self.generateSubStrsFromLCS()
            subStrCount = len(subStrs)
            for ind in range(subStrCount-1):
                sstr1 = subStrs[ind]
                sstr2 = subStrs[ind+1]
                minMaxDist = self.distanceBetweenSubStrs(sstr1, sstr2)
                sstr1 = sstr1.replace(".", "\\.")
                sstr2 = sstr2.replace(".", "\\.")
                cregex += "{0}.[{1}-{2}].{{{3}, {4}}}.{5}".format(sstr1, str(self.charRange[0]),
                          str(self.charRange[1]), minMaxDist[0], minMaxDist[1], sstr2)
        return cregex

    def generateSubStrsFromLCS(self):
        # initialize SequenceMatcher object with 
        # input string
        cs = []
        str1 = self.inputList[0]
        seqMatch = SequenceMatcher(None, str1, self.lcs)
        # output will be like [Match(a=0, b=0, size=2), Match(a=3, b=2, size=2), Match(a=5, b=4, size=0)]
        blocks = seqMatch.get_matching_blocks()
        for block in blocks:
            if block.size > 2:
                sstr = str1[block.a:block.a+block.size]
                cs.append(sstr)
        print("substrings are: %s" %cs)
        return cs

    def distanceBetweenSubStrs(self, sstr1, sstr2):
        input_list = self.inputList
        minDist, maxDist = 9999, 0
        for inStr in input_list:
            s1index = inStr.index(sstr1)
            s2index = inStr.index(sstr2)
            dist = s2index - (s1index + len(sstr1))
            minDist = min(minDist, dist)
            maxDist = max(maxDist, dist)
        return [minDist, maxDist]

    def generateCharRanges(self):
        self.uc = sorted(set(''.join(self.inputList)))
        start = self.uc[0]
        for ch in gre.uc:
            if ch >= '0':
                start = ch
                break
        self.charRange = [start, gre.uc[-1]]
        return

    def findRegex(self, input_strs):
        print(input_strs)
        input_strs.sort()
        self.inputList = input_strs
        self.lcs = gre.computeLCS()
        self.generateCharRanges()
        print("LCS is: %s" %self.lcs)
        if (len(self.lcs) < 3):
            print("LCS len is < 3 chars, ignoring LCS")
            self.lcs = ""
        pattern  = self.computeRegex()
        print("RegEx generated is : %s" %pattern)
        return pattern

my_list = ["www.abcd.com", "www.help.com", "www.hello.com", "www.whoami.com", "www.elliot.com", "www.mrrobot.com"]
#my_list = ["1000", "10000", "9999", "12345", "1000000", "10000000", "10000001", "hello"]
#my_list = ["helo", "hellow", "qorld", "qwerty", "im noise", "im sound", "let's check"]
#my_list = ["i'm noise", "hello", "unrelted words", "www.ksrtc.co.in"]
gre = GenRegEx(strict=True)

gre.findRegex(my_list)
