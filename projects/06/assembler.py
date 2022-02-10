# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:48:01 2021

@author: Joyce
"""

a = open('D:/nand2tetris/projects/06/add/Add.asm')
b = open('D:/nand2tetris/projects/06/max/Max.asm')
c = open('D:/nand2tetris/projects/06/max/MaxL.asm')
d = open('D:/nand2tetris/projects/06/pong/Pong.asm')
e = open('D:/nand2tetris/projects/06/pong/PongL.asm')
f = open('D:/nand2tetris/projects/06/rect/Rect.asm')
g = open('D:/nand2tetris/projects/06/rect/RectL.asm')
h = a.read()
i = b.read()
j = c.read()
k = d.read()
l = e.read()
m = f.read()
n = g.read()

class Assembler:
    def __init__(self, content):
        self.content = content
        
    def delatecomments(self):
        
        # remove leading line comments
        while self.content[0] != '@': 
            self.content = self.content[1:]
            
        # remove in_line comments
        while '//' in self.content:
            locate = self.content.find('//')
            while True:
                if locate == self.content:
                    break
                elif self.content[locate] == '\n':
                    break
                else:
                    self.content = self.content[:locate] + self.content[locate++1:]

    def delate_space(self):
        # delate all spaces
        while ' ' in self.content:
            locate = self.content.find(' ')
            if locate == len(self.content)-1:
                self.content = self.content[:locate]
            else:
                self.content = self.content[:locate]+self.content[locate+1:]        

    def split_content(self):
        # Put each line of command into a list.
        self.content = self.content.split('\n')
        
        if '' in self.content:
            self.content.remove('')
            
    def predefined_symbols_to_decimal(self):
        # translate predefined-symbols to its decimal code.
        length = len(self.content)
        for k in range(length):
            if '@' in self.content[k]:
                if self.content[k][1:] == 'SP':
                    self.content[k] = '@0'
                elif self.content[k][1:] == 'LCL':
                    self.content[k] = '@1'
                elif self.content[k][1:] == 'ARG':
                    self.content[k] = '@2'
                elif self.content[k][1:] == 'THIS':
                    self.content[k] = '@3'
                elif self.content[k][1:] == 'THAT':
                    self.content[k] = '@4'
                elif self.content[k][1:] == 'R0':
                    self.content[k] = '@0'
                elif self.content[k][1:] == 'R1':
                    self.content[k] = '@1'
                elif self.content[k][1:] == 'R2':
                    self.content[k] = '@2'
                elif self.content[k][1:] == 'R3':
                    self.content[k] = '@3'
                elif self.content[k][1:] == 'R4':
                    self.content[k] = '@4'
                elif self.content[k][1:] == 'R5':
                    self.content[k] = '@5'
                elif self.content[k][1:] == 'R6':
                    self.content[k] = '@6'
                elif self.content[k][1:] == 'R7':
                    self.content[k] = '@7'
                elif self.content[k][1:] == 'R8':
                    self.content[k] = '@8'
                elif self.content[k][1:] == 'R9':
                    self.content[k] = '@9'
                elif self.content[k][1:] == 'R10':
                    self.content[k] = '@10'
                elif self.content[k][1:] == 'R11':
                    self.content[k] = '@11'
                elif self.content[k][1:] == 'R12':
                    self.content[k] = '@12'
                elif self.content[k][1:] == 'R13':
                    self.content[k] = '@13'
                elif self.content[k][1:] == 'R14':
                    self.content[k] = '@14'
                elif self.content[k][1:] == 'R15':
                    self.content[k] = '@15'
                elif self.content[k][1:] == 'SCREEN':
                    self.content[k] = '@16384'
                elif self.content[k][1:] == 'KBD':
                    self.content[k] = '@24576'
     
    def label_symbols_to_decimal(self):
        # create label_symbols_table
        length = len(self.content)
        l = 0
        label_symbols_table = {}
        while l < length:
            if '(' in self.content[l]:
                label_symbols_table[self.content[l][1:-1]]=str(l)
                self.content = self.content[:l] + self.content[l+1:]
                l -= 1
                length -= 1
            l += 1
        # translate label-symbols to decimal number
        for m in range(len(self.content)):
            if '@' in self.content[m]:
                if self.content[m][1:] in label_symbols_table:
                    self.content[m] = '@' + label_symbols_table[self.content[m][1:]]
               
    def variable_symbols_to_decimal(self):
        # translate variable symbols to decimal number.
        variable_symbols_table = {}
        variable_symbols_locate = 16
        length = len(self.content)
        for n in range(length):
            if '@' in self.content[n] and self.content[n][1:].isdigit() == False and self.content[n][1:] not in variable_symbols_table:
                variable_symbols_table[self.content[n][1:]] = str(variable_symbols_locate)
                variable_symbols_locate += 1
                
        for o in range(length):
            if '@' in self.content[o] and self.content[o][1:] in variable_symbols_table:
                self.content[o] = '@' + variable_symbols_table[self.content[o][1:]]
        
    def a_ins_translation(self):
        # translate to A-instruction.
        length = len(self.content)
        for i in range(length):
            if ('@' in (self.content[i])) and (type(eval((self.content[i][1:]))) == int):
                decimal = eval(self.content[i][1:])
                self.content[i] = (16-len(bin(decimal)[2:]))*'0' + bin(decimal)[2:]
    
    def c_ins_translation(self):
        # translate to C-instruction.
        length = len(self.content)
        for j in range(length):
            if '=' in self.content[j]: # no jump
                locate = self.content[j].find('=')
                dest = self.content[j][:locate]
                comp = self.content[j][locate+1:]
                jump = '000'
                self.content[j] = '111' + comp_trans_to_binary(comp) + dest_trans_to_binary(dest) + jump
            elif ';' in self.content[j]:
                locate = self.content[j].find(';')
                dest = '000'
                comp = self.content[j][:locate]
                jump = self.content[j][locate+1:]
                self.content[j] = '111' + comp_trans_to_binary(comp) + dest + jump_trans_to_binary(jump)


def comp_trans_to_binary(x):
    if x == '0':
        return '0101010'
    elif x == '1':
        return '0111111'
    elif x == '-1':
        return '0111010'
    elif x == 'D':
        return '0001100'
    elif x == 'A':
        return '0110000'
    elif x == '!D':
        return '0001101'
    elif x == '!A':
        return '0110001'
    elif x == '-D':
        return '0001111'
    elif x == '-A':
        return '0110011'
    elif x == 'D+1':
        return '0011111'
    elif x == 'A+1':
        return '0110111'
    elif x == 'D-1':
        return '0001110'
    elif x == 'A-1':
        return '0110010'
    elif x == 'D+A':
        return '0000010'
    elif x == 'D-A':
        return '0010011'
    elif x == 'A-D':
        return '0000111'
    elif x == 'D&A':
        return '0000000'
    elif x == 'D|A':
        return '0010101'
    elif x == 'M':
        return '1110000'
    elif x == '!M':
        return '1110001'
    elif x == '-M':
        return '1110011'
    elif x == 'M+1':
        return '1110111'
    elif x == 'M-1':
        return '1110010'
    elif x == 'D+M':
        return '1000010'
    elif x == 'D-M':
        return '1010011'
    elif x == 'M-D':
        return '1000111'
    elif x == 'D&M':
        return '1000000'
    elif x == 'D|M':
        return '1010101'

def dest_trans_to_binary(x):
    if x == '':
        return '000'
    elif x == 'M':
        return '001'
    elif x == 'D':
        return '010'
    elif x == 'MD':
        return '011'
    elif x == 'A':
        return '100'
    elif x == 'AM':
        return '101'
    elif x == 'AD':
        return '110'
    elif x == 'AMD':
        return '111'
    
def jump_trans_to_binary(x):
    if x == 'JGT':
        return '001'
    elif x == 'JEQ':
        return '010'
    elif x == 'JGE':
        return '011'
    elif x == 'JLT':
        return '100'
    elif x == 'JNE':
        return '101'
    elif x == 'JLE':
        return '110'
    elif x == 'JMP':
        return '111'

x = Assembler(n)
x.delatecomments()
x.delate_space()
x.split_content()
x.predefined_symbols_to_decimal()
x.label_symbols_to_decimal()
x.variable_symbols_to_decimal()
x.a_ins_translation()
x.c_ins_translation()

output = ''
for i in x.content:
    output = output + i + '\n'
with open('C:/Users/Joyce/Desktop/RectLcompare.hack','w') as f:
    f.write(output)