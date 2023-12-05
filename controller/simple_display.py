import tkinter as tk
import asyncio

class SliderWindow:

    def __init__(self):
        self._running = False
        self._slider_value = 0
        self.root = tk.Tk()
        self.root.title("Motor Control Test")
        self.root.geometry("400x200")

        self.slider = tk.Scale(self.root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self._on_slider_change)
        self.slider.pack(padx=20, pady=20)

        self.label_text = tk.StringVar()
        self.label = tk.Label(self.root, textvariable=self.label_text, font=('Comic Sans', 18))
        self.label.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.loop = asyncio.get_event_loop()

    async def run(self):
        self._running = True
        while self._running:
            await asyncio.sleep(0.01)
            self.root.update()
            
    def set_slider_value(self, value) -> None:
        self.slider.set(value)
        self._slider_value = value

    def _on_slider_change(self, event):
        self._slider_value = float(event)

    def _on_closing(self):
        self._running = False

    def get_slider_value(self) -> float:
        return self._slider_value
    
    def set_text(self, text: str) -> None:
        self.label_text.set(text)