"""
TkinterToKivy - A simple module to translate tkinter code to Kivy code

Usage:
    import tkintertokivy as ttk
    
    # Translate complete tkinter code
    kivy_code = ttk.translate(your_tkinter_code)
    
    # Or translate specific components
    kivy_button = ttk.translate_button(tkinter_button_code)
    kivy_imports = ttk.translate_imports(tkinter_import_code)
    
    # Auto-translate mode: Just import this module and write tkinter code normally
    # The module will automatically intercept and translate to Kivy
    
Example:
    import tkintertokivy as ttk
    
    tkinter_code = '''
    import tkinter as tk
    root = tk.Tk()
    button = tk.Button(root, text="Click Me")
    button.pack()
    root.mainloop()
    '''
    
    kivy_code = ttk.translate(tkinter_code)
    print(kivy_code)
"""

import sys
import types
import inspect

# Store original modules for restoration if needed
_original_modules = {}

def auto_translate_mode():
    """
    Enable automatic translation mode. After calling this, tkinter code will be
    automatically translated to Kivy code.
    """
    # Create a fake tkinter module that translates calls to Kivy
    fake_tkinter = types.ModuleType('tkinter')
    
    # Store original if it exists
    if 'tkinter' in sys.modules:
        _original_modules['tkinter'] = sys.modules['tkinter']
    
    # Create fake Tk class that starts Kivy app
    class FakeTk:
        def __init__(self):
            self._kivy_app = None
            self._widgets = []
            self._title = "Kivy App"
            self._setup_kivy()
            
        def _setup_kivy(self):
            # Import Kivy components
            try:
                from kivy.app import App
                from kivy.uix.boxlayout import BoxLayout
                from kivy.uix.button import Button
                from kivy.uix.label import Label
                
                class AutoApp(App):
                    def __init__(self, parent_tk, **kwargs):
                        self.parent_tk = parent_tk
                        super().__init__(**kwargs)
                        
                    def build(self):
                        self.layout = BoxLayout(orientation='vertical')
                        # Add any widgets that were created before mainloop
                        for widget in self.parent_tk._widgets:
                            self.layout.add_widget(widget)
                        return self.layout
                
                self._kivy_app_class = AutoApp
                
            except ImportError:
                print("Warning: Kivy not installed. Running in simulation mode.")
                self._kivy_app_class = None
        
        def title(self, text):
            # Store title for Kivy app
            self._title = text
            print(f"Window title set to: {text}")
            
        def geometry(self, size):
            # Store geometry for Kivy app
            self._geometry = size
            print(f"Window geometry set to: {size}")
            
        def mainloop(self):
            if self._kivy_app_class:
                print(f"Starting Kivy app with {len(self._widgets)} widgets...")
                app = self._kivy_app_class(self)
                if hasattr(self, '_title'):
                    app.title = self._title
                app.run()
            else:
                print("Kivy not available - simulating mainloop")
                print(f"Would display window '{self._title}' with {len(self._widgets)} widgets")
                for i, widget in enumerate(self._widgets):
                    print(f"  Widget {i+1}: {widget}")
        
        # Window information methods (winfo_*)
        def winfo_screenwidth(self):
            """Return screen width in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.system_size[0]) if Window.system_size else 1920
            except:
                return 1920  # Default fallback
                
        def winfo_screenheight(self):
            """Return screen height in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.system_size[1]) if Window.system_size else 1080
            except:
                return 1080  # Default fallback
                
        def winfo_width(self):
            """Return window width in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.width)
            except:
                return 800  # Default fallback
                
        def winfo_height(self):
            """Return window height in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.height)
            except:
                return 600  # Default fallback
                
        def winfo_x(self):
            """Return window x position"""
            try:
                from kivy.core.window import Window
                return int(Window.left) if hasattr(Window, 'left') else 100
            except:
                return 100  # Default fallback
                
        def winfo_y(self):
            """Return window y position"""
            try:
                from kivy.core.window import Window
                return int(Window.top) if hasattr(Window, 'top') else 100
            except:
                return 100  # Default fallback
                
        def winfo_reqwidth(self):
            """Return requested width"""
            return self.winfo_width()
            
        def winfo_reqheight(self):
            """Return requested height"""
            return self.winfo_height()
            
        def winfo_rootx(self):
            """Return root window x position"""
            return self.winfo_x()
            
        def winfo_rooty(self):
            """Return root window y position"""
            return self.winfo_y()
            
        def winfo_exists(self):
            """Return True if window exists"""
            return True
            
        def winfo_viewable(self):
            """Return True if window is viewable"""
            return True
            
        # Window configuration methods
        def overrideredirect(self, flag):
            """Remove/restore window decorations"""
            self._override_redirect = flag
            print(f"Override redirect set to: {flag} (removes title bar and decorations)")
            
        def withdraw(self):
            """Hide the window"""
            self._withdrawn = True
            print("Window withdrawn (hidden)")
            
        def deiconify(self):
            """Show the window after withdraw"""
            self._withdrawn = False
            print("Window deiconified (shown)")
            
        def iconify(self):
            """Minimize the window"""
            self._iconified = True
            print("Window iconified (minimized)")
            
        def option_add(self, pattern, value, priority=None):
            """Add option to the option database"""
            if not hasattr(self, '_options'):
                self._options = {}
            self._options[pattern] = value
            print(f"Option added: {pattern} = {value}")
            
        def minsize(self, width=None, height=None):
            """Set minimum window size"""
            if width is not None or height is not None:
                self._min_width = width or 1
                self._min_height = height or 1
                print(f"Minimum size set to: {width}x{height}")
            return getattr(self, '_min_width', 1), getattr(self, '_min_height', 1)
            
        def maxsize(self, width=None, height=None):
            """Set maximum window size"""
            if width is not None or height is not None:
                self._max_width = width or 9999
                self._max_height = height or 9999
                print(f"Maximum size set to: {width}x{height}")
            return getattr(self, '_max_width', 9999), getattr(self, '_max_height', 9999)
            
        def resizable(self, width=None, height=None):
            """Set whether window can be resized"""
            if width is not None or height is not None:
                self._resizable_width = bool(width)
                self._resizable_height = bool(height)
                print(f"Resizable set to: width={width}, height={height}")
            return getattr(self, '_resizable_width', True), getattr(self, '_resizable_height', True)
            
        def configure(self, **kwargs):
            """Configure window options"""
            for key, value in kwargs.items():
                if key == 'bg' or key == 'background':
                    self._bg_color = value
                    print(f"Background color set to: {value}")
                elif key == 'fg' or key == 'foreground':
                    self._fg_color = value
                    print(f"Foreground color set to: {value}")
                elif key == 'width':
                    self._width = value
                    print(f"Width set to: {value}")
                elif key == 'height':
                    self._height = value
                    print(f"Height set to: {value}")
                else:
                    # Store any other configuration
                    if not hasattr(self, '_config'):
                        self._config = {}
                    self._config[key] = value
                    print(f"Configuration set: {key} = {value}")
                    
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            if option == 'bg' or option == 'background':
                return getattr(self, '_bg_color', 'white')
            elif option == 'fg' or option == 'foreground':
                return getattr(self, '_fg_color', 'black')
            elif option == 'width':
                return getattr(self, '_width', 800)
            elif option == 'height':
                return getattr(self, '_height', 600)
            elif hasattr(self, '_config') and option in self._config:
                return self._config[option]
            else:
                return None
                
        # Event binding methods
        def bind(self, sequence, func, add=None):
            """Bind an event sequence to a callback function"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # For Kivy integration, we could set up keyboard bindings here
            # For now, just store the binding for compatibility
            return f"binding_{len(self._bindings)}"
            
        def unbind(self, sequence, funcid=None):
            """Remove an event binding"""
            if hasattr(self, '_bindings') and sequence in self._bindings:
                del self._bindings[sequence]
                print(f"Event unbound: {sequence}")
            
        def bind_all(self, sequence, func, add=None):
            """Bind an event to all widgets (global binding)"""
            return self.bind(sequence, func, add)
            
        def unbind_all(self, sequence):
            """Remove a global event binding"""
            return self.unbind(sequence)
            
        def focus_set(self):
            """Set focus to this window"""
            self._has_focus = True
            print("Focus set to window")
            
        def focus_force(self):
            """Force focus to this window"""
            self._has_focus = True
            print("Focus forced to window")
            
        def focus_get(self):
            """Get the widget that currently has focus"""
            return self if getattr(self, '_has_focus', False) else None
            
        def grab_set(self):
            """Set a global grab on this window"""
            self._has_grab = True
            print("Global grab set on window")
            
        def grab_release(self):
            """Release the global grab"""
            self._has_grab = False
            print("Global grab released")
            
        def grab_current(self):
            """Get the window that currently has the grab"""
            return self if getattr(self, '_has_grab', False) else None
            
        # Window protocol methods
        def protocol(self, protocol_name, func=None):
            """Set or get a window protocol handler"""
            if not hasattr(self, '_protocols'):
                self._protocols = {}
                
            if func is None:
                # Return current handler
                return self._protocols.get(protocol_name, None)
            else:
                # Set new handler
                self._protocols[protocol_name] = func
                print(f"Protocol handler set: {protocol_name} -> {func.__name__ if hasattr(func, '__name__') else func}")
                
                # Handle common protocols
                if protocol_name == "WM_DELETE_WINDOW":
                    print("Window close handler registered (will be called when app is closed)")
                elif protocol_name == "WM_SAVE_YOURSELF":
                    print("Save session handler registered")
                elif protocol_name == "WM_TAKE_FOCUS":
                    print("Focus handler registered")
                
                return func
                
        def destroy(self):
            """Destroy the window"""
            # Call WM_DELETE_WINDOW protocol if set
            if hasattr(self, '_protocols') and "WM_DELETE_WINDOW" in self._protocols:
                try:
                    self._protocols["WM_DELETE_WINDOW"]()
                    print("WM_DELETE_WINDOW protocol handler called")
                except Exception as e:
                    print(f"Error calling WM_DELETE_WINDOW handler: {e}")
            
            self._destroyed = True
            print("Window destroyed")
            
        def quit(self):
            """Quit the application"""
            print("Application quit requested")
            # In a real implementation, this would stop the Kivy app
            self._quit_requested = True
            
        def wm_title(self, title=None):
            """Set or get window title (alternative to title())"""
            if title is None:
                return getattr(self, '_title', 'Kivy App')
            else:
                self.title(title)
                return title
                
        def wm_geometry(self, geometry=None):
            """Set or get window geometry (alternative to geometry())"""
            if geometry is None:
                return getattr(self, '_geometry', '800x600+100+100')
            else:
                self.geometry(geometry)
                return geometry
                
        def wm_state(self, state=None):
            """Set or get window state"""
            if state is None:
                if getattr(self, '_withdrawn', False):
                    return 'withdrawn'
                elif getattr(self, '_iconified', False):
                    return 'iconic'
                else:
                    return 'normal'
            else:
                if state == 'withdrawn':
                    self.withdraw()
                elif state == 'iconic':
                    self.iconify()
                elif state == 'normal':
                    self.deiconify()
                print(f"Window state set to: {state}")
                return state
        
        def after(self, delay, func, *args):
            """Schedule a function to be called after a delay"""
            import threading
            from random import randint
            
            def delayed_call():
                import time
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                try:
                    func(*args)
                except Exception as e:
                    print(f"Error in after callback: {e}")
            
            # In a real implementation, this would integrate with Kivy's Clock
            # For now, use threading to simulate the delay
            thread = threading.Thread(target=delayed_call)
            thread.daemon = True
            thread.start()
            
            # Return a fake job ID for after_cancel compatibility
            job_id = f"after_job_{randint(1000, 9999)}"
            if not hasattr(self, '_after_jobs'):
                self._after_jobs = {}
            self._after_jobs[job_id] = thread
            print(f"Tk after scheduled: {delay}ms delay, job ID: {job_id}")
            return job_id
        
        def after_cancel(self, job_id):
            """Cancel a scheduled after job"""
            if hasattr(self, '_after_jobs') and job_id in self._after_jobs:
                # Note: Can't actually cancel a thread once started, but remove from tracking
                del self._after_jobs[job_id]
                print(f"Tk after job cancelled: {job_id}")
            else:
                print(f"Tk after job not found or already completed: {job_id}")
        
        def after_idle(self, func, *args):
            """Schedule a function to be called when the system is idle"""
            # For simplicity, just call immediately in a thread
            import threading
            
            def idle_call():
                try:
                    func(*args)
                except Exception as e:
                    print(f"Error in after_idle callback: {e}")
            
            thread = threading.Thread(target=idle_call)
            thread.daemon = True
            thread.start()
            print("Tk after_idle scheduled")
            return thread
            
        def attributes(self, *args):
            """Get or set window attributes"""
            if not args:
                # Return all attributes
                return getattr(self, '_attributes', {})
            elif len(args) == 1:
                # Get specific attribute
                attr_name = args[0]
                if not hasattr(self, '_attributes'):
                    self._attributes = {}
                return self._attributes.get(attr_name, None)
            elif len(args) == 2:
                # Set attribute
                attr_name, value = args
                if not hasattr(self, '_attributes'):
                    self._attributes = {}
                self._attributes[attr_name] = value
                print(f"Window attribute set: {attr_name} = {value}")
                return value
            else:
                print(f"Window attributes called with {len(args)} arguments: {args}")
                return None
    
    # Create fake Button class
    class FakeButton:
        def __init__(self, parent, *args, **kwargs):
            self.parent = parent
            self.kwargs = kwargs.copy()
            self._command = None
            
            # Handle positional arguments - first positional arg is typically 'text'
            if args:
                self.kwargs['text'] = args[0]  # First positional argument is text
                if len(args) > 1:
                    print(f"Warning: Button received {len(args)} positional arguments, only using first as text")
            
            self._create_kivy_button()
            
        def _create_kivy_button(self):
            try:
                from kivy.uix.button import Button
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                if 'text' in self.kwargs:
                    kivy_kwargs['text'] = self.kwargs['text']
                    
                # Handle background color
                if 'bg' in self.kwargs or 'background' in self.kwargs:
                    color = self.kwargs.get('bg', self.kwargs.get('background'))
                    if color is not None and color != '':
                        if color == 'white':
                            kivy_kwargs['background_color'] = (1, 1, 1, 1)
                        elif color == 'black':
                            kivy_kwargs['background_color'] = (0, 0, 0, 1)
                        elif color == 'blue':
                            kivy_kwargs['background_color'] = (0, 0, 1, 1)
                        elif color == 'red':
                            kivy_kwargs['background_color'] = (1, 0, 0, 1)
                        elif color == 'green':
                            kivy_kwargs['background_color'] = (0, 1, 0, 1)
                        elif color == 'gray' or color == 'grey':
                            kivy_kwargs['background_color'] = (0.5, 0.5, 0.5, 1)
                        elif isinstance(color, str) and color.startswith('#'):
                            # Handle hex colors
                            try:
                                hex_color = color[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    kivy_kwargs['background_color'] = (r, g, b, 1)
                                else:
                                    kivy_kwargs['background_color'] = (0.9, 0.9, 0.9, 1)
                            except:
                                kivy_kwargs['background_color'] = (0.9, 0.9, 0.9, 1)
                        else:
                            kivy_kwargs['background_color'] = (0.9, 0.9, 0.9, 1)  # Default light gray
                    else:
                        # Handle None or empty color - use default
                        kivy_kwargs['background_color'] = (0.9, 0.9, 0.9, 1)  # Default light gray
                        
                # Handle text color
                if 'fg' in self.kwargs or 'foreground' in self.kwargs:
                    color = self.kwargs.get('fg', self.kwargs.get('foreground'))
                    if color is not None and color != '':
                        if color == 'white':
                            kivy_kwargs['color'] = (1, 1, 1, 1)
                        elif color == 'black':
                            kivy_kwargs['color'] = (0, 0, 0, 1)
                        elif isinstance(color, str) and color.startswith('#'):
                            # Handle hex colors for text
                            try:
                                hex_color = color[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    kivy_kwargs['color'] = (r, g, b, 1)
                                else:
                                    kivy_kwargs['color'] = (0, 0, 0, 1)  # Default black text
                            except:
                                kivy_kwargs['color'] = (0, 0, 0, 1)  # Default black text
                        else:
                            kivy_kwargs['color'] = (0, 0, 0, 1)  # Default black text
                    else:
                        kivy_kwargs['color'] = (0, 0, 0, 1)  # Default black text
                else:
                    kivy_kwargs['color'] = (0, 0, 0, 1)  # Default black text
                    
                # Handle font
                if 'font' in self.kwargs:
                    font = self.kwargs['font']
                    if isinstance(font, (tuple, list)):
                        # Font tuple format: (family, size) or (family, size, weight)
                        if len(font) >= 2:
                            font_family = font[0]
                            font_size = font[1]
                            # Convert tkinter font size to Kivy font_size
                            if isinstance(font_size, (int, float)):
                                kivy_kwargs['font_size'] = f"{font_size}sp"
                            else:
                                # If font_size is a variable, use a reasonable default
                                kivy_kwargs['font_size'] = '16sp'
                            print(f"Button font set: {font_family}, size {font_size}")
                        if len(font) >= 3:
                            font_weight = font[2]
                            if 'bold' in str(font_weight).lower():
                                # Kivy doesn't have bold directly, but we can note it's bold
                                print(f"Button font weight: {font_weight} (bold styling noted)")
                    else:
                        # Simple font name or size
                        kivy_kwargs['font_size'] = '14sp'  # Default size
                        print(f"Button font: {font}")
                
                # Handle size constraints
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height']
                    
                if 'command' in self.kwargs:
                    self._command = self.kwargs['command']
                
                self.kivy_button = Button(**kivy_kwargs)
                
                # Bind command if provided
                if self._command:
                    self.kivy_button.bind(on_press=lambda x: self._command())
                    
            except ImportError:
                print(f"Simulating button creation with: {self.kwargs}")
                self.kivy_button = f"Button({self.kwargs})"
        
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_button'):
                    self.parent._widgets.append(self.kivy_button)
                    # If parent is a Frame, immediately add to its Kivy layout
                    if hasattr(self.parent, '_add_child_to_layout'):
                        self.parent._add_child_to_layout(self.kivy_button)
                print(f"Button packed: {self.kwargs.get('text', 'No text')}")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            """Handle place geometry manager with x, y, width, height"""
            # Store place parameters
            self._place_info = kwargs.copy()
            
            if hasattr(self, 'kivy_button'):
                # Handle positioning - Kivy uses absolute positioning differently than tkinter
                if 'x' in kwargs:
                    self.kivy_button.pos_hint = {}  # Clear pos_hint to use absolute positioning
                    self.kivy_button.x = kwargs['x']
                    print(f"Button x position set to: {kwargs['x']}")
                    
                if 'y' in kwargs:
                    # Kivy uses bottom-left origin, tkinter uses top-left
                    # For proper positioning, we need to convert the coordinate system
                    self.kivy_button.pos_hint = {}  # Clear pos_hint to use absolute positioning
                    self.kivy_button.y = kwargs['y']
                    print(f"Button y position set to: {kwargs['y']}")
                
                # Handle sizing - if width/height not specified, use reasonable defaults instead of fullscreen
                if 'width' in kwargs:
                    self.kivy_button.size_hint_x = None
                    self.kivy_button.width = kwargs['width']
                    print(f"Button width set to: {kwargs['width']}")
                else:
                    # Set reasonable default width if not specified
                    if not hasattr(self.kivy_button, 'width') or self.kivy_button.size_hint_x is not None:
                        self.kivy_button.size_hint_x = None
                        button_text = self.kwargs.get('text', 'Button')
                        # Estimate width based on text length (rough approximation)
                        estimated_width = max(100, len(str(button_text)) * 8 + 20)
                        self.kivy_button.width = estimated_width
                        print(f"Button width auto-set to: {estimated_width} (based on text length)")
                    
                if 'height' in kwargs:
                    self.kivy_button.size_hint_y = None
                    self.kivy_button.height = kwargs['height']
                    print(f"Button height set to: {kwargs['height']}")
                else:
                    # Set reasonable default height if not specified
                    if not hasattr(self.kivy_button, 'height') or self.kivy_button.size_hint_y is not None:
                        self.kivy_button.size_hint_y = None
                        self.kivy_button.height = 40  # Standard button height
                        print(f"Button height auto-set to: 40 (default)")
                
                # Handle relative positioning (relx, rely, relwidth, relheight)
                if 'relx' in kwargs or 'rely' in kwargs or 'relwidth' in kwargs or 'relheight' in kwargs:
                    pos_hint = {}
                    size_hint = [None, None]  # Start with absolute sizing
                    
                    if 'relx' in kwargs:
                        pos_hint['x'] = kwargs['relx']
                        print(f"Button relative x position set to: {kwargs['relx']}")
                    if 'rely' in kwargs:
                        pos_hint['y'] = kwargs['rely']
                        print(f"Button relative y position set to: {kwargs['rely']}")
                    
                    if pos_hint:
                        self.kivy_button.pos_hint = pos_hint
                    
                    if 'relwidth' in kwargs:
                        size_hint[0] = kwargs['relwidth']
                        self.kivy_button.size_hint_x = kwargs['relwidth']
                        print(f"Button relative width set to: {kwargs['relwidth']}")
                    if 'relheight' in kwargs:
                        size_hint[1] = kwargs['relheight']
                        self.kivy_button.size_hint_y = kwargs['relheight']
                        print(f"Button relative height set to: {kwargs['relheight']}")
            
            # Add to parent (similar to pack)
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_button'):
                    # For place geometry, we need a different approach than pack
                    # We should use a FloatLayout or similar that supports absolute positioning
                    if hasattr(self.parent, 'kivy_frame') and hasattr(self.parent.kivy_frame, 'add_widget'):
                        try:
                            # Try to change parent layout to FloatLayout for absolute positioning
                            from kivy.uix.floatlayout import FloatLayout
                            if not isinstance(self.parent.kivy_frame, FloatLayout):
                                print("Warning: place() works best with FloatLayout parent. Current parent layout may not position correctly.")
                        except ImportError:
                            pass
                    
                    if self.kivy_button not in self.parent._widgets:
                        self.parent._widgets.append(self.kivy_button)
                    # If parent is a Frame, immediately add to its Kivy layout
                    if hasattr(self.parent, '_add_child_to_layout'):
                        self.parent._add_child_to_layout(self.kivy_button)
                        
            place_params = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
            print(f"Button placed: {self.kwargs.get('text', 'No text')} with {place_params}")
            
        def place_info(self):
            """Return current place configuration"""
            return getattr(self, '_place_info', {})
        
        def configure(self, **kwargs):
            """Configure button options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                
                # Update the Kivy button if it exists
                if hasattr(self, 'kivy_button') and hasattr(self.kivy_button, key):
                    if key == 'text':
                        self.kivy_button.text = str(value)
                        print(f"Button text updated to: {value}")
                    elif key == 'command':
                        self._command = value
                        # Rebind the command
                        if hasattr(self.kivy_button, 'bind'):
                            self.kivy_button.bind(on_press=lambda x: self._command())
                        print(f"Button command updated")
                    elif key == 'bg' or key == 'background':
                        # Update background color
                        if value == 'white':
                            self.kivy_button.background_color = (1, 1, 1, 1)
                        elif value == 'black':
                            self.kivy_button.background_color = (0, 0, 0, 1)
                        elif value == 'blue':
                            self.kivy_button.background_color = (0, 0, 1, 1)
                        elif value == 'red':
                            self.kivy_button.background_color = (1, 0, 0, 1)
                        elif value == 'green':
                            self.kivy_button.background_color = (0, 1, 0, 1)
                        elif value == 'gray' or value == 'grey':
                            self.kivy_button.background_color = (0.5, 0.5, 0.5, 1)
                        elif isinstance(value, str) and value.startswith('#'):
                            try:
                                hex_color = value[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    self.kivy_button.background_color = (r, g, b, 1)
                            except:
                                pass
                        print(f"Button background color updated to: {value}")
                    elif key == 'fg' or key == 'foreground':
                        # Update text color
                        if value == 'white':
                            self.kivy_button.color = (1, 1, 1, 1)
                        elif value == 'black':
                            self.kivy_button.color = (0, 0, 0, 1)
                        elif isinstance(value, str) and value.startswith('#'):
                            try:
                                hex_color = value[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    self.kivy_button.color = (r, g, b, 1)
                            except:
                                pass
                        print(f"Button text color updated to: {value}")
                    elif key == 'width':
                        self.kivy_button.size_hint_x = None
                        self.kivy_button.width = value
                        print(f"Button width updated to: {value}")
                    elif key == 'height':
                        self.kivy_button.size_hint_y = None
                        self.kivy_button.height = value
                        print(f"Button height updated to: {value}")
                    elif key == 'state':
                        self.kivy_button.disabled = (value in ['disabled', 'DISABLED'])
                        print(f"Button state updated to: {value}")
                        
                print(f"Button configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            if option == 'text' and hasattr(self, 'kivy_button'):
                return self.kivy_button.text
            elif option == 'command':
                return self._command
            return self.kwargs.get(option, None)
        
        @property
        def command(self):
            """Access the button's command function"""
            return self._command
        
        def __str__(self):
            return f"TkButton(text='{self.kwargs.get('text', '')}')"
    
    # Create fake Label class
    class FakeLabel:
        def __init__(self, parent, *args, **kwargs):
            self.parent = parent
            self.kwargs = kwargs.copy()
            
            # Handle positional arguments - first positional arg is typically 'text'
            if args:
                self.kwargs['text'] = args[0]  # First positional argument is text
                if len(args) > 1:
                    print(f"Warning: Label received {len(args)} positional arguments, only using first as text")
            
            self._create_kivy_label()
            
        def _create_kivy_label(self):
            try:
                from kivy.uix.label import Label
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                if 'text' in self.kwargs:
                    kivy_kwargs['text'] = self.kwargs['text']
                else:
                    kivy_kwargs['text'] = ''  # Default empty text for labels without text
                    
                # Note: Kivy Labels don't have background_color, we'll handle bg differently
                if 'bg' in self.kwargs:
                    # Store background color for potential use with Canvas later
                    self._bg_color = self.kwargs['bg']
                    print(f"Label background color stored: {self._bg_color} (Note: Kivy Labels don't support background_color directly)")
                    
                if 'fg' in self.kwargs:
                    color = self.kwargs['fg']
                    if color is not None and color != '':
                        if color == 'white':
                            kivy_kwargs['color'] = (1, 1, 1, 1)
                        elif color == 'black':
                            kivy_kwargs['color'] = (0, 0, 0, 1)
                        elif isinstance(color, str) and color.startswith('#'):
                            # Handle hex colors
                            try:
                                hex_color = color[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    kivy_kwargs['color'] = (r, g, b, 1)
                                else:
                                    kivy_kwargs['color'] = (1, 1, 1, 1)
                            except:
                                kivy_kwargs['color'] = (1, 1, 1, 1)
                        else:
                            kivy_kwargs['color'] = (1, 1, 1, 1)  # Default white text
                    else:
                        kivy_kwargs['color'] = (1, 1, 1, 1)  # Default white text
                        
                if 'font' in self.kwargs:
                    # Font handling (simplified)
                    kivy_kwargs['font_size'] = '14sp'  # Default size
                    
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_label = Label(**kivy_kwargs)
                
                # If there's a background color, we could add it via Canvas instructions
                # but for simplicity, we'll just note it for now
                    
            except ImportError:
                print(f"Simulating label creation with: {self.kwargs}")
                self.kivy_label = f"Label({self.kwargs})"
        
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_label'):
                    self.parent._widgets.append(self.kivy_label)
                    # If parent is a Frame, immediately add to its Kivy layout
                    if hasattr(self.parent, '_add_child_to_layout'):
                        self.parent._add_child_to_layout(self.kivy_label)
                print(f"Label packed: {self.kwargs.get('text', 'No text')}")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure label options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                print(f"Label configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
        
        def __str__(self):
            return f"TkLabel(text='{self.kwargs.get('text', '')}')"
    
    # Create fake Frame class
    class FakeFrame:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._widgets = []  # Store child widgets
            self._create_kivy_frame()
            
        def _create_kivy_frame(self):
            try:
                from kivy.uix.boxlayout import BoxLayout
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle orientation
                if 'orient' in self.kwargs:
                    if self.kwargs['orient'] == 'horizontal':
                        kivy_kwargs['orientation'] = 'horizontal'
                    else:
                        kivy_kwargs['orientation'] = 'vertical'
                else:
                    kivy_kwargs['orientation'] = 'vertical'  # Default
                
                # Handle background color
                if 'bg' in self.kwargs or 'background' in self.kwargs:
                    color = self.kwargs.get('bg', self.kwargs.get('background'))
                    if color is not None and color != '':
                        if color == 'white':
                            self._bg_color = (1, 1, 1, 1)
                        elif color == 'black':
                            self._bg_color = (0, 0, 0, 1)
                        elif isinstance(color, str) and color.startswith('#'):
                            # Handle hex colors
                            try:
                                hex_color = color[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    self._bg_color = (r, g, b, 1)
                                else:
                                    self._bg_color = (0.9, 0.9, 0.9, 1)
                            except:
                                self._bg_color = (0.9, 0.9, 0.9, 1)
                        else:
                            self._bg_color = (0.9, 0.9, 0.9, 1)  # Default light gray
                    else:
                        self._bg_color = (0.9, 0.9, 0.9, 1)  # Default light gray
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_frame = BoxLayout(**kivy_kwargs)
                
                # Add background color if specified
                if hasattr(self, '_bg_color'):
                    try:
                        from kivy.graphics import Color, Rectangle
                        with self.kivy_frame.canvas.before:
                            Color(*self._bg_color)
                            self.rect = Rectangle(size=self.kivy_frame.size, pos=self.kivy_frame.pos)
                        
                        # Bind to update rectangle when frame size changes
                        def update_rect(instance, value):
                            self.rect.pos = instance.pos
                            self.rect.size = instance.size
                        self.kivy_frame.bind(size=update_rect, pos=update_rect)
                    except ImportError:
                        pass
                    
            except ImportError:
                print(f"Simulating frame creation with: {self.kwargs}")
                self.kivy_frame = f"Frame({self.kwargs})"
        
        def pack(self, **kwargs):
            # Add child widgets to this frame's Kivy layout first
            if hasattr(self, 'kivy_frame') and hasattr(self.kivy_frame, 'add_widget'):
                for child_widget in self._widgets:
                    if hasattr(child_widget, 'add_widget'):  # It's a Kivy widget
                        try:
                            # Only add if not already added
                            if child_widget not in self.kivy_frame.children:
                                self.kivy_frame.add_widget(child_widget)
                                print(f"Added child widget to frame: {type(child_widget).__name__}")
                        except Exception as e:
                            print(f"Error adding child to frame: {e}")
            
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_frame'):
                    self.parent._widgets.append(self.kivy_frame)
                print(f"Frame packed with {len(self._widgets)} child widgets")
        
        def _add_child_to_layout(self, child_widget):
            """Add a child widget to this frame's layout immediately when it's packed"""
            if hasattr(self, 'kivy_frame') and hasattr(self.kivy_frame, 'add_widget'):
                if hasattr(child_widget, 'add_widget'):  # It's a Kivy widget
                    try:
                        # Only add if not already added
                        if child_widget not in self.kivy_frame.children:
                            self.kivy_frame.add_widget(child_widget)
                            print(f"Immediately added child to frame: {type(child_widget).__name__}")
                    except Exception as e:
                        print(f"Error immediately adding child to frame: {e}")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure frame options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                print(f"Frame configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
            
        def winfo_children(self):
            """Return list of child widgets"""
            return self._widgets
            
        def destroy(self):
            """Destroy the frame and all child widgets"""
            for widget in self._widgets:
                if hasattr(widget, 'destroy'):
                    widget.destroy()
            self._widgets.clear()
            print("Frame destroyed")
            
        def bind(self, sequence, func, add=None):
            """Bind an event sequence to a callback function"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Frame event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # For Kivy integration, we could set up event bindings here
            # For now, just store the binding for compatibility
            return f"binding_{len(self._bindings)}"
            
        def unbind(self, sequence, funcid=None):
            """Remove an event binding"""
            if hasattr(self, '_bindings') and sequence in self._bindings:
                del self._bindings[sequence]
                print(f"Frame event unbound: {sequence}")
                
        def focus_set(self):
            """Set focus to this frame"""
            self._has_focus = True
            print("Focus set to frame")
            
        def focus_force(self):
            """Force focus to this frame"""
            self._has_focus = True
            print("Focus forced to frame")
            
        def focus_get(self):
            """Get the widget that currently has focus"""
            return self if getattr(self, '_has_focus', False) else None
            
        def pack_configure(self, **kwargs):
            """Configure pack options for the frame"""
            for key, value in kwargs.items():
                if key == 'padx':
                    self._pack_padx = value
                    print(f"Frame pack padx set to: {value}")
                elif key == 'pady':
                    self._pack_pady = value
                    print(f"Frame pack pady set to: {value}")
                elif key == 'fill':
                    self._pack_fill = value
                    print(f"Frame pack fill set to: {value}")
                elif key == 'expand':
                    self._pack_expand = value
                    print(f"Frame pack expand set to: {value}")
                elif key == 'side':
                    self._pack_side = value
                    print(f"Frame pack side set to: {value}")
                else:
                    print(f"Frame pack configured: {key} = {value}")
                    
        def pack_info(self):
            """Return current pack configuration"""
            return {
                'padx': getattr(self, '_pack_padx', 0),
                'pady': getattr(self, '_pack_pady', 0),
                'fill': getattr(self, '_pack_fill', 'none'),
                'expand': getattr(self, '_pack_expand', False),
                'side': getattr(self, '_pack_side', 'top')
            }
        
        def __str__(self):
            return f"TkFrame(children={len(self._widgets)})"
    
    # Create fake Canvas class
    class FakeCanvas:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._canvas_items = []  # Store canvas items (lines, rectangles, etc.)
            self._create_kivy_canvas()
            
        def _create_kivy_canvas(self):
            try:
                from kivy.uix.widget import Widget
                from kivy.graphics import Canvas, Color, Line, Rectangle, Ellipse
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle background color
                if 'bg' in self.kwargs or 'background' in self.kwargs:
                    color = self.kwargs.get('bg', self.kwargs.get('background'))
                    if color is not None and color != '':
                        if color == 'white':
                            self._bg_color = (1, 1, 1, 1)
                        elif color == 'black':
                            self._bg_color = (0, 0, 0, 1)
                        elif isinstance(color, str) and color.startswith('#'):
                            # Handle hex colors
                            try:
                                hex_color = color[1:]
                                if len(hex_color) == 6:
                                    r = int(hex_color[0:2], 16) / 255.0
                                    g = int(hex_color[2:4], 16) / 255.0
                                    b = int(hex_color[4:6], 16) / 255.0
                                    self._bg_color = (r, g, b, 1)
                                else:
                                    self._bg_color = (1, 1, 1, 1)
                            except:
                                self._bg_color = (1, 1, 1, 1)
                        else:
                            self._bg_color = (1, 1, 1, 1)  # Default white
                    else:
                        self._bg_color = (1, 1, 1, 1)  # Default white
                else:
                    self._bg_color = (1, 1, 1, 1)  # Default white
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_canvas = Widget(**kivy_kwargs)
                
                # Add background color
                with self.kivy_canvas.canvas.before:
                    Color(*self._bg_color)
                    self.bg_rect = Rectangle(size=self.kivy_canvas.size, pos=self.kivy_canvas.pos)
                
                # Bind to update rectangle when canvas size changes
                def update_rect(instance, value):
                    self.bg_rect.pos = instance.pos
                    self.bg_rect.size = instance.size
                self.kivy_canvas.bind(size=update_rect, pos=update_rect)
                    
            except ImportError:
                print(f"Simulating canvas creation with: {self.kwargs}")
                self.kivy_canvas = f"Canvas({self.kwargs})"
        
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_canvas'):
                    self.parent._widgets.append(self.kivy_canvas)
                    # If parent is a Frame, immediately add to its Kivy layout
                    if hasattr(self.parent, '_add_child_to_layout'):
                        self.parent._add_child_to_layout(self.kivy_canvas)
                print(f"Canvas packed with {len(self._canvas_items)} items")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure canvas options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'scrollregion':
                    print(f"Canvas scroll region set to: {value}")
                elif key == 'yscrollcommand':
                    print(f"Canvas Y scroll command set: {value}")
                elif key == 'xscrollcommand':
                    print(f"Canvas X scroll command set: {value}")
                else:
                    print(f"Canvas configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
            
        def after(self, delay, func, *args):
            """Schedule a function to be called after a delay"""
            import threading
            from random import randint
            def delayed_call():
                import time
                time.sleep(delay / 1000.0)  # Convert ms to seconds
                func(*args)
            
            # In a real implementation, this would integrate with Kivy's Clock
            thread = threading.Thread(target=delayed_call)
            thread.daemon = True
            thread.start()
            
            # Return a fake job ID for after_cancel compatibility
            job_id = f"after_job_{randint(1000, 9999)}"
            if not hasattr(self, '_after_jobs'):
                self._after_jobs = {}
            self._after_jobs[job_id] = thread
            print(f"Canvas after scheduled: {delay}ms delay, job ID: {job_id}")
            return job_id
            
        def after_cancel(self, job_id):
            """Cancel a scheduled after job"""
            if hasattr(self, '_after_jobs') and job_id in self._after_jobs:
                # Note: Can't actually cancel a thread once started, but remove from tracking
                del self._after_jobs[job_id]
                print(f"Canvas after job cancelled: {job_id}")
            else:
                print(f"Canvas after job not found or already completed: {job_id}")
            
        # Canvas drawing methods
        def create_line(self, x1, y1, x2, y2, **kwargs):
            """Create a line on the canvas"""
            item_id = len(self._canvas_items) + 1
            line_data = {
                'type': 'line',
                'coords': [x1, y1, x2, y2],
                'options': kwargs,
                'id': item_id
            }
            self._canvas_items.append(line_data)
            print(f"Canvas line created: ({x1}, {y1}) to ({x2}, {y2}) with options {kwargs}")
            
            # Draw on Kivy canvas if available
            try:
                if hasattr(self, 'kivy_canvas'):
                    from kivy.graphics import Color, Line
                    with self.kivy_canvas.canvas:
                        # Handle color
                        if 'fill' in kwargs:
                            color = kwargs['fill']
                            if color == 'black':
                                Color(0, 0, 0, 1)
                            elif color == 'red':
                                Color(1, 0, 0, 1)
                            elif color == 'blue':
                                Color(0, 0, 1, 1)
                            elif color == 'green':
                                Color(0, 1, 0, 1)
                            else:
                                Color(0, 0, 0, 1)  # Default black
                        else:
                            Color(0, 0, 0, 1)  # Default black
                            
                        # Handle width
                        width = kwargs.get('width', 1)
                        Line(points=[x1, y1, x2, y2], width=width)
            except ImportError:
                pass
                
            return item_id
            
        def create_rectangle(self, x1, y1, x2, y2, **kwargs):
            """Create a rectangle on the canvas"""
            item_id = len(self._canvas_items) + 1
            rect_data = {
                'type': 'rectangle',
                'coords': [x1, y1, x2, y2],
                'options': kwargs,
                'id': item_id
            }
            self._canvas_items.append(rect_data)
            print(f"Canvas rectangle created: ({x1}, {y1}) to ({x2}, {y2}) with options {kwargs}")
            
            # Draw on Kivy canvas if available
            try:
                if hasattr(self, 'kivy_canvas'):
                    from kivy.graphics import Color, Rectangle
                    with self.kivy_canvas.canvas:
                        # Handle fill color
                        if 'fill' in kwargs:
                            color = kwargs['fill']
                            if color == 'red':
                                Color(1, 0, 0, 1)
                            elif color == 'blue':
                                Color(0, 0, 1, 1)
                            elif color == 'green':
                                Color(0, 1, 0, 1)
                            elif color == 'yellow':
                                Color(1, 1, 0, 1)
                            else:
                                Color(0.5, 0.5, 0.5, 1)  # Default gray
                        else:
                            Color(0.5, 0.5, 0.5, 1)  # Default gray
                            
                        width = x2 - x1
                        height = y2 - y1
                        Rectangle(pos=(x1, y1), size=(width, height))
            except ImportError:
                pass
                
            return item_id
            
        def create_oval(self, x1, y1, x2, y2, **kwargs):
            """Create an oval/ellipse on the canvas"""
            item_id = len(self._canvas_items) + 1
            oval_data = {
                'type': 'oval',
                'coords': [x1, y1, x2, y2],
                'options': kwargs,
                'id': item_id
            }
            self._canvas_items.append(oval_data)
            print(f"Canvas oval created: ({x1}, {y1}) to ({x2}, {y2}) with options {kwargs}")
            
            # Draw on Kivy canvas if available
            try:
                if hasattr(self, 'kivy_canvas'):
                    from kivy.graphics import Color, Ellipse
                    with self.kivy_canvas.canvas:
                        # Handle fill color
                        if 'fill' in kwargs:
                            color = kwargs['fill']
                            if color == 'red':
                                Color(1, 0, 0, 1)
                            elif color == 'blue':
                                Color(0, 0, 1, 1)
                            elif color == 'green':
                                Color(0, 1, 0, 1)
                            elif color == 'yellow':
                                Color(1, 1, 0, 1)
                            else:
                                Color(0.5, 0.5, 0.5, 1)  # Default gray
                        else:
                            Color(0.5, 0.5, 0.5, 1)  # Default gray
                            
                        width = x2 - x1
                        height = y2 - y1
                        Ellipse(pos=(x1, y1), size=(width, height))
            except ImportError:
                pass
                
            return item_id
            
        def create_text(self, x, y, text="", **kwargs):
            """Create text on the canvas"""
            item_id = len(self._canvas_items) + 1
            text_data = {
                'type': 'text',
                'coords': [x, y],
                'text': text,
                'options': kwargs,
                'id': item_id
            }
            self._canvas_items.append(text_data)
            print(f"Canvas text created: '{text}' at ({x}, {y}) with options {kwargs}")
            
            # For text, we'd need a Label widget in Kivy, but for simplicity, just store it
            return item_id
            
        def create_window(self, x, y=None, window=None, anchor="nw", **kwargs):
            """Create a window (widget) on the canvas"""
            # Handle both create_window(x, y, window=widget) and create_window((x, y), window=widget)
            if y is None and isinstance(x, (tuple, list)) and len(x) == 2:
                x, y = x
            elif y is None:
                y = 0
                
            item_id = len(self._canvas_items) + 1
            window_data = {
                'type': 'window',
                'coords': [x, y],
                'window': window,
                'anchor': anchor,
                'options': kwargs,
                'id': item_id
            }
            self._canvas_items.append(window_data)
            print(f"Canvas window created: widget at ({x}, {y}) with anchor='{anchor}' and options {kwargs}")
            
            # In Kivy, we would add the widget to the canvas widget
            try:
                if hasattr(self, 'kivy_canvas') and window and hasattr(window, 'kivy_frame'):
                    self.kivy_canvas.add_widget(window.kivy_frame)
                    print(f"Widget added to Kivy canvas")
            except Exception as e:
                print(f"Note: Could not add widget to Kivy canvas: {e}")
                
            return item_id
            
        def delete(self, item_id):
            """Delete a canvas item"""
            self._canvas_items = [item for item in self._canvas_items if item.get('id') != item_id]
            print(f"Canvas item {item_id} deleted")
            
        def delete_all(self):
            """Delete all canvas items"""
            self._canvas_items.clear()
            print("All canvas items deleted")
            
        def find_all(self):
            """Return list of all item IDs"""
            return [item.get('id') for item in self._canvas_items]
            
        def coords(self, item_id, *coords):
            """Get or set coordinates of a canvas item"""
            for item in self._canvas_items:
                if item.get('id') == item_id:
                    if coords:
                        item['coords'] = list(coords)
                        print(f"Canvas item {item_id} coordinates updated to {coords}")
                    return item['coords']
            return None
            
        def itemconfig(self, item_id, **kwargs):
            """Configure a canvas item"""
            for item in self._canvas_items:
                if item.get('id') == item_id:
                    item['options'].update(kwargs)
                    print(f"Canvas item {item_id} configured with {kwargs}")
                    break
                    
        def itemcget(self, item_id, option):
            """Get configuration option for a canvas item"""
            for item in self._canvas_items:
                if item.get('id') == item_id:
                    return item['options'].get(option, None)
            return None
            
        def bbox(self, item_id):
            """Get bounding box of a canvas item"""
            for item in self._canvas_items:
                if item.get('id') == item_id:
                    if item['type'] in ['line', 'rectangle', 'oval']:
                        coords = item['coords']
                        if len(coords) >= 4:
                            x1, y1, x2, y2 = coords[:4]
                            return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
                    elif item['type'] == 'window':
                        x, y = item['coords']
                        # Return approximate bounding box (would need actual widget size)
                        return (x, y, x + 100, y + 100)
                    elif item['type'] == 'text':
                        x, y = item['coords']
                        # Return approximate text bounding box
                        return (x, y, x + 50, y + 20)
            return None
                    
        def bind(self, sequence, func, add=None):
            """Bind an event to the canvas"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Canvas event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # For Kivy integration, we could set up event bindings here
            # For now, just store the binding for compatibility
            return f"binding_{len(self._bindings)}"
            
        def unbind(self, sequence, funcid=None):
            """Remove an event binding"""
            if hasattr(self, '_bindings') and sequence in self._bindings:
                del self._bindings[sequence]
                print(f"Canvas event unbound: {sequence}")
                
        def bind_all(self, sequence, func, add=None):
            """Bind an event to all widgets (global binding)"""
            if not hasattr(self, '_global_bindings'):
                self._global_bindings = {}
            self._global_bindings[sequence] = func
            print(f"Canvas global event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # For mouse wheel events, we could set up global Kivy bindings
            if sequence == "<MouseWheel>":
                print("Global mouse wheel binding registered (affects all widgets)")
            elif sequence == "<Button-4>" or sequence == "<Button-5>":
                print("Global mouse wheel binding registered for Linux (affects all widgets)")
                
            return f"global_binding_{len(self._global_bindings)}"
            
        def unbind_all(self, sequence):
            """Remove a global event binding"""
            if hasattr(self, '_global_bindings') and sequence in self._global_bindings:
                del self._global_bindings[sequence]
                print(f"Canvas global event unbound: {sequence}")
            
        def focus_set(self):
            """Set focus to the canvas"""
            self._has_focus = True
            print("Focus set to canvas")
            
        def update(self):
            """Update the canvas display"""
            print("Canvas updated")
            
        def update_idletasks(self):
            """Update idle tasks"""
            print("Canvas idle tasks updated")
            
        def yview(self, *args):
            """Handle vertical scrolling"""
            if not args:
                # Return current view
                return (0.0, 1.0)  # (top, bottom) fractions
            elif len(args) == 1:
                if args[0] == 'moveto':
                    # Should have second argument, but handle gracefully
                    return
                elif isinstance(args[0], (int, float)):
                    # Scroll to fraction
                    print(f"Canvas yview: scroll to fraction {args[0]}")
            elif len(args) == 2:
                command, value = args
                if command == 'moveto':
                    print(f"Canvas yview: move to {value}")
                elif command == 'scroll':
                    print(f"Canvas yview: scroll by {value}")
            print(f"Canvas yview called with args: {args}")
            
        def xview(self, *args):
            """Handle horizontal scrolling"""
            if not args:
                # Return current view
                return (0.0, 1.0)  # (left, right) fractions
            elif len(args) == 1:
                if args[0] == 'moveto':
                    # Should have second argument, but handle gracefully
                    return
                elif isinstance(args[0], (int, float)):
                    # Scroll to fraction
                    print(f"Canvas xview: scroll to fraction {args[0]}")
            elif len(args) == 2:
                command, value = args
                if command == 'moveto':
                    print(f"Canvas xview: move to {value}")
                elif command == 'scroll':
                    print(f"Canvas xview: scroll by {value}")
            print(f"Canvas xview called with args: {args}")
            
        def yview_moveto(self, fraction):
            """Move view to fraction of total height"""
            print(f"Canvas yview_moveto: {fraction}")
            
        def xview_moveto(self, fraction):
            """Move view to fraction of total width"""
            print(f"Canvas xview_moveto: {fraction}")
            
        def yview_scroll(self, number, what):
            """Scroll vertically by number of units"""
            print(f"Canvas yview_scroll: {number} {what}")
            
        def xview_scroll(self, number, what):
            """Scroll horizontally by number of units"""
            print(f"Canvas xview_scroll: {number} {what}")
        
        def __str__(self):
            return f"TkCanvas(items={len(self._canvas_items)})"
    
    # Create fake Scrollbar class
    class FakeScrollbar:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._command = kwargs.get('command')  # Store scroll command
            self._orient = kwargs.get('orient', 'vertical')  # Default vertical
            self._create_kivy_scrollbar()
            
        def _create_kivy_scrollbar(self):
            try:
                from kivy.uix.scrollview import ScrollView
                from kivy.uix.slider import Slider
                
                # In Kivy, scrollbars are typically part of ScrollView
                # For compatibility, we'll create a Slider that can act as a scrollbar
                kivy_kwargs = {}
                
                # Handle orientation
                if self._orient == 'horizontal':
                    kivy_kwargs['orientation'] = 'horizontal'
                    kivy_kwargs['size_hint'] = (1, None)
                    kivy_kwargs['height'] = 20
                else:  # vertical
                    kivy_kwargs['orientation'] = 'vertical'
                    kivy_kwargs['size_hint'] = (None, 1)
                    kivy_kwargs['width'] = 20
                
                # Handle size constraints
                if 'width' in self.kwargs:
                    if self._orient == 'vertical':
                        kivy_kwargs['width'] = self.kwargs['width']
                        kivy_kwargs['size_hint_x'] = None
                    
                if 'height' in self.kwargs:
                    if self._orient == 'horizontal':
                        kivy_kwargs['height'] = self.kwargs['height']
                        kivy_kwargs['size_hint_y'] = None
                
                # Set value range (0 to 1 for scrollbar)
                kivy_kwargs['min'] = 0
                kivy_kwargs['max'] = 1
                kivy_kwargs['value'] = 0
                
                self.kivy_scrollbar = Slider(**kivy_kwargs)
                
                # Bind the slider value changes to the command if provided
                if self._command:
                    def on_value_change(instance, value):
                        # Call the command with the scroll position
                        try:
                            self._command('moveto', value)
                        except:
                            # Fallback - just call with value
                            try:
                                self._command(value)
                            except:
                                print(f"Scrollbar command call failed: {self._command}")
                    
                    self.kivy_scrollbar.bind(value=on_value_change)
                    
            except ImportError:
                print(f"Simulating scrollbar creation with: {self.kwargs}")
                self.kivy_scrollbar = f"Scrollbar({self.kwargs})"
        
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_scrollbar'):
                    self.parent._widgets.append(self.kivy_scrollbar)
                    # If parent is a Frame, immediately add to its Kivy layout
                    if hasattr(self.parent, '_add_child_to_layout'):
                        self.parent._add_child_to_layout(self.kivy_scrollbar)
                print(f"Scrollbar packed: {self._orient} orientation")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure scrollbar options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'command':
                    self._command = value
                elif key == 'orient':
                    self._orient = value
                print(f"Scrollbar configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
            
        def set(self, first, last):
            """Set the scrollbar position and size"""
            print(f"Scrollbar set: first={first}, last={last}")
            # Update the Kivy slider if available
            if hasattr(self, 'kivy_scrollbar') and hasattr(self.kivy_scrollbar, 'value'):
                try:
                    # Convert tkinter scrollbar format to slider value
                    self.kivy_scrollbar.value = float(first)
                except:
                    pass
                    
        def get(self):
            """Get the current scrollbar position"""
            if hasattr(self, 'kivy_scrollbar') and hasattr(self.kivy_scrollbar, 'value'):
                try:
                    value = self.kivy_scrollbar.value
                    return (value, min(1.0, value + 0.1))  # Return (first, last) tuple
                except:
                    pass
            return (0.0, 1.0)  # Default values
            
        def delta(self, delta_x, delta_y):
            """Calculate scroll delta (for mouse wheel)"""
            if self._orient == 'horizontal':
                return delta_x / 120.0  # Standard scroll unit
            else:
                return delta_y / 120.0
                
        def fraction(self, x, y):
            """Convert pixel coordinates to scroll fraction"""
            # Simplified - in real implementation would consider scrollbar size
            if self._orient == 'horizontal':
                return max(0.0, min(1.0, x / 100.0))
            else:
                return max(0.0, min(1.0, y / 100.0))
                
        def identify(self, x, y):
            """Identify which part of scrollbar is at coordinates"""
            # Simplified implementation
            return "slider"  # Could return "arrow1", "trough1", "slider", "trough2", "arrow2"
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the scrollbar"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Scrollbar event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
        
        def __str__(self):
            return f"TkScrollbar(orient='{self._orient}')"
    
    # Create fake Menu class
    class FakeMenu:
        def __init__(self, parent=None, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._menu_items = []  # Store menu items
            self._submenus = {}    # Store submenus
            self._create_kivy_menu()
            
        def _create_kivy_menu(self):
            try:
                # In Kivy, menus would be handled differently (ActionBar, Popup, etc.)
                # For now, we'll simulate menu functionality
                print(f"Menu created with options: {self.kwargs}")
                
            except ImportError:
                print(f"Simulating menu creation with: {self.kwargs}")
        
        def add_command(self, **kwargs):
            """Add a command item to the menu"""
            label = kwargs.get('label', 'Menu Item')
            command = kwargs.get('command', None)
            accelerator = kwargs.get('accelerator', None)
            
            menu_item = {
                'type': 'command',
                'label': label,
                'command': command,
                'accelerator': accelerator,
                'options': kwargs
            }
            self._menu_items.append(menu_item)
            
            accel_text = f" ({accelerator})" if accelerator else ""
            print(f"Menu command added: '{label}'{accel_text}")
            
        def add_cascade(self, **kwargs):
            """Add a submenu to the menu"""
            label = kwargs.get('label', 'Submenu')
            menu = kwargs.get('menu', None)
            
            menu_item = {
                'type': 'cascade',
                'label': label,
                'menu': menu,
                'options': kwargs
            }
            self._menu_items.append(menu_item)
            
            if menu:
                self._submenus[label] = menu
                
            print(f"Menu cascade added: '{label}' -> submenu")
            
        def add_separator(self):
            """Add a separator line to the menu"""
            menu_item = {
                'type': 'separator'
            }
            self._menu_items.append(menu_item)
            print("Menu separator added")
            
        def add_checkbutton(self, **kwargs):
            """Add a checkbutton item to the menu"""
            label = kwargs.get('label', 'Check Item')
            variable = kwargs.get('variable', None)
            command = kwargs.get('command', None)
            
            menu_item = {
                'type': 'checkbutton',
                'label': label,
                'variable': variable,
                'command': command,
                'options': kwargs
            }
            self._menu_items.append(menu_item)
            print(f"Menu checkbutton added: '{label}'")
            
        def add_radiobutton(self, **kwargs):
            """Add a radiobutton item to the menu"""
            label = kwargs.get('label', 'Radio Item')
            variable = kwargs.get('variable', None)
            value = kwargs.get('value', None)
            command = kwargs.get('command', None)
            
            menu_item = {
                'type': 'radiobutton',
                'label': label,
                'variable': variable,
                'value': value,
                'command': command,
                'options': kwargs
            }
            self._menu_items.append(menu_item)
            print(f"Menu radiobutton added: '{label}' (value: {value})")
            
        def delete(self, index, end=None):
            """Delete menu items"""
            if end is None:
                end = index
                
            # Handle string indices like 'end', 'last'
            if isinstance(index, str):
                if index == 'end' or index == 'last':
                    index = len(self._menu_items) - 1
                else:
                    index = 0
            if isinstance(end, str):
                if end == 'end' or end == 'last':
                    end = len(self._menu_items) - 1
                    
            # Delete items in range
            if 0 <= index < len(self._menu_items) and 0 <= end < len(self._menu_items):
                for i in range(end, index - 1, -1):
                    if i < len(self._menu_items):
                        deleted_item = self._menu_items.pop(i)
                        print(f"Menu item deleted: {deleted_item.get('label', 'item')}")
                        
        def insert_command(self, index, **kwargs):
            """Insert a command item at specific position"""
            label = kwargs.get('label', 'Menu Item')
            command = kwargs.get('command', None)
            
            menu_item = {
                'type': 'command',
                'label': label,
                'command': command,
                'options': kwargs
            }
            
            if isinstance(index, str) and index == 'end':
                self._menu_items.append(menu_item)
            else:
                self._menu_items.insert(index, menu_item)
                
            print(f"Menu command inserted at {index}: '{label}'")
            
        def entryconfig(self, index, **kwargs):
            """Configure a menu item"""
            if isinstance(index, str) and index == 'end':
                index = len(self._menu_items) - 1
                
            if 0 <= index < len(self._menu_items):
                self._menu_items[index]['options'].update(kwargs)
                label = self._menu_items[index].get('label', f'item {index}')
                print(f"Menu item configured: '{label}' with {kwargs}")
                
        def entrycget(self, index, option):
            """Get configuration option for a menu item"""
            if isinstance(index, str) and index == 'end':
                index = len(self._menu_items) - 1
                
            if 0 <= index < len(self._menu_items):
                return self._menu_items[index]['options'].get(option, None)
            return None
            
        def invoke(self, index):
            """Invoke (execute) a menu item"""
            if isinstance(index, str) and index == 'end':
                index = len(self._menu_items) - 1
                
            if 0 <= index < len(self._menu_items):
                item = self._menu_items[index]
                if item['type'] == 'command' and item.get('command'):
                    try:
                        item['command']()
                        print(f"Menu command invoked: '{item.get('label', 'item')}'")
                    except Exception as e:
                        print(f"Error invoking menu command: {e}")
                        
        def post(self, x, y):
            """Display menu as popup at coordinates"""
            print(f"Menu posted as popup at ({x}, {y}) with {len(self._menu_items)} items")
            
        def unpost(self):
            """Hide popup menu"""
            print("Menu unposted (hidden)")
            
        def tk_popup(self, x, y, entry=None):
            """Display menu as popup (alternative method)"""
            self.post(x, y)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the menu"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Menu event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
        def configure(self, **kwargs):
            """Configure menu options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                print(f"Menu configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
        
        def __str__(self):
            return f"TkMenu(items={len(self._menu_items)})"
    
    # Create fake Notebook class (for tabbed interfaces)
    class FakeNotebook:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._tabs = []  # Store tab information
            self._current_tab = 0  # Currently selected tab index
            self._create_kivy_notebook()
            
        def _create_kivy_notebook(self):
            try:
                from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_notebook = TabbedPanel(**kivy_kwargs)
                # Clear default tab
                self.kivy_notebook.clear_tabs()
                
                print(f"Notebook created with options: {self.kwargs}")
                    
            except ImportError:
                print(f"Simulating notebook creation with: {self.kwargs}")
                self.kivy_notebook = f"Notebook({self.kwargs})"
        
        def add(self, child, **kwargs):
            """Add a tab to the notebook"""
            text = kwargs.get('text', f'Tab {len(self._tabs) + 1}')
            state = kwargs.get('state', 'normal')
            
            tab_info = {
                'child': child,
                'text': text,
                'state': state,
                'options': kwargs
            }
            self._tabs.append(tab_info)
            
            print(f"Notebook tab added: '{text}' (total tabs: {len(self._tabs)})")
            
            # Add to Kivy notebook if available
            try:
                if hasattr(self, 'kivy_notebook') and hasattr(self.kivy_notebook, 'add_widget'):
                    from kivy.uix.tabbedpanel import TabbedPanelItem
                    
                    # Create a new tab item
                    tab_item = TabbedPanelItem(text=text)
                    
                    # Add the child widget to the tab
                    if hasattr(child, 'kivy_frame'):
                        tab_item.add_widget(child.kivy_frame)
                    elif hasattr(child, 'kivy_canvas'):
                        tab_item.add_widget(child.kivy_canvas)
                    elif hasattr(child, 'kivy_label'):
                        tab_item.add_widget(child.kivy_label)
                    
                    # Add tab to notebook
                    self.kivy_notebook.add_widget(tab_item)
                    print(f"Tab '{text}' added to Kivy TabbedPanel")
                    
            except Exception as e:
                print(f"Note: Could not add tab to Kivy notebook: {e}")
            
        def insert(self, pos, child, **kwargs):
            """Insert a tab at specific position"""
            text = kwargs.get('text', f'Tab {len(self._tabs) + 1}')
            
            tab_info = {
                'child': child,
                'text': text,
                'options': kwargs
            }
            
            if pos == 'end' or pos >= len(self._tabs):
                self._tabs.append(tab_info)
            else:
                self._tabs.insert(pos, tab_info)
                
            print(f"Notebook tab inserted at position {pos}: '{text}'")
            
        def forget(self, tab_id):
            """Remove a tab from the notebook"""
            if isinstance(tab_id, int) and 0 <= tab_id < len(self._tabs):
                removed_tab = self._tabs.pop(tab_id)
                print(f"Notebook tab removed: '{removed_tab['text']}'")
            elif hasattr(tab_id, '__class__'):
                # Remove by child widget
                for i, tab in enumerate(self._tabs):
                    if tab['child'] == tab_id:
                        removed_tab = self._tabs.pop(i)
                        print(f"Notebook tab removed: '{removed_tab['text']}'")
                        break
                        
        def hide(self, tab_id):
            """Hide a tab (similar to forget but can be restored)"""
            if isinstance(tab_id, int) and 0 <= tab_id < len(self._tabs):
                self._tabs[tab_id]['state'] = 'hidden'
                print(f"Notebook tab hidden: '{self._tabs[tab_id]['text']}'")
                
        def tab(self, tab_id, option=None, **kwargs):
            """Configure or query tab options"""
            if isinstance(tab_id, int) and 0 <= tab_id < len(self._tabs):
                tab_info = self._tabs[tab_id]
                
                if option is None and not kwargs:
                    # Return all options
                    return tab_info['options']
                elif option is not None and not kwargs:
                    # Get specific option
                    return tab_info['options'].get(option, None)
                else:
                    # Set options
                    if option is not None:
                        kwargs[option] = kwargs.get(option, None)
                    tab_info['options'].update(kwargs)
                    print(f"Notebook tab configured: '{tab_info['text']}' with {kwargs}")
                    
        def tabs(self):
            """Return list of all tab widgets"""
            return [tab['child'] for tab in self._tabs]
            
        def index(self, tab_id):
            """Get the index of a tab"""
            if hasattr(tab_id, '__class__'):
                # Find by widget
                for i, tab in enumerate(self._tabs):
                    if tab['child'] == tab_id:
                        return i
            elif tab_id == 'current':
                return self._current_tab
            elif tab_id == 'end':
                return len(self._tabs) - 1
            return -1
            
        def select(self, tab_id=None):
            """Select a tab or get currently selected tab"""
            if tab_id is None:
                # Return currently selected tab
                if 0 <= self._current_tab < len(self._tabs):
                    return self._tabs[self._current_tab]['child']
                return None
            else:
                # Select specified tab
                if isinstance(tab_id, int) and 0 <= tab_id < len(self._tabs):
                    self._current_tab = tab_id
                    tab_text = self._tabs[tab_id]['text']
                    print(f"Notebook tab selected: '{tab_text}' (index {tab_id})")
                    
        def enable_traversal(self):
            """Enable keyboard traversal of tabs"""
            print("Notebook keyboard traversal enabled")
            
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_notebook'):
                    self.parent._widgets.append(self.kivy_notebook)
                print(f"Notebook packed with {len(self._tabs)} tabs")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure notebook options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                print(f"Notebook configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the notebook"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Notebook event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # Handle tab selection events
            if sequence == "<<NotebookTabChanged>>":
                print("Tab change event binding registered")
        
        # Window information methods (winfo_*)
        def winfo_width(self):
            """Return notebook width in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.width) if hasattr(self, 'kivy_notebook') else 800
            except:
                return 800  # Default fallback
                
        def winfo_height(self):
            """Return notebook height in pixels"""
            try:
                from kivy.core.window import Window
                return int(Window.height) if hasattr(self, 'kivy_notebook') else 600
            except:
                return 600  # Default fallback
                
        def winfo_reqwidth(self):
            """Return requested width"""
            return self.kwargs.get('width', self.winfo_width())
            
        def winfo_reqheight(self):
            """Return requested height"""
            return self.kwargs.get('height', self.winfo_height())
            
        def pack_configure(self, **kwargs):
            """Configure pack options for the notebook"""
            for key, value in kwargs.items():
                if key == 'padx':
                    self._pack_padx = value
                    print(f"Notebook pack padx set to: {value}")
                elif key == 'pady':
                    self._pack_pady = value
                    print(f"Notebook pack pady set to: {value}")
                elif key == 'fill':
                    self._pack_fill = value
                    print(f"Notebook pack fill set to: {value}")
                elif key == 'expand':
                    self._pack_expand = value
                    print(f"Notebook pack expand set to: {value}")
                elif key == 'side':
                    self._pack_side = value
                    print(f"Notebook pack side set to: {value}")
                else:
                    print(f"Notebook pack configured: {key} = {value}")
                    
        def pack_info(self):
            """Return current pack configuration"""
            return {
                'padx': getattr(self, '_pack_padx', 0),
                'pady': getattr(self, '_pack_pady', 0),
                'fill': getattr(self, '_pack_fill', 'none'),
                'expand': getattr(self, '_pack_expand', False),
                'side': getattr(self, '_pack_side', 'top')
            }
        
        def __str__(self):
            return f"TkNotebook(tabs={len(self._tabs)})"
    
    # Create fake Entry class (for text input)
    class FakeEntry:
        def __init__(self, parent, *args, **kwargs):
            self.parent = parent
            self.kwargs = kwargs.copy()
            
            # Handle positional arguments - Entry doesn't typically take text as first arg,
            # but let's handle it for consistency
            if args:
                # Entry widgets don't usually take text as first positional arg in tkinter,
                # but we'll handle it just in case
                print(f"Warning: Entry received {len(args)} positional arguments, ignoring them")
            
            self._text_var = self.kwargs.get('textvariable', None)
            self._value = kwargs.get('value', '')
            self._create_kivy_entry()
            
        def _create_kivy_entry(self):
            try:
                from kivy.uix.textinput import TextInput
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle text content
                if 'value' in self.kwargs:
                    kivy_kwargs['text'] = str(self.kwargs['value'])
                elif self._text_var and hasattr(self._text_var, 'get'):
                    kivy_kwargs['text'] = str(self._text_var.get())
                else:
                    kivy_kwargs['text'] = ''
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width'] * 8  # Approximate character width
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height'] * 20  # Approximate line height
                
                # Handle multiline
                kivy_kwargs['multiline'] = self.kwargs.get('multiline', False)
                
                # Handle read-only state
                if 'state' in self.kwargs:
                    if self.kwargs['state'] == 'readonly' or self.kwargs['state'] == 'disabled':
                        kivy_kwargs['readonly'] = True
                
                # Handle font
                if 'font' in self.kwargs:
                    # Simplified font handling
                    kivy_kwargs['font_size'] = '14sp'
                
                # Handle show parameter (for password fields)
                if 'show' in self.kwargs:
                    kivy_kwargs['password'] = True
                
                self.kivy_entry = TextInput(**kivy_kwargs)
                
                # Bind text changes to textvariable if provided
                if self._text_var and hasattr(self._text_var, 'set'):
                    def on_text_change(instance, value):
                        self._text_var.set(value)
                    self.kivy_entry.bind(text=on_text_change)
                    
                print(f"Entry created with text: '{kivy_kwargs.get('text', '')}' and options: {self.kwargs}")
                    
            except ImportError:
                print(f"Simulating entry creation with: {self.kwargs}")
                self.kivy_entry = f"Entry({self.kwargs})"
        
        def get(self):
            """Get the current text content"""
            if hasattr(self, 'kivy_entry') and hasattr(self.kivy_entry, 'text'):
                return self.kivy_entry.text
            return self._value
            
        def set(self, text):
            """Set the text content"""
            self._value = str(text)
            if hasattr(self, 'kivy_entry') and hasattr(self.kivy_entry, 'text'):
                self.kivy_entry.text = str(text)
            print(f"Entry text set to: '{text}'")
            
        def insert(self, index, text):
            """Insert text at specified index"""
            current_text = self.get()
            if isinstance(index, str):
                if index == 'end':
                    index = len(current_text)
                else:
                    index = 0
            
            new_text = current_text[:index] + str(text) + current_text[index:]
            self.set(new_text)
            print(f"Text inserted at index {index}: '{text}'")
            
        def delete(self, start, end=None):
            """Delete text from start to end index"""
            current_text = self.get()
            
            if isinstance(start, str):
                if start == 'end':
                    start = len(current_text)
                else:
                    start = 0
                    
            if end is None:
                end = start + 1
            elif isinstance(end, str):
                if end == 'end':
                    end = len(current_text)
                    
            new_text = current_text[:start] + current_text[end:]
            self.set(new_text)
            print(f"Text deleted from {start} to {end}")
            
        def clear(self):
            """Clear all text"""
            self.set('')
            print("Entry cleared")
            
        def select_range(self, start, end):
            """Select text from start to end"""
            if hasattr(self, 'kivy_entry'):
                try:
                    self.kivy_entry.select_text(start, end)
                    print(f"Text selected from {start} to {end}")
                except:
                    pass
                    
        def select_all(self):
            """Select all text"""
            text_length = len(self.get())
            self.select_range(0, text_length)
            print("All text selected")
            
        def icursor(self, index):
            """Set the insertion cursor position"""
            if hasattr(self, 'kivy_entry'):
                try:
                    self.kivy_entry.cursor = (index, 0)
                    print(f"Cursor set to position {index}")
                except:
                    pass
                    
        def index(self, mark):
            """Get index of mark (INSERT, END, etc.)"""
            if mark == 'insert' or mark == 'INSERT':
                if hasattr(self, 'kivy_entry'):
                    try:
                        return self.kivy_entry.cursor[0]
                    except:
                        pass
                return 0
            elif mark == 'end' or mark == 'END':
                return len(self.get())
            return 0
            
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_entry'):
                    self.parent._widgets.append(self.kivy_entry)
                print(f"Entry packed with text: '{self.get()}'")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure entry options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'state':
                    if hasattr(self, 'kivy_entry'):
                        self.kivy_entry.readonly = (value in ['readonly', 'disabled'])
                elif key == 'textvariable':
                    self._text_var = value
                print(f"Entry configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            if option == 'text':
                return self.get()
            return self.kwargs.get(option, None)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the entry"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Entry event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # Handle common entry events
            if sequence == "<Return>" or sequence == "<Enter>":
                print("Return key binding registered")
            elif sequence == "<FocusIn>":
                print("Focus in binding registered")
            elif sequence == "<FocusOut>":
                print("Focus out binding registered")
            elif sequence == "<KeyPress>":
                print("Key press binding registered")
                
        def focus_set(self):
            """Set focus to the entry"""
            self._has_focus = True
            if hasattr(self, 'kivy_entry'):
                try:
                    self.kivy_entry.focus = True
                except:
                    pass
            print("Focus set to entry")
            
        def focus_force(self):
            """Force focus to the entry"""
            self.focus_set()
            print("Focus forced to entry")
            
        def focus_get(self):
            """Get focus state"""
            return self if getattr(self, '_has_focus', False) else None
        
        def __str__(self):
            return f"TkEntry(text='{self.get()}')"
    
    # Create fake StringVar class (for tkinter variables)
    class FakeStringVar:
        def __init__(self, value=""):
            self._value = str(value)
            self._callbacks = []  # Store trace callbacks
            
        def get(self):
            """Get the current value"""
            return self._value
            
        def set(self, value):
            """Set the value and trigger any trace callbacks"""
            old_value = self._value
            self._value = str(value)
            
            # Trigger callbacks if value changed
            if old_value != self._value:
                for callback in self._callbacks:
                    try:
                        callback()
                    except Exception as e:
                        print(f"StringVar callback error: {e}")
                        
            print(f"StringVar set to: '{self._value}'")
            
        def trace(self, mode, callback):
            """Add a callback to be called when the variable changes"""
            self._callbacks.append(callback)
            print(f"StringVar trace added for mode: {mode}")
            return f"trace_{len(self._callbacks)}"
            
        def trace_remove(self, mode, cbname):
            """Remove a trace callback"""
            # Simplified implementation - would need proper callback ID tracking
            print(f"StringVar trace removed: {cbname}")
            
        def trace_info(self):
            """Get information about traces"""
            return [(f"trace_{i}", "write", callback) for i, callback in enumerate(self._callbacks)]
            
        def __str__(self):
            return f"StringVar(value='{self._value}')"
    
    # Create fake IntVar class (for integer variables)
    class FakeIntVar:
        def __init__(self, value=0):
            try:
                self._value = int(value)
            except (ValueError, TypeError):
                self._value = 0
            self._callbacks = []
            
        def get(self):
            """Get the current value"""
            return self._value
            
        def set(self, value):
            """Set the value and trigger any trace callbacks"""
            old_value = self._value
            try:
                self._value = int(value)
            except (ValueError, TypeError):
                self._value = 0
                
            # Trigger callbacks if value changed
            if old_value != self._value:
                for callback in self._callbacks:
                    try:
                        callback()
                    except Exception as e:
                        print(f"IntVar callback error: {e}")
                        
            print(f"IntVar set to: {self._value}")
            
        def trace(self, mode, callback):
            """Add a callback to be called when the variable changes"""
            self._callbacks.append(callback)
            print(f"IntVar trace added for mode: {mode}")
            return f"trace_{len(self._callbacks)}"
            
        def trace_remove(self, mode, cbname):
            """Remove a trace callback"""
            print(f"IntVar trace removed: {cbname}")
            
        def trace_info(self):
            """Get information about traces"""
            return [(f"trace_{i}", "write", callback) for i, callback in enumerate(self._callbacks)]
            
        def __str__(self):
            return f"IntVar(value={self._value})"
    
    # Create fake DoubleVar class (for float variables)
    class FakeDoubleVar:
        def __init__(self, value=0.0):
            try:
                self._value = float(value)
            except (ValueError, TypeError):
                self._value = 0.0
            self._callbacks = []
            
        def get(self):
            """Get the current value"""
            return self._value
            
        def set(self, value):
            """Set the value and trigger any trace callbacks"""
            old_value = self._value
            try:
                self._value = float(value)
            except (ValueError, TypeError):
                self._value = 0.0
                
            # Trigger callbacks if value changed
            if old_value != self._value:
                for callback in self._callbacks:
                    try:
                        callback()
                    except Exception as e:
                        print(f"DoubleVar callback error: {e}")
                        
            print(f"DoubleVar set to: {self._value}")
            
        def trace(self, mode, callback):
            """Add a callback to be called when the variable changes"""
            self._callbacks.append(callback)
            print(f"DoubleVar trace added for mode: {mode}")
            return f"trace_{len(self._callbacks)}"
            
        def trace_remove(self, mode, cbname):
            """Remove a trace callback"""
            print(f"DoubleVar trace removed: {cbname}")
            
        def trace_info(self):
            """Get information about traces"""
            return [(f"trace_{i}", "write", callback) for i, callback in enumerate(self._callbacks)]
            
        def __str__(self):
            return f"DoubleVar(value={self._value})"
    
    # Create fake BooleanVar class (for boolean variables)
    class FakeBooleanVar:
        def __init__(self, value=False):
            self._value = bool(value)
            self._callbacks = []
            
        def get(self):
            """Get the current value"""
            return self._value
            
        def set(self, value):
            """Set the value and trigger any trace callbacks"""
            old_value = self._value
            self._value = bool(value)
                
            # Trigger callbacks if value changed
            if old_value != self._value:
                for callback in self._callbacks:
                    try:
                        callback()
                    except Exception as e:
                        print(f"BooleanVar callback error: {e}")
                        
            print(f"BooleanVar set to: {self._value}")
            
        def trace(self, mode, callback):
            """Add a callback to be called when the variable changes"""
            self._callbacks.append(callback)
            print(f"BooleanVar trace added for mode: {mode}")
            return f"trace_{len(self._callbacks)}"
            
        def trace_remove(self, mode, cbname):
            """Remove a trace callback"""
            print(f"BooleanVar trace removed: {cbname}")
            
        def trace_info(self):
            """Get information about traces"""
            return [(f"trace_{i}", "write", callback) for i, callback in enumerate(self._callbacks)]
            
        def __str__(self):
            return f"BooleanVar(value={self._value})"
    
    # Create fake Checkbutton class (for checkbox widgets)
    class FakeCheckbutton:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._variable = kwargs.get('variable', None)
            self._value = kwargs.get('value', 1)  # Default value when checked
            self._is_checked = kwargs.get('checked', False)
            self._create_kivy_checkbutton()
            
        def _create_kivy_checkbutton(self):
            try:
                from kivy.uix.checkbox import CheckBox
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle initial state
                if self._variable and hasattr(self._variable, 'get'):
                    # Check if variable value matches our value
                    kivy_kwargs['active'] = (self._variable.get() == self._value)
                else:
                    kivy_kwargs['active'] = self._is_checked
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None  
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_checkbutton = CheckBox(**kivy_kwargs)
                
                # Bind checkbox state changes to variable if provided
                if self._variable and hasattr(self._variable, 'set'):
                    def on_checkbox_change(instance, value):
                        if value:  # Checked
                            self._variable.set(self._value)
                        else:  # Unchecked
                            self._variable.set(0 if isinstance(self._value, int) else "")
                    self.kivy_checkbutton.bind(active=on_checkbox_change)
                    
                # Handle command callback
                if 'command' in self.kwargs:
                    def on_state_change(instance, value):
                        try:
                            self.kwargs['command']()
                        except Exception as e:
                            print(f"Checkbutton command error: {e}")
                    self.kivy_checkbutton.bind(active=on_state_change)
                    
                print(f"Checkbutton created with active={kivy_kwargs.get('active', False)} and options: {self.kwargs}")
                    
            except ImportError:
                print(f"Simulating checkbutton creation with: {self.kwargs}")
                self.kivy_checkbutton = f"Checkbutton({self.kwargs})"
        
        def get(self):
            """Get the current state (1 if checked, 0 if unchecked)"""
            if hasattr(self, 'kivy_checkbutton') and hasattr(self.kivy_checkbutton, 'active'):
                return self._value if self.kivy_checkbutton.active else 0
            return 1 if self._is_checked else 0
            
        def set(self, value):
            """Set the checkbox state"""
            is_checked = bool(value)
            self._is_checked = is_checked
            
            if hasattr(self, 'kivy_checkbutton') and hasattr(self.kivy_checkbutton, 'active'):
                self.kivy_checkbutton.active = is_checked
                
            # Update variable if bound
            if self._variable and hasattr(self._variable, 'set'):
                if is_checked:
                    self._variable.set(self._value)
                else:
                    self._variable.set(0 if isinstance(self._value, int) else "")
                    
            print(f"Checkbutton set to: {'checked' if is_checked else 'unchecked'}")
            
        def toggle(self):
            """Toggle the checkbox state"""
            current_state = self.get()
            self.set(0 if current_state else 1)
            print(f"Checkbutton toggled to: {'checked' if self.get() else 'unchecked'}")
            
        def select(self):
            """Select (check) the checkbox"""
            self.set(1)
            print("Checkbutton selected")
            
        def deselect(self):
            """Deselect (uncheck) the checkbox"""
            self.set(0)
            print("Checkbutton deselected")
            
        def flash(self):
            """Flash the checkbox (tkinter compatibility)"""
            print("Checkbutton flashed")
            
        def invoke(self):
            """Invoke the checkbox command"""
            if 'command' in self.kwargs:
                try:
                    self.kwargs['command']()
                    print("Checkbutton command invoked")
                except Exception as e:
                    print(f"Error invoking checkbutton command: {e}")
            
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_checkbutton'):
                    self.parent._widgets.append(self.kivy_checkbutton)
                print(f"Checkbutton packed: {'checked' if self.get() else 'unchecked'}")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure checkbutton options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'variable':
                    self._variable = value
                elif key == 'value':
                    self._value = value
                elif key == 'state':
                    if hasattr(self, 'kivy_checkbutton'):
                        self.kivy_checkbutton.disabled = (value in ['disabled', 'DISABLED'])
                print(f"Checkbutton configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            if option == 'variable':
                return self._variable
            elif option == 'value':
                return self._value
            return self.kwargs.get(option, None)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the checkbutton"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Checkbutton event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # Handle common checkbutton events
            if sequence == "<Button-1>" or sequence == "<ButtonPress-1>":
                print("Mouse click binding registered")
            elif sequence == "<Return>" or sequence == "<Enter>":
                print("Return key binding registered")
                
        def focus_set(self):
            """Set focus to the checkbutton"""
            self._has_focus = True
            if hasattr(self, 'kivy_checkbutton'):
                try:
                    self.kivy_checkbutton.focus = True
                except:
                    pass
            print("Focus set to checkbutton")
            
        def focus_force(self):
            """Force focus to the checkbutton"""
            self.focus_set()
            print("Focus forced to checkbutton")
            
        def focus_get(self):
            """Get focus state"""
            return self if getattr(self, '_has_focus', False) else None
        
        def __str__(self):
            return f"TkCheckbutton(checked={'True' if self.get() else 'False'})"
    
    # Create fake Radiobutton class (for radio button widgets)
    class FakeRadiobutton:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._variable = kwargs.get('variable', None)
            self._value = kwargs.get('value', 1)  # Value this radio button represents
            self._is_selected = kwargs.get('selected', False)
            self._create_kivy_radiobutton()
            
        def _create_kivy_radiobutton(self):
            try:
                from kivy.uix.checkbox import CheckBox
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle initial state - radio button is selected if variable equals our value
                if self._variable and hasattr(self._variable, 'get'):
                    kivy_kwargs['active'] = (self._variable.get() == self._value)
                else:
                    kivy_kwargs['active'] = self._is_selected
                
                # For radio buttons, we use group behavior (only one can be selected)
                if self._variable:
                    kivy_kwargs['group'] = f"radiogroup_{id(self._variable)}"
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width']
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None  
                    kivy_kwargs['height'] = self.kwargs['height']
                
                self.kivy_radiobutton = CheckBox(**kivy_kwargs)
                
                # Bind radio button state changes to variable if provided
                if self._variable and hasattr(self._variable, 'set'):
                    def on_radio_change(instance, value):
                        if value:  # Selected
                            self._variable.set(self._value)
                        # Note: For radio buttons, we don't unset the variable when deselected
                        # because another radio button in the group will set it
                    self.kivy_radiobutton.bind(active=on_radio_change)
                    
                # Handle command callback
                if 'command' in self.kwargs:
                    def on_state_change(instance, value):
                        if value:  # Only trigger command when selected, not deselected
                            try:
                                self.kwargs['command']()
                            except Exception as e:
                                print(f"Radiobutton command error: {e}")
                    self.kivy_radiobutton.bind(active=on_state_change)
                    
                print(f"Radiobutton created with active={kivy_kwargs.get('active', False)}, value={self._value}, and options: {self.kwargs}")
                    
            except ImportError:
                print(f"Simulating radiobutton creation with: {self.kwargs}")
                self.kivy_radiobutton = f"Radiobutton({self.kwargs})"
        
        def get(self):
            """Get the current state (1 if selected, 0 if not selected)"""
            if hasattr(self, 'kivy_radiobutton') and hasattr(self.kivy_radiobutton, 'active'):
                return self._value if self.kivy_radiobutton.active else 0
            return self._value if self._is_selected else 0
            
        def set(self, value):
            """Set the radio button state"""
            is_selected = bool(value)
            self._is_selected = is_selected
            
            if hasattr(self, 'kivy_radiobutton') and hasattr(self.kivy_radiobutton, 'active'):
                self.kivy_radiobutton.active = is_selected
                
            # Update variable if bound and selected
            if self._variable and hasattr(self._variable, 'set') and is_selected:
                self._variable.set(self._value)
                    
            print(f"Radiobutton set to: {'selected' if is_selected else 'deselected'} (value: {self._value})")
            
        def select(self):
            """Select this radio button"""
            self.set(1)
            print(f"Radiobutton selected (value: {self._value})")
            
        def deselect(self):
            """Deselect this radio button (note: usually handled by group)"""
            self.set(0)
            print(f"Radiobutton deselected (value: {self._value})")
            
        def flash(self):
            """Flash the radio button (tkinter compatibility)"""
            print(f"Radiobutton flashed (value: {self._value})")
            
        def invoke(self):
            """Invoke the radio button command"""
            if 'command' in self.kwargs:
                try:
                    self.kwargs['command']()
                    print(f"Radiobutton command invoked (value: {self._value})")
                except Exception as e:
                    print(f"Error invoking radiobutton command: {e}")
            
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_radiobutton'):
                    self.parent._widgets.append(self.kivy_radiobutton)
                print(f"Radiobutton packed: {'selected' if self.get() else 'deselected'} (value: {self._value})")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure radiobutton options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'variable':
                    self._variable = value
                elif key == 'value':
                    self._value = value
                elif key == 'state':
                    if hasattr(self, 'kivy_radiobutton'):
                        self.kivy_radiobutton.disabled = (value in ['disabled', 'DISABLED'])
                print(f"Radiobutton configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            if option == 'variable':
                return self._variable
            elif option == 'value':
                return self._value
            return self.kwargs.get(option, None)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the radiobutton"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Radiobutton event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # Handle common radiobutton events
            if sequence == "<Button-1>" or sequence == "<ButtonPress-1>":
                print("Mouse click binding registered")
            elif sequence == "<Return>" or sequence == "<Enter>":
                print("Return key binding registered")
                
        def focus_set(self):
            """Set focus to the radiobutton"""
            self._has_focus = True
            if hasattr(self, 'kivy_radiobutton'):
                try:
                    self.kivy_radiobutton.focus = True
                except:
                    pass
            print(f"Focus set to radiobutton (value: {self._value})")
            
        def focus_force(self):
            """Force focus to the radiobutton"""
            self.focus_set()
            print(f"Focus forced to radiobutton (value: {self._value})")
            
        def focus_get(self):
            """Get focus state"""
            return self if getattr(self, '_has_focus', False) else None
        
        def __str__(self):
            return f"TkRadiobutton(selected={'True' if self.get() else 'False'}, value={self._value})"
    
    # Create fake Text class (for multi-line text widgets)
    class FakeText:
        def __init__(self, parent, **kwargs):
            self.parent = parent
            self.kwargs = kwargs
            self._content = kwargs.get('value', '')
            self._insert_position = '1.0'  # Line.column format (tkinter style)
            self._marks = {'insert': '1.0', 'current': '1.0'}
            self._create_kivy_text()
            
        def _create_kivy_text(self):
            try:
                from kivy.uix.textinput import TextInput
                
                # Translate tkinter parameters to Kivy
                kivy_kwargs = {}
                
                # Handle initial text content
                kivy_kwargs['text'] = self._content
                
                # Handle size
                if 'width' in self.kwargs:
                    kivy_kwargs['size_hint_x'] = None
                    kivy_kwargs['width'] = self.kwargs['width'] * 8  # Approximate character width
                    
                if 'height' in self.kwargs:
                    kivy_kwargs['size_hint_y'] = None
                    kivy_kwargs['height'] = self.kwargs['height'] * 20  # Approximate line height
                
                # Text widget is always multiline
                kivy_kwargs['multiline'] = True
                
                # Handle text wrapping
                if 'wrap' in self.kwargs:
                    wrap_mode = self.kwargs['wrap']
                    if wrap_mode == 'word':
                        kivy_kwargs['do_wrap'] = True
                    elif wrap_mode == 'char':
                        kivy_kwargs['do_wrap'] = True
                    elif wrap_mode == 'none':
                        kivy_kwargs['do_wrap'] = False
                else:
                    kivy_kwargs['do_wrap'] = True  # Default to word wrap
                
                # Handle read-only state
                if 'state' in self.kwargs:
                    if self.kwargs['state'] == 'readonly' or self.kwargs['state'] == 'disabled':
                        kivy_kwargs['readonly'] = True
                
                # Handle font
                if 'font' in self.kwargs:
                    kivy_kwargs['font_size'] = '14sp'
                
                # Handle scrollbars
                if 'yscrollcommand' in self.kwargs:
                    # Note: Kivy TextInput has built-in scrolling
                    pass
                
                self.kivy_text = TextInput(**kivy_kwargs)
                
                print(f"Text widget created with content length: {len(self._content)} chars and options: {self.kwargs}")
                    
            except ImportError:
                print(f"Simulating text widget creation with: {self.kwargs}")
                self.kivy_text = f"Text({self.kwargs})"
        
        def get(self, start='1.0', end='end'):
            """Get text content from start to end position"""
            if hasattr(self, 'kivy_text') and hasattr(self.kivy_text, 'text'):
                full_text = self.kivy_text.text
            else:
                full_text = self._content
            
            if start == '1.0' and end == 'end':
                return full_text
            
            # Simplified position handling - in real tkinter, positions are "line.column"
            # For now, just return full text for any range
            return full_text
            
        def insert(self, index, text):
            """Insert text at specified position"""
            current_text = self.get()
            
            # Simplified index handling
            if index == 'end' or index == 'end-1c':
                new_text = current_text + str(text)
            elif index == '1.0':
                new_text = str(text) + current_text
            else:
                # Insert at end for any other index
                new_text = current_text + str(text)
            
            self._content = new_text
            if hasattr(self, 'kivy_text') and hasattr(self.kivy_text, 'text'):
                self.kivy_text.text = new_text
            
            print(f"Text inserted at {index}: '{text[:50]}{'...' if len(str(text)) > 50 else ''}'")
            
        def delete(self, start, end=None):
            """Delete text from start to end position"""
            if end is None:
                end = f"{start}+1c"  # Delete one character
            
            if start == '1.0' and end == 'end':
                # Clear all text
                self._content = ''
                if hasattr(self, 'kivy_text') and hasattr(self.kivy_text, 'text'):
                    self.kivy_text.text = ''
                print("All text deleted")
            else:
                # Simplified - for complex position handling, would need proper parsing
                print(f"Text deleted from {start} to {end}")
            
        def clear(self):
            """Clear all text"""
            self.delete('1.0', 'end')
            
        def see(self, index):
            """Scroll to make the given position visible"""
            print(f"Scrolling to position: {index}")
            
        def mark_set(self, mark, index):
            """Set a mark at the given position"""
            self._marks[mark] = index
            print(f"Mark '{mark}' set to position {index}")
            
        def mark_unset(self, *marks):
            """Remove the given marks"""
            for mark in marks:
                if mark in self._marks:
                    del self._marks[mark]
                    print(f"Mark '{mark}' removed")
            
        def mark_names(self):
            """Return list of all mark names"""
            return list(self._marks.keys())
            
        def mark_next(self, index):
            """Return the next mark after the given position"""
            # Simplified implementation
            return None
            
        def mark_previous(self, index):
            """Return the previous mark before the given position"""
            # Simplified implementation
            return None
            
        def index(self, mark):
            """Get the position of a mark"""
            if mark in self._marks:
                return self._marks[mark]
            elif mark == 'insert':
                return self._insert_position
            elif mark == 'end':
                # Calculate end position based on content
                lines = self.get().split('\n')
                return f"{len(lines)}.{len(lines[-1]) if lines else 0}"
            return '1.0'
            
        def search(self, pattern, index='1.0', stopindex='end', **kwargs):
            """Search for pattern in text"""
            text = self.get()
            import re
            
            if kwargs.get('regexp', False):
                try:
                    match = re.search(pattern, text)
                    if match:
                        # Simplified - return approximate position
                        return '1.0'
                except:
                    pass
            else:
                # Simple string search
                if pattern in text:
                    return '1.0'
            
            return None
            
        def tag_add(self, tag, start, end=None):
            """Add a tag to text range"""
            if end is None:
                end = f"{start}+1c"
            print(f"Tag '{tag}' added from {start} to {end}")
            
        def tag_remove(self, tag, start=None, end=None):
            """Remove a tag from text range"""
            if start is None:
                start = '1.0'
            if end is None:
                end = 'end'
            print(f"Tag '{tag}' removed from {start} to {end}")
            
        def tag_config(self, tag, **kwargs):
            """Configure tag appearance"""
            print(f"Tag '{tag}' configured with options: {kwargs}")
            
        def tag_names(self, index=None):
            """Return list of tag names at position"""
            return []  # Simplified
            
        def compare(self, index1, op, index2):
            """Compare two text positions"""
            # Simplified comparison
            return True
            
        def bbox(self, index):
            """Get bounding box of character at position"""
            # Return approximate bounding box
            return (0, 0, 10, 20)
            
        def dlineinfo(self, index):
            """Get display line info for position"""
            return (0, 0, 100, 20, 0)  # x, y, width, height, baseline
            
        def yview(self, *args):
            """Handle vertical scrolling for scrollbar compatibility"""
            if not args:
                # Return current view as (top, bottom) fractions
                return (0.0, 1.0)
            elif len(args) == 1:
                # Move to fraction
                fraction = float(args[0])
                print(f"Text yview moveto: {fraction}")
            elif len(args) == 2:
                # Scroll by units
                what, number = args
                print(f"Text yview scroll: {number} {what}")
            
        def xview(self, *args):
            """Handle horizontal scrolling for scrollbar compatibility"""
            if not args:
                # Return current view as (left, right) fractions
                return (0.0, 1.0)
            elif len(args) == 1:
                # Move to fraction
                fraction = float(args[0])
                print(f"Text xview moveto: {fraction}")
            elif len(args) == 2:
                # Scroll by units
                what, number = args
                print(f"Text xview scroll: {number} {what}")
            
        def yview_moveto(self, fraction):
            """Move vertical view to fraction"""
            print(f"Text yview_moveto: {fraction}")
            
        def xview_moveto(self, fraction):
            """Move horizontal view to fraction"""
            print(f"Text xview_moveto: {fraction}")
            
        def yview_scroll(self, number, what):
            """Scroll vertically by number of units"""
            print(f"Text yview_scroll: {number} {what}")
            
        def xview_scroll(self, number, what):
            """Scroll horizontally by number of units"""
            print(f"Text xview_scroll: {number} {what}")
            
        def pack(self, **kwargs):
            # Add to parent's widget list
            if hasattr(self.parent, '_widgets'):
                if hasattr(self, 'kivy_text'):
                    self.parent._widgets.append(self.kivy_text)
                print(f"Text widget packed with {len(self.get())} characters")
        
        def grid(self, **kwargs):
            self.pack(**kwargs)
            
        def place(self, **kwargs):
            self.pack(**kwargs)
            
        def configure(self, **kwargs):
            """Configure text widget options"""
            for key, value in kwargs.items():
                self.kwargs[key] = value
                if key == 'state':
                    if hasattr(self, 'kivy_text'):
                        self.kivy_text.readonly = (value in ['readonly', 'disabled'])
                elif key == 'wrap':
                    if hasattr(self, 'kivy_text'):
                        if value == 'word' or value == 'char':
                            self.kivy_text.do_wrap = True
                        else:
                            self.kivy_text.do_wrap = False
                print(f"Text widget configured: {key} = {value}")
                
        def config(self, **kwargs):
            """Alias for configure"""
            return self.configure(**kwargs)
            
        def cget(self, option):
            """Get configuration option"""
            return self.kwargs.get(option, None)
            
        def bind(self, sequence, func, add=None):
            """Bind an event to the text widget"""
            if not hasattr(self, '_bindings'):
                self._bindings = {}
            self._bindings[sequence] = func
            print(f"Text widget event bound: {sequence} -> {func.__name__ if hasattr(func, '__name__') else func}")
            
            # Handle common text events
            if sequence == "<KeyPress>":
                print("Key press binding registered")
            elif sequence == "<Button-1>":
                print("Mouse click binding registered")
            elif sequence == "<FocusIn>":
                print("Focus in binding registered")
            elif sequence == "<FocusOut>":
                print("Focus out binding registered")
                
        def focus_set(self):
            """Set focus to the text widget"""
            self._has_focus = True
            if hasattr(self, 'kivy_text'):
                try:
                    self.kivy_text.focus = True
                except:
                    pass
            print("Focus set to text widget")
            
        def focus_force(self):
            """Force focus to the text widget"""
            self.focus_set()
            print("Focus forced to text widget")
            
        def focus_get(self):
            """Get focus state"""
            return self if getattr(self, '_has_focus', False) else None
        
        def __str__(self):
            return f"TkText(lines={len(self.get().split('\\n'))}, chars={len(self.get())})"
    
    # Create fake tkFont module for font handling
    class FakeFont:
        def __init__(self, family="Arial", size=12, weight="normal", slant="roman"):
            self.family = family
            self.size = size
            self.weight = weight
            self.slant = slant
            
        def __str__(self):
            return f"Font(family='{self.family}', size={self.size})"
            
        def configure(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
                
        def cget(self, option):
            return getattr(self, option, None)
            
        def copy(self):
            return FakeFont(self.family, self.size, self.weight, self.slant)
    
    def nametofont(name):
        """Simulate tkinter.font.nametofont - returns a default font"""
        if name == "TkDefaultFont":
            return FakeFont("Arial", 12)
        elif name == "TkTextFont":
            return FakeFont("Arial", 10)
        elif name == "TkFixedFont":
            return FakeFont("Courier", 10)
        elif name == "TkMenuFont":
            return FakeFont("Arial", 10)
        else:
            return FakeFont("Arial", 12)
    
    def Font(**kwargs):
        """Simulate tkinter.font.Font constructor"""
        family = kwargs.get('family', 'Arial')
        size = kwargs.get('size', 12)
        weight = kwargs.get('weight', 'normal')
        slant = kwargs.get('slant', 'roman')
        return FakeFont(family, size, weight, slant)
    
    # Create fake tkinter.font module
    fake_font_module = types.ModuleType('tkinter.font')
    fake_font_module.Font = Font
    fake_font_module.nametofont = nametofont
    fake_font_module.NORMAL = "normal"
    fake_font_module.BOLD = "bold"
    fake_font_module.ITALIC = "italic"
    fake_font_module.ROMAN = "roman"
    
    # Create fake messagebox functions for dialog boxes
    def showinfo(title, message, **kwargs):
        """Show an info dialog"""
        print(f"INFO: {title} - {message}")
        # In a real implementation, you might use Kivy's Popup
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as KivyLabel
            from kivy.uix.button import Button as KivyButton
            from kivy.uix.boxlayout import BoxLayout
            
            # Create popup layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            label = KivyLabel(text=message, text_size=(400, None), halign='center')
            button = KivyButton(text='OK', size_hint_y=None, height=40)
            
            layout.add_widget(label)
            layout.add_widget(button)
            
            popup = Popup(title=title, content=layout, size_hint=(0.6, 0.4))
            button.bind(on_press=popup.dismiss)
            popup.open()
            
        except ImportError:
            print("Kivy not available - using console output for dialog")
        return 'ok'
    
    def showerror(title, message, **kwargs):
        """Show an error dialog"""
        print(f"ERROR: {title} - {message}")
        # In a real implementation, you might use Kivy's Popup with error styling
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as KivyLabel
            from kivy.uix.button import Button as KivyButton
            from kivy.uix.boxlayout import BoxLayout
            
            # Create popup layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            label = KivyLabel(text=f"❌ {message}", text_size=(400, None), halign='center')
            button = KivyButton(text='OK', size_hint_y=None, height=40)
            
            layout.add_widget(label)
            layout.add_widget(button)
            
            popup = Popup(title=f"Error: {title}", content=layout, size_hint=(0.6, 0.4))
            button.bind(on_press=popup.dismiss)
            popup.open()
            
        except ImportError:
            print("Kivy not available - using console output for error dialog")
        return 'ok'
    
    def showwarning(title, message, **kwargs):
        """Show a warning dialog"""
        print(f"WARNING: {title} - {message}")
        # In a real implementation, you might use Kivy's Popup with warning styling
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as KivyLabel
            from kivy.uix.button import Button as KivyButton
            from kivy.uix.boxlayout import BoxLayout
            
            # Create popup layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            label = KivyLabel(text=f"⚠️ {message}", text_size=(400, None), halign='center')
            button = KivyButton(text='OK', size_hint_y=None, height=40)
            
            layout.add_widget(label)
            layout.add_widget(button)
            
            popup = Popup(title=f"Warning: {title}", content=layout, size_hint=(0.6, 0.4))
            button.bind(on_press=popup.dismiss)
            popup.open()
            
        except ImportError:
            print("Kivy not available - using console output for warning dialog")
        return 'ok'
    
    def askyesno(title, message, **kwargs):
        """Show a yes/no question dialog"""
        print(f"QUESTION: {title} - {message}")
        # For now, return True as default. In real implementation, show Kivy dialog
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as KivyLabel
            from kivy.uix.button import Button as KivyButton
            from kivy.uix.boxlayout import BoxLayout
            
            # Create popup layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            label = KivyLabel(text=f"❓ {message}", text_size=(400, None), halign='center')
            
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            yes_button = KivyButton(text='Yes')
            no_button = KivyButton(text='No')
            
            button_layout.add_widget(yes_button)
            button_layout.add_widget(no_button)
            
            layout.add_widget(label)
            layout.add_widget(button_layout)
            
            popup = Popup(title=title, content=layout, size_hint=(0.6, 0.4))
            
            result = [None]  # Use list to allow modification in nested function
            
            def yes_pressed(instance):
                result[0] = True
                popup.dismiss()
                
            def no_pressed(instance):
                result[0] = False
                popup.dismiss()
            
            yes_button.bind(on_press=yes_pressed)
            no_button.bind(on_press=no_pressed)
            popup.open()
            
            # Note: In a real implementation, you'd need to handle async behavior
            # For now, return True as default
            return True
            
        except ImportError:
            print("Kivy not available - using console output for question dialog")
            print("  Defaulting to 'Yes' response")
            return True
    
    def askokcancel(title, message, **kwargs):
        """Show an OK/Cancel dialog"""
        print(f"CONFIRM: {title} - {message}")
        # For now, return True as default. In real implementation, show Kivy dialog
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label as KivyLabel
            from kivy.uix.button import Button as KivyButton
            from kivy.uix.boxlayout import BoxLayout
            
            # Create popup layout
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            label = KivyLabel(text=message, text_size=(400, None), halign='center')
            
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            ok_button = KivyButton(text='OK')
            cancel_button = KivyButton(text='Cancel')
            
            button_layout.add_widget(ok_button)
            button_layout.add_widget(cancel_button)
            
            layout.add_widget(label)
            layout.add_widget(button_layout)
            
            popup = Popup(title=title, content=layout, size_hint=(0.6, 0.4))
            
            result = [None]  # Use list to allow modification in nested function
            
            def ok_pressed(instance):
                result[0] = True
                popup.dismiss()
                
            def cancel_pressed(instance):
                result[0] = False
                popup.dismiss()
            
            ok_button.bind(on_press=ok_pressed)
            cancel_button.bind(on_press=cancel_pressed)
            popup.open()
            
            # Note: In a real implementation, you'd need to handle async behavior
            # For now, return True as default
            return True
            
        except ImportError:
            print("Kivy not available - using console output for confirm dialog")
            print("  Defaulting to 'OK' response")
            return True
    
    def askretrycancel(title, message, **kwargs):
        """Show a Retry/Cancel dialog"""
        print(f"RETRY: {title} - {message}")
        # For now, return True as default
        print("  Defaulting to 'Retry' response")
        return True
    
    def askyesnocancel(title, message, **kwargs):
        """Show a Yes/No/Cancel dialog"""
        print(f"QUESTION: {title} - {message}")
        # For now, return True as default
        print("  Defaulting to 'Yes' response")
        return True
    
    # Create fake tkinter.messagebox module
    fake_messagebox_module = types.ModuleType('tkinter.messagebox')
    fake_messagebox_module.showinfo = showinfo
    fake_messagebox_module.showerror = showerror
    fake_messagebox_module.showwarning = showwarning
    fake_messagebox_module.askyesno = askyesno
    fake_messagebox_module.askokcancel = askokcancel
    fake_messagebox_module.askretrycancel = askretrycancel
    fake_messagebox_module.askyesnocancel = askyesnocancel
    
    # Message box constants
    fake_messagebox_module.OK = 'ok'
    fake_messagebox_module.CANCEL = 'cancel'
    fake_messagebox_module.YES = 'yes'
    fake_messagebox_module.NO = 'no'
    fake_messagebox_module.RETRY = 'retry'
    fake_messagebox_module.IGNORE = 'ignore'
    fake_messagebox_module.ABORT = 'abort'
    
    print("MessageBox support added - dialog boxes will work with Kivy popups")

    # Create fake tkinter.ttk module (themed tkinter)
    fake_ttk_module = types.ModuleType('tkinter.ttk')
    # TTK widgets are essentially the same as regular tkinter widgets for our purposes
    fake_ttk_module.Button = FakeButton
    fake_ttk_module.Label = FakeLabel
    
    # Add other common TTK widgets (using same base classes for simplicity)
    fake_ttk_module.Entry = FakeEntry  # Proper entry class
    fake_ttk_module.Frame = FakeFrame  # Now uses proper Frame class
    fake_ttk_module.Checkbutton = FakeCheckbutton  # Proper checkbutton class
    fake_ttk_module.Radiobutton = FakeRadiobutton  # Proper radiobutton class
    fake_ttk_module.Text = FakeText  # Proper text widget class
    fake_ttk_module.Scale = FakeLabel  # Placeholder
    fake_ttk_module.Progressbar = FakeLabel  # Placeholder
    fake_ttk_module.Combobox = FakeLabel  # Placeholder
    fake_ttk_module.Treeview = FakeLabel  # Placeholder
    fake_ttk_module.Notebook = FakeNotebook  # Proper notebook class
    fake_ttk_module.Separator = FakeLabel  # Placeholder
    fake_ttk_module.Scrollbar = FakeScrollbar  # Scrollbar widget
    
    print("TTK (themed tkinter) support added - ttk widgets will use same translations as regular tkinter")
    
    # Set up the fake module attributes
    fake_tkinter.Tk = FakeTk
    fake_tkinter.Button = FakeButton
    fake_tkinter.Label = FakeLabel
    fake_tkinter.Entry = FakeEntry
    fake_tkinter.Text = FakeText  # Add text widget
    fake_tkinter.Frame = FakeFrame
    fake_tkinter.Canvas = FakeCanvas
    fake_tkinter.Scrollbar = FakeScrollbar
    fake_tkinter.Menu = FakeMenu
    fake_tkinter.Notebook = FakeNotebook  # Add notebook to main tkinter module too
    fake_tkinter.Checkbutton = FakeCheckbutton  # Add checkbutton widget
    fake_tkinter.Radiobutton = FakeRadiobutton  # Add radiobutton widget
    fake_tkinter.StringVar = FakeStringVar
    fake_tkinter.IntVar = FakeIntVar
    fake_tkinter.DoubleVar = FakeDoubleVar
    fake_tkinter.BooleanVar = FakeBooleanVar
    fake_tkinter.font = fake_font_module
    fake_tkinter.ttk = fake_ttk_module
    fake_tkinter.messagebox = fake_messagebox_module  # Add messagebox module
    
    # Replace tkinter, tkinter.font, tkinter.ttk, and tkinter.messagebox in sys.modules
    sys.modules['tkinter'] = fake_tkinter
    sys.modules['tkinter.font'] = fake_font_module
    sys.modules['tkinter.ttk'] = fake_ttk_module
    sys.modules['tkinter.messagebox'] = fake_messagebox_module
    
    print("Auto-translation mode enabled - tkinter calls will be converted to Kivy")
    return fake_tkinter

def disable_auto_translate():
    """
    Disable automatic translation mode and restore original tkinter.
    """
    if 'tkinter' in _original_modules:
        sys.modules['tkinter'] = _original_modules['tkinter']
    elif 'tkinter' in sys.modules:
        del sys.modules['tkinter']
        
    # Also clean up font, ttk, and messagebox modules
    if 'tkinter.font' in sys.modules:
        del sys.modules['tkinter.font']
    if 'tkinter.ttk' in sys.modules:
        del sys.modules['tkinter.ttk']
    if 'tkinter.messagebox' in sys.modules:
        del sys.modules['tkinter.messagebox']

def translate_imports(tkinter_code):
    """
    Translates tkinter imports to Kivy imports.
    
    Args:
        tkinter_code (str): String containing tkinter import statements
        
    Returns:
        str: Equivalent Kivy import statements
    """
    import re
    
    # Common import translations
    kivy_imports = []
    
    # Check for tkinter imports
    if re.search(r'import\s+tkinter\s+as\s+tk', tkinter_code):
        kivy_imports.extend([
            "from kivy.app import App",
            "from kivy.uix.boxlayout import BoxLayout",
            "from kivy.uix.button import Button",
            "from kivy.uix.label import Label"
        ])
    elif re.search(r'from\s+tkinter\s+import', tkinter_code):
        kivy_imports.extend([
            "from kivy.app import App",
            "from kivy.uix.boxlayout import BoxLayout", 
            "from kivy.uix.button import Button",
            "from kivy.uix.label import Label"
        ])
    elif re.search(r'import\s+tkinter', tkinter_code):
        kivy_imports.extend([
            "from kivy.app import App",
            "from kivy.uix.boxlayout import BoxLayout",
            "from kivy.uix.button import Button", 
            "from kivy.uix.label import Label"
        ])
    
    return '\n'.join(kivy_imports)

def translate_window(tkinter_code):
    """
    Translates tkinter window creation to Kivy App structure.
    
    Args:
        tkinter_code (str): String containing tkinter window code
        
    Returns:
        str: Equivalent Kivy App structure
    """
    import re
    
    # Look for tk.Tk() or tkinter.Tk()
    if re.search(r'(?:tk\.)?Tk\(\)', tkinter_code):
        app_template = '''class MainApp(App):
    def build(self):
        # Create main layout
        layout = BoxLayout(orientation='vertical')
        
        # Add your widgets here
        # Example: layout.add_widget(Button(text='Hello'))
        
        return layout

# Run the app
if __name__ == '__main__':
    MainApp().run()'''
        return app_template
    
    return tkinter_code

def translate_button(tkinter_button_code):
    """
    Translates tkinter Button calls to Kivy Button calls.
    
    Args:
        tkinter_button_code (str): String containing tkinter Button constructor call
        
    Returns:
        str: Equivalent Kivy Button constructor call
    """
    import re
    
    # Common parameter mappings from tkinter to Kivy
    param_mappings = {
        'text': 'text',
        'command': 'on_press',  # Note: Kivy uses on_press instead of command
        'width': 'size_hint_x',  # Kivy uses size_hint or size
        'height': 'size_hint_y',
        'bg': 'background_color',
        'background': 'background_color',
        'fg': 'color',
        'foreground': 'color',
        'font': 'font_name',  # Simplified mapping
        'state': 'disabled',  # Need to convert DISABLED/NORMAL to True/False
        'relief': None,  # No direct equivalent in Kivy
        'bd': None,  # No direct equivalent (border)
        'borderwidth': None,
        'padx': None,  # Kivy handles padding differently
        'pady': None,
    }
    
    # Extract the Button constructor call
    button_pattern = r'(?:tk\.)?Button\s*\((.*?)\)'
    match = re.search(button_pattern, tkinter_button_code, re.DOTALL)
    
    if not match:
        return "# Could not parse tkinter Button call"
    
    params_str = match.group(1).strip()
    
    # Handle case where first parameter is the parent (like Button(root, text="..."))
    # Split by comma and check if first part is not a keyword argument
    parts = [p.strip() for p in params_str.split(',')]
    
    # If first part doesn't contain '=', it's likely the parent widget
    if parts and '=' not in parts[0]:
        # Remove the parent parameter as Kivy handles this differently
        params_str = ','.join(parts[1:])
    
    # Parse parameters (simplified parsing)
    # This handles basic cases - could be enhanced for more complex scenarios
    param_pattern = r'(\w+)\s*=\s*([^,]+?)(?=,\s*\w+\s*=|$)'
    params = re.findall(param_pattern, params_str)
    
    kivy_params = []
    kivy_bindings = []
    
    for param_name, param_value in params:
        param_name = param_name.strip()
        param_value = param_value.strip()
        
        if param_name in param_mappings:
            kivy_param = param_mappings[param_name]
            
            if kivy_param is None:
                # Skip parameters that don't have Kivy equivalents
                continue
            elif param_name == 'command':
                # Handle command -> on_press conversion
                # Extract function name from command
                func_match = re.search(r'(\w+)', param_value)
                if func_match:
                    func_name = func_match.group(1)
                    kivy_bindings.append(f"button.bind(on_press={func_name})")
                continue
            elif param_name == 'state':
                # Convert DISABLED/NORMAL to boolean
                if 'DISABLED' in param_value.upper():
                    kivy_params.append(f"disabled=True")
                else:
                    kivy_params.append(f"disabled=False")
                continue
            elif param_name in ['width', 'height']:
                # Convert absolute size to size_hint (simplified)
                kivy_params.append(f"{kivy_param}=None")
                if param_name == 'width':
                    kivy_params.append(f"width={param_value}")
                else:
                    kivy_params.append(f"height={param_value}")
                continue
            else:
                kivy_params.append(f"{kivy_param}={param_value}")
        else:
            # Keep unknown parameters as comments
            kivy_params.append(f"# {param_name}={param_value}  # No direct Kivy equivalent")
    
    # Build the Kivy Button call
    kivy_code = f"Button({', '.join(kivy_params)})"
    
    # Add binding if there was a command
    if kivy_bindings:
        kivy_code += "\n" + "\n".join(kivy_bindings)
    
    return kivy_code

def translate(tkinter_code):
    """
    Complete translator that handles imports, window creation, and widgets.
    
    Args:
        tkinter_code (str): Complete tkinter code
        
    Returns:
        str: Equivalent Kivy code
    """
    import re
    
    lines = tkinter_code.split('\n')
    kivy_lines = []
    imports_added = False
    app_structure_added = False
    in_build_method = False
    
    for line in lines:
        original_line = line
        line_stripped = line.strip()
        
        # Handle imports
        if re.search(r'import\s+tkinter|from\s+tkinter', line_stripped):
            if not imports_added:
                kivy_lines.extend([
                    "from kivy.app import App",
                    "from kivy.uix.boxlayout import BoxLayout",
                    "from kivy.uix.button import Button",
                    "from kivy.uix.label import Label",
                    "from kivy.uix.textinput import TextInput",
                    ""
                ])
                imports_added = True
            continue
            
        # Handle window creation
        elif re.search(r'(?:tk\.)?Tk\(\)', line_stripped):
            if not app_structure_added:
                kivy_lines.extend([
                    "class MainApp(App):",
                    "    def build(self):",
                    "        self.layout = BoxLayout(orientation='vertical')",
                    ""
                ])
                app_structure_added = True
                in_build_method = True
            # Handle root = tk.Tk() assignments by commenting them out
            if '=' in line_stripped:
                kivy_lines.append(f"        # {line_stripped}  # Root window - replaced by App.build()")
            continue
            
        # Handle window configuration (title, geometry, etc.)
        elif re.search(r'\.title\(|\.geometry\(|\.resizable\(', line_stripped):
            # Skip these as they don't directly translate to Kivy build method
            kivy_lines.append(f"        # {line_stripped}  # Window config - handle in App if needed")
            continue
            
        # Handle mainloop
        elif re.search(r'\.mainloop\(\)', line_stripped):
            kivy_lines.extend([
                "",
                "        return self.layout",
                "",
                "if __name__ == '__main__':",
                "    MainApp().run()"
            ])
            in_build_method = False
            continue
            
        # Handle Button creation
        elif re.search(r'(?:tk\.)?Button\s*\(', line_stripped):
            kivy_button = translate_button(line_stripped)
            if 'button.bind' in kivy_button:
                button_part, bind_part = kivy_button.split('\n', 1)
                kivy_lines.append(f"        button = {button_part}")
                kivy_lines.append(f"        {bind_part}")
                kivy_lines.append("        self.layout.add_widget(button)")
            else:
                kivy_lines.append(f"        button = {kivy_button}")
                kivy_lines.append("        self.layout.add_widget(button)")
            continue
            
        # Handle pack, grid, place methods
        elif re.search(r'\.pack\(\)|\.grid\(\)|\.place\(\)', line_stripped):
            # These are handled by add_widget in Kivy
            kivy_lines.append("        # Layout handled by add_widget() above")
            continue
            
        # Handle function definitions and other code
        else:
            if line_stripped and not line_stripped.startswith('#'):
                # If we're not in the app structure yet, keep functions at module level
                if not app_structure_added or line_stripped.startswith('def ') or line_stripped.startswith('class '):
                    kivy_lines.append(original_line)
                else:
                    # Skip variable assignments that reference root window
                    if re.search(r'root\s*=', line_stripped):
                        continue
                    # Other code goes in build method with proper indentation
                    if in_build_method:
                        kivy_lines.append(f"        {original_line}")
                    else:
                        kivy_lines.append(original_line)
            else:
                # Keep comments and empty lines
                kivy_lines.append(original_line)
    
    return '\n'.join(kivy_lines)

# Convenience aliases for backward compatibility and ease of use
tkinter_to_kivy = translate
tkinter_to_kivy_button = translate_button
tkinter_to_kivy_imports = translate_imports
tkinter_to_kivy_window = translate_window

# Main public API
__all__ = [
    'translate',           # Main translation function
    'translate_button',    # Button-specific translation
    'translate_imports',   # Import translation
    'translate_window',    # Window translation
    'auto_translate_mode', # Enable automatic translation
    'disable_auto_translate', # Disable automatic translation
    'tk',                 # Fake tkinter module
    'tkFont',             # Fake tkinter.font module
    'Label',              # Fake Label class
    'messagebox',         # Fake messagebox module
    # Aliases for backward compatibility
    'tkinter_to_kivy',
    'tkinter_to_kivy_button', 
    'tkinter_to_kivy_imports',
    'tkinter_to_kivy_window'
]

# Auto-enable translation mode when module is imported
# You can disable this by calling disable_auto_translate()
fake_tk_module = auto_translate_mode()

# Make tk available directly from this module for convenience
tk = fake_tk_module
tkFont = fake_tk_module.font  # Make tkFont available for font operations
messagebox = fake_tk_module.messagebox  # Make messagebox available directly

# Also make common tkinter classes available directly
Tk = fake_tk_module.Tk
Button = fake_tk_module.Button
Label = fake_tk_module.Label
Frame = fake_tk_module.Frame
Canvas = fake_tk_module.Canvas
Scrollbar = fake_tk_module.Scrollbar


# Example usage and test cases
if __name__ == "__main__":
    # Test cases for button translation
    button_test_cases = [
        'Button(text="Click Me", command=my_function)',
        'tk.Button(root, text="Submit", bg="blue", fg="white", command=submit_data)',
        'Button(master, text="Cancel", width=10, height=2, state=DISABLED)',
        'Button(text="OK", font=("Arial", 12), relief=RAISED, bd=2)',
        'tk.Button(root, text="With Root Parent")',
        'Button(window, text="Another Parent", bg="green")'
    ]
    
    print("Tkinter to Kivy Button Translation Examples:")
    print("=" * 50)
    
    for i, tkinter_code in enumerate(button_test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Tkinter: {tkinter_code}")
        print(f"Kivy:    {translate_button(tkinter_code)}")
    
    # Test complete code translation
    print("\n" + "=" * 50)
    print("Complete Code Translation Example:")
    print("=" * 50)
    
    sample_tkinter_code = """import tkinter as tk

def button_click():
    print("Button clicked!")

root = tk.Tk()
root.title("My App")
root.geometry("300x200")

button1 = tk.Button(root, text="Click Me", command=button_click)
button1.pack()

button2 = tk.Button(root, text="Exit", bg="red", fg="white")
button2.pack()

root.mainloop()"""
    
    print("\nOriginal Tkinter Code:")
    print("-" * 30)
    print(sample_tkinter_code)
    
    print("\nTranslated Kivy Code:")
    print("-" * 30)
    print(translate(sample_tkinter_code))
    
    print("\n" + "=" * 50)
    print("Note: This is a basic translator. Complex cases may need manual adjustment.")
    print("Additional imports may be needed depending on widgets used.")
