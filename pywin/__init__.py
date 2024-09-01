import os
import tkinter as tk
from tkinter import ttk
from PIL import Image
from tkinter import messagebox
import ctypes

class app:
    def __init__(self):
        self.tempdir = './_pywin'
        self.win = tk.Tk()
        self.ismenu = False
        self.__tempdir()
        self.win.resizable(False, False)
        ttk.Style().configure('TButton', background='white', foreground='black')
        self.win.geometry('700x400')
        self._title = 'pywin'
        self.win.config(bg='white')
        default_icon = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.win.tk.call('tk', 'scaling', ScaleFactor / 75)
        default_icon.save(f'{self.tempdir}/resources/default.ico', format='ICO')
        self.win.iconbitmap(f'{self.tempdir}/resources/default.ico')
    def label(self,text='',color='black',bg=None,x=0,y=0,font='微软雅黑',size=10):
        if bg==None:
            if self.bgcolor==None:
                bg='white'
            else:
                bg = self.bgcolor
        tk.Label(text=text,fg=color,bg=bg,font=(font,size)).place(x=0,y=0)
    def size(self,width,height):
        width = str(width)
        height = str(height)
        self.win.geometry(f'{width}x{height}')
    def resizable(self,choice=True):
        self.win.resizable(choice, choice)
    def inputbox(self, style='default', x=0, y=0):
        entry = ttk.Entry()
        entry.place(x=x, y=y)
        return entry

    def msgbox(self, title='无标题', text=''):
        messagebox.showinfo(title, text)

    def set_gradient_bg(self, color1, color2, direction='vertical'):
        for widget in self.win.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        canvas = tk.Canvas(self.win, bg=color1, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)

        def interpolate_color(start_color, end_color, factor):
            start_color = start_color.lstrip('#')
            end_color = end_color.lstrip('#')
            start_rgb = [int(start_color[i:i+2], 16) for i in (0, 2, 4)]
            end_rgb = [int(end_color[i:i+2], 16) for i in (0, 2, 4)]
            new_rgb = [int(start + (end - start) * factor) for start, end in zip(start_rgb, end_rgb)]
            return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

        width = self.win.winfo_width()
        height = self.win.winfo_height()
        steps = height if direction == 'vertical' else width
        for i in range(steps):
            factor = i / steps
            color = interpolate_color(color1, color2, factor)
            if direction == 'vertical':
                canvas.create_line(0, i, width, i, fill=color, width=1)
            else:
                canvas.create_line(i, 0, i, height, fill=color, width=1)

        ttk.Style().configure('TButton', background=color1, foreground='black')
        self.win.config(bg=color1)

    def set_bg(self,color):
        self.bgcolor = color
        self.win.config(bg=color)
    def button(self, text='按钮', style='default', x=1, y=1, onclick=None):
        if style == 'default':
            btn = ttk.Button(self.win, text=text, command=onclick)
            btn.place(x=x, y=y)
        return btn

    def menu(self, text='菜单', onclick=None):
        if not self.ismenu:
            self.menu_bar = tk.Menu(self.win)
            self.win.config(menu=self.menu_bar)
            self.ismenu = True
        new_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=text, menu=new_menu, command=onclick)
        return new_menu

    def __tempdir(self):
        os.makedirs(f'{self.tempdir}/', exist_ok=True)
        os.makedirs(f'{self.tempdir}/resources/', exist_ok=True)

    def set_title(self, title):
        self._title = title
        self.win.title(title)

    def display(self):
        self.win.mainloop()

    def close(self):
        self.win.destroy()
