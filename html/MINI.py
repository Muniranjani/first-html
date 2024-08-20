from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteEntry 
import keyword
import re
from tkinter.filedialog import asksaveasfilename, askopenfilename 
import subprocess

file_path = ''

def get_words(event):
    text = editor.get("1.0", "end-1c")
    words = text.split()
    for i in words:
        if keyword.iskeyword(i):
            search_word = i
            pattern = r"\b" + re.escape(search_word) + r"\b"
            for match in re.finditer(pattern, editor.get("1.0", "end"), re.IGNORECASE):
                start_index = match.start()
                end_index = match.end()
                editor.tag_add("found", f"1.0+{start_index}c", f"1.0+{end_index}c")
    characters_to_recolor = [':', ',', '(', ')', '{', '}', '[', ']', ';']
    for char in characters_to_recolor:
        start_index = "1.0"
        while True:
            start_index = editor.search(char, start_index, stopindex="end", nocase=True, exact=False)
            if not start_index:
                break
            end_index = editor.index(f"{start_index}+1c")
            editor.tag_add("character", start_index, end_index)
            start_index = end_index

    double_quotes_pattern = r'"([^"]*)"'
    for match in re.finditer(double_quotes_pattern, editor.get("1.0", "end")):
        start_index = match.start(1)
        end_index = match.end(1)
        editor.tag_add("quoted_text", f"1.0+{start_index}c", f"1.0+{end_index}c")

    single_quotes_pattern = r"'([^']*)'"
    for match in re.finditer(single_quotes_pattern, editor.get("1.0", "end")):
        start_index = match.start(1)
        end_index = match.end(1)
        editor.tag_add("quoted_text", f"1.0+{start_index}c", f"1.0+{end_index}c")

    content = editor.get("1.0", "end")
    start_index = "1.0"
    while True:
        start_index = editor.search("#", start_index, stopindex="end", nocase=True, exact=False)
        if not start_index:
            break
        end_index = editor.search("\n", start_index, stopindex="end", exact=True)
        editor.tag_add("italic", start_index, end_index)
        start_index = end_index

    recolor_after_dot()

def equalsymbol(event):
    start_index = "1.0"
    while True:
        start_index = editor.search("=", start_index, stopindex="end", nocase=True, exact=True)
        if not start_index:
            break
        end_index = f"{start_index}+1c"
        editor.tag_add("found", start_index, end_index)
        start_index = end_index

def set_file_path(path):
    global file_path
    file_path = path

def open_file(event=1):
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
    compiler.title(path + ' New Python IDE')
    code1 = editor.get('1.0', END)
    if code1 == code:
        compiler.title(path + ' New Python IDE')
    else:
        compiler.title('*' + path + ' New Python IDE')
    get_words()

def save_as(event=1):
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
        compiler.title("Untitle")
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
    compiler.title(path + ' New Python IDE')

def update_line_numbers(event):
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")
    num_lines = editor.index("end-1c").split(".")[0]
    for i in range(1, int(num_lines) + 1):
        line_numbers.insert("end", f" {i}\n")
    line_numbers.config(state="disabled")

def recolor_after_dot(event=None):
    pattern = r"\.\s*([a-zA-Z0-9_]+)"
    text = editor.get("1.0", "end")
    matches = re.finditer(pattern, text)
    for match in matches:
        start_index = f"1.0+{match.start(1)}c"
        end_index = f"1.0+{match.end(1)}c"
        editor.tag_add("after_dot", start_index, end_index)

def run(event=1):
    c2 = Tk()
    c2.title("Output Window")
    code_output = Text(c2, height=10, bg="#292C34", fg="#CACACA", borderwidth=0,
                       font=('Droid Sans Mono', 18), highlightbackground="#2e3138")
    code_output.pack(fill="both", expand=True)
    if file_path == '':
        messagebox.showwarning("Warning", "File Not Saved")
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    if error != '':
        k = 1.0 + float(len(error) / 10)
        print(len(error))
        print(k)
        code_output.insert('1.0', error)
        code_output.tag_add("start", '1.0', str(k))
        code_output.tag_configure("start", foreground="red")

def on_scroll(*args):
    line_numbers.yview(*args)
    editor.yview(*args)

def exits(event=1):
    if file_path == '':
        ch = messagebox.askquestion("Warning", "Are you sure to quit")
        if ch == "yes":
            exit()
    u = keyword.kwlist
    print(u)

compiler = Tk()
compiler.title('Untitled New Python IDE')
#c1 = PhotoImage(file="logo.png")
#compiler.iconphoto(False, c1)

menu_bar = Menu(compiler)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file, accelerator="Ctrl+O")
compiler.bind('<Control-x>', exits)
compiler.bind('<Control-Shift-s>', save_as)

compiler.bind('<Control-s>', save_as)
compiler.bind('<Control-o>', open_file)
compiler.bind('<F5>', run)
file_menu.add_command(label='Save', command=save_as, accelerator="Ctrl+S")
file_menu.add_command(label='Save As', command=save_as, accelerator="Ctrl+Shift+S")
file_menu.add_command(label='Exit', command=exits, accelerator="Ctrl+Shift+S")
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run, accelerator="F5")
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

frame = Frame(compiler)
frame.pack(fill="both", expand=True)

ks = Scrollbar(frame)
ks.pack(side="right", fill="y")

line_numbers = Text(frame, width=4, bg="#23262b", fg="#919399", state="disabled",
                    font=('Droid Sans Mono', 12), borderwidth=0, highlightbackground="#3D4048",
                    yscrollcommand=ks.set)
line_numbers.pack(side="left", fill="y", expand=False)
line_numbers.tag_configure("S.no", justify="center")

editor = Text(frame, wrap="word", bg="#292C34", fg="#CACACA", borderwidth=0, undo=True, yscrollcommand=ks.set)
editor.configure(insertbackground='#CACACA', font=('Droid Sans Mono', 12))
editor.pack(side="left", fill="both", expand=True)

editor.bind("<space>", get_words)
editor.bind("<Tab>", get_words)
editor.bind("<Return>", get_words)
editor.bind("<Key>", equalsymbol)
editor.bind("<KeyRelease>", update_line_numbers)
editor.tag_configure("found", foreground="#C678DD")
editor.tag_configure("quoted_text", foreground="#8CB272")
editor.tag_configure("character", foreground="gold")
editor.tag_configure("after_dot", foreground="#5284AF")
editor.bind("<KeyPress>", recolor_after_dot)
ks.config(command=on_scroll)
editor.tag_configure("italic", font=('Droid Sans Mono', 12, "italic"), foreground="gray")

compiler.mainloop()
