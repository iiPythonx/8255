preload:
    .a "It has been "
    .b " years since the UNIX epoch.\n"

main:

    ; Starting numbers
    ldi r1, 2026
    ldi r2, 1970

    ; Calculate difference
    sub r1, r2

    ; I/O
    ldi r3, &a
    swa r3, 0x0022  ; Send string &a to terminal
    swa r1, 0x0024  ; Send resulting number to terminal
    ldi r3, &b
    swa r3, 0x0022  ; Send string &b to terminal
