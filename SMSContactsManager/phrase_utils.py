import csv
import tkinter as tk

def load_phrases_from_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader if row]


def insert_selected_phrase(text_widget, listbox_phrases):
    selected_index = listbox_phrases.curselection()
    if selected_index:
        selected_phrase = listbox_phrases.get(selected_index[0])
        text_widget.insert(tk.END, selected_phrase + ' ')


def remove_selected_phrase(listbox_phrases, frequently_used_phrases, file_path):
    selected_index = listbox_phrases.curselection()[0]
    listbox_phrases.delete(selected_index)
    frequently_used_phrases.pop(selected_index)

    # Update the CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for phrase in frequently_used_phrases:
            writer.writerow([phrase])

def add_new_phrase(freq_message, listbox_phrases, frequently_used_phrases, file_path):
    new_phrase = freq_message.get()
    frequently_used_phrases.append(new_phrase)
    listbox_phrases.insert(tk.END, new_phrase)

    # Update the CSV file
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([new_phrase])

    freq_message.delete(0, tk.END) # Clear the entry widget
