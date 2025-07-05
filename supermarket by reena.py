import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Global list to store items currently added to the bill
current_bill_items = []

# Product database with predefined items and their prices
product_database = {
    "Apple": 2.50,
    "Banana": 1.20,
    "Milk(1L)": 3.00,
    "Bread": 2.25,
    "Eggs(1 Doz)": 4.50,
    "Chicken(1kg)": 8.75,
    "Rice (5kg)": 10.00,
    "Pasta (500g)": 1.75,
    "Cheese (200g)": 3.80,
    "Water Bottle": 1.00
}

def add_item_to_bill():
    """
    Adds an item to the current bill.
    Validates input, checks if the product exists, and updates the bill.
    """
    item_name = item_name_entry.get().strip()
    quantity_str = quantity_entry.get().strip()

    # Input validation
    if not item_name or not quantity_str:
        messagebox.showwarning("Input Error", "Please fill in item name and quantity.")
        return

    if item_name not in product_database:
        messagebox.showwarning("Product Not Found", f"{item_name} is not in our product database.")
        return

    try:
        quantity = int(quantity_str)
        if quantity <= 0:
            messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a whole number.")
        return

    price = product_database[item_name]
    subtotal = quantity * price
    found_item = False

    # Check if the item already exists in the bill to update quantity and subtotal
    for item in current_bill_items:
        if item['name'].lower() == item_name.lower():
            item['quantity'] += quantity
            item['subtotal'] += subtotal
            found_item = True
            break

    # If item is new, add it to the bill
    if not found_item:
        item = {
            'name': item_name,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        }
        current_bill_items.append(item)

    # Update GUI displays
    update_item_list_display()
    clear_item_input_fields()
    update_bill_preview()

def update_item_list_display():
    """
    Refreshes the Treeview widget in the 'Add items' tab to show current bill items.
    Also updates the 'Current Total' label on this tab.
    """
    # Clear existing items in the Treeview
    for i in item_display_tree.get_children():
        item_display_tree.delete(i)

    # Insert current bill items into the Treeview
    for item in current_bill_items:
        item_display_tree.insert("", "end", values=(item['name'], item['quantity'], f"₹{item['subtotal']:.2f}"))

    # Calculate and update the total for the input tab
    total_amount = sum(item['subtotal'] for item in current_bill_items)
    input_tab_total_label.config(text=f"Current Total: ₹{total_amount:.2f}")

def update_bill_preview():
    """
    Generates and displays the full invoice in the 'View Bill' tab's text area.
    Calculates and updates the 'Grand Total'.
    """
    bill_text_area.config(state=tk.NORMAL) # Enable editing to clear and insert text
    bill_text_area.delete(1.0, tk.END) # Clear existing text

    if not current_bill_items:
        bill_text_area.insert(tk.END, "No items added yet. Add items in the 'Add items' tab.\n")
        total_bill_label.config(text="Grand Total: ₹0.00")
        bill_text_area.config(state=tk.DISABLED) # Disable editing after update
        return

    # Add header information
    bill_text_area.insert(tk.END, "--- Supermarket Invoice ---\n\n")
    bill_text_area.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    bill_text_area.insert(tk.END, "-" * 50 + "\n")
    bill_text_area.insert(tk.END, f"{'Item':<20}{'Qty':<8}{'Price':<10}{'Subtotal':<10}\n")
    bill_text_area.insert(tk.END, "-" * 50 + "\n")

    total_amount = 0.0
    # Add each item's details
    for item in current_bill_items:
        bill_text_area.insert(
            tk.END,
            f"{item['name']:<20}{item['quantity']:<8}{item['price']:<10.2f}{item['subtotal']:<10.2f}\n"
        )
        total_amount += item['subtotal']

    # Add footer information
    bill_text_area.insert(tk.END, "-" * 50 + "\n")
    bill_text_area.insert(tk.END, f"Total items: {len(current_bill_items)}\n")
    bill_text_area.insert(tk.END, f"Amount Payable: ₹{total_amount:.2f}\n")
    bill_text_area.insert(tk.END, "\nThank you for shopping with us! Visit again!\n")

    total_bill_label.config(text=f"Grand Total: ₹{total_amount:.2f}") # Update main total label
    bill_text_area.config(state=tk.DISABLED) # Disable editing

