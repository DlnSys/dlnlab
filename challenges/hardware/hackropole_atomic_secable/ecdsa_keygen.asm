main:
    MOV     R0, #12     ;wordsize
    MOV     RD, =n
    MOVC    RD, R0
    MOV     R1, #256    ;192+64
    RND     R1          ;random scalar
    MOD     RC, R1
    MOV     RD, =p
    MOVC    RD, R0      ;load p in module
    JR      scalarMultiplication
;Inputs:
; k in RC
; module loaded
;Outputs:
; R0 = [k].G.x()
; R1 = [k].G.y()
scalarMultiplication:
    MOV     R6, #1
    MOV     R0, #12     ;wordsize
    MOV     R4, =tabX
    MOV     RB, R4
    ADD     R4, R4, R6
    MOV     R5, #4
    ADD     R5, R5, R4  ;assuming tabY is after tabX
    MOVCW   R4          ;R4 = @Gx
    MOVC    R4, R0      ;R4 = -Gx
    MOVCW   R5          ;R5 = @Gy
    MOVC    R5, R0      ;R5 = -Gy

    MOV     R0, RD
    SUB     R4, R0, R4  ;X = Gx
    SUB     R5, R0, R5  ;Y = Gy
    ;MOV     R6, #1      ;Z = 1 (R6 is already at value 1)

    MOV     R8, #96     ;bitsize/2
    MOV     R9, #0      ;to decrement loop counter

    JR      startLoopMultiplication
loopMultiplication:
    ;=====  Launch addition or doubling
    MOV     R0, RD
    CA      RA          ;doubling or addition
startLoopMultiplication:
    ;===== First read of scalar bits
    MOV     R0, R8
    MOV     R3, RC
    SRL     R3, R3, R0
    MOV     R0, #96     ;bitsize/2
    SRL     R2, R3, R0
    MOV     R0, #1
    AND     R2, R2, R0
    AND     R3, R3, R0
    SLL     R2, R2, R0
    XOR     R2, R2, R3
    SLL     R2, R2, R0

    MOV     R3, R9
    XOR     R2, R2, R3
    MOV     R3, =tabAtomic
    ADD     R3, R3, R2
    MOVCW   R3          ;R3 = tabAtomic[b1|b0|c]
    AND     R2, R3, R0
    SRL     R3, R3, R0
    ;MOV     R9, R2
    MOV     R0, =tabOperation
    ADD     R0, R0, R2
    MOV     RA, R0
    MOVCW   RA          ;if R2 = 0 add, doubling otherwise
    MOV     R2, RB
    ADD     R2, R2, R3
    MOV     R3, #4
    ADD     R3, R3, R2
    MOVCW   R2          ;R2 = @mGx, @mPx or @mQx
    MOVCW   R3          ;R3 = @mGy, @mPy or @mQy
    MOV     R0, #12     ;wordsize
    MOVC    R2, R0      ;R2 = mGx, mPx or mQx
    MOVC    R3, R0      ;R3 = mGy, mPy, or mQy
    XOR     R0, R2, R3
    MOV     RE, R0

    ;=====  Second read of scalar bits
    MOV     R0, R8
    MOV     R3, RC
    SRL     R3, R3, R0
    MOV     R0, #96     ;bitsize/2
    SRL     R2, R3, R0
    MOV     R0, #1
    AND     R2, R2, R0
    AND     R3, R3, R0
    SLL     R2, R2, R0
    XOR     R2, R2, R3
    SLL     R2, R2, R0

    MOV     R3, R9
    XOR     R2, R2, R3
    MOV     R3, =tabAtomic
    ADD     R3, R3, R2
    MOVCW   R3          ;R3 = tabAtomic[b1|b0|c]
    AND     R2, R3, R0
    SRL     R3, R3, R0
    MOV     R9, R2
    MOV     R0, =tabOperation
    ADD     R0, R0, R2
    MOV     RA, R0
    MOVCW   RA          ;if R2 = 0 add, doubling otherwise
    MOV     R2, RB
    ADD     R2, R2, R3
    MOV     R3, #4
    ADD     R3, R3, R2
    MOVCW   R2          ;R2 = @mGx, @mPx or @mQx
    MOVCW   R3          ;R3 = @mGy, @mPy or @mQy
    MOV     R0, #12     ;wordsize
    MOVC    R2, R0      ;R2 = mGx, mPx or mQx
    MOVC    R3, R0      ;R3 = mGy, mPy, or mQy

    MOV     R0, RE
    XOR     R0, R0, R2
    XOR     R0, R0, R3
    MUL     R0, R0, R6
    JNZR    endMultiplicationWithError

    ;=====  Update index of the scalar
    MOV     R0, R8
    MOV     RE, R3          ;save R3
    MOV     R3, R9
    SUB     R0, R0, R3
    MOV     R8, R0
    MOV     R3, RE          ;restore R3
    JCR     loopMultiplication

    ;=====  Correct the result
    MUL     R1, R6, R6
    MOD     R1, R1
    MUL     R7, R1, R6
    MOD     R7, R7
    MOV     R2, RB
    MOV     R3, #2
    ADD     R2, R2, R3
    MOV     R3, #4
    ADD     R3, R3, R2
    MOVCW   R2          ;R2 = @mPx
    MOVCW   R3          ;R3 = @mPy
    MOV     R0, #12     ;wordsize
    MOVC    R2, R0
    MOVC    R3, R0
    MOV     R0, RD
    SUB     R3, R0, R3
    CA      add

    ;=====  From Jacobian to Affine
    CA      toAffine
    STP
