import tkinter as tk
from tkinter import font


class MyWindow:
    def __init__(self, window, compound_names, compound_quantities, text):
        self.window = window
        self.compound_names = compound_names
        self.compound_quantities = compound_quantities
        self.paired_entries = []  # List to store the paired entries
        self.selected_name_index = None  # Index of the selected compound name
        self.selected_quantity_index = None  # Index of the selected compound quantity
        self.previous_name_values = list(compound_names)  # Store previous name values
        self.previous_quantity_values = list(compound_quantities)  # Store previous quantity values
        window.title("Popup Window")
        window.geometry('800x600')  # Set the width of the window

        # Set column widths
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)

        self.text_area = tk.Text(window, height=10, width=80)  # Increase the width of the text field
        self.text_area.grid(row=0, column=0, columnspan=2, pady=10)  # Position in the grid
        self.text_area.bind('<Return>', self.on_confirm)
        self.text_area.bind('<Shift_R>', self.on_confirm_shift)
        self.text_area.bind('<Shift_L>', self.on_confirm_shift)
        self.text_area.bind('<KeyPress>', self.on_space)  # Bind key press event

        # Increase the font size
        text_font = font.Font(size=14)
        self.text_area.configure(font=text_font)

        self.remove_button_1 = tk.Button(window, text="Remove Entry from Compound Names", command=self.remove_displayed_word_1)
        self.remove_button_1.grid(row=1, column=0, padx=10, pady=10)  # Position in the grid

        self.remove_button_2 = tk.Button(window, text="Remove Entry from Compound Quantities", command=self.remove_displayed_word_2)
        self.remove_button_2.grid(row=1, column=1, padx=10, pady=10)  # Position in the grid

        self.cancel_button = tk.Button(window, text="Cancel", command=self.quit)
        self.cancel_button.grid(row=2, column=0, columnspan=2, pady=10)  # Position in the grid

        self.label_1 = tk.Label(window, text="Compound Names:")
        self.label_1.grid(row=3, column=0, sticky='w')  # Position in the grid

        self.compound_names_listbox = tk.Listbox(window, selectbackground="lightblue")  # Set the background color for selected items
        self.compound_names_listbox.grid(row=4, column=0, padx=10)  # Position in the grid
        self.compound_names_listbox.bind('<<ListboxSelect>>', self.on_select_name)  # Bind selection event for names
        for name in compound_names:
            self.compound_names_listbox.insert(tk.END, name)

        self.label_2 = tk.Label(window, text="Compound Quantities:")
        self.label_2.grid(row=3, column=1, sticky='w')  # Position in the grid

        self.compound_quantities_listbox = tk.Listbox(window, selectbackground="lightblue")  # Set the background color for selected items
        self.compound_quantities_listbox.grid(row=4, column=1, padx=10)  # Position in the grid
        self.compound_quantities_listbox.bind('<<ListboxSelect>>', self.on_select_quantity)  # Bind selection event for quantities
        for quantity in compound_quantities:
            self.compound_quantities_listbox.insert(tk.END, quantity)

        self.initialize_text(text)
        self.text_area.config(state='disabled')

        self.continue_button = tk.Button(window, text="Continue", command=self.continue_execution)
        self.continue_button.grid(row=5, column=0, columnspan=2, pady=10)  # Position in the grid

    def on_space(self, event):
        if event.char == ' ':
            self.paired_entries = list(zip(self.compound_names_listbox.get(0, tk.END), self.compound_quantities_listbox.get(0, tk.END)))
            self.quit()

    def on_select_name(self, event):
        selected_indices = self.compound_names_listbox.curselection()
        if selected_indices:
            if self.selected_name_index is not None:
                self.compound_names_listbox.itemconfig(self.selected_name_index, background="white")  # Remove highlight from previously selected name
            self.selected_name_index = selected_indices[0]
            self.compound_names_listbox.itemconfig(self.selected_name_index, background="lightblue")  # Highlight newly selected name

    def on_select_quantity(self, event):
        selected_indices = self.compound_quantities_listbox.curselection()
        if selected_indices:
            if self.selected_quantity_index is not None:
                self.compound_quantities_listbox.itemconfig(self.selected_quantity_index, background="white")  # Remove highlight from previously selected quantity
            self.selected_quantity_index = selected_indices[0]
            self.compound_quantities_listbox.itemconfig(self.selected_quantity_index, background="lightblue")  # Highlight newly selected quantity

    def update_highlighting(self):
        for i, name in enumerate(self.compound_names):
            if name != self.previous_name_values[i]:
                self.compound_names_listbox.itemconfig(i, background="yellow")
            else:
                self.compound_names_listbox.itemconfig(i, background="white")
        for i, quantity in enumerate(self.compound_quantities):
            if quantity != self.previous_quantity_values[i]:
                self.compound_quantities_listbox.itemconfig(i, background="yellow")
            else:
                self.compound_quantities_listbox.itemconfig(i, background="white")

    def initialize_text(self, text):
        lines = text.split("\n")
        for line in lines:
            self.text_area.insert(tk.END, line + "\n")

    def quit(self):
        self.window.quit()
        self.window.destroy()

    def continue_execution(self):
        self.paired_entries = None
        self.quit()

    def on_confirm(self, event=None):
        try:
            start_index = self.text_area.index('sel.first')
            end_index = self.text_area.index('sel.last')
            selected_text = self.text_area.get(start_index, end_index)
            self.compound_names_listbox.delete(tk.ANCHOR)
            self.compound_names_listbox.insert(tk.ANCHOR, selected_text)
            self.compound_names.insert
        except tk.TclError:
            pass

    def on_confirm_shift(self, event=None):
        try:
            start_index = self.text_area.index('sel.first')
            end_index = self.text_area.index('sel.last')
            selected_text = self.text_area.get(start_index, end_index)
            self.compound_quantities_listbox.delete(tk.ANCHOR)
            self.compound_quantities_listbox.insert(tk.ANCHOR, selected_text)
        except tk.TclError:
            pass

    def remove_displayed_word_1(self):
        self.compound_names_listbox.delete(tk.ANCHOR)

    def remove_displayed_word_2(self):
        self.compound_quantities_listbox.delete(tk.ANCHOR)

    def initialize_text(self, text):
        text = text
        self.text_area.insert('1.0', text)
        self.text_area.tag_config("highlight1", background="yellow")
        self.text_area.tag_config("highlight2", background="cyan")
        for word in self.compound_names:
            start = 1.0
            while True:
                pos = self.text_area.search(word, start, stopindex=tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                self.text_area.tag_add("highlight1", pos, end)
                start = end
        for word in self.compound_quantities:
            start = 1.0
            while True:
                pos = self.text_area.search(word, start, stopindex=tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                self.text_area.tag_add("highlight2", pos, end)
                start = end

    # def quit(self):
    #     compound_names = list(self.compound_names_listbox.get(0, tk.END))
    #     compound_quantities = list(self.compound_quantities_listbox.get(0, tk.END))
    #     self.paired_entries = list(zip(compound_names, compound_quantities))
    #     self.window.quit()
    #     self.window.destroy()


    def on_finish(self, event=None):
        self.quit()


def create_popup(text, vars_and_vals):
    root = tk.Tk()
    compound_names = [a[0] for a in vars_and_vals]
    compound_quantities = [a[1] for a in vars_and_vals]
    my_window = MyWindow(root, compound_names, compound_quantities, text)
    root.mainloop()

    return my_window.paired_entries
