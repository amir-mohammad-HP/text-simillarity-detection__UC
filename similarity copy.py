import string

class Analyzer:
    original = None
    lines = None
    legitimate_words = set()
    words_inline = []
    word_dic = {}


    def __init__(self, filename:str) -> None:
        self.filename = filename 
        self._readfile()
        self._clean()
        self._analyze()

    def _readfile(self) -> None:
        with open(self.filename) as file:
            self.original = file.readlines()

    def _clean(self) -> None:
        self.lines = []
        for line in self.original:
            _line = ""
            for w in line:
                _line +=  w if w not in string.punctuation else w.replace(w, " ")

            self.lines.append(_line)
            self.words_inline.append(_line.split())

        
    def _analyze(self) -> None:
        for lineNo in range(1, len(self.lines) + 1): 
            for word in self.getWordsInLine(lineNo):
                _word = self.setLegitimateWord(word)
                if _word :
                    self.countWords(_word, lineNo)

    def getLines(self):
        return self.lines

    def getLine(self, lineNo:int):
        return self.lines[lineNo - 1]

    def getNumberOfLines(self):
        return len(self.lines)

    def setLegitimateWord(self, word:str) -> None:
        if len(word) >= 3:
            word = word.strip()
            word = word.lower()

            self.legitimate_words.add(word)
            return word
        return None

    def getLegitimateWords(self):
        return list(self.legitimate_words)

    def wordIsLegitimate(self, word:str):
        return word in self.getLegitimateWords()

    def countWords(self, word:str, line:int):
        if self.word_dic.get(word):
            self.word_dic[word]['count'] += 1
            self.word_dic[word]["inline"].append(line)
            return
        self.word_dic[word] = {
            'count' : 1,
            'inline' : [line,],
        }
    
    def getWordDic(self, word):
        return self.word_dic.get(word)

    def isRepeated(self, word):
        return self.getWordDic(word).get("count") > 2

    def getRepeats(self, line:list):
        
        def _ (word):
            return self.isRepeated(word)
        return list(filter( _ , line))

    def getWordsInLine(self, lineNo:int):
        return self.words_inline[lineNo-1]

    def removeStylings(self, strList:list):
        _r = []
        for _string in strList:
            # temp = ''.join(s.lower() for s in _string if ord(s)>31 and ord(s)<126)
            temp = _string.format('ascii', errors='ignore').lower()
            _r.append(temp)

        return _r

class Compare:
    comparisions_done = {}

    def __init__(self, A:Analyzer, B:Analyzer) -> None:
        self.A = A
        self.B = B
        
    def AvsB(self):
        a = self.A
        b = self.B

        self.comparisions_done["A versus B"] = []
        for alineNO in range(1, a.getNumberOfLines()+1):
            line_comare = {}
            # iterate over lines of file a
            line_a = list(filter(lambda l: a.wordIsLegitimate(l),a.removeStylings(a.getWordsInLine(alineNO))))
            line_a = a.getRepeats(line_a) # filter words repeates atleast twise in the first file
            
            for blineNO in range(1, b.getNumberOfLines()+1):
                # iterate over files of file b
                
                line_b = list(filter(lambda l: b.wordIsLegitimate(l),b.removeStylings(b.getWordsInLine(blineNO))))
                '''
                    << probem >>
                    here is the problem because it reads the wrong file .
                    it's like because some variables defined in the main section of Analyzer class 
                    this class acts as a global variable in which the __init__ function does not call 
                    on the second assignment which is the "b" variable on the program
                    
                '''
                print(blineNO, line_b)
                if len(line_a) == 0 :
                    line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                        f'line A': line_a,
                        f'line B': line_b,
                        'similarity': 0,
                    }
                else:
                    if len(line_b) == 0:
                        line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                            f'line A': line_a,
                            f'line B': line_b,
                            'similarity': 0,
                        }
                    else:
                        line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                            f'line A': line_a,
                            f'line B': line_b,
                            'similarity': self._compare_line_by_line(line_a, line_b),
                        }


            
            # i'm done with this line:
            self.comparisions_done["A versus B"].append(line_comare)

    def _compare_line_by_line(self, line:list, compareto:list):
        '''get list of words in line (with satisfied requirements and return the similarity to caompareto'''
        common = set()
        total = set(compareto)
        for word in line:
            if word in compareto:
                common.add(word)

            total.add(word)
        return (len(common)/len(total))*100

    def getResultA(self):
        return self.comparisions_done.get('A versus B') or ['no comarisions have been done']


a = Analyzer('test.txt')
b = Analyzer('text1.text')

c = Compare(a, b)
c.AvsB()
A_B = c.getResultA()
for i in A_B:
    for (j, k) in i.items():
        # print(j, "=>")
        # print(" similarity : ", k['similarity'])
        # print(" file1 : ", k['line A'])
        # print(" file2 : ", k['line B'])
        pass