endMultiplicationWithError:
    MOV     R0, #0
    MOV     R1, #0
    MOV     R2, #0
    MOV     R3, #255
    STP

toAffine:
    MOV     R0, RD
    MOV     R1, #2
    SUB     R0, R0, R1
    MOV     RA, RC
    MOV     RC, R0
    POW     R2, R6      ;R2 = Z^-1
    MOV     RC, RA
    MUL     R3, R2, R2
    MOD     R3, R3      ;R3 = Z^-2
    MUL     R0, R3, R4
    MOD     R0, R0      ;R0 = x
    MUL     R1, R2, R5
    MOD     R2, R1
    MUL     R1, R2, R3
    MOD     R1, R1      ;R1 = y
    RET

;R0 = p
;R1 = Z^2
;R2 = -Xq
;R3 = -Yq
;R4 = X
;R5 = Y
;R6 = Z
;R7 = Z^3
double:
    ADD     R0, R5, R5  ;R0 = Y+Y
    MUL     R1, R0, R5  ;R1 = R0.Y = B
    MOD     R1, R1
    ADD     R5, R1, R1  ;Y2 = R1+R1
    MUL     R2, R4, R4  ;R2 = X.X
    MOD     R2, R2
    MUL     R3, R0, R6  ;R3 = R0.Z
    MOD     R3, R3
    MUL     R6, R5, R4  ;Z = Y2.X = C
    MOD     R6, R6
    MUL     R0, R1, R5  ;R0 = R1.Y2 = D
    MOD     R0, R0
    MUL     R1, R3, R3  ;Z^2 = R3.R3
    MOD     R1, R1
    ADD     R4, R2, R2  ;R4 = 2.R2
    ADD     R2, R4, R2  ;R2 = 3.R2
    MOD     R2, R2      ;R2 = 3X.X
    MUL     R4, R2, R2  ;R4 = R2.R2
    MOD     R4, R4
    SUB     R4, R4, R6  ;R4 = A.A-C
    SUB     R4, R4, R6  ;R4 = A.A-2.C
    MOD     R4, R4
    SUB     R6, R6, R4  ;R6 = C-X2
    MUL     R7, R1, R3  ;Z^3 = Z.Z^2
    MOD     R7, R7
    MUL     R5, R2, R6  ;Y2 = A.(C-X2)
    MOD     R5, R5
    SUB     R5, R5, R0  ;Y2 = A.(C-X2) - D
    MOD     R5, R5
    MOV     R6, R3
    RET

