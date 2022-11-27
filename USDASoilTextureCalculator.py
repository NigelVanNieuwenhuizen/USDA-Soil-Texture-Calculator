import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import Progressbar
import os, textwrap, time, sys

# to build application...
# cd to directory, then: pyinstaller --onefile --noconsole USDASoilTextureCalculator.py

class SoilTextureCalculator():
    """An application to calculate USDA soil texture from sand, silt, and clay components."""
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(False,False)
        self.window.title("USDA Soil Texture Calculator")
        self.in_file = tk.StringVar()
        self.in_file_data = []
        self.input_delimiter_str = tk.StringVar(value = '","')
        self.sand_col = []
        self.silt_col = []
        self.clay_col = []
        self.out_col_name = tk.StringVar(value="Texture")
        self.output_formats = [".csv",".txt"]
        self.output_delimiter_str = tk.StringVar(value = '","')
    
    def launch(self):
        """Open the Soil Texture Calculator GUI"""
        pad=5
        self.station_labelframe = tk.LabelFrame(self.window,text="Select File")
        self.station_labelframe.grid(row=0,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.file_select_frame = tk.Frame(self.station_labelframe)
        self.file_select_frame.grid(row=0,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.file_select_label = tk.Label(self.file_select_frame,text="File (.csv or .txt):     ")
        self.file_select_label.grid(row = 0, column = 0,padx=pad,pady=pad)
        self.file_select_entry = ttk.Entry(self.file_select_frame,textvariable=self.in_file,justify="right",width=49)
        self.file_select_entry.grid(row=0,column=1,padx=pad,pady=pad)
        self.choose_file_button = ttk.Button(self.file_select_frame,text="...",width=4,command=self.choose_file)
        self.choose_file_button.grid(row=0,column=2,padx=pad+4,pady=pad)
        self.delim_header_frame = tk.Frame(self.station_labelframe)
        self.delim_header_frame.grid(row=1,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.input_delim_label = tk.Label(self.delim_header_frame,text="Input Delimiter:      ")
        self.input_delim_label.grid(row=0,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.input_delim_entry = ttk.Entry(self.delim_header_frame,textvariable=self.input_delimiter_str,justify="right",width=10)
        self.input_delim_entry.grid(row=0,column=1,padx=pad,pady=pad,sticky=tk.W)
        self.input_delim_space = tk.Label(self.delim_header_frame,text="")
        self.input_delim_space.grid(row=0,column=2,padx=pad*6+1,pady=pad,sticky=tk.W)
        self.sand_select_frame = tk.Frame(self.station_labelframe)
        self.sand_select_frame.grid(row=2,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.sand_select_label = tk.Label(self.sand_select_frame,text="Sand Field:              ")
        self.sand_select_label.grid(row = 0, column = 0,padx=pad,pady=pad,sticky=tk.W)
        self.sand_select_combo = ttk.Combobox(self.sand_select_frame,state="readonly",width = 46)
        self.sand_select_combo.grid(row=0,column=1,padx=pad,pady=pad,sticky=tk.W)
        self.silt_select_frame = tk.Frame(self.station_labelframe)
        self.silt_select_frame.grid(row=3,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.silt_select_label = tk.Label(self.silt_select_frame,text="Silt Field:                   ")
        self.silt_select_label.grid(row = 0, column = 0,padx=pad,pady=pad,sticky=tk.W)
        self.silt_select_combo = ttk.Combobox(self.silt_select_frame,state="readonly",width = 46)
        self.silt_select_combo.grid(row=0,column=1,padx=0,pady=pad,sticky=tk.W)
        self.clay_select_frame = tk.Frame(self.station_labelframe)
        self.clay_select_frame.grid(row=4,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.clay_select_label = tk.Label(self.clay_select_frame,text="Clay Field:                ")
        self.clay_select_label.grid(row = 0, column = 0,padx=pad,pady=pad,sticky=tk.W)
        self.clay_select_combo = ttk.Combobox(self.clay_select_frame,state="readonly",width = 46)
        self.clay_select_combo.grid(row=0,column=1,padx=2,pady=pad,sticky=tk.W)

        self.settings_labelframe = tk.LabelFrame(self.window,text="Settings")
        self.settings_labelframe.grid(row=1,column=0,padx=pad,pady=pad,sticky=tk.W) 
        self.output_column_frame = tk.Frame(self.settings_labelframe)
        self.output_column_frame.grid(row = 0, column = 0, padx = pad, pady = pad, sticky = tk.W)
        self.output_column_label = tk.Label(self.output_column_frame,text = "Output Column Name: ")
        self.output_column_label.grid(row=0,column=0,padx=pad,pady=pad,sticky = tk.W)
        self.output_column_entry = ttk.Entry(self.output_column_frame,textvariable=self.out_col_name,justify="right",width=10)
        self.output_column_entry.grid(row=0,column=1,padx=pad,pady=pad,sticky=tk.W)
        self.output_format_frame = tk.Frame(self.settings_labelframe)
        self.output_format_frame.grid(row=2,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.output_format_file = tk.Label(self.output_format_frame,text="Output Format:              ")
        self.output_format_file.grid(row = 0, column = 0,padx=pad,pady=pad)
        self.output_format_combo = ttk.Combobox(self.output_format_frame,state="readonly",values=self.output_formats,width = 7,justify="left")
        self.output_format_combo.grid(row=0,column=1,padx=pad+2,pady=pad,sticky=tk.W)
        self.output_format_combo.current(0)
        self.output_space = tk.Label(self.output_format_frame,text="")
        self.output_space.grid(row=0,column=2,padx=pad*7,pady=pad)
        self.output_delimiter_label = tk.Label(self.output_format_frame,text = "Output Delimiter:")
        self.output_delimiter_label.grid(row=0,column=3,padx=pad,pady=pad)
        self.output_delimiter_entry = ttk.Entry(self.output_format_frame,textvariable=self.output_delimiter_str,justify="right",width=10)
        self.output_delimiter_entry.grid(row=0,column=4,padx=pad,pady=pad,sticky=tk.W)
        
        self.command_labelframe = tk.LabelFrame(self.window,text="Commands")
        self.command_labelframe.grid(row=2,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.button_frame = tk.Frame(self.command_labelframe)
        self.button_frame.grid(row=1,column=0,padx=pad,pady=pad,sticky=tk.W)
        self.help_button = ttk.Button(self.button_frame,text="Help",command=self.open_help)
        self.help_button.grid(row=0,column=0,padx=2,pady=pad)
        self.open_file_button = ttk.Button(self.button_frame,text="Open File",command=self.open_file)
        self.open_file_button.grid(row=0,column=2,padx=2,pady=pad)
        self.command_space = tk.Label(self.button_frame,text="")
        self.command_space.grid(row=0,column=3,padx=pad*11+2,pady=pad)
        self.run_button = ttk.Button(self.button_frame,text="Run",command=self.run,width=13)
        self.run_button.grid(row=0,column=4,padx=2,pady=pad)
        self.progbar = Progressbar(self.button_frame, length = 100, mode = 'determinate')
        self.progbar.grid(row = 0, column = 5, padx = 4, pady = pad, sticky = tk.E)

        # resize and reposition window
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws/2) - 251)
        y = int((hs/2) - 211)
        self.window.geometry(f"502x422+{x}+{y}")

        self.window.mainloop()
    
    def choose_file(self):
        """Choose a file to load fields."""
        filename = filedialog.askopenfilename(parent = self.window,title = "Select file", filetypes = (("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*"))) #open an existing file
        if len(filename) > 0: #if they didn't press cancel
            self.load_file(filename)
    
    def load_file(self,filename):
        """Load the file and parse the data."""
        try:
            file = open(filename, 'r')
            self.in_file_data = [row.strip().split(self.input_delimiter_str.get()[1:-1]) for row in file.readlines()]
            file.close()
            headers = self.in_file_data[0]
            self.in_file.set(filename)
            self.sand_select_combo.config(values=headers)
            self.sand_select_combo.current(0)
            self.silt_select_combo.config(values=headers)
            self.silt_select_combo.current(0)
            self.clay_select_combo.config(values=headers)
            self.clay_select_combo.current(0)
        except:
            messagebox.showwarning("USDA Soil Texture Calculator","An unknown error occured while trying to load the file.")
    
    def open_help(self):
        """Attempt to open the help file PDF"""
        path = os.path.dirname(os.path.realpath(__file__))
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        try:
            os.startfile(path+os.sep+"USDASoilTextureCalculatorManual.pdf")
        except:
            messagebox.showwarning("USDA Soil Texture Calculator","Cannot find the USDA Soil Texture Calculator Manual. It should be located in the same directory as the application. If not, it may have been moved or deleted.")

    def open_file(self):
        """Open the file."""
        if self.in_file.get() != "":
            try:
                os.startfile(self.in_file.get())
            except:
                messagebox.showwarning("USDA Soil Texture Calculator","An unknown error occurred while trying to open the file.")
        else:
            messagebox.showwarning("USDA Soil Texture Calculator","You have not specified a file.")
        
    def return_column(self,column):
        """Return the values of a column from the input file as a list."""
        headers = self.in_file_data[0]
        column = headers.index(column)

        col_vals = []
        append = col_vals.append
        line_count = 1
        for _ in range(len(self.in_file_data)):
            data = self.in_file_data[line_count]
            val = data[column]
            if (val.startswith("'") or val.startswith('"')) and (val.endswith("'") or val.endswith('"')):
                val = val[1:-1]
            try:
                append(float(data[column]))
            except:
                try:
                    append(int(data[column]))
                except:
                    append(data[column])
            line_count += 1
            if line_count == len(self.in_file_data):
                break
        return col_vals

    def append_output_column(self,data,header):
        """Add a column of data to the output file."""
        v_vals = data[:]
        if self.in_file_data: #if there's already data
            v_vals.insert(0,header)
            line_count = 0
            output = []
            append = output.append
            for row in range(len(self.in_file_data)):
                data = self.in_file_data[row]
                d_append=data.append
                d_append(str(v_vals[row]))
                data = [str(val) for val in data]
                append(data)
                line_count += 1
                if line_count == len(self.in_file_data):
                    break
            self.in_file_data = output
        else:
            append = self.in_file_data.append
            v_vals.insert(0,header)
            for val in v_vals:
                append([str(val)])

    def write_data(self,file):
        """Attempt to write the output data to a file."""
        try:
            self.run_button.config(text="Writing data...")
            ld = len(self.in_file_data)
            file = open(file, 'w') 
            curr_percent = 0
            for i in range(ld):
                row = self.in_file_data[i]
                row = [str(val) for val in row]
                row = self.output_delimiter_str.get()[1:-1].join(row) + "\n"
                file.writelines(f"{row}") 
                percent = int((i/ld) * 100)
                if percent > curr_percent:
                    curr_percent = percent
                    self.progbar['value'] = curr_percent
                    self.progbar.update_idletasks()
                self.window.update_idletasks()
            file.close()
        except:
            pass

    def run(self):
        """Attempt to calculature soil textures."""
         # first perform a check for incorrect parameters
        self.window.update_idletasks()
        can_run = True
        
        if not self.in_file_data:
            can_run = False
            messagebox.showwarning("USDA Soil Texture Calculator","Please choose a file to load soil component fields.")
        else:
            self.sand_col = self.return_column(self.sand_select_combo.get())
            self.silt_col = self.return_column(self.silt_select_combo.get())
            self.clay_col = self.return_column(self.clay_select_combo.get())
        if self.out_col_name.get() == "":
            can_run = False
            messagebox.showwarning("USDA Soil Texture Calculator","Please specify an output texture column name.")
        if not self.output_delimiter_str.get().startswith('"') or not self.output_delimiter_str.get().endswith('"'):
            can_run = False
            messagebox.showwarning("USDA Soil Texture Calculator","Please enclose the output delimiter in double quotations.")

            # if all parameters appear correct, run the app
        if can_run:
            start = time.perf_counter()
            self.run_button.config(text="Calculating...")
            curr_percent = 0
            num_rows = len(self.sand_col)
            count = 0
            errors = 0
            out_vals = []
            for s in range(num_rows):
                # try:
                sand = self.sand_col[s]
                silt = self.silt_col[s]
                clay = self.clay_col[s]
                texture = ""

                if sand <= 45 and silt <= 40 and clay >= 40:
                    texture = "Clay"
                elif sand <= 65 and sand >= 45 and silt <= 20 and clay >= 35 and clay <= 55:
                    texture = "Sandy Clay"
                elif sand <= 20 and silt >= 40 and silt <= 60 and clay >= 40 and clay <= 60:
                    texture = "Silty Clay"
                elif sand >= 45 and sand <= 80 and silt <= 28 and clay >= 20 and clay <= 35:
                    texture = "Sandy Clay Loam"
                elif sand >= 20 and sand <= 45 and silt >= 15 and silt <= 53 and clay >= 27 and clay <= 40:
                    texture = "Clay Loam"
                elif sand <= 20 and silt >= 40 and silt <= 73 and clay >= 27 and clay <= 40:
                    texture = "Silty Clay Loam"
                elif sand >= 43 and sand <= 85 and silt <= 50 and clay <= 20:
                    texture = "Sandy Loam"
                elif sand >= 23 and sand <= 52 and silt >= 28 and silt <= 50 and clay >= 7 and clay <= 27:
                    texture = "Loam"
                elif sand <= 50 and silt >= 50 and silt <= 88 and clay <= 27:
                    texture = "Silt Loam"
                elif sand <= 20 and silt >= 80 and clay <= 12:
                    texture = "Silt"
                elif sand >= 70 and sand <= 90 and silt <= 30 and clay <= 15:
                    texture = "Loamy Sand"
                elif sand >= 85 and silt <= 15 and clay <= 10:
                    texture = "Sand"
                else:
                    texture = "Not Available"
                out_vals.append(texture)
                # except:
                    # errors += 1
                    # out_vals.append("")
                count += 1
                # update progress and window
                count += 1
                percent = int((count/num_rows) * 100)
                if percent > curr_percent:
                    curr_percent = percent
                    self.progbar['value'] = curr_percent
                    self.progbar.update_idletasks()
                self.window.update_idletasks()
            
            # write the data
            self.progbar['value'] = 0
            self.append_output_column(out_vals,self.out_col_name.get())
            filename = self.in_file.get()[:-4] + self.output_format_combo.get()
            # filename = filename[:-4] + self.output_format_combo.get()
            self.write_data(filename)

            # calculate time
            end = time.perf_counter()
            dur = end-start
            units = "seconds"
            if dur/3600 > 1:
                dur /= 3600
                units = "hours"
            elif dur/60 > 1:
                dur /= 60
                units = "minutes"
            self.progbar['value'] = 0
            self.run_button.config(text="Run")
            message = f"""
            Calculation complete!


            Time to completion: {dur:.2f} {units}
            Successful calculations: {num_rows-errors} of {num_rows} rows
            Failed calculations (errors): {errors} row{'s' if errors != 1 else ''}"""
            messagebox.showinfo("USDA Soil Texture Calculator",textwrap.dedent(message).lstrip())


def main():
    app = SoilTextureCalculator()
    app.launch()

if __name__ == '__main__':
    main()