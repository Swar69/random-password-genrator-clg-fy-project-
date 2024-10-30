import random
import string
import tkinter as tk
from tkinter import messagebox, ttk

# Dictionary to map words to numbers (extended up to 100)
words_to_numbers = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
    "one hundred": 100
}

# Adding the ability to have combinations like "twenty one", "seventy five"
for tens in ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]:
    for ones in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
        words_to_numbers[f"{tens} {ones}"] = words_to_numbers[tens] + words_to_numbers[ones]

# Function to convert a list of words to numbers
def words_to_total_length(words_list):
    total_length = 0
    for word in words_list:
        word = word.lower()  # Convert input to lowercase
        if word in words_to_numbers:
            total_length += words_to_numbers[word]
        else:
            raise ValueError(f"Invalid word input: {word}")
    return total_length

# Function to generate the password
def generate_password():
    try:
        user_input = entry_length.get()  # Get the user's input from the entry box
        
        # Split the input into individual words (if any) and check if it's a valid number or word
        words_list = user_input.split()
        
        # Try converting words list into a total length
        if all(word.isdigit() for word in words_list):
            length = sum(int(word) for word in words_list)  # If the input is all numbers, sum them up
        else:
            length = words_to_total_length(words_list)  # If it's words, convert them to a total number
            
        if length < 1 or length > 100:
            raise ValueError("Length must be between 1 and 100.")
        
        # Characters to choose from (letters, digits, punctuation)
        chars = string.ascii_letters + string.digits + string.punctuation
        
        # Generate the password
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Clear the output field and insert the generated password
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))

# Autocomplete functionality
class AutocompleteEntry(ttk.Entry):
    def __init__(self, autocomplete_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_list = sorted(autocomplete_list)
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace("w", self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", lambda event: generate_password())
        
        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == "":
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for word in words:
                    self.lb.insert(tk.END, word)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def comparison(self):
        pattern = self.var.get().lower()
        return [word for word in self.autocomplete_list if word.startswith(pattern)]

# Create the main window
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x300")  # Set window size

# Add a label for instructions
label_instruction = tk.Label(root, text="Enter password length (numbers or words, e.g., 'five six three'):")
label_instruction.pack(pady=10)

# Autocomplete-enabled entry box for password length
autocomplete_words = list(words_to_numbers.keys())
entry_length = AutocompleteEntry(autocomplete_words, root, width=50)
entry_length.pack(pady=5)

# Button to generate the password
button_generate = tk.Button(root, text="Generate Password", command=generate_password)
button_generate.pack(pady=10)


# Entry widget to display the generated password (copyable)
entry_password = tk.Entry(root, width=50)  # Entry widget to make the password copyable
entry_password.pack(pady=10)

# Run the application
root.mainloop()
