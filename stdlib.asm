section .bss
    stdlib.printSpace resb 8

stdlib.SYS_WRITE equ 1

stdlib.STD_OUT equ 1
stdlib.STD_ERROR equ 2

section .text

stdlib.print:
    pop rbx
    pop rax
    push rbx
    mov [stdlib.printSpace], rax
    mov rbx, 0
    stdlib.print_loop1:
        mov cl, [rax]
        cmp cl, 0
        je stdlib.print_loop2
        inc rbx
        inc rax
        jmp stdlib.print_loop1
    stdlib.print_loop2:
        mov rax, stdlib.SYS_WRITE
        mov rdi, stdlib.STD_OUT
        mov rsi, [stdlib.printSpace]
        mov rdx, rbx
        syscall
    ret

stdlib.exit:
    pop rbx
    pop rax
    push rbx
    mov rdi, rax
    mov rax, 60
    syscall

stdlib.printError:
    pop rbx
    pop rax
    push rbx
    mov [stdlib.printSpace], rax
    mov rbx, 0
    stdlib.printError_loop1:
        mov cl, [rax]
        cmp cl, 0
        je stdlib.printError_loop2
        inc rbx
        inc rax
        jmp stdlib.printError_loop1
    stdlib.printError_loop2:
        mov rax, stdlib.SYS_WRITE
        mov rdi, stdlib.STD_ERROR
        mov rsi, [stdlib.printSpace]
        mov rdx, rbx
        syscall
    ret