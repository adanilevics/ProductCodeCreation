import tkinter as tk
from tkinter import ttk

class PrecesKods:
    def __init__(self, root):
        self.root = root
        self.root.title("PrecesKods")

        self.product_label = ttk.Label(root, text="Prece:")
        self.product_combobox = ttk.Combobox(root, values=[item["description"] for item in product_data["items"]], state="readonly")
        self.varieties_label = ttk.Label(root, text="Preces varianti:")
        self.varieties_comboboxes = []
        self.product_code_label = ttk.Label(root, text="Preces kods:")
        self.variety_labels = []  # Initialize the variety labels list

        self.product_combobox.bind("<<ComboboxSelected>>", self.update_varieties)

        self.product_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.varieties_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Set the initial row for varieties
        self.varieties_row = 2

        self.update_varieties(None)  # Initialize the varieties

        self.product_code_label.grid(row=self.varieties_row + len(self.varieties_comboboxes) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def update_varieties(self, event):
        selected_product_description = self.product_combobox.get()

        if not selected_product_description:
            return

        # Clear previous varieties
        for combo_box in self.varieties_comboboxes:
            combo_box.destroy()
        self.varieties_comboboxes = []

        # Clear previous variety labels
        for label in self.variety_labels:
            label.destroy()
        self.variety_labels = []

        selected_product = next((item for item in product_data["items"] if item["description"] == selected_product_description), None)

        # Check if the selected product has varieties
        if selected_product.get("varieties"):
            # Display varieties for the selected product
            for i, variety_code in enumerate(selected_product["varieties"]):
                variety = next(v for v in product_data["varieties"] if v["code"] == variety_code)

                variety_label = ttk.Label(self.root, text=variety["description"] + ":")
                variety_combobox = ttk.Combobox(self.root, values=[opt["description"] for opt in variety["options"]], state="readonly")

                variety_label.grid(row=self.varieties_row + i, column=0, padx=10, pady=5, sticky="w")
                variety_combobox.grid(row=self.varieties_row + i, column=1, padx=10, pady=5, sticky="w")

                self.variety_labels.append(variety_label)
                self.varieties_comboboxes.append(variety_combobox)

                variety_combobox.bind("<<ComboboxSelected>>", self.update_product_code)

        # Update the row index of the product code label dynamically
        self.product_code_label.grid(row=self.varieties_row + len(self.varieties_comboboxes) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.update_product_code(None)

    def update_product_code(self, event):
        selected_product_description = self.product_combobox.get()
        selected_product = next(item for item in product_data["items"] if item["description"] == selected_product_description)

        product_code = selected_product["code"]

        for i, variety_combobox in enumerate(self.varieties_comboboxes):
            selected_option_description = variety_combobox.get()
            variety_code = next((opt["code"] for variety in product_data["varieties"] for opt in variety["options"] if opt["description"] == selected_option_description), "")
            product_code += "." + variety_code

        # Update the row index of the product code label dynamically
        self.product_code_label.grid(row=self.varieties_row + len(self.varieties_comboboxes) + 1, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        self.product_code_label["text"] = f"Preces kods: {product_code}"

if __name__ == "__main__":
    product_data = {
        "varieties": [
            {"code": "SIZE", "description": "Izmērs", "options": [
                {"code": "S", "description": "Small"},
                {"code": "M", "description": "Medium"},
                {"code": "L", "description": "Large"}
            ]},
            {"code": "COLOR", "description": "Krāsa", "options": [
                {"code": "RED", "description": "Sarkans"},
                {"code": "BLU", "description": "Zils"},
                {"code": "WHI", "description": "Balts"}
            ]},
            {"code": "SHOE-SIZE", "description": "Apavu izmērs", "options": [
                {"code": "37", "description": "37"},
                {"code": "38", "description": "38"},
                {"code": "39", "description": "39"},
                {"code": "40", "description": "40"},
                {"code": "41", "description": "41"},
                {"code": "42", "description": "42"},
                {"code": "43", "description": "43"},
                {"code": "44", "description": "44"}
            ]}
        ],
        "items": [
            {"code": "0001", "description": "T-krekls Rīga", "varieties": ["COLOR", "SIZE"]},
            {"code": "0002", "description": "T-krekls ar saules attēlu", "varieties": ["SIZE"]},
            {"code": "1001", "description": "Zābaki 'Great stuff'", "varieties": ["SHOE-SIZE"]},
            {"code": "1002", "description": "Čības ar puķītēm", "varieties": ["COLOR", "SHOE-SIZE"]},
            {"code": "2001", "description": "Melna lodīšu pildspalva", "varieties": []}
        ]
    }

    root = tk.Tk()
    app = PrecesKods(root)
    root.mainloop()
