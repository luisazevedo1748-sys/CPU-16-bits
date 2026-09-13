; Divide 7 por 5 e deixa o quociente no R0 e o resto no R2.
; Termina com HLT, portanto o resultado no Out fica definitivo.

        LDI   R0, 7
        LDI   R1, 5

        DIV   R0, R0, R1     ; quociente -> R0, resto -> HI
        MFHI  R2             ; resto -> R2

        ADD   R3, R2, R2     ; so para o resto ficar visivel no Out
        HLT