;R0 = p
;R1 = Z^2
;R2 = -Xq
;R3 = -Yq
;R4 = X
;R5 = Y
;R6 = Z
;R7 = Z^3
add:
    ADD     R2, R2, R0  ;R2 = (-Xq)+p
    MUL     R0, R2, R1  ;R0 = (-Xq).Z^2
    MOD     R0, R0
    ADD     R1, R4, R0  ;R1 = X+R0 = -E
    MUL     R2, R1, R1  ;R2 = R1.R1 = E^2
    MOD     R2, R2
    MUL     R0, R4, R2  ;R0 = X.R2 = AE^2
    MOD     R0, R0
    MUL     R4, R3, R7  ;X3 = (-Yq).Z^3
    MOD     R4, R4
    MUL     R3, R6, R1  ;R3 = R1.Z = Z.(-E)
    MOD     R3, R3
    MUL     R6, R2, R1  ;Z = R2.R1 = -E^3
    MOD     R6, R6
    ADD     R1, R0, R0  ;R1 = 2AE^2
    ADD     R2, R5, R4  ;R2 = -F
    MOD     R2, R2
    MUL     R4, R2, R2  ;R4 = F^2
    MOD     R4, R4
    SUB     R1, R1, R6  ;R1 = 2AE^2+E^3
    SUB     R4, R4, R1  ;X3 = F^2-E^3-2AE^2
    MOD     R4, R4
    SUB     R0, R0, R4  ;R0 = AE^2-X3
    MUL     R1, R5, R6  ;R1 = -C.E^3
    MOD     R1, R1
    MUL     R5, R0, R2  ;R5 = -F(AE^2-X3)
    MOD     R5, R5
    SUB     R5, R5, R1  ;Y3 = -F(AE^2-X3)+CE^3
    MOD     R5, R5
    MOV     R6, R3
    RET
tabAtomic:
    .word   1, 7, 3, 2, 5, 4, 7, 6
tabOperation:
    .word   =add, =double
tabX:
    .word   =mQx, =mGx, =mPx, =mQx
tabY:
    .word   =mQy, =mGy, =mPy, =mQy
p:
;0xfffffffffffffffffffffffffffffffffffffffeffffee37
    .word    0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xfffe, 0xffff, 0xee37
n:
;0xfffffffffffffffffffffffe26f2fc170f69466a74defd8d
    .word    0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xfffe, 0x26f2, 0xfc17, 0x0f69, 0x466a, 0x74de, 0xfd8d
mGx:
;0x24b00ef13fa81651d94f82fd7f480bcbe25a2e4d151f81ba
    .word    0x24b0, 0x0ef1, 0x3fa8, 0x1651, 0xd94f, 0x82fd, 0x7f48, 0x0bcb, 0xe25a, 0x2e4d, 0x151f, 0x81ba
mGy:
;0x64d0d09263a9d7587bbe9c2fea4179cbbf7d557626a1be9a
    .word    0x64d0, 0xd092, 0x63a9, 0xd758, 0x7bbe, 0x9c2f, 0xea41, 0x79cb, 0xbf7d, 0x5576, 0x26a1, 0xbe9a
mPx:
;0x8637294d0c49aaceee6383d4590293b5b5f5bc36c3c7ea76
    .word    0x8637, 0x294d, 0x0c49, 0xaace, 0xee63, 0x83d4, 0x5902, 0x93b5, 0xb5f5, 0xbc36, 0xc3c7, 0xea76
mPy:
;0x149bc8a41c5ecf918e5d1b2dd10231b3c69d5d5348b76319
    .word    0x149b, 0xc8a4, 0x1c5e, 0xcf91, 0x8e5d, 0x1b2d, 0xd102, 0x31b3, 0xc69d, 0x5d53, 0x48b7, 0x6319
mQx:
;0xfc448d3663c54400eb39aef34d3f5a7b9bf68f44d394e378
    .word    0xfc44, 0x8d36, 0x63c5, 0x4400, 0xeb39, 0xaef3, 0x4d3f, 0x5a7b, 0x9bf6, 0x8f44, 0xd394, 0xe378
mQy:
;0xa0dacc30925eb5e26583fbaec1203159d872c6165d3878f0
    .word    0xa0da, 0xcc30, 0x925e, 0xb5e2, 0x6583, 0xfbae, 0xc120, 0x3159, 0xd872, 0xc616, 0x5d38, 0x78f0