from tkinter import *
from tkinter import ttk
import os, platform, pip, virtualenv
import shutil
from cffi.setuptools_ext import execfile

ALL_SCHEMAS_ENTRIES = []
class HyperManager:
    def __init__(self, master=None):
        self.master = master
        #self.master.geometry("500x300")
        self.master.resizable(width=False, height=False)
        self.default_font = ("Arial", "10")
        self.default_pady = 5
        self.default_width = 40
        self.current_rows_count = 0

        self.main_container = Frame(self.master, padx=40, pady=20)
        self.main_container.pack(side=LEFT)

        # ============== title container
        self.host_title = Label(self.main_container, text="Database Configuration", font=("Arial", "10", "bold"), pady=self.default_pady)
        self.host_title.grid(row=0, columnspan=3)

        # ============== database developer container
        self.database_devel_label = Label(self.main_container, text="Choose your database", pady=self.default_pady)
        self.database_devel_label.grid(row=1, column=0)
        self.database_devel_combo = ttk.Combobox(self.main_container, values=["postgres"])
        self.database_devel_combo.grid(row=1, column=1)
        
        # ============== IP container
        self.ip_label = Label(self.main_container, font=self.default_font, text="IP (leave blank to localhost)", pady=self.default_pady)
        self.ip_label.grid(row=2, column=0)
        self.ip_input = Entry(self.main_container, width=20)
        self.ip_input.grid(row=2, column=1)

        # ============== Port container
        self.port_label = Label(self.main_container, text="Port", font=self.default_font, pady=self.default_pady)
        self.port_label.grid(row=3, column=0)
        self.port_input = Entry(self.main_container, width=10)
        self.port_input.grid(row=3, column=1)

        # ============== database container
        self.database_name_port_label = Label(self.main_container, text="Database name", font=self.default_font, pady=self.default_pady)
        self.database_name_port_label.grid(row=4, column=0)
        self.database_name_input = Entry(self.main_container, width=10)
        self.database_name_input.grid(row=4, column=1)

        # ============== username container
        self.username_label = Label(self.main_container, text="Username", font=self.default_font, pady=self.default_pady)
        self.username_label.grid(row=5, column=0)
        self.username_input = Entry(self.main_container, width=10)
        self.username_input.grid(row=5, column=1)

        # ============== password container
        self.password_label = Label(self.main_container, text="Password", font=self.default_font, pady=self.default_pady)
        self.password_label.grid(row=6, column=0)
        self.password_input = Entry(self.main_container, show="*", width=10)
        self.password_input.grid(row=6, column=1)

        # ============== schemas container
        self.schemas_label = Label(self.main_container, text="Schemas", font=self.default_font)
        self.schemas_label.grid(row=7, column=0)
        self.schema_entry_input = Entry(self.main_container, width=10)
        self.schema_entry_input.grid(row=7, column=1)
        self.add_schemas_button = Button(self.main_container, text="+", command=self.add_entry_schema)
        self.add_schemas_button.grid(row=7, column=2)


        # ============== side container ==============
        self.side_container = Frame(self.master, padx=40, pady=20)
        self.side_container.pack(anchor="w")

        self.gen_environ_button = Button(self.side_container, text="Config Environment", command=self.config_env, width=20, pady=5)
        self.gen_environ_button.pack()

        self.project_name_label = Label(self.side_container, text="Django project name", font=self.default_font)
        self.project_name_label.pack()
        self.project_name_entry_input = Entry(self.side_container, width=10)
        self.project_name_entry_input.pack()
        self.app_name_label = Label(self.side_container, text="Django project name", font=self.default_font)
        self.app_name_label.pack()
        self.app_name_entry_input = Entry(self.side_container, width=10)
        self.app_name_entry_input.pack()
        self.gen_models_button = Button(self.side_container, text="Generate Models", state='disabled', command=self.generate_models, width=20, pady=5)
        self.gen_models_button.pack()
        self.gen_files_button = Button(self.side_container, text="Generate Files", state='disabled', command=self.generate_files, width=20, pady=5)
        self.gen_files_button.pack()

    def add_entry_schema(self):
        if self.current_rows_count == 0:
            self.current_rows_count = self.schema_entry_input.grid_info()['row']
        new_schema_entry = Entry(self.main_container, width=10)
        new_schema_entry.grid(row=self.current_rows_count + 1, column=1)
        self.current_rows_count += 1
        ALL_SCHEMAS_ENTRIES.append(new_schema_entry)

    def config_env(self):
        self.gen_environ_button.config(state='disabled')

        venv_dir = os.path.join(os.path.expanduser("~"), ".venv")
        #try:
        #    shutil.rmtree(venv_dir)
        #except OSError as e:
        #    print ("Error: %s - %s." % (e.filename, e.strerror))

        virtualenv.create_environment(venv_dir)
        exec(open(venv_dir + '\\Scripts\\activate_this.py').read(), {'__file__': venv_dir + '\\Scripts\\activate_this.py'})
        #exec(open('E:\\Users\\gabriel1.estagio\\.venv\\Scripts\\activate_this.py').read(), {'__file__': 'E:\\Users\\gabriel1.estagio\\.venv\\Scripts\\activate_this.py'})
        #os.system("pip install -r requirements.txt")
        os.system("pip install django")
        os.system("python setup.py install")

        self.gen_models_button.config(state='normal')

    def generate_models(self):
        self.project_name_entry_input.config(state='disabled')
        self.app_name_entry_input.config(state='disabled')
        self.gen_models_button.config(state='disabled')
        self.gen_files_button.config(state='normal')

    def generate_files(self):
        pass

root = Tk()
HyperManager(root)
root.mainloop()
