# 🌀 Tkinter-to-Kivy Project

**Take your native Tkinter code and live-translate it into Kivy!**  
This experimental toolkit lets you run Tkinter-style syntax on top of a Kivy backend — giving you a glimpse into how well your GUI code adapts to a cross-platform framework.

## ⚠️ Alpha Disclaimer

This is **very much an alpha** translator. Bugs? Absolutely. Quirks? Plenty.  
It’s more of an exploratory toolkit than a production-ready solution. The goal is to stress-test your Tkinter code and see how well it **might** translate — or fail entirely.  
If it crashes gloriously or misbehaves creatively, let us know in the [Issues tab](../../issues)!

---

## 🧠 How It Works

Simply import from `tkintertokivy` to enable translation mode. Then use Tkinter syntax as you normally would.

```python
# Enable translation with special imports
from tkintertokivy import tk       # Tk module wrapper
from tkintertokivy import tkFont   # Font handling
from tkintertokivy import Label    # Widget translation

# Load Tkinter modules
import tkinter as tk
import tkinter.ttk as ttk
from tkintertokivy import auto_translate_mode

# Activate translation mode
auto_translate_mode()

# Continue with typical Tkinter widgets
from tkinter import Entry
from tkinter import StringVar, Checkbutton, Radiobutton, IntVar, Text, Button, messagebox
```

> 🔍 **Important:** Make sure the `tkintertokivy` module is located in the **same directory** as the main program that imports it. Relative import paths are not supported at this time.

---

## ⭐ Show Support & Get Involved

If you like the idea behind this project, please **star** it on GitHub — it helps others discover it too!  
We’re also actively looking for **volunteer contributors**. No commissions, no paychecks — just curiosity, creativity, and community.  
Whether you want to squash bugs, polish translations, or break the system in elegant ways, your input is welcome.

---

## 💬 Questions or Ideas?

Ping us in [Issues](../../issues) to report translation problems, share improvement ideas, or ask about contributing.

---

## 📜Demo Code

<img width="811" height="636" alt="image" src="https://github.com/user-attachments/assets/c24f3d2b-9acf-46ee-b6c7-367c1298d88e" />

```
# Enable translation with special imports
from tkintertokivy import tk       # Tk module wrapper
from tkintertokivy import tkFont   # Font handling
from tkintertokivy import Label    # Widget translation

# Load Tkinter modules
import tkinter as tk
import tkinter.ttk as ttk
from tkintertokivy import auto_translate_mode

# Activate translation mode
auto_translate_mode()

# Continue with typical Tkinter widgets
from tkinter import Entry
from tkinter import StringVar, Checkbutton, Radiobutton, IntVar, Text, Button, messagebox

def button_click():
    print("Button clicked!")

root = tk.Tk()
root.title("My Demo App")

button = tk.Button(root, text="Click Me", bg="blue", command=button_click)
button.place(x=50, y=0, width=100, height=30)
check = Checkbutton(root, text="Check Me", variable=IntVar())
check.place(x=200, y=0, width=100, height=30)
entry1 = Entry(root)
entry1.place(x=350, y=0, width=100, height=30)
entry1.insert(0, "Type here")

root.mainloop()
```

<img width="320" height="368" alt="355979072-ea2ae750-d9e6-4a64-8755-dc9322d70816" src="https://github.com/user-attachments/assets/035e8a72-2d52-4612-abeb-8c34adafc9d5" />
