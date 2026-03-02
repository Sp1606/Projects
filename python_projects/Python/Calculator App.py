import tkinter as tk
from tkinter import messagebox
import math

# Function to update the input field
def press(key):
    entry_var.set(entry_var.get() + str(key))

# Function to evaluate the expression
def calculate():
    try:
        expression = entry_var.get()
        expression = expression.replace("π", str(math.pi))  # Replace π with its value
        expression = expression.replace("^", "**")  # Handle power operation
        expression = expression.replace("e", str(math.e))  # Replace 'e' with its value
        
        result = eval(expression)  # Evaluates the expression
        entry_var.set(result)
    except ZeroDivisionError:
        messagebox.showerror("Error", "Cannot divide by zero")
        entry_var.set("")
    except:
        messagebox.showerror("Error", "Invalid input")
        entry_var.set("")

# Function to clear the input field
def clear():
    entry_var.set("")

# Function for scientific operations
def scientific_operation(op):
    try:
        expression = entry_var.get()
        if op == "sin":
            result = math.sin(math.radians(float(expression)))
        elif op == "cos":
            result = math.cos(math.radians(float(expression)))
        elif op == "tan":
            result = math.tan(math.radians(float(expression)))
        elif op == "log":
            result = math.log10(float(expression))
        elif op == "ln":
            result = math.log(float(expression))
        elif op == "√":
            result = math.sqrt(float(expression))
        elif op == "x²":
            result = float(expression) ** 2
        elif op == "x³":
            result = float(expression) ** 3
        elif op == "!":
            result = math.factorial(int(expression))
        elif op == "e^x":
            result = math.exp(float(expression))

        entry_var.set(result)
    except ValueError:
        messagebox.showerror("Error", "Invalid input for operation")
        entry_var.set("")

# Create GUI window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("400x600")

# Input field
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 20), justify="right", bd=10, relief="ridge")
entry.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=8)

# Button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('√', 1, 4),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('x²', 2, 4),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('x³', 3, 4),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('^', 4, 3), ('π', 4, 4),
    ('(', 5, 0), (')', 5, 1), ('log', 5, 2), ('ln', 5, 3), ('e^x', 5, 4),
    ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('!', 6, 3), ('e', 6, 4),
]

# Creating buttons dynamically
for (text, row, col) in buttons:
    if text in ["sin", "cos", "tan", "log", "ln", "√", "x²", "x³", "!", "e^x"]:
        btn = tk.Button(root, text=text, font=("Arial", 14), bg="lightblue", command=lambda t=text: scientific_operation(t), height=2, width=5)
    else:
        btn = tk.Button(root, text=text, font=("Arial", 14), command=lambda t=text: press(t), height=2, width=5)
    btn.grid(row=row, column=col, padx=5, pady=5)

# Special buttons
equal_btn = tk.Button(root, text="=", font=("Arial", 16), bg="green", fg="white", command=calculate, height=2, width=11)
equal_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

clear_btn = tk.Button(root, text="C", font=("Arial", 16), bg="red", fg="white", command=clear, height=2, width=11)
clear_btn.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

# Run the application
root.mainloop()
