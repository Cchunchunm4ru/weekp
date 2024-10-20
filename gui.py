import tkinter as tk 
from tkinter import ttk
import csv
import os
from PIL import Image, ImageTk

def main():
    root = tk.Tk()
    root.geometry('1000x600')
    root.title('planner')

    label = tk.Label(root, text="hello chunchun \n heres the plan for the week \n continue the grind", font=(48))
    label.pack()

    def bg():
        bg_img = Image.open('775121.webp')
        bg_img = bg_img.resize((1000, 1000))
        bg_img = ImageTk.PhotoImage(bg_img)
        bg_lab = tk.Label(root, image=bg_img)
        bg_lab.place(relwidth=1, relheight=1)
        bg_lab.image = bg_img

    bg()

    def treefun():
        global tree, columns  # Declare tree as global
        columns = ('time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
        tree = ttk.Treeview(root, column=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor='center', width=100)
        
        tree.pack(padx=100, pady=20)

    filename = 'py.csv'

    def tree_save():
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for row in tree.get_children():
                writer.writerow(tree.item(row)['values'])

    def load_data():
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    tree.insert('', 'end', values=row)

    def clear_entries():
        entry_time.delete(0, tk.END)
        entry_monday.delete(0, tk.END)
        entry_tuesday.delete(0, tk.END)
        entry_wednesday.delete(0, tk.END)
        entry_thursday.delete(0, tk.END)
        entry_friday.delete(0, tk.END)
        entry_saturday.delete(0, tk.END)
        entry_sunday.delete(0, tk.END)

    def add_row():
        new_data = [entry_time.get(), entry_monday.get(), entry_tuesday.get(), entry_wednesday.get(),
                    entry_thursday.get(), entry_friday.get(), entry_saturday.get(), entry_sunday.get()]
        tree.insert('', 'end', values=new_data)
        tree_save()  
        clear_entries()

    def edit_row():
        selected_item = tree.selection()
        if selected_item:
            tree.item(selected_item[0], values=[entry_time.get(), entry_monday.get(), entry_tuesday.get(),
                                                 entry_wednesday.get(), entry_thursday.get(), entry_friday.get(),
                                                 entry_saturday.get(), entry_sunday.get()])
            tree_save()  
            clear_entries()

    def delete_row():
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item[0])
            tree_save()  # Update the CSV after deletion

    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0])['values']
            entry_time.delete(0, tk.END)
            entry_time.insert(0, values[0])
            entry_monday.delete(0, tk.END)
            entry_monday.insert(0, values[1])
            entry_tuesday.delete(0, tk.END)
            entry_tuesday.insert(0, values[2])
            entry_wednesday.delete(0, tk.END)
            entry_wednesday.insert(0, values[3])
            entry_thursday.delete(0, tk.END)
            entry_thursday.insert(0, values[4])
            entry_friday.delete(0, tk.END)
            entry_friday.insert(0, values[5])
            entry_saturday.delete(0, tk.END)
            entry_saturday.insert(0, values[6])
            entry_sunday.delete(0, tk.END)
            entry_sunday.insert(0, values[7])

    def navigate(event):
        current_selection = tree.selection()
        if current_selection:
            index = tree.index(current_selection[0])
            if event.keysym == 'Down':
                next_index = index + 1
                if next_index < len(tree.get_children()):
                    tree.selection_set(tree.get_children()[next_index])
                    tree.focus(tree.get_children()[next_index])
                    on_select(event)
            elif event.keysym == 'Up':
                previous_index = index - 1
                if previous_index >= 0:
                    tree.selection_set(tree.get_children()[previous_index])
                    tree.focus(tree.get_children()[previous_index])
                    on_select(event)

    # Entry fields for new data
    entry_time = tk.Entry(root)
    entry_time.pack()
    entry_monday = tk.Entry(root)
    entry_monday.pack()
    entry_tuesday = tk.Entry(root)
    entry_tuesday.pack()
    entry_wednesday = tk.Entry(root)
    entry_wednesday.pack()
    entry_thursday = tk.Entry(root)
    entry_thursday.pack()
    entry_friday = tk.Entry(root)
    entry_friday.pack()
    entry_saturday = tk.Entry(root)
    entry_saturday.pack()
    entry_sunday = tk.Entry(root)
    entry_sunday.pack()

    btn_add = tk.Button(root, text="Add Row", command=add_row)
    btn_add.pack()
    btn_edit = tk.Button(root, text="Edit Row", command=edit_row)
    btn_edit.pack()
    btn_delete = tk.Button(root, text="Delete Row", command=delete_row)
    btn_delete.pack()

    # Create treeview before loading data
    treefun()
    load_data()
    tree.bind("<<TreeviewSelect>>", on_select)
    tree.bind("<Key>", navigate)

    root.mainloop()

if __name__ == '__main__':
    main()
