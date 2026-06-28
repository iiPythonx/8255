.preload
    a: "It has been "
    b: " years since the UNIX epoch.\n"

.main
    ldi r1, 2026
    ldi r2, 1970
    sub r1, r2
    ldi r3, &a
    swa r3, 0x0022
    swa r1, 0x0024
    ldi r3, &b
    swa r3, 0x0022
