import tkinter as tk
from tkinter import messagebox
import os
import argparse


class DataEntryApp:
    def __init__(self, master, output_file, entry_labels):
        self.master = master
        master.title("Data Entry GUI")
        self.entry_vars = []
        self.entry_labels = entry_labels
        self.output_file = output_file
        self.setup_gui()

    def setup_gui(self):
        self.create_heading_label()
        self.create_and_place_entries()
        self.create_and_place_buttons()
        self.create_and_place_messages()
        self.configure_weights()
        self.bind_functions()

    def create_heading_label(self):
        heading_label = tk.Label(
            self.master, text="Data Entry Form", font=("Helvetica", 16, "bold")
        )
        heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="nsew")

    def create_and_place_entries(self):
        for i, label_text in enumerate(self.entry_labels):
            var = tk.StringVar()
            entry_label = tk.Label(self.master, text=label_text + ":")
            entry = tk.Entry(self.master, width=30, textvariable=var)
            entry_label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")
            entry.grid(row=i + 1, column=1, padx=10, pady=5, sticky="ew")
            entry_label.grid_configure(columnspan=2)
            entry.grid_configure(columnspan=2)
            self.entry_vars.append(var)

    def create_and_place_buttons(self):
        self.save_button = tk.Button(self.master, text="Save", command=self.save_data)
        self.save_button.grid(
            row=len(self.entry_labels) + 1,
            column=0,
            columnspan=2,
            pady=(10, 5),
            sticky="nsew",
        )

        self.exit_button = tk.Button(self.master, text="Exit", command=self.on_exit)
        self.exit_button.grid(
            row=len(self.entry_labels) + 2,
            column=0,
            columnspan=2,
            pady=(0, 10),
            sticky="nsew",
        )

    def create_and_place_messages(self):
        self.success_label = tk.Label(self.master, text="", fg="green")
        self.error_label = tk.Label(self.master, text="", fg="red")
        self.success_label.grid(
            row=len(self.entry_labels) + 3, column=0, columnspan=2, pady=5
        )
        self.error_label.grid(
            row=len(self.entry_labels) + 4, column=0, columnspan=2, pady=5
        )

    def configure_weights(self):
        for i in range(len(self.entry_labels) + 5):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_columnconfigure(0, weight=1, uniform="equal")
        self.master.grid_columnconfigure(1, weight=1, uniform="equal")

    def bind_functions(self):
        self.master.bind("<Return>", lambda event: self.save_data())
        self.exit_button.bind("<Return>", lambda event: self.on_exit())
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def save_data(self):
        try:
            values = [var.get() for var in self.entry_vars]

            for i, value in enumerate(values):
                if (
                    not value and i != 0
                ):  # Skip checking Serial Number for non-numeric values
                    raise ValueError(f"{self.entry_labels[i]} must not be empty")

            # Format the heading and data
            heading = (
                "\t".join(["{: <15}".format(label) for label in self.entry_labels])
                + "\n"
            )
            data = "\t".join(["{: <15}".format(value) for value in values]) + "\n"

            with open(self.output_file, "a+") as f:
                f.seek(0)  # Move to the beginning of the file
                if not f.read():  # If file is empty, write the heading
                    f.write(heading)

                f.write(data)

            self.clear_entries()
            self.display_message("Data saved successfully!", "green")

        except ValueError as ve:
            self.display_message(str(ve), "red")
        except Exception as e:
            self.display_message(f"An unexpected error occurred: {str(e)}", "red")

    def clear_entries(self):
        for var in self.entry_vars:
            var.set("")

    def display_message(self, message, color):
        label = self.success_label if color == "green" else self.error_label
        label.config(text=message, fg=color)
        self.master.after(3000, self.clear_message)

    def clear_message(self):
        self.success_label.config(text="")
        self.error_label.config(text="")

    def on_exit(self):
        if messagebox.askyesno("Exit", "Do you really want to exit?"):
            self.master.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data Entry GUI")
    parser.add_argument("--output-file", default="data.txt", help="Output file path")
    args = parser.parse_args()

    # Get column labels from the user
    column_labels = input("Enter column labels separated by commas: ").split(",")

    root = tk.Tk()
    app = DataEntryApp(root, output_file=args.output_file, entry_labels=column_labels)
    root.mainloop()
