import tkinter, os

from runtime.services.backend.utilities import p, local_directory

def critical_error():
    def stop_engine():
        window.destroy()
        os._exit(1)
    window = tkinter.Tk()
    window.title("Bloxel: Critical Error")
    window.iconbitmap(default="runtime/assets/textures/user_interface/icon.ico")
    window.geometry("300x100")
    window.resizable(False, False)
    tkinter.Label(window, text="Critical Error: Unable to create the necessary directories!").pack(pady=10)
    tkinter.Button(window, text="OK", command=stop_engine).pack()
    window.mainloop()

def verify_local_directory():
    if os.path.isdir(local_directory()):
        p(f"SERVICES: directory.py found = {local_directory()}")
        p(f"SERVICES: directory.py stopping (code 0)")
    else:
        p(f"SERVICES: directory.py could not find {local_directory()}, creating the necessary directories...")
        create_local_directory()

def create_local_directory():
    try:  
        os.makedirs(local_directory(), exist_ok=True)
        p(f"SERVICES: directory.py created = {local_directory()}")

        os.makedirs(os.path.join(local_directory(), "logs"), exist_ok=True)
        p(f"SERVICES: directory.py created = {os.path.join(local_directory(), "logs")}")

        open(os.path.join(local_directory(), "configuration.json"), "a").close()
        p(f"SERVICES: directory.py created = {os.path.join(local_directory(), "configuration.json")}")

        p(f"SERVICES: directory.py finished creating = {local_directory()}")
        p(f"SERVICES: directory.py stopping (code 1)")
    except:
        p(f"SERVICES: directory.py failed")
        p(f"SERVICES: directory.py stopping (code 2)")
        critical_error()

def start_service_directory():
    p("SERVICES: directory.py started")