def clear_bill():
    """
    Clears all items from the current bill, resetting the system.
    """
    global current_bill_items
    current_bill_items = [] # Empty the list
    update_item_list_display() # Refresh item display
    update_bill_preview()      # Refresh bill preview
    clear_item_input_fields()  # Clear input fields
    messagebox.showinfo("Bill Cleared", "The current bill has been cleared.")

def clear_item_input_fields():
    """
    Clears the text from the item name and quantity entry fields.
    """
    item_name_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    item_name_entry.focus_set() # Set focus back to item name entry

def populate_autocomplete(event=None):
    """
    Provides autocomplete suggestions for item names based on the product database.
    Displays suggestions in a Listbox.
    """
    typed_text = item_name_entry.get().strip().lower()
    suggestions = [p for p in product_database if p.lower().startswith(typed_text)]

    item_name_listbox.delete(0, tk.END) # Clear previous suggestions
    for suggestion in suggestions:
        item_name_listbox.insert(tk.END, suggestion) # Insert new suggestions

    # Position and show/hide the listbox based on suggestions
    if suggestions and typed_text: # Only show if there's typed text and suggestions
        item_name_listbox.place(
            x=item_name_entry.winfo_x(),
            y=item_name_entry.winfo_y() + item_name_entry.winfo_height(),
            width=item_name_entry.winfo_width()
        )
    else:
        item_name_listbox.place_forget() # Hide if no suggestions or input

def select_autocomplete_item(event):
    """
    Handles selection from the autocomplete listbox.
    Fills the item name entry with the selected item and hides the listbox.
    """
    if item_name_listbox.curselection(): # Check if an item is selected
        selected_item = item_name_listbox.get(item_name_listbox.curselection())
        item_name_entry.delete(0, tk.END)
        item_name_entry.insert(0, selected_item)
        item_name_listbox.place_forget() # Hide the listbox
        quantity_entry.focus_set() # Move focus to quantity entry

# --- GUI Setup ---
root = tk.Tk()
root.title("Supermarket Billing System (Advanced)")
root.geometry("900x700") # Initial window size
root.resizable(True, True) # Allow resizing

# Colors & Fonts for a modern look
BG_COLOR = "#ECEFF1"         # Light Grey Blue
HEADER_COLOR = "#263238"     # Dark Blue Grey
ACCENT_COLOR = "#4CAF50"     # Green
TEXT_COLOR = "#212121"       # Dark Grey
BUTTON_PRIMARY = "#1976D2"   # Blue
BUTTON_DANGER = "#D32F2F"    # Red
FONT_HEADING = ("Montserrat", 22, "bold")
FONT_SUBHEADING = ("Roboto", 14, "bold")
FONT_NORMAL = ("Open Sans", 11)
FONT_MONO = ("Consolas", 10) # Monospaced font for bill preview

# Apply ttk (themed Tkinter) styles for a better look
style = ttk.Style()
style.theme_use('clam') # Use 'clam' theme for a flatter, modern look
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.map("TNotebook.Tab", background=[("selected", ACCENT_COLOR)], foreground=[("selected", "white")])
style.configure("TNotebook.Tab", font=FONT_SUBHEADING)
style.configure("Treeview.Heading", font=FONT_SUBHEADING, background=HEADER_COLOR, foreground="white")
style.configure("Treeview", font=FONT_NORMAL, rowheight=25)

# Main window background color
root.config(bg=BG_COLOR)

# --- Header Frame ---
header_frame = tk.Frame(root, bg=HEADER_COLOR)
header_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
header_label = tk.Label(header_frame, text="SuperMart Billing System", font=FONT_HEADING, fg="white", bg=HEADER_COLOR)
header_label.pack(pady=15)

# --- Notebook (Tabbed Interface) ---
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

# --- 'Add Items' Tab ---
add_items_tab = tk.Frame(notebook, bg=BG_COLOR, padx=10, pady=10)
notebook.add(add_items_tab, text="+ Add items")

# Input Section Frame
input_section_frame = tk.LabelFrame(add_items_tab, text="Enter Item Details", font=FONT_SUBHEADING,
                                    bg=BG_COLOR, fg=TEXT_COLOR, padx=15, pady=15)
input_section_frame.pack(pady=10, padx=10, fill=tk.X)

# Item Name Input with Autocomplete
tk.Label(input_section_frame, text="Item Name:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).grid(
    row=0, column=0, padx=5, pady=5, sticky=tk.W)
