
import os.path
import argparse
import constant as cs

def is_number(s):
    try:
        float(s)    
        return True
    except ValueError:
        return False


def read_grammar(grammar_file):
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    a = [x.replace("->", "").split() for x in lines]
    a = [x for x in a if x]
    return a

def read_input(input_file):
    cek_komentar = False
    with open(input_file) as content:
        array = content.readlines()
        array2 = []
        hasil = [] #hasil berupa array of word yang bisa berupa terminal ataupun variable
        for i in range (len(array)):
            array2.append(array[i].split())
        for f in array2:
            for string in f:
                if cek_komentar:
                    hasil.append("word")
                elif string in cs.terminal:
                    hasil.append(string)
                    if string == '"""':
                        hasil.append("komentar")
                        cek_komentar = True
                else:
                    if is_number(string):
                        hasil.append("integer")
                    else:
                        hasil.append("word")
        hasil.append("epsilon")
    # hasil dalam bentuk array of string:
    # ['while', '(', 'word', '=', 'True', ')', ':', 'continue', 'while', '(', 'word', '=', 'False', ')', ':', 'pass', '-', 'epsilon']
    return hasil



def parse(file_grammar:str,file_input:str):
    grammar = read_grammar(file_grammar)
    inputan = read_input(file_input)
    length = len(inputan)
    print("-----------INPUT----------\n",inputan)
    CYK = [[[] for x in range(length - y)] for y in range(length)]
    """
        misal input A B C D, length = 4
        []
        [][]
        [][][]
        [][][][]
    """
    # inputan = list(enumerate(inputan))
    #mengenumerasikan, yaitu masing masing elemen diberi indeksnya
    #bentuk inputan sekarang : [(0,'while'),(1,'('),(2,'word'),....]
    j = -1
    print("length cyk 0 : ",len(CYK[0]))
    for symbol in inputan:
        found = False
    # i melambangkan angkanya, inputan melambangkan elemen
        for rule in grammar:                     # Bentuk Rule = ['S', 'WHILE_COND', 'EPSILON']
            #print("rule - ",rule[0])
            if f"'{symbol}'" == rule[1]:         # Misalnya ada terminal berbentuk 'symbol' , maka di append
                if(not(found)):
                    j += 1
                found = True
                a = Node(rule[0],symbol)
                #print(a)
                #print(j)
                CYK[0][j].append(a)

    for baris in range(2, length + 1): #berapa banyak total baris dikurang satu krn baris ke-0 sudah terisi
    # ini buat looping di parse table nya
        for kolom in range(0, length - baris + 1): #cek jumlah kolom pada satu baris
            for index_kiri in range(1, baris): #satu kotak cek berapa kali
                kotak_kiri = CYK[index_kiri - 1][kolom]
                kotak_kanan = CYK[baris - index_kiri - 1][kolom + index_kiri]
                for rule in grammar:   # Bentuk Rule = ['S', 'WHILE_COND', 'EPSILON']
                    left_nodes = [n for n in kotak_kiri if n.symbol == rule[1]]
                    if left_nodes:
                        right_nodes = [n for n in kotak_kanan if n.symbol == rule[2]]
                        CYK[baris - 1][kolom].extend(
                            [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                        )
    HASIL = filterCYK(CYK)
    return HASIL

def filterCYK(CYK: list):
    newCYK = []
    for i in range (len(CYK)):
        newArr1 = []
        for j in range (len(CYK[i])):
            newArr = []
            for k in range (len(CYK[i][j])):
                if(CYK[i][j][k].symbol not in newArr ):
                    newArr.append(CYK[i][j][k].symbol)
            newArr1.append(newArr)
        newCYK.append(newArr1)
    return newCYK


def printCYK(CYK :list):
    for i in range ((len(CYK)-1),-1,-1):
        for j in range (0,len(CYK[i])):
            print(CYK[i][j],end='')
        print()

class Node:
    """
    Digunakan untuk menyimpan informasi dari simbol non terminal. Sebuah node bisa punya maksimal
    2 anak. Bila dipanggil dalam suatu fungsi, akan mereturn simbol dari node tersebut
    """
    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2
    def __repr__(self):
        """
        Mengembalikan symbol bila dipanggil
        """
        return self.symbol

def run():
    file_grammar = input("Masukkan nama file grammar : ")
    file_input = input("Masukkan nama file input : ")
    CYK = parse(file_grammar,file_input)
    length = len(CYK) # [['DEF'], ['FUNCTION', 'VARIABLE', 'CONSTANT'] ]
    # cyk[0] -> ['DEF']
    # CYK[0][0] -> 'DEF'
    # CYK[0][0][1] -> 'E'
    # print("CYK \n",CYK)
    # for i,N in enumerate(CYK):
    #     print(i," N ",N)
    if(CYK[length-1][0] != []):
        if(f"'{CYK[length-1][0][0]}'" == "'S'"):
            print("Accepted")
        else:
            print("Syntax Error")
    else:
        print("Syntax Error")
    print("================================= CARA MENCETAK CYK ===================================")
    printCYK(CYK)


run()