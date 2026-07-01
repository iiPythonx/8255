preload:
    .strftime "The current time is %H:%M:%S %p."

terminate:
    hlt

main:

    ; Send address of format string to time driver
    ldi r1, &strftime
    swa r1, 0x0054

    ; Ask time driver to write time value to 0x2100
    ldi r1, 0x2100
    swa r1, 0x0056

    ; Send that string to the terminal
    swa r1, 0x0022

    ; Sleep 500ms
    ldi r1, 500
    swa r1, 0x0058

    ; Carriage return
    ldi r1, 13
    swa r1, 0x0020

    ; Infinite loop
    jmp main
