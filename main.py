import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageDraw, ImageFont

DARK_BLUE = "#293b5f"
NAVY = "#47597e"
LIGHT_BLUE = "#dbe6fd"
SAND = "#b2ab8c"


class WatermarkApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Watermark App")
        self.window.config(padx=10, pady=10, bg=DARK_BLUE)
        self.img = None
        self.photo_name = ''
        self.img_height = 0
        self.img_width = 0

        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.grid(row=1, column=0, columnspan=3, pady=20, padx=20)

        self.title = tk.Label(text="Watermark App", font=("Arial", 24), fg=SAND, bg=NAVY)
        self.title.grid(row=0, column=0, columnspan=2, pady=15)

        self.load_btn = tk.Button(text="Select Photo", command=self.select_image)
        self.load_btn.grid(row=0, column=2)

        self.text_entry = tk.Entry(width=25)
        self.text_entry.insert(tk.END, string="Type Watermark Text Here")
        self.text_entry.grid(row=3, column=0, pady=10)

        self.add_watermark_btn = tk.Button(text="Preview Watermark", command=self.preview_watermark)
        self.add_watermark_btn.grid(row=4, column=0, pady=10)

        self.save_btn = tk.Button(text="Save Image", command=self.save_image)
        self.save_btn.grid(row=4, column=1, pady=10)

        self.text_label = tk.Label(text="Text", font=("Arial", 14), fg=SAND, bg=NAVY)
        self.text_label.grid(row=2, column=0)

        self.font_label = tk.Label(text="Font", font=("Arial", 14), fg=SAND, bg=NAVY)
        self.font_label.grid(row=2, column=1, pady=10)

        self.font_size_label = tk.Label(text="Font Size", font=("Arial", 14), fg=SAND, bg=NAVY)
        self.font_size_label.grid(row=2, column=2, pady=10)

        self.listbox = tk.Listbox(height=3)
        self.fonts = ["Arial", "Verdana", "Times"]
        for item in self.fonts:
            self.listbox.insert(self.fonts.index(item), item)
        self.listbox.grid(row=3, column=1, pady=10)

        self.font_size = tk.Spinbox(from_=80, to=400, width=5, command=self.spinbox_used)
        self.font_size.grid(row=3, column=2, pady=10)

        self.success_text = tk.StringVar()
        self.success_text.set('')
        self.success_label = tk.Label(self.window, textvariable=self.success_text, fg=LIGHT_BLUE, bg=NAVY)
        self.success_label.grid(row=5, column=0, columnspan=3)

        self.window.mainloop()

    def spinbox_used(self):
        self.font_size.get()

    def select_image(self):
        self.photo_name = tk.filedialog.askopenfilename()
        self.img = Image.open(self.photo_name)
        print(self.img)
        self.img_width = self.img.size[0]
        self.img_height = self.img.size[1]
        self.display_img()

    def preview_watermark(self):
        self.img = Image.open(self.photo_name)
        draw = ImageDraw.Draw(self.img)
        text = f"{self.text_entry.get()}"
        selection = self.listbox.curselection()
        if selection:
            selected_font = self.listbox.get(self.listbox.curselection()).lower()
        else:
            selected_font = 'arial'
        font = ImageFont.truetype(font=f'{selected_font}', size=int(self.font_size.get()))
        textwidth, textheight = draw.textsize(text, font)

        margin = 35
        x = self.img_width - textwidth - margin
        y = self.img_height - textheight - margin
        draw.text((x, y), text, font=font)
        self.display_img()

    def save_image(self):
        watermarked_name = self.photo_name[:-4] + "WM.jpg"
        self.img.save(f'{watermarked_name}')
        self.success_text.set(f"Success!! File saved to {watermarked_name}")

    def display_img(self):
        f_size = (400, 400)
        factor = min(float(f_size[1]) / self.img_height, float(f_size[0]) / self.img_width)

        width = int(self.img_width * factor)

        height = int(self.img_height * factor)

        rImg = self.img.resize((width, height), Image.ANTIALIAS)
        rImg = ImageTk.PhotoImage(rImg)
        self.canvas.create_image(200, 200, image=rImg)
        self.canvas.image = rImg


watermark_app = WatermarkApp()
