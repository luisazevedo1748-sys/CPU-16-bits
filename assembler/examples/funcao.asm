; Chama duas vezes uma funcao que duplica o R1.
; R1 comeca em 5, passa a 10, depois a 20.

        LDI   R0, dobrar     ; endereco da funcao num registo
        LDI   R1, 5

        CALL  (R0)           ; R1 -> 10
        CALL  (R0)           ; R1 -> 20

fim:    JMP   fim

dobrar: ADD   R1, R1, R1
        RET
