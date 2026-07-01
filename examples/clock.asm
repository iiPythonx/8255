preload:
    .time   "The current time is "
    .on     " on "
    .invis  "\033[?25l"
    .show   "\033[?25h"
    .escape "\033["

fix_hour:
    sub r1, r2
    ret

fix_hour_init:
    jgt fix_hour
    ret

zero_pad:
    ldi r7, 0
    swa r7, 0x0024
    ret

zp_check:
    jlt zero_pad
    ret

am:
    ldi r1, 65
    ret

pm:
    ldi r1, 80
    ret

suffix:
    jlt am
    jge pm
    ret

unit:

    ; Colon
    ldi r7, 58
    swa r7, 0x0020

    ; Actual number
    ldi r2, 10
    cmp r1, r2      ; Check if we need to zero pad
    cal zp_check

    swa r1, 0x0024
    ret

reset:
    ldi r1, &escape
    swa r1, 0x0022

    ldi r1, 49
    swa r1, 0x0020  ; 1

    ldi r1, 50
    swa r1, 0x0020  ; 2

    ldi r1, 68
    swa r1, 0x0020  ; m

    ret

clock:

    ; Fetch hour
    lwa r1, 0x0056

    ; Check for PM
    ldi r2, 12      ; PM = Past 12
    cmp r1, r2
    cal fix_hour_init

    ; Zero padding check
    ldi r2, 10
    cmp r1, r2
    cal zp_check

    ; Hour
    swa r1, 0x0024

    ; Minute
    lwa r1, 0x0054
    cal unit

    ; Second
    lwa r1, 0x0052
    cal unit

    ; PM
    lwa r1, 0x0056
    ldi r2, 12
    cmp r1, r2
    cal suffix

    ldi r2, 32
    swa r2, 0x0020  ; Space
    swa r1, 0x0020  ; A / P
    ldi r1, 77
    swa r1, 0x0020  ; M
    ldi r1, 46
    swa r1, 0x0020  ; .

    ; Reset back to start of time section
    cal reset

    ; Sleep and repeat
    ldi r1, 500
    swa r1, 0x005E
    jmp clock

terminate:
    ldi r1, &show
    swa r1, 0x0022
    hlt

main:

    ; Hide cursor
    ldi r1, &invis
    swa r1, 0x0022

    ; Show current time message
    ldi r1, &time
    swa r1, 0x0022

    ; And start looping
    jmp clock
