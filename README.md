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
