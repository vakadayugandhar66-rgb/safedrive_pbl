import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE = "trips.json"

def load():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save():
    with open(FILE, "w") as f:
        json.dump(trips, f, indent=4)

trips = load()

def display():
    for row in table.get_children():
        table.delete(row)

    for trip in trips:
        table.insert("", "end", values=(
            trip["id"], trip["driver"], trip["vehicle"],
            trip["state"], trip["city"], trip["date"]
        ))

    total.config(text="Total Trips: " + str(len(trips)))

def add_trip():
    if not all(entry.get().strip() for entry in entries):
        messagebox.showwarning("Warning", "Enter all details")
        return

    trip = {
        "id": max([t["id"] for t in trips], default=0) + 1,
        "driver": entries[0].get(),
        "vehicle": entries[1].get(),
        "state": entries[2].get(),
        "city": entries[3].get(),
        "date": entries[4].get()
    }

    trips.append(trip)
    save()
    display()
    clear()
    messagebox.showinfo("Success", "Trip Added Successfully!")

def clear():
    for entry in entries:
        entry.delete(0, tk.END)

def edit_trip():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a trip first")
        return

    trip_id = table.item(selected[0])["values"][0]
    trip = next(t for t in trips if t["id"] == trip_id)

    for entry, key in zip(entries, ["driver", "vehicle", "state", "city", "date"]):
        entry.delete(0, tk.END)
        entry.insert(0, trip[key])

    trips.remove(trip)
    save()
    display()

def delete_trip():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a trip first")
        return

    trip_id = table.item(selected[0])["values"][0]

    if messagebox.askyesno("Confirm", "Delete this trip?"):
        trips[:] = [t for t in trips if t["id"] != trip_id]
        save()
        display()

root = tk.Tk()
root.title("SafeDrive - Vehicle Trip Logger")
root.geometry("900x600")
root.configure(bg="#eaf2f8")

tk.Label(root, text="SafeDrive Vehicle Trip Logger",
         font=("Arial", 22, "bold"),
         bg="#eaf2f8", fg="#163b65").pack(pady=15)

total = tk.Label(root, text="Total Trips: 0",
                 font=("Arial", 14, "bold"), bg="#eaf2f8")
total.pack()

form = tk.Frame(root, bg="#eaf2f8")
form.pack(pady=15)

labels = ["Driver Name", "Vehicle Number", "State", "City", "Date"]

entries = []

for i, label in enumerate(labels):
    tk.Label(form, text=label, bg="#eaf2f8",
             font=("Arial", 11)).grid(row=i, column=0, padx=10, pady=5)

    entry = tk.Entry(form, width=30)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

buttons = tk.Frame(root, bg="#eaf2f8")
buttons.pack(pady=10)

tk.Button(buttons, text="Add Trip", width=12,
          bg="#27ae60", fg="white", command=add_trip).grid(row=0, column=0, padx=5)

tk.Button(buttons, text="Edit Trip", width=12,
          bg="#2980b9", fg="white", command=edit_trip).grid(row=0, column=1, padx=5)

tk.Button(buttons, text="Delete Trip", width=12,
          bg="#c0392b", fg="white", command=delete_trip).grid(row=0, column=2, padx=5)

tk.Button(buttons, text="Clear", width=12,
          command=clear).grid(row=0, column=3, padx=5)

table = ttk.Treeview(root, columns=("ID", "Driver", "Vehicle",
                                    "State", "City", "Date"),
                     show="headings")

for col in ("ID", "Driver", "Vehicle", "State", "City", "Date"):
    table.heading(col, text=col)
    table.column(col, width=130)

table.pack(fill="both", expand=True, padx=15, pady=15)

display()

root.mainloop()