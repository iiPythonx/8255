.preload
    a: "It has been "
    b: " years since the UNIX epoch.\n"

.main
    ldi r1, 2026
    ldi r2, 1970
    sub r1, r2
    ldi r3, &a
    str r3, 0x0022
    str r1, 0x0024
    ldi r3, &b
    str r3, 0x0022
