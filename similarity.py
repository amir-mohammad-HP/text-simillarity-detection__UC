# main project file
import string

class Analyzer:
    
    def __init__(self, filename:str) -> None:
        self.filename = filename 

        self.original = None
        self.lines = None
        self.legitimate_words = set()
        self.words_inline = []
        self.word_dic = {}

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
        return self.getWordDic(word).get("count") >= 2

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
    '''
    this module compare the two Analyzer instances

    the comparision is base of the nesseccary requirement on the each Analyzer module to compare 

    1- All word from Analyzer are more than 3 letter 
    2- There is no punctuation
    3- All the word from first file which is the basement of the comparision are ...
        lower case(this condition applies on both files) and repeats at least 2 times in the ...
        first file(this condition only applies for the first file) .
    
    after instantiating the module ,for being convenient only method you need to call is "getResultA" and "getResultB" 
    and you get proper result .

    although you have access to other methods as if you need to .

    '''
    comparisions_done = {}

    def __init__(self, A:Analyzer, B:Analyzer) -> None:
        self.A = A
        self.B = B
        
    def AvsB(self) -> None:
        a = self.A
        b = self.B
        self.comparisions_done["A versus B"] = self.Compare(a, b)
    
    def BvsA(self) -> None:
        a = self.B
        b = self.A
        self.comparisions_done["B versus A"] = self.Compare(a, b)

    def Compare(self, A:Analyzer, B:Analyzer) -> list:
        a = A
        b = B

        result = []
        for alineNO in range(1, a.getNumberOfLines()+1):
            
            line_comare = {}
            # iterate over lines of file a
            line_a = list(filter(lambda l: a.wordIsLegitimate(l),a.removeStylings(a.getWordsInLine(alineNO))))
            line_a = a.getRepeats(line_a) # filter words repeates atleast twise in the first file
            
            for blineNO in range(1, b.getNumberOfLines()+1):
                # iterate over files of file b
                
                line_b = list(filter(lambda l: b.wordIsLegitimate(l),b.removeStylings(b.getWordsInLine(blineNO))))
                # print(blineNO, line_b)
                if len(line_a) == 0 :
                    line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                        f'line {a.filename}': line_a,
                        f'line {b.filename}': line_b,
                        'similarity': 0,
                    }
                else:
                    if len(line_b) == 0:
                        line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                            f'line {a.filename}': line_a,
                            f'line {b.filename}': line_b,
                            'similarity': 0,
                        }
                    else:
                        line_comare[f'line {alineNO} compate to line {blineNO}'] = {
                            f'line {a.filename}': line_a,
                            f'line {b.filename}': line_b,
                            'similarity': self._compare_line_by_line(line_a, line_b),
                        }


            
            # i'm done with this line:
            result.append(line_comare)

        return result

    def _compare_line_by_line(self, line:list, compareto:list):
        '''get list of words in line (with satisfied requirements and return the similarity to caompareto'''
        common = set()
        total = set(compareto)
        for word in line:
            if word in compareto:
                common.add(word)

            total.add(word)
        return (len(common)/len(total))*100

    def getResultA(self) -> list:
        self.AvsB()
        return self.comparisions_done.get('A versus B') or ['no comarisions have been done']

    def getResultB(self) -> list:
        self.BvsA()
        return self.comparisions_done.get('B versus A') or ['no comarisions have been done']

class bcolors:
    '''just for better visualization'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


a = Analyzer('test.txt')
b = Analyzer('text1.text')

c = Compare(a, b)

print()
print(f'{bcolors.BOLD}{bcolors.WARNING} resulst for A compare to B : {bcolors.ENDC}\n')

A_B = c.getResultA()
for i in A_B:
    for (j, k) in i.items():
        print(f"{bcolors.BOLD}",j, f"=>", end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKGREEN} similarity : ", k['similarity'], end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKCYAN} file1 : ", k[f'line {a.filename}'], end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKCYAN} file2 : ", k[f'line {b.filename}'], end=f"{bcolors.ENDC}\n")
        print()
        pass

print()
print(f'{bcolors.BOLD}{bcolors.WARNING} resulst for B compare to A : {bcolors.ENDC}\n')

B_A = c.getResultB()
for i in B_A:
    for (j, k) in i.items():
        print(f"{bcolors.BOLD}",j, f"=>", end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKGREEN} similarity : ", k['similarity'], end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKCYAN} file1 : ", k[f'line {b.filename}'], end=f"{bcolors.ENDC}\n")
        print(f" {bcolors.OKCYAN} file2 : ", k[f'line {a.filename}'], end=f"{bcolors.ENDC}\n")
        print()
#         pass