item_name_entry = tk.Entry(input_section_frame, font=FONT_NORMAL, width=40)
item_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
item_name_entry.bind("<KeyRelease>", populate_autocomplete) # Bind key release for autocomplete

# Autocomplete Listbox (initially hidden)
item_name_listbox = tk.Listbox(input_section_frame, font=FONT_NORMAL, height=5, selectmode=tk.SINGLE, bd=1, relief="solid")
item_name_listbox.bind("<<ListboxSelect>>", select_autocomplete_item)
# This listbox is placed dynamically by populate_autocomplete

# Quantity Input
tk.Label(input_section_frame, text="Quantity:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).grid(
    row=1, column=0, padx=5, pady=5, sticky=tk.W)
quantity_entry = tk.Entry(input_section_frame, font=FONT_NORMAL, width=15)
quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Add Item Button
add_item_button = tk.Button(input_section_frame, text="Add Item to Bill", command=add_item_to_bill,
                            font=FONT_SUBHEADING, bg=BUTTON_PRIMARY, fg="white", padx=15, pady=8)
add_item_button.grid(row=2, column=0, columnspan=2, pady=15)

# Current Total Label for the input tab
input_tab_total_label = tk.Label(input_section_frame, text="Current Total: ₹0.00", font=FONT_SUBHEADING,
                                 bg=BG_COLOR, fg=BUTTON_DANGER) # Highlight current total
input_tab_total_label.grid(row=3, column=0, columnspan=2, pady=10)

# Frame for displaying added items (Treeview)
added_items_frame = tk.LabelFrame(add_items_tab, text="Items in Current Bill", font=FONT_SUBHEADING,
                                  bg=BG_COLOR, fg=TEXT_COLOR, padx=10, pady=10)
added_items_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Treeview widget for displaying bill items
columns = ('item_name', 'quantity', 'subtotal') # Removed 'price' from display as it's less critical here
item_display_tree = ttk.Treeview(added_items_frame, columns=columns, show='headings', height=10)
item_display_tree.heading('item_name', text='Item Name', anchor=tk.W)
item_display_tree.heading('quantity', text='Quantity', anchor=tk.W)
item_display_tree.heading('subtotal', text='Subtotal', anchor=tk.W)

# Column widths and stretch properties
item_display_tree.column('item_name', width=200, stretch=tk.YES)
item_display_tree.column('quantity', width=100, stretch=tk.NO)
item_display_tree.column('subtotal', width=150, stretch=tk.NO) # Increased subtotal width
item_display_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the Treeview
tree_scrollbar = ttk.Scrollbar(added_items_frame, orient="vertical", command=item_display_tree.yview)
tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
item_display_tree.configure(yscrollcommand=tree_scrollbar.set)

# --- 'View Bill' Tab ---
view_bill_tab = tk.Frame(notebook, bg=BG_COLOR, padx=10, pady=10)
notebook.add(view_bill_tab, text="View Bill")

# Frame for displaying the complete invoice
bill_display_frame = tk.LabelFrame(view_bill_tab, text="Complete Invoice", font=FONT_SUBHEADING,
                                   bg=BG_COLOR, fg=TEXT_COLOR, padx=10, pady=10)
bill_display_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Text area for the bill preview
bill_text_area = tk.Text(bill_display_frame, font=FONT_MONO, bg="white", fg=TEXT_COLOR, wrap=tk.WORD,
                         bd=2, relief="groove") # Added border for better visibility
bill_text_area.pack(expand=True, fill=tk.BOTH)

# Scrollbar for the bill text area
bill_scrollbar = ttk.Scrollbar(bill_text_area, command=bill_text_area.yview)
bill_text_area.config(yscrollcommand=bill_scrollbar.set)
bill_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# --- Control Frame (Bottom Section) ---
control_frame = tk.Frame(root, bg=HEADER_COLOR)
control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

# Grand Total Label
total_bill_label = tk.Label(control_frame, text="Grand Total: ₹0.00", font=("Montserrat", 20, "bold"),
                            bg=HEADER_COLOR, fg="white")
total_bill_label.pack(side=tk.LEFT, padx=20, pady=10)

# Clear Bill Button
clear_bill_button = tk.Button(control_frame, text="Clear Bill", command=clear_bill,
                              font=FONT_SUBHEADING, bg=BUTTON_DANGER, fg="white", padx=20, pady=10)
clear_bill_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Initial updates to display empty states
update_item_list_display()
update_bill_preview()

# Start the Tkinter event loop
root.mainloop()
