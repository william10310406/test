import tkinter as tk
from tkinter import scrolledtext
import sys
import io


def screencoding():
    # 創建子視窗
    sub_root = tk.Toplevel()
    sub_root.title("Coding Window")

    # 創建一個文本框來編寫程式碼
    code_area = scrolledtext.ScrolledText(sub_root, wrap=tk.WORD)
    code_area.pack(expand=True, fill="both")

    # 創建一個文本框來顯示輸出和錯誤訊息
    output_area = scrolledtext.ScrolledText(sub_root, wrap=tk.WORD, height=10)
    output_area.pack(expand=True, fill="both")

    # 創建一個輸入框來模擬 input() 函數
    input_var = tk.StringVar()
    input_entry = tk.Entry(sub_root, textvariable=input_var)
    input_entry.pack()

    # 定義自訂的 input 函數
    def custom_input(prompt=""):
        output_area.insert(tk.END, prompt + "\n")
        input_var.set("")  # 清空輸入框
        input_entry.focus()
        sub_root.wait_variable(input_var)
        return input_var.get()

    # 定義在按下 Enter 鍵時回傳值的函數
    def on_enter(event):
        input_var.set(input_entry.get())

    # 綁定 Enter 鍵事件
    input_entry.bind("<Return>", on_enter)

    # 定義執行程式碼的函數
    def execute_code():
        code = code_area.get("1.0", tk.END)
        output_area.delete("1.0", tk.END)
        try:
            # 重定向 stdout 和 stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = io.StringIO()
            sys.stderr = io.StringIO()

            # 將自訂的 input 函數加入全域變數
            globals()["input"] = custom_input

            # 執行程式碼
            exec(code, globals())

            # 獲取輸出
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()

            # 恢復 stdout 和 stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # 顯示輸出和錯誤
            if output:
                output_area.insert(tk.END, "Output:\n" + output)
            if error:
                output_area.insert(tk.END, "Error:\n" + error)
        except Exception as e:
            output_area.insert(tk.END, "Error:\n" + str(e))

    # 創建一個按鈕來執行程式碼
    execute_button = tk.Button(sub_root, text="執行", command=execute_code)
    execute_button.pack()

    # 啟動子視窗事件循環
    sub_root.mainloop()


def screen(width, height):
    # 創建主視窗
    root = tk.Tk()
    root.title("Main Window")
    # 設定視窗大小
    root.geometry(f"{width}x{height}")

    # 創建一個按鈕來打開 coding 視窗
    coding_button = tk.Button(root, text="coding", command=screencoding)
    coding_button.pack()

    # 啟動主事件循環
    root.mainloop()


def open():
    screen(800, 600)
