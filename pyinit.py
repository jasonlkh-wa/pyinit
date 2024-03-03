import platform
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os


# CR-someday add a check-box to allow the name of file to be machinize project name instead of main.py
def system_compatability_check():
    """Return error message if the operating system is not MacOS."""
    if platform.system() != "Darwin":
        root = Tk()

        width = 250
        height = 150
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        root.geometry(f"{width}x{height}+{(ws-width)//2}+{(hs-height)//2}")
        root.title("Incompatible system")

        Label(root, text="Only MacOS is supported", font="Roboto 20").pack()
        ttk.Button(root, text="OK", command=root.destroy).pack()
        root.mainloop()


def browse_folder():
    folder_dir = filedialog.askdirectory()
    folder_dir_entry.delete(0, END)
    folder_dir_entry.insert(0, folder_dir)


def create_project():
    folder_name = folder_name_entry.get()
    folder_dir = folder_dir_entry.get()
    conda_env = conda_env_listbox.get(ACTIVE)
    if not folder_name:
        error_label.config(text="Please enter a folder name.")
        return
    if not folder_dir:
        error_label.config(text="Please select a folder directory.")
        return
    folder_path = f"{folder_dir}/{folder_name}"

    try:
        match project_type.get():
            case "basic":
                if is_use_folder_name_as_main_py_filename:
                    folder_name = folder_name.replace("-", "_").replace(" ", "_")
                    main_py_script_name = f"{folder_name}.py"
                else:
                    main_py_script_name = "main.py"
                cmd = f"{PWD}/resources/{init_scripts['basic']} -n {main_py_script_name} -f {folder_path} -venv {conda_env}"
            case "machine learning":
                cmd = f"{PWD}/resources/{init_scripts['machine learning']} -f {folder_path} -venv {conda_env}"

        subprocess.run(
            cmd,
            shell=True,
            check=True,
        )

        root.destroy()
        messagebox.showinfo("Success", "Python project folder successfully created!")
        subprocess.Popen(["code", folder_path])

    except subprocess.CalledProcessError:
        error_label.config(
            text="Error creating project. Please check your input and try again."
        )


if __name__ == "__main__":
    system_compatability_check()
    PWD = os.path.dirname(__file__)

    init_scripts = {
        "basic": "basic_project_init.sh",
        "machine learning": "ml_project_init.sh",
    }

    # Create the root Tkinter window
    root = Tk()
    root.title("Create Project")

    # Configure window size
    width = 465
    height = 470
    root.geometry(
        f"{width}x{height}+{(root.winfo_screenwidth() - width)//2}+{(root.winfo_screenheight()-height)//2}"
    )

    # Create the folder directory label and entry
    folder_dir_label = Label(root, text="Folder Directory:")
    folder_dir_label.grid(row=0, column=0)

    folder_dir_entry = Entry(root)
    folder_dir_entry.grid(row=0, column=1)

    browse_button = Button(root, text="Browse", command=browse_folder)
    browse_button.grid(row=0, column=2)

    # Create the folder name label and entry
    folder_name_label = Label(root, text="Folder Name:")
    folder_name_label.grid(row=1, column=0)

    folder_name_entry = Entry(root)
    folder_name_entry.grid(row=1, column=1)

    # Create the Conda environment label and listbox
    conda_env_label = Label(root, text="Conda Environment:")
    conda_env_label.grid(row=2, column=0)

    conda_env_listbox = Listbox(root)
    conda_env_listbox.grid(row=2, column=1)

    # Get a list of available Conda environments
    output = subprocess.check_output(["conda", "info", "--envs"]).decode("utf-8")
    env_lines = output.split("\n")[2:]
    conda_envs = [line.split()[0] for line in env_lines if line.strip()]
    for env in conda_envs:
        if env != "base":  # skip base venv as it has different file path
            conda_env_listbox.insert(END, env)

    # Create a drop-down for project type
    project_type_label = Label(root, text="Project Type:")
    project_type_label.grid(row=3, column=0)

    project_type = StringVar()
    project_type_dropdown = OptionMenu(root, project_type, *init_scripts.keys())
    project_type.set("basic")
    project_type_dropdown.grid(row=3, column=1)

    # Create a checkbox for choosing between main.py as or machinized folder name as the main py file name
    is_use_folder_name_as_main_py_filename = tk.BooleanVar()
    is_use_folder_name_as_main_py_filename_checkbox = tk.Checkbutton(
        root, text="Folder name as main script name"
    )
    is_use_folder_name_as_main_py_filename_checkbox.select()
    is_use_folder_name_as_main_py_filename_checkbox.grid(row=4, column=0, columnspan=2)

    # Create the error and success labels
    error_label = Label(root, fg="red")
    error_label.grid(row=5, column=0, columnspan=2)

    # Create the confirm button
    confirm_button = Button(root, text="Create Project", command=create_project)
    confirm_button.grid(row=6, column=0)

    for i in root.winfo_children():
        i.grid_configure(padx=10, pady=10, sticky=W)
    # Start the Tkinter event loop
    root.mainloop()
