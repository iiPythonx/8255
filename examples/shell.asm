; Copyright (c) 2026 iiPython

preload:
    .clear     "\033[2J\033[H"
    .return    "\033[2K\r"
    .prompt    "\033[32m$\033[0m "
    .greeting  "\nWelcome to \033[32mNocturne Shell\033[0m!\nCopyright (c) 2026 iiPython\n\n"
    .goodbye   "\n\033[31mGoodbye!\033[0m\n"
    .no_cmd    "\033[32mNocturne\033[0m: no such command exists!\n"
    .version   "\033[32mNocturne Shell\033[0m v0.2.0, powered by \033[34m8255\033[0m.\n"
    .help      "Commands: \033[32mhelp\033[0m, \033[32mmem\033[0m, \033[32mdate\033[0m, \033[32mclear\033[0m, \033[32mversion\033[0m, \033[32mexit\033[0m\n"
    .strftime  "%a %b %-d %H:%M:%S %p %Z %Y\n"
    .mem1      "Probing... "
    .mem2      "\rMemory usage: "
    .mem3      " B / 4096 B ("
    .mem4      "%)\n"

    ; Commands
    .str_version "version"
    .str_help    "help"
    .str_exit    "exit"
    .str_clear   "clear"
    .str_mem     "mem"
    .str_date    "date"

terminate:
    ldi r1, 10
    swa r1, D_WRITE_CHR
    ldi r1, &goodbye
    swa r1, D_WRITE_STR
    hlt

write:
    ldi r1, &return
    swa r1, D_WRITE_STR

    ; Prompt
    ldi r1, &prompt
    swa r1, D_WRITE_STR

    ; String write
    ldi r1, 0x2400
    swa r1, D_WRITE_STR
    ret

check_failed:
    ldi r1, 1
    ret

_check_left:
    ldi r8, 1
    ret

_check_left_fail:
    ldi r8, 0
    ret

check_left:
    ldi r7, 0
    cmp r3, r7
    jeq _check_left
    jne _check_left_fail
    ret

_check_right:
    ldi r9, 1
    ret

_check_right_fail:
    ldi r9, 2
    ret

check_right:
    ldi r7, 0
    cmp r4, r7
    jeq _check_right
    jne _check_right_fail
    ret

cmd_read_abort:
    ldi r1, 0
    ret

_check_cmd:

    ; Read current bytes
    lbr r3, r1

    ldi r4, 0x2400
    add r4, r5
    lbr r4, r4

    ; Increment
    inc r1
    inc r5

    ; Check both sides
    cal check_left
    cal check_right

    cmp r8, r9
    jeq cmd_read_abort

    ; Comparison
    cmp r3, r4
    jeq _check_cmd
    jne check_failed

_set_cmd_status:
    ldi r8, 1
    swa r8, 0x2910
    ret

set_cmd_status:
    ldi r8, 0
    cmp cr, r8
    jeq _set_cmd_status
    ret

check_cmd:
    ldi r5, 0
    cal _check_cmd
    ldi r3, 0
    cmp r1, r3
    cal set_cmd_status
    cmp r1, r3
    ret

cmd_version:
    ldi r1, &version
    swa r1, D_WRITE_STR
    ret

cmd_help:
    ldi r1, &help
    swa r1, D_WRITE_STR
    ret

cmd_exit:
    ldi r1, &goodbye
    swa r1, D_WRITE_STR
    hlt

cmd_clear:
    ldi r1, &clear
    swa r1, D_WRITE_STR
    ret

cmd_date:
    ldi r1, &strftime
    swa r1, D_SET_TIME_FMT
    ldi r1, 0x2850
    swa r1, D_READ_TIME_FMT
    swa r1, D_WRITE_STR
    ret

count_mem:

    ; Have we hit the stack?
    ldi r3, 0x3000
    cmp r2, r3
    jeq skip_mem_count     ; If yes, then return

    ; Load byte from DATA
    lbr r3, r2
    ldi r4, 0
    cmp r3, r4             ; Is it NULL? (0)
    jeq skip_byte_count    ; If it is, skip it
    inc r1                 ; If it isn't, increment R1
    skip_byte_count:

    ; Increment DATA pointer
    inc r2

    ; And loop back
    jmp count_mem

    ; Finally, return (once we hit STACK)
    skip_mem_count:
    ret

cmd_mem:
    ldi r1, &mem1
    swa r1, D_WRITE_STR

    ; Starting counters
    ldi r1, 0
    ldi r2, 0x2000
    cal count_mem
    mov r2, r1             ; I love abusing r1, so move to r2

    ; Logging
    ldi r1, &mem2
    swa r1, D_WRITE_STR
    swa r2, D_WRITE_INT
    ldi r1, &mem3
    swa r1, D_WRITE_STR

    ; Percentage
    ldi r1, 100
    mul r2, r1
    ldi r1, 0x1000
    div r2, r1

    swa r2, D_WRITE_INT

    ; Closing
    ldi r1, &mem4
    swa r1, D_WRITE_STR
    ret

no_such_command:
    ldi r1, &no_cmd
    swa r1, D_WRITE_STR
    ret

check_cmd_status:
    lwa r1, 0x2910
    ldi r7, 1
    cmp r1, r7
    jne no_such_command
    ret

execute:

    ; Newline
    ldi r1, 10
    swa r1, D_WRITE_CHR

    ; String check
    ldi r1, 0
    swa r1, 0x2910

    ; Commands
    ldi r1, &str_version
    cal check_cmd
    jne skip_version
    cal cmd_version
    skip_version:

    ldi r1, &str_help
    cal check_cmd
    jne skip_help
    cal cmd_help
    skip_help:

    ldi r1, &str_exit
    cal check_cmd
    jne skip_exit
    cal cmd_exit
    skip_exit:

    ldi r1, &str_clear
    cal check_cmd
    jne skip_clear
    cal cmd_clear
    skip_clear:

    ldi r1, &str_mem
    cal check_cmd
    jne skip_mem
    cal cmd_mem
    skip_mem:

    ldi r1, &str_date
    cal check_cmd
    jne skip_date
    cal cmd_date
    skip_date:

    ; Check command status
    cal check_cmd_status

    ; Reset feed address
    ldi r2, 0x2400
    ldi r1, 0

    ; Mark as zero
    sbr r1, r2
    
    ; Pass back
    ldi r9, 10
    ret

backspace:
    dec r2

    ldi r1, 0
    swr r1, r2

    ; Pass back
    ldi r9, 10
    ret

push:

    ; Append to RAM
    sbr r1, r2

    ; Push back address
    inc r2

    ; Null terminate it (for WRITE_STR)
    ldi r1, 0
    swr r1, r2

    ret

shell:
    cal write

    ; Intake
    lwa r1, D_READ_CHR
    ldi r9, 0

    ; Check for [ENTER]
    ldi r3, 10
    cmp r1, r3
    jne skip_execute
    cal execute
    skip_execute:

    ; Check for [BACKSPACE]
    ldi r3, 127
    cmp r1, r3
    jne skip_backspace
    cal backspace
    skip_backspace:

    ; Everything else
    ldi r3, 10
    cmp r9, r3
    jeq skip_push
    cal push
    skip_push:

    ; Push to terminal
    cal write
    jmp shell

main:

    ; Greeting
    ldi r1, &clear
    swa r1, D_WRITE_STR

    ldi r1, &greeting
    swa r1, D_WRITE_STR

    ; Feed store
    ldi r2, 0x2400

    ; Loop
    jmp shell
