// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

  // LOOP1 is used as initialization and determine
  // whether the screen should be black or white.
  (LOOP1)
    @i
    M=0 // initialize i=0
    @8192
    D=A
    @n // n equals to the number of registers in SCREEN Memory.
    M=D
    @SCREEN
    D=A
    @addr
    M=D //addr is an address register used to specify the
          //address of the screen that needs to be modified.
          
    @KBD
    D=M
    @NOTOUCH
    D;JEQ
    @TOUCH
    0;JMP
  (NOTOUCH)
    @screen
    M=0
    @LOOP2
    0;JMP
  (TOUCH)
    @screen
    M=-1
    @LOOP2
    0;JMP // if (KBD==0): screen=0
          //     else screen=-1

  // LOOP2 in each turn, register pointed by addr becomes
  // the corresponding color, addr++, i++. 
  (LOOP2)
    @screen
    D=M
    @addr
    A=M
    M=D //M[addr]=screen   

    @addr
    M=M+1 // addr++, point to the next register in screen

    @i
    M=M+1 // i++

    @LOOP3
    0;JMP // goto LOOP3

  (LOOP3)
    @KBD
    D=M
    @NOTOUCHNEW
    D;JEQ
    @TOUCHNEW
    0;JMP
  (NOTOUCHNEW)
    @newscreen
    M=0
    @NOUSE
    0;JMP
  (TOUCHNEW)
    @newscreen
    M=-1 
    @NOUSE
    0;JMP // if (KBD==0): newscreen=0
          //     else newscreen=-1
  (NOUSE)
    @newscreen
    D=M
    @screen
    D=D-M
    @LOOP4
    D;JEQ
    @LOOP1
    0;JMP

  (LOOP4) // if (i==n) goto LOOP3, else goto LOOP2
    @i
    D=M
    @n
    D=D-M
    @LOOP3
    D;JEQ
    @LOOP2
    0;JMP
