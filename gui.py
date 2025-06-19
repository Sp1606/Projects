import tkinter as tk
from voice_module import get_voice_input, speak
from calculator_engine import calculate

def run_gui():
    def solve():
        expr = entry.get()
        result = calculate(expr)
        output_label.config(text=f"Result: {result}")
        speak(f"The result is {result}")

    def voice_command():
        query = get_voice_input()
        entry.delete(0, tk.END)
        entry.insert(0, query)
        solve()

    root = tk.Tk()
    root.title("AI Voice Calculator")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Enter Expression:", font=("Arial", 14)).pack(pady=10)
    entry = tk.Entry(root, font=("Arial", 14), width=30)
    entry.pack(pady=5)

    tk.Button(root, text="Calculate", font=("Arial", 12), command=solve).pack(pady=10)
    tk.Button(root, text="🎤 Voice Input", font=("Arial", 12), command=voice_command).pack(pady=5)

    output_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
    output_label.pack(pady=20)

    root.mainloop()