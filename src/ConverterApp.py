import tkinter as tk
from tkinter import filedialog, messagebox
import image 

class ConverterApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("PPM/PGM Image Converter")
        
        self.file_path = tk.StringVar()
        self.conversion_type = tk.StringVar()
        self.conversion_type.set("convert to PGM")
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="Select an image file:").pack(pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_file).pack()
        tk.Label(self.root, textvariable=self.file_path).pack(pady=10)
        tk.Label(self.root, text="Select conversion type:").pack(pady=5)
        
        conversion_menu = tk.OptionMenu(self.root, self.conversion_type, "Convert to PGM", "Shrink PGM", "Copy PPM", "Copy PGM")
        conversion_menu.pack()
        
        tk.Button(self.root, text="Convert", command=self.convert_file).pack(pady=10)
        
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.ppm;*.pgm")])
        self.file_path.set(file_path)
    
    def convert_file(self):
        input_file = self.file_path.get()
        if not input_file:
            return
        
        conversion_type = self.conversion_type.get()
        
        if conversion_type == "convert to PGM":
            output_file = filedialog.asksaveasfilename(defaultextension=".pgm", filetypes=[("PGM files", "*.pgm")])
            if not output_file:
                return
            
            img = image.read_ppm(input_file)
            if img:
                converted_image = image.convert_to_pgm(img)
                image.write_pgm(converted_image, output_file)
                messagebox.showinfo("Conversion Complete!", "Image conversion to PGM successfully completed!")
                
                
        elif conversion_type == "Shrink PGM":
            output_file = filedialog.asksaveasfilename(defaultextension=".pgm", filetypes=[("PGM files", "*.pgm")])
            if not output_file:
                return
            img = image.read_pgm(input_file)
            if img:
                converted_image = image.shrink_pgm(img)
                image.write_pgm(converted_image, output_file)
                messagebox.showinfo("Conversion Complete!", "Image PGM successfully shrunken!")
                
                
        elif conversion_type == "Copy PPM":
            output_file = filedialog.asksaveasfilename(defaultextension=".ppm", filetypes=[("PPM files", "*.ppm")])
            if not output_file:
                return
            img = image.read_ppm(input_file)
            if img:
                image.write_ppm(img, output_file)
                messagebox.showinfo("Copy Complete!", "Image PPM successfully copied!")
        
        
        elif conversion_type == "Copy PGM":
            output_file = filedialog.asksaveasfilename(defaultextension=".pgm", filetypes=[("PGM files", "*.pgm")])
            if not output_file:
                return
            img = image.read_pgm(input_file)
            if img:
                image.write_pgm(img, output_file)
                messagebox.showinfo("Copy Complete!", "Image PGM successfully copied!")
            
            
                        

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()