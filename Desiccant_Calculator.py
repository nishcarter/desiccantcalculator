import tkinter as tk

# Flag to prevent infinite loop between conversion functions
updating_entries = False

def calculate_shelf_life():
    try:
        # Get values from entries
        U = float(U_entry.get())
        D = float(D_entry.get())
        WVTR_in = WVTR_in_var.get()
        WVTR_m2 = WVTR_m2_var.get()
        L_in = L_in_var.get()  # Length in inches
        W_in = W_in_var.get()  # Width in inches

        # Check which WVTR input is used and convert if necessary
        if WVTR_in:
            WVTR = float(WVTR_in)
        elif WVTR_m2:
            WVTR = float(WVTR_m2) / 15.50031
        else:
            raise ValueError("Please enter a value for WVTR.")

        # Check if inch entries are used, otherwise convert millimeters to inches
        if not L_in:
            L_mm = L_var.get()
            L_in = float(L_mm) / 25.4
        else:
            L_in = float(L_in)

        if not W_in:
            W_mm = W_var.get()
            W_in = float(W_mm) / 25.4
        else:
            W_in = float(W_in)

        A = (L_in * W_in) * 2  # Total surface area in square inches

        # Calculate shelf life in months based on the formula provided in JEDEC spec
        calculated_shelf_life = (U * D) / (0.304 * WVTR * A)

        # Set the result color based on the calculated shelf life
        result_color = "green" if calculated_shelf_life > 24 else "red"

        # Display the result
        result_label.config(text=f"Calculated Shelf Life: {calculated_shelf_life:.2f} months", fg=result_color)

    except ValueError as e:
        result_label.config(text=str(e), fg="red")

def mm_to_inch_update(*args):
    global updating_entries
    if not updating_entries:
        updating_entries = True
        try:
            L_mm = L_var.get()
            W_mm = W_var.get()
            if L_mm:
                L_in = float(L_mm) / 25.4
                L_in_var.set(f"{L_in:.2f}")
            if W_mm:
                W_in = float(W_mm) / 25.4
                W_in_var.set(f"{W_in:.2f}")
        except ValueError:
            L_in_var.set("")
            W_in_var.set("")
        finally:
            updating_entries = False

def inch_to_mm_update(*args):
    global updating_entries
    if not updating_entries:
        updating_entries = True
        try:
            L_in = L_in_var.get()
            W_in = W_in_var.get()
            if L_in:
                L_mm = float(L_in) * 25.4
                L_var.set(f"{L_mm:.2f}")
            if W_in:
                W_mm = float(W_in) * 25.4
                W_var.set(f"{W_mm:.2f}")
        except ValueError:
            L_var.set("")
            W_var.set("")
        finally:
            updating_entries = False

def wvtr_in_to_m2_update(*args):
    global updating_entries
    if not updating_entries:
        updating_entries = True
        try:
            WVTR_in = WVTR_in_var.get()
            if WVTR_in:
                WVTR_m2 = float(WVTR_in) * 15.50031
                WVTR_m2_var.set(f"{WVTR_m2:.5f}")  # Display up to five decimal places
        except ValueError:
            WVTR_m2_var.set("")
        finally:
            updating_entries = False

def wvtr_m2_to_in_update(*args):
    global updating_entries
    if not updating_entries:
        updating_entries = True
        try:
            WVTR_m2 = WVTR_m2_var.get()
            if WVTR_m2:
                WVTR_in = float(WVTR_m2) / 15.50031
                WVTR_in_var.set(f"{WVTR_in:.5f}")  # Display up to five decimal places
        except ValueError:
            WVTR_in_var.set("")
        finally:
            updating_entries = False

def clear_all_entries():
    global updating_entries
    updating_entries = True  # Prevent conversion functions from triggering
    # Clear all StringVar instances
    L_var.set("")
    W_var.set("")
    L_in_var.set("")
    W_in_var.set("")
    WVTR_in_var.set("")
    WVTR_m2_var.set("")
    U_entry.delete(0, tk.END)
    D_entry.delete(0, tk.END)
    # Clear the result label
    result_label.config(text="")
    updating_entries = False  # Allow conversion functions to trigger again

# Create the main window
root = tk.Tk()
root.title("Shelf Life Calculator")
root.geometry("1000x600")  # Set the size of the window

# Define font
large_font = ("Verdana", 12)

# Create StringVar instances for the millimeter, inch and WVTR entries
L_var = tk.StringVar()
W_var = tk.StringVar()
L_in_var = tk.StringVar()
W_in_var = tk.StringVar()
WVTR_in_var = tk.StringVar()
WVTR_m2_var = tk.StringVar()

# Define the layout
# Labels and entry fields for user inputs
tk.Label(root, text="Amount of desiccant in UNITS (U):", font=large_font).grid(row=0, column=0, sticky="W")
tk.Label(root, text="The amount of water in grams that a UNIT of desiccant can absorb at 10% RH and 25°C (D):", font=large_font).grid(row=1, column=0, sticky="W")
tk.Label(root, text="WVTR in grams / 100 inches square:", font=large_font).grid(row=2, column=0, sticky="W")
tk.Label(root, text="WVTR in grams / meters square:", font=large_font).grid(row=3, column=0, sticky="W")
tk.Label(root, text="Length of MBB (if in millimeters):", font=large_font).grid(row=4, column=0, sticky="W")
tk.Label(root, text="Width of MBB (if in millimeters):", font=large_font).grid(row=5, column=0, sticky="W")
tk.Label(root, text="Length of MBB (if in inches):", font=large_font).grid(row=6, column=0, sticky="W")
tk.Label(root, text="Width of MBB (if in inches):", font=large_font).grid(row=7, column=0, sticky="W")

U_entry = tk.Entry(root, font=large_font)
D_entry = tk.Entry(root, font=large_font)
WVTR_in_entry = tk.Entry(root, textvariable=WVTR_in_var, font=large_font)
WVTR_m2_entry = tk.Entry(root, textvariable=WVTR_m2_var, font=large_font)
L_entry = tk.Entry(root, textvariable=L_var, font=large_font)
W_entry = tk.Entry(root, textvariable=W_var, font=large_font)
L_in_entry = tk.Entry(root, textvariable=L_in_var, font=large_font)
W_in_entry = tk.Entry(root, textvariable=W_in_var, font=large_font)

U_entry.grid(row=0, column=1)
D_entry.grid(row=1, column=1)
WVTR_in_entry.grid(row=2, column=1)
WVTR_m2_entry.grid(row=3, column=1)
L_entry.grid(row=4, column=1)
W_entry.grid(row=5, column=1)
L_in_entry.grid(row=6, column=1)
W_in_entry.grid(row=7, column=1)

# Label for displaying the results
result_label = tk.Label(root, text="", font=large_font)
result_label.grid(row=9, column=0, columnspan=2)

# Add trace to StringVar instances to update entries dynamically
L_var.trace_add("write", mm_to_inch_update)
W_var.trace_add("write", mm_to_inch_update)
L_in_var.trace_add("write", inch_to_mm_update)
W_in_var.trace_add("write", inch_to_mm_update)
WVTR_in_var.trace_add("write", wvtr_in_to_m2_update)
WVTR_m2_var.trace_add("write", wvtr_m2_to_in_update)

# Button to perform calculation
calculate_button = tk.Button(root, text="Calculate", font=large_font, command=calculate_shelf_life)
calculate_button.grid(row=11, column=0, columnspan=2, pady=10)

# Create a clear button
clear_button = tk.Button(root, text="Clear", font=large_font, command=clear_all_entries)
clear_button.grid(row=12, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
