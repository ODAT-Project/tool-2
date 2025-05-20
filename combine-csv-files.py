import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

class CSVCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Combiner App")
        #make the window larger
        self.root.geometry("600x400")

        #create menu bar with About Me section
        menubar = tk.Menu(self.root)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About Me", command=self.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

        #about Me text at top
        about_frame = tk.Frame(self.root)
        about_frame.pack(pady=10)
        about_label = tk.Label(
            about_frame,
            text="About: combine cleaned csv file -- developed by ODAT project",
            wraplength=550,
            justify="left"
        )
        about_label.pack()

        #buttons for selecting and combining files
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        self.select_files_btn = tk.Button(
            btn_frame,
            text="Select CSV Files",
            command=self.select_files,
            width=20
        )
        self.select_files_btn.pack(side="left", padx=10)

        self.combine_files_btn = tk.Button(
            btn_frame,
            text="Combine and Save CSV",
            command=self.combine_and_save,
            width=20
        )
        self.combine_files_btn.pack(side="left", padx=10)

        self.selected_files = []

    def show_about(self):
        messagebox.showinfo(
            "About Me",
            "CSV Combiner App\nDeveloped by ODAT project"
        )

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(
            title="Select CSV Files",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*")]
        )
        if not self.selected_files:
            messagebox.showinfo("No Files Selected", "Please select at least one CSV file.")
        else:
            messagebox.showinfo("Files Selected", f"{len(self.selected_files)} files selected.")

    def combine_and_save(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected. Please select files first.")
            return

        try:
            combined_data = pd.DataFrame()
            reference_header = None

            for file in self.selected_files:
                df = pd.read_csv(file)

                if reference_header is None:
                    reference_header = set(df.columns)
                else:
                    common_columns = reference_header.intersection(set(df.columns))
                    df = df[list(common_columns)]

                combined_data = pd.concat([combined_data, df], ignore_index=True)

            save_path = filedialog.asksaveasfilename(
                title="Save Combined CSV",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")]
            )
            if save_path:
                combined_data.to_csv(save_path, index=False)
                messagebox.showinfo("Success", f"Combined CSV saved to {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVCombinerApp(root)
    root.mainloop()
