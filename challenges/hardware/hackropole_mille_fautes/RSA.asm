    MOV     R0, #0
    MOV     R1, #1
    MOV     R2, R1          ;initialize output with 1
loop:
    MUL     R4, R2, R6      ;current_result * A     (multiply)
    MOD     R4, R4
    AND     R3, R5, R1      ;read lsb of exponent
    MUL     R4, R3, R4      ;R4 = current_result * A if lsb is 1
    XOR     R3, R3, R1
    MUL     R2, R3, R2      ;R2 = current_result if lsb is 0
    ADD     R2, R2, R4
    POW     R6, R6          ;A**2                   (square)
    SRL     R5, R5, R1      ;drop lsb of exponent
    CMP     R5, R0          ;is exponent > 0 ?
    JNZR    loop
    STP
