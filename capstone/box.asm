// Box.asm for K = 05
// Start Row = 5 (RAM 16384 + 32*5 = 16544)
// Height = 20 rows, Width = 16 * ((5 mod 4) + 1) = 32 pixels (2 words)

(LOOP)
    @KBD
    D=M
    @SET_BLACK
    D;JNE          // If any key is pressed, set color = -1 (black)

    @color
    M=0            // Otherwise, set color = 0 (white)
    @DRAW_INIT
    0;JMP

(SET_BLACK)
    @color
    M=-1

(DRAW_INIT)
    @16544         // Starting RAM address for row 5
    D=A
    @rowAddr
    M=D

    @20            // Box height = 20 rows
    D=A
    @rowCount
    M=D

(ROW_LOOP)
    @rowCount
    D=M
    @LOOP
    D;JEQ          // If all 20 rows are drawn, return to keyboard check

    @rowAddr
    D=M
    @currAddr
    M=D            // Set pointer to start of current row

    @2             // Box width = 2 words (32 pixels)
    D=A
    @colCount
    M=D

(COL_LOOP)
    @colCount
    D=M
    @NEXT_ROW
    D;JEQ          // If both words in this row are drawn, go to next row

    @color
    D=M
    @currAddr
    A=M
    M=D            // Draw 16 pixels

    @currAddr
    M=M+1          // Move 1 word (16 pixels) right
    @colCount
    M=M-1
    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @rowAddr
    M=D+M        // Move down 1 row (32 words = 512 pixels)
    @rowCount
    M=M-1
    @ROW_LOOP
    0;JMP
