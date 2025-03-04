<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk  # For Combobox
from tkinter import messagebox
import requests
import re

# Currency codes (ISO 4217) and *Descriptive* names.
# This makes it easier for users to understand and choose currencies.
CURRENCIES = {
    "USD": "United States Dollar (USD)",
    "EUR": "Euro (EUR)",
    "GBP": "British Pound (GBP)",
    "JPY": "Japanese Yen (JPY)",
    "CAD": "Canadian Dollar (CAD)",
    "AUD": "Australian Dollar (AUD)",
    "CHF": "Swiss Franc (CHF)",
    "CNY": "Chinese Yuan (CNY)",
    "INR": "Indian Rupee (INR)",  # Added ISO code
    "BRL": "Brazilian Real (BRL)",
    "RUB": "Russian Ruble (RUB)",
    "KRW": "South Korean Won (KRW)",
    "MXN": "Mexican Peso (MXN)",
    # Add more currencies here
}

class CurrencyConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")

        # --- Styling ---

        # Set a larger font size for most elements
        self.font_size = 14  # You can adjust this value
        self.font = ("Arial", self.font_size)

        # Padding for elements
        self.padx = 10
        self.pady = 10

        # --- UI Elements ---

        # Amount Input
        self.amount_label = tk.Label(master, text="Amount:", font=self.font)
        self.amount_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.amount_entry = tk.Entry(master, font=self.font)  # Apply font
        self.amount_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        # From Currency Selection
        self.from_label = tk.Label(master, text="From Currency:", font=self.font)
        self.from_label.grid(row=1, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.from_currency = tk.StringVar()

        # Use the descriptive names in the Combobox
        currency_names = list(CURRENCIES.values())
        self.from_combo = ttk.Combobox(master, textvariable=self.from_currency,
                                       values=currency_names, state="readonly", font=self.font)  # Apply font
        self.from_combo.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.from_combo.set("United States Dollar (USD)")  # Default value (Descriptive Name)

        # To Currency Selection
        self.to_label = tk.Label(master, text="To Currency:", font=self.font)
        self.to_label.grid(row=2, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.to_currency = tk.StringVar()
        self.to_combo = ttk.Combobox(master, textvariable=self.to_currency,
                                     values=currency_names, state="readonly", font=self.font)  # Apply font
        self.to_combo.grid(row=2, column=1, padx=self.padx, pady=self.pady)
        self.to_combo.set("Euro (EUR)")  # Default value (Descriptive Name)

        # Convert Button
        self.convert_button = tk.Button(master, text="Convert", command=self.convert_currency, font=self.font)  # Apply font
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=self.pady)

        # Result Label
        self.result_label = tk.Label(master, text="", font=self.font)  # Apply font
        self.result_label.grid(row=4, column=0, columnspan=2, pady=self.pady)


    def convert_currency(self):
        """Handles the currency conversion process."""
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return

        # Get selected currency *names* from Combobox
        from_currency_name = self.from_currency.get()
        to_currency_name = self.to_currency.get()

        # Find the *code* corresponding to the selected name
        from_currency = self.get_currency_code(from_currency_name)
        to_currency = self.get_currency_code(to_currency_name)

        if not from_currency or not to_currency:
            messagebox.showerror("Error", "Invalid currency selection. Please select from the list.")
            return


        conversion_result = get_currency_conversion_rate(from_currency, to_currency, amount)

        if conversion_result is not None:
            self.result_label.config(text=f"{amount:.2f} {from_currency} is equal to {conversion_result:.2f} {to_currency}")
        else:
            self.result_label.config(text="Could not retrieve conversion rate.")


    def get_currency_code(self, currency_name):
        """Helper function to get the currency code from the name."""
        for code, name in CURRENCIES.items():
            if name == currency_name:
                return code
        return None # Code was not found



def get_currency_conversion_rate(from_currency, to_currency, amount=1):
    """
    Fetches currency conversion rate from Google Finance using regular expressions.
    (Same as before, but copied here for self-containment)
    """

    url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        html_content = response.text

        pattern = r'<div class="YMlKec.*?">([\d.]+)<\/div>'
        match = re.search(pattern, html_content)

        if match:
            try:
                exchange_rate = float(match.group(1))
                converted_amount = amount * exchange_rate
                return converted_amount
            except ValueError:
                print("Could not convert extracted text to float.")
                return None
        else:
            print("Could not find exchange rate using regex.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



if __name__ == "__main__":
    root = tk.Tk()

    # Set a default window size (optional)
    root.geometry("400x300")  # width x height

    gui = CurrencyConverterGUI(root)
=======
import tkinter as tk
from tkinter import ttk  # For Combobox
from tkinter import messagebox
import requests
import re

# Currency codes (ISO 4217) and *Descriptive* names.
# This makes it easier for users to understand and choose currencies.
CURRENCIES = {
    "USD": "United States Dollar (USD)",
    "EUR": "Euro (EUR)",
    "GBP": "British Pound (GBP)",
    "JPY": "Japanese Yen (JPY)",
    "CAD": "Canadian Dollar (CAD)",
    "AUD": "Australian Dollar (AUD)",
    "CHF": "Swiss Franc (CHF)",
    "CNY": "Chinese Yuan (CNY)",
    "INR": "Indian Rupee (INR)",  # Added ISO code
    "BRL": "Brazilian Real (BRL)",
    "RUB": "Russian Ruble (RUB)",
    "KRW": "South Korean Won (KRW)",
    "MXN": "Mexican Peso (MXN)",
    # Add more currencies here
}

class CurrencyConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Currency Converter")

        # --- Styling ---

        # Set a larger font size for most elements
        self.font_size = 14  # You can adjust this value
        self.font = ("Arial", self.font_size)

        # Padding for elements
        self.padx = 10
        self.pady = 10

        # --- UI Elements ---

        # Amount Input
        self.amount_label = tk.Label(master, text="Amount:", font=self.font)
        self.amount_label.grid(row=0, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.amount_entry = tk.Entry(master, font=self.font)  # Apply font
        self.amount_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady)

        # From Currency Selection
        self.from_label = tk.Label(master, text="From Currency:", font=self.font)
        self.from_label.grid(row=1, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.from_currency = tk.StringVar()

        # Use the descriptive names in the Combobox
        currency_names = list(CURRENCIES.values())
        self.from_combo = ttk.Combobox(master, textvariable=self.from_currency,
                                       values=currency_names, state="readonly", font=self.font)  # Apply font
        self.from_combo.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.from_combo.set("United States Dollar (USD)")  # Default value (Descriptive Name)

        # To Currency Selection
        self.to_label = tk.Label(master, text="To Currency:", font=self.font)
        self.to_label.grid(row=2, column=0, sticky=tk.W, padx=self.padx, pady=self.pady)
        self.to_currency = tk.StringVar()
        self.to_combo = ttk.Combobox(master, textvariable=self.to_currency,
                                     values=currency_names, state="readonly", font=self.font)  # Apply font
        self.to_combo.grid(row=2, column=1, padx=self.padx, pady=self.pady)
        self.to_combo.set("Euro (EUR)")  # Default value (Descriptive Name)

        # Convert Button
        self.convert_button = tk.Button(master, text="Convert", command=self.convert_currency, font=self.font)  # Apply font
        self.convert_button.grid(row=3, column=0, columnspan=2, pady=self.pady)

        # Result Label
        self.result_label = tk.Label(master, text="", font=self.font)  # Apply font
        self.result_label.grid(row=4, column=0, columnspan=2, pady=self.pady)


    def convert_currency(self):
        """Handles the currency conversion process."""
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return

        # Get selected currency *names* from Combobox
        from_currency_name = self.from_currency.get()
        to_currency_name = self.to_currency.get()

        # Find the *code* corresponding to the selected name
        from_currency = self.get_currency_code(from_currency_name)
        to_currency = self.get_currency_code(to_currency_name)

        if not from_currency or not to_currency:
            messagebox.showerror("Error", "Invalid currency selection. Please select from the list.")
            return


        conversion_result = get_currency_conversion_rate(from_currency, to_currency, amount)

        if conversion_result is not None:
            self.result_label.config(text=f"{amount:.2f} {from_currency} is equal to {conversion_result:.2f} {to_currency}")
        else:
            self.result_label.config(text="Could not retrieve conversion rate.")


    def get_currency_code(self, currency_name):
        """Helper function to get the currency code from the name."""
        for code, name in CURRENCIES.items():
            if name == currency_name:
                return code
        return None # Code was not found



def get_currency_conversion_rate(from_currency, to_currency, amount=1):
    """
    Fetches currency conversion rate from Google Finance using regular expressions.
    (Same as before, but copied here for self-containment)
    """

    url = f"https://www.google.com/finance/quote/{from_currency}-{to_currency}"

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        html_content = response.text

        pattern = r'<div class="YMlKec.*?">([\d.]+)<\/div>'
        match = re.search(pattern, html_content)

        if match:
            try:
                exchange_rate = float(match.group(1))
                converted_amount = amount * exchange_rate
                return converted_amount
            except ValueError:
                print("Could not convert extracted text to float.")
                return None
        else:
            print("Could not find exchange rate using regex.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



if __name__ == "__main__":
    root = tk.Tk()

    # Set a default window size (optional)
    root.geometry("400x300")  # width x height

    gui = CurrencyConverterGUI(root)
>>>>>>> 3b02cf551ec84237dd5a8f1c782cdd8f9f5699b9
    root.mainloop()