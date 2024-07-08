; func stdlib.print 1 func stdlib.exit 1 func stdlib.printError 1 const stdlib.SYS_WRITE const stdlib.SYS_EXIT const stdlib.STD_OUT const stdlib.STD_ERROR

section .bss
    stdlib.printSpace resb 8 ;private

stdlib.SYS_WRITE equ 1
stdlib.SYS_EXIT equ 60

stdlib.STD_OUT equ 1
stdlib.STD_ERROR equ 2

section .text

stdlib.print:
    pop rbx
    pop rax
    push rbx
    mov [stdlib.printSpace], rax
    mov rbx, 0
    stdlib.print_loop1: ;private
        mov cl, [rax]
        cmp cl, 0
        je stdlib.print_loop2
        inc rbx
        inc rax
        jmp stdlib.print_loop1
    stdlib.print_loop2: ;private
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
    mov rax, stdlib.SYS_EXIT
    syscall

stdlib.printError:
    pop rbx
    pop rax
    push rbx
    mov [stdlib.printSpace], rax
    mov rbx, 0
    stdlib.printError_loop1: ;private
        mov cl, [rax]
        cmp cl, 0
        je stdlib.printError_loop2
        inc rbx
        inc rax
        jmp stdlib.printError_loop1
    stdlib.printError_loop2: ;private
        mov rax, stdlib.SYS_WRITE
        mov rdi, stdlib.STD_ERROR
        mov rsi, [stdlib.printSpace]
        mov rdx, rbx
        syscall
    ret