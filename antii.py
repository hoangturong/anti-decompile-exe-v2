import sys
import os
import ctypes
import threading
import time
import random
import marshal
import builtins


def hide_console():
    if os.name == 'nt':  # Chỉ áp dụng trên Windows
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
#   1. Phát hiện Debugger trên Windows & Linux
def is_debugger_active():
    try:
        if os.name == "nt":  # Windows
            return ctypes.windll.kernel32.IsDebuggerPresent() != 0
        else:  # Linux/Mac
            with open("/proc/self/status", "r") as f:
                for line in f:
                    if "TracerPid" in line:
                        return int(line.split(":")[1].strip()) > 0
    except:
        return False
    return False

#   2. Xóa `sys.settrace()` và `sys.setprofile()` để chặn debug
def remove_trace_functions():
    sys.settrace = lambda *args, **kwargs: None
    sys.setprofile = lambda *args, **kwargs: None

#   3. Chặn import các module debug
def block_debug_imports():
    debug_modules = ["pdb", "pydevd", "pydevd_tracing", "ptrace"]
    for mod in debug_modules:
        sys.modules[mod] = None

#   4. Kiểm tra xem có đang chạy trong sandbox hoặc VM không
def is_sandboxed():
    sandbox_files = [
        "/bin/qemu-ga", "/bin/vmtoolsd", "/bin/xenstore", "/usr/bin/VBoxService",
        "/usr/bin/VBoxClient", "/usr/bin/qemu-system-x86_64"
    ]
    return any(os.path.exists(f) for f in sandbox_files)

#   5. Tạo thread kiểm tra debugger liên tục
def anti_debugger_thread():
    while True:
        if is_debugger_active() or sys.gettrace():
            print("Debugger detected! Exiting...")
            os._exit(1)
        time.sleep(0.5)

#   6. Mã hóa & làm rối bytecode để tránh phân tích
def obfuscate_code():
    encrypted_code = marshal.dumps(lambda: "Protected Code")
    exec(marshal.loads(encrypted_code))

#   7. Fake lỗi ngẫu nhiên nếu bị debug
def fake_errors():
    error_list = [
        ZeroDivisionError, ValueError, MemoryError, KeyboardInterrupt, SystemExit
    ]
    if sys.gettrace():
        raise random.choice(error_list)("Status Error")

#   8. Xóa chính mình khỏi bộ nhớ sau khi chạy
def delete_self_from_memory():
    del sys.modules[__name__]

#   9. Đổi tên process để tránh bị theo dõi
def rename_process():
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("System Idle Process")
    except:
        pass

#   10. Fake crash log để đánh lừa hacker
def fake_crash_log():
    with open("crash_log.txt", "w") as f:
        f.write("Fatal Error 0x800F0922: Kernel Panic\n")

#   11. Chặn đọc bytecode từ `__code__.co_code`
def protect_bytecode():
    class FakeCode:
        def __getattr__(self, name):
            if name in ["co_code", "co_consts", "co_names"]:
                return b"\x00" * 256  # Trả về bytecode giả
            return lambda *args, **kwargs: None

    class FakeFunction:
        __code__ = FakeCode()

    # Chỉ fake một số function nhất định, không ảnh hưởng đến các thread quan trọng
    protected_functions = [
        "obfuscate_code",
        "fake_errors",
        "random_crash",
        "fake_unicode_error"
    ]

    for func_name in protected_functions:
        if func_name in globals() and callable(globals()[func_name]):
            globals()[func_name] = FakeFunction()  


#   12. Fake biến rác để gây rối
def obfuscate_variables():
    for _ in range(500):
        exec(f"trong_dz_{random.randint(1000,9999)} = {random.randint(1000,9999)}")

#   13. Xóa built-in functions
def clear_builtins():
    try:
        builtins.__dict__.clear()
    except:
        pass

#   14. Thay đổi sys.argv trong runtime
def modify_argv():
    sys.argv = ["virut.py", "windows", "linux"]

#   15. Đổi nội dung chính nó để tránh reverse-engineering
def modify_self():
    try:
        with open(__file__, "w") as f:
            f.write("# File has been modified dynamically")
    except:
        pass

#   16. Thêm lỗi UnicodeDecodeError nếu bị debug
def fake_unicode_error():
    if sys.gettrace():
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid character")

#   17. Chạy code ngẫu nhiên để gây rối
def execute_random_code():
    code_list = [
        "print('start...')",
        "print('crash...')",
        "print('debug...')"
    ]
    exec(random.choice(code_list))

#   18. Tạo các hàm rác vô nghĩa
def fake_functions():
    def useless_function_1(): return 123
    def useless_function_2(): return 456
    def useless_function_3(): return 789

#   19. Gây crash ngẫu nhiên nếu bị phân tích
def random_crash():
    if sys.gettrace():
        os._exit(1)

#   20. Bật tất cả cơ chế bảo vệ
def protect():
    hide_console()
    remove_trace_functions()
    block_debug_imports()
    rename_process()
    protect_bytecode()  #  Đã fix lỗi
    fake_crash_log()
    delete_self_from_memory()
    
    # Chạy kiểm tra debugger trong nền (KHÔNG bị ảnh hưởng)
    thread = threading.Thread(target=anti_debugger_thread, daemon=True)
    thread.start()

    # Nếu phát hiện sandbox, thoát ngay lập tức
    if is_sandboxed():
        print("Running in a sandbox! Exiting...")
        os._exit(1)

    print("Maximum protection enabled!")

