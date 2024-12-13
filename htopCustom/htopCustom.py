import tkinter as tk
from tkinter import ttk
import psutil
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Monitor")
        self.geometry("800x600")
        self.configure(bg='black')
        self.attributes("-topmost", True)  # Keep the window always on top

        self.create_widgets()
        self.update_info()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.tree = ttk.Treeview(self, columns=("Property", "Value"), show="headings", style="Treeview")
        self.tree.heading("Property", text="Property")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the CPU and RAM usage graphs
        self.graph_frame = tk.Frame(self, bg='black')
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Create CPU usage graph
        self.cpu_fig, self.cpu_ax = plt.subplots()
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.graph_frame)
        self.cpu_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create RAM and Swap usage graph
        self.ram_fig, self.ram_ax = plt.subplots()
        self.ram_canvas = FigureCanvasTkAgg(self.ram_fig, master=self.graph_frame)
        self.ram_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def update_info(self):
        self.tree.delete(*self.tree.get_children())

        # Operating System Information
        self.tree.insert("", "end", values=("Operating System", platform.system()))
        self.tree.insert("", "end", values=("OS Version", platform.version()))
        self.tree.insert("", "end", values=("OS Release", platform.release()))

        # CPU Information
        self.tree.insert("", "end", values=("CPU", platform.processor()))
        self.tree.insert("", "end", values=("CPU Cores (Physical)", psutil.cpu_count(logical=False)))
        self.tree.insert("", "end", values=("CPU Cores (Logical)", psutil.cpu_count(logical=True)))
        self.tree.insert("", "end", values=("CPU Frequency", f"{psutil.cpu_freq().current:.2f} MHz"))

        # RAM Information
        virtual_memory = psutil.virtual_memory()
        self.tree.insert("", "end", values=("Total RAM", f"{virtual_memory.total / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("Available RAM", f"{virtual_memory.available / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("Used RAM", f"{virtual_memory.used / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("RAM Usage Percentage", f"{virtual_memory.percent}%"))

        # Swap Information
        swap_memory = psutil.swap_memory()
        self.tree.insert("", "end", values=("Total Swap", f"{swap_memory.total / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("Used Swap", f"{swap_memory.used / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("Free Swap", f"{swap_memory.free / (1024 ** 3):.2f} GB"))
        self.tree.insert("", "end", values=("Swap Usage Percentage", f"{swap_memory.percent}%"))

        # Load Average
        if hasattr(psutil, "getloadavg"):
            load1, load5, load15 = psutil.getloadavg()
            self.tree.insert("", "end", values=("Load Average (1 min)", f"{load1:.2f}"))
            self.tree.insert("", "end", values=("Load Average (5 min)", f"{load5:.2f}"))
            self.tree.insert("", "end", values=("Load Average (15 min)", f"{load15:.2f}"))

        # Uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        self.tree.insert("", "end", values=("Uptime", str(uptime).split('.')[0]))

        # Tasks, Threads, and Running Processes
        self.tree.insert("", "end", values=("Total Tasks", len(psutil.pids())))
        self.tree.insert("", "end", values=("Total Threads", sum(p.num_threads() for p in psutil.process_iter())))
        self.tree.insert("", "end", values=("Running Processes", len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_RUNNING])))

        # Update CPU and RAM usage graphs
        self.update_graphs()

        # Schedule the update_info method to be called again after 1000ms (1 second)
        self.after(1000, self.update_info)

    def update_graphs(self):
        # Update CPU usage graph
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        self.cpu_ax.clear()
        self.cpu_ax.bar(range(len(cpu_percent)), cpu_percent, color='green')
        self.cpu_ax.set_ylim(0, 100)
        self.cpu_ax.set_title("CPU Usage (%)", color='white')
        self.cpu_ax.set_facecolor('black')
        self.cpu_ax.tick_params(axis='x', colors='white')
        self.cpu_ax.tick_params(axis='y', colors='white')
        self.cpu_canvas.draw()

        # Update RAM and Swap usage graph
        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
        self.ram_ax.clear()
        self.ram_ax.bar(['RAM Used', 'RAM Free', 'Swap Used', 'Swap Free'],
                        [virtual_memory.used / (1024 ** 3), virtual_memory.free / (1024 ** 3),
                         swap_memory.used / (1024 ** 3), swap_memory.free / (1024 ** 3)],
                        color=['blue', 'blue', 'red', 'red'])
        self.ram_ax.set_title("Memory Usage (GB)", color='white')
        self.ram_ax.set_facecolor('black')
        self.ram_ax.tick_params(axis='x', colors='white')
        self.ram_ax.tick_params(axis='y', colors='white')
        self.ram_canvas.draw()

if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
