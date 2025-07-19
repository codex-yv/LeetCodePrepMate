from tkinter import *
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from utils import searchById, searchByCompany

all_data_by_id = searchById.getDatabyId()
all_company = searchByCompany.getDataByCompany()

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, width = 300, bg = "white")
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack()


        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def delete_all_labels(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def remove_scrollable_frame(self):
        self.place_forget()


def label_clicked(event):
    widget = event.widget

    # Traverse up until we find the CTkLabel
    while widget is not None and not isinstance(widget, ctk.CTkLabel):
        widget = widget.master

    if widget is not None and isinstance(widget, ctk.CTkLabel):
        search_entry.delete(0, END)
        search_entry.insert(0, widget.cget("text"))
        scroll_frame.remove_scrollable_frame()
    

def dropDown(words):
    scroll_frame.place(x = 520, y = 105)

    for word in words:
        label = ctk.CTkLabel(scroll_frame.scrollable_frame, text=word, anchor="w", padx=10, fg_color="white",
                            width=290)
        label.pack(fill="x", pady=2, padx = 2)
        label.bind("<Button-1>", label_clicked)

char_list = []
comp_name_glo = []
def on_enter_search(event):
    global all_data_by_id, all_company, comp_name_glo
    if cb_for_id.get():
        entry_val = search_entry.get()
        FindClass = searchById.FindDataByID()
        r_val = FindClass.findDatabyId(k=entry_val, s=all_data_by_id)

        if r_val not in [101, 404]:
            q_name.configure(text = FindClass.question)
            q_type_val.configure(text = FindClass.difficulty)
            q_accept_val.configure(text = FindClass.acceptance)
            ttl_companies.configure(text = f"Total Companies:{FindClass.total}")
            q_link.configure(text = FindClass.link)

            clear_show_tree_for_id()
            show_tree_for_id(FindClass.companies)
        elif r_val == 101:
            messagebox.showerror("No Input", "First enter the question number!")
        else:
            messagebox.showinfo("Not found", "Question number not found!")
    else:
        comp_name = search_entry.get()
        comp_name_glo.insert(0, comp_name)
        company = searchByCompany.FindDataByCompany()
        find_comp = company.findDataByCompany(all_company, cname=comp_name)
        if find_comp not in [101, 404]:
            company_name.configure(text = comp_name)
            easy_text.configure(text = f"Easy   {str(company.easy)}")
            medium_text.configure(text = f"Medium   {str(company.medium)}")
            hard_text.configure(text =  f"Hard   {str(company.hard)}")
            total_value.configure(text = f"{str(company.totalq)}")

            clear_show_tree_for_comp()
            show_tree_for_comp(data = company.data_ldict)



company = searchByCompany.FindDataByCompany()
def on_keypress(event):
    if cb_for_comp.get():
        scroll_frame.delete_all_labels()
        global char_list, all_company
        if event.char and event.keysym not in  ["space", "BackSpace"] :
            char_list.append(event.char)
            drop_down_data = company.dropDownList(all_company, char_list)
            dropDown(drop_down_data)
        elif event.char and event.keysym in ["space"]:
            char_list.append("_")
            drop_down_data = company.dropDownList(all_company, char_list)
            dropDown(drop_down_data)
        elif event.char and event.keysym in ["BackSpace"]:
            try:
                char_list.pop()
                drop_down_data = company.dropDownList(all_company, char_list)
                dropDown(drop_down_data)
            except IndexError:
                drop_down_data = company.dropDownList(all_company, cname=[])
                dropDown(drop_down_data)
    else:
        pass

def on_cb_for_id_toggle():
    if cb_for_id.get():
        tree_for_comp.pack_forget()
        vsb2.pack_forget()
        infolabel.pack(padx = 140, pady = 120)
        if search_entry.get():
            search_entry.delete(0, END)
        
        custom_btn_frame.place_forget()
        cb_for_comp.deselect()
        search_entry.configure(placeholder_text="Search Question Number")
        company_info_frame.pack_forget()
        ques_info_frame.pack(fill=X, expand=True, padx=10, pady=(5, 10))
    else:
        # Prevent unchecking if the other isn't selected
        if not cb_for_comp.get():
            cb_for_id.select()  # Re-check it

        

def on_cb_for_comp_toggle():
    if cb_for_comp.get():
        tree_for_id.pack_forget()
        vsb.pack_forget()
        infolabel.pack(padx = 140, pady = 120)
        if search_entry.get():
            search_entry.delete(0, END)
        
        custom_btn_frame.place(x = 730, y = 315)
        cb_for_id.deselect()
        search_entry.configure(placeholder_text="Search Company Name")
        ques_info_frame.pack_forget()
        company_info_frame.pack(fill=X, expand=True, padx=10, pady=(0, 10))
    else:
        if not cb_for_id.get():
            cb_for_comp.select()  # Re-check it


def show_tree_for_id(data:list[dict])->None:
    infolabel.pack_forget()
    # Insert data into treeview
    for idx, item in enumerate(data, start=1):
        tree_for_id.insert("", "end", values=(idx, item['company_name'], round(item['frequency'], 6)))

    # Add Treeview to the window
    tree_for_id.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

def copy_to_clipboard(text):
    win.clipboard_clear()
    win.clipboard_append(text)
    messagebox.showinfo("Copied", f"Content copied to clipboard:\n{text}")

def on_question_row_select(event):
    selected_item = tree_for_comp.focus()
    if selected_item:
        values = tree_for_comp.item(selected_item, 'values')
        copy_to_clipboard(values[0])

def clear_show_tree_for_id():
    for row in tree_for_id.get_children():
        tree_for_id.delete(row)

def show_tree_for_comp(data):
    infolabel.pack_forget()
    for q in data:
        tree_for_comp.insert("", "end", values=(
            q['id'],
            q['question'],
            round(q['frequency'], 4),
            q['difficulty'].capitalize(),
            q['acceptance'],
        ))

    tree_for_comp.pack(side="left", fill="both", expand=True)
    vsb2.pack(side="right", fill="y")
    tree_for_comp.bind("<<TreeviewSelect>>", on_question_row_select)
def clear_show_tree_for_comp():
    for row in tree_for_comp.get_children():
        tree_for_comp.delete(row)

def sortingDataCollection():
    global comp_name_glo
    if comp_name_glo:
        company = searchByCompany.FindDataByCompany()
        find_comp = company.findDataByCompany(all_company, cname=comp_name_glo[0])
        sorted_infos = company.sortedDifficulty(company.data_ldict)
        if sorted_infos != 101:
            return company
        else:
            messagebox.showerror("Error", "Some internal error occurred!")
    else:
        messagebox.showinfo("Empty data", "Please give company name!")

def sort_hard():
    funcCompnay = sortingDataCollection()
    clear_show_tree_for_comp()
    show_tree_for_comp(funcCompnay.only_hard)
    
def sort_medium():
    funcCompnay = sortingDataCollection()
    clear_show_tree_for_comp()
    show_tree_for_comp(funcCompnay.only_medium)

def sort_easy():
    funcCompnay = sortingDataCollection()
    clear_show_tree_for_comp()
    show_tree_for_comp(funcCompnay.only_easy)

def reset_all():
    funcCompnay = sortingDataCollection()
    clear_show_tree_for_comp()
    show_tree_for_comp(funcCompnay.data_ldict)

def on_question_row_select(event):
    selected_item = tree_for_comp.focus()
    if selected_item:
        values = tree_for_comp.item(selected_item, 'values')
        funcCompany = sortingDataCollection()
        for idd in funcCompany.data_ldict:
            if idd["id"] == int(values[0]):
                copy_to_clipboard(idd["link"])
                break

win = Tk()

win.title("LeetCodePrepMate-Solve the right questions for your dream companies.")
win.geometry("900x600")

main_frame = Frame(win, bg="#fbfcfc")
main_frame.propagate(False)
main_frame.pack(fill='both', expand=True)

main_canvas=Canvas(main_frame,bg='white',bd=0,highlightthickness=0, relief='ridge')
main_canvas.propagate(False)
main_canvas.pack(fill='both', expand=True)


cwd = os.getcwd()
imagepath1=os.path.join(cwd, "Assets", "mainImg3.png") #cwd+"\\Assets\\UIUX\\passwordss.png"
openphoto1=Image.open(imagepath1).resize((900,600))
bgimage1=ImageTk.PhotoImage(openphoto1)
main_canvas.create_image(450,300, image=bgimage1)

dashboard_frame = ctk.CTkFrame(main_canvas, bg_color="white", fg_color="white", height=250, width=400, border_width=1, border_color="black")
dashboard_frame.propagate(False)
dashboard_frame.place(x = 20, y = 50)


total_link_visited = ctk.CTkLabel(dashboard_frame, text="Total Link Visited:", font=("poppins", 18, 'bold'), fg_color="white", bg_color="White",
                                  text_color="Blue", justify = "left")

total_link_visited.pack(anchor = 'nw', padx = 20, pady = (20, 10))

total_companies_searched = ctk.CTkLabel(dashboard_frame, text="Total Companies Searched:", font=("poppins", 18, 'bold'), fg_color="white", bg_color="White",
                                  text_color="Blue", justify = "left")

total_companies_searched.pack(anchor = 'nw', padx = 20, pady = (10, 10))

total_questions_searched = ctk.CTkLabel(dashboard_frame, text="Total Questions Searched:", font=("poppins", 18, 'bold'), fg_color="white", bg_color="White",
                                  text_color="Blue", justify = "left")

total_questions_searched.pack(anchor = 'nw', padx = 20, pady = (10, 20))



info_frame = ctk.CTkFrame(main_canvas, bg_color="white", fg_color="white", width=420, height=250, border_width=0, border_color="black")
info_frame.propagate(False)
info_frame.place(x=460, y=50)

# Search Entry at the top
search_entry = ctk.CTkEntry(info_frame, font=("poppins", 15), fg_color="white", bg_color="white", border_width=1, border_color="black",
                            placeholder_text="Search Question Number", height=40, width=300, corner_radius=20)
search_entry.pack(side='top', anchor='n', pady=(10, 5))

search_entry.bind("<Return>", on_enter_search)
search_entry.bind("<KeyPress>", on_keypress)

scroll_frame = ScrollableFrame(win)


# Frame to hold checkboxes side by side
checkbox_frame = ctk.CTkFrame(info_frame, fg_color="white")
checkbox_frame.pack(side='top', pady=(0, 5))

cb_for_id = ctk.CTkCheckBox(checkbox_frame, text="Question Number", font=("poppins", 12, 'bold'), fg_color="white", bg_color="white",
                            text_color="black", checkbox_height=20, checkbox_width=20, checkmark_color="green", command=on_cb_for_id_toggle)
cb_for_id.pack(side='left', padx=(0, 10))
cb_for_id.select()

cb_for_comp = ctk.CTkCheckBox(checkbox_frame, text="Company Name", font=("poppins", 12, 'bold'), fg_color="white", bg_color="white",
                              text_color="black", checkbox_height=20, checkbox_width=20, checkmark_color="green", command=on_cb_for_comp_toggle)
cb_for_comp.pack(side='left')

# Question info frame at the bottom
ques_info_frame = ctk.CTkFrame(info_frame, fg_color="white", height=150, corner_radius=20, border_width=1, border_color="black")
ques_info_frame.propagate(False)
ques_info_frame.pack(fill=X, expand=True, padx=10, pady=(5, 10))

# ROW 1 - Problem
q_name = ctk.CTkLabel(ques_info_frame, text="Problem:", font=("poppins", 14, 'bold'), fg_color="white", bg_color="white", text_color="Black")
q_name.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10, 2))

# ROW 2 - Difficulty | Difficulty Value | Acceptance | Acceptance Value
q_type = ctk.CTkLabel(ques_info_frame, text="Difficulty:", font=("poppins", 12), fg_color="white", bg_color="white", text_color="Black")
q_type.grid(row=1, column=0, sticky="w", padx=10)

q_type_val = ctk.CTkLabel(ques_info_frame, text="Medium", font=("poppins", 12, 'bold'), fg_color="white", bg_color="white", text_color="Black")
q_type_val.grid(row=1, column=1, sticky="w", padx=5)

q_accept = ctk.CTkLabel(ques_info_frame, text="Acceptance:", font=("poppins", 12), fg_color="white", bg_color="white", text_color="Black")
q_accept.grid(row=1, column=2, sticky="w", padx=10)

q_accept_val = ctk.CTkLabel(ques_info_frame, text="65%", font=("poppins", 12, 'bold'), fg_color="white", bg_color="white", text_color="Black")
q_accept_val.grid(row=1, column=3, sticky="w", padx=5)

# ROW 3 - Total Companies
ttl_companies = ctk.CTkLabel(ques_info_frame, text="Total Companies: 12", font=("poppins", 12), fg_color="white", bg_color="white", text_color="Black")
ttl_companies.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 2))

# ROW 4 - Question Link
q_link = ctk.CTkLabel(ques_info_frame, text="Question Link: https://...", font=("poppins", 12), fg_color="white", bg_color="white", text_color="Black")
q_link.grid(row=3, column=0, columnspan=4, sticky="w", padx=10, pady=(5, 10))

# Company Info Frame
company_info_frame = ctk.CTkFrame(info_frame, fg_color="white", height=150, corner_radius=20, border_width=1, border_color="black")
company_info_frame.propagate(False)

# ROW 1 - Company Name
company_name = ctk.CTkLabel(company_info_frame, text="Company:", font=("poppins", 14, 'bold'),
                            fg_color="white", bg_color="white", text_color="Black")
company_name.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10, 2))
# ROW 2 - Easy | Medium | Hard (Optimized spacing)
easy_text = ctk.CTkLabel(company_info_frame, text="Easy: 12", font=("poppins", 12),
                         fg_color="white", bg_color="white", text_color="Black")
easy_text.grid(row=1, column=0, sticky="w", padx=(10, 30))

medium_text = ctk.CTkLabel(company_info_frame, text="Medium: 18", font=("poppins", 12),
                           fg_color="white", bg_color="white", text_color="Black")
medium_text.grid(row=1, column=1, sticky="w", padx=(40, 30))

hard_text = ctk.CTkLabel(company_info_frame, text="Hard: 6", font=("poppins", 12),
                         fg_color="white", bg_color="white", text_color="Black")
hard_text.grid(row=1, column=2, sticky="w", padx=(40, 30))


# ROW 3 - Total Questions
total_label = ctk.CTkLabel(company_info_frame, text="Total Questions:", font=("poppins", 12),
                           fg_color="white", bg_color="white", text_color="Black")
total_label.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))

total_value = ctk.CTkLabel(company_info_frame, text="36", font=("poppins", 12, 'bold'),
                           fg_color="white", bg_color="white", text_color="Black")
total_value.grid(row=2, column=1, sticky="w", padx=5, pady=(5, 10))

dataTreeFrame = ctk.CTkFrame(main_canvas, bg_color="white", fg_color="white", width=700, height=270,
                                border_width=1, border_color='black')
dataTreeFrame.place(x = 20, y = 315)

vsb = ttk.Scrollbar(dataTreeFrame, orient="vertical")

tree_for_id = ttk.Treeview(dataTreeFrame, columns=("SLNO", "Companies", "Frequency"), show="headings",yscrollcommand=vsb.set)
vsb.config(command=tree_for_id.yview)


# Define columns
tree_for_id.heading("SLNO", text="SLNO")
tree_for_id.heading("Companies", text="Companies")
tree_for_id.heading("Frequency", text="Frequency")

# Set column widths
tree_for_id.column("SLNO", width=50, anchor="center")
tree_for_id.column("Companies", width=200, anchor="w")
tree_for_id.column("Frequency", width=150, anchor="center")



vsb2 = ttk.Scrollbar(dataTreeFrame, orient="vertical")
tree_for_comp = ttk.Treeview(
    dataTreeFrame,
    columns=("ID", "Question", "Frequency", "Difficulty", "Acceptance"),
    show="headings",
    yscrollcommand=vsb2.set
)
vsb2.config(command=tree_for_comp.yview)

# Define headings
tree_for_comp.heading("ID", text="ID")
tree_for_comp.heading("Question", text="Question")
tree_for_comp.heading("Frequency", text="Frequency")
tree_for_comp.heading("Difficulty", text="Difficulty")
tree_for_comp.heading("Acceptance", text="Acceptance")


# Set column properties
tree_for_comp.column("ID", width=50, anchor="center")
tree_for_comp.column("Question", width=180, anchor="w")
tree_for_comp.column("Frequency", width=100, anchor="center")
tree_for_comp.column("Difficulty", width=100, anchor="center")
tree_for_comp.column("Acceptance", width=100, anchor="center")



infolabel = ctk.CTkLabel(dataTreeFrame, text="To see data search companies or Question Number",
                         font=("poppins", 18), fg_color="white", bg_color="white", text_color="black")
infolabel.pack(padx = 140, pady = 120)


custom_btn_frame = ctk.CTkFrame(main_canvas, fg_color="white", height=270, width=160)
custom_btn_frame.propagate(False)

sort_label = ctk.CTkLabel(custom_btn_frame, text="Sort by:", font=("poppins", 18, 'bold'), fg_color="white",
                          bg_color="white", text_color="Black")
sort_label.pack(pady = (20, 20))

hard_btn = ctk.CTkButton(custom_btn_frame, text="Hard", font=("poppins", 15, 'bold'), fg_color="red", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2', command = sort_hard)
hard_btn.pack(pady = (0, 10))


medium_btn = ctk.CTkButton(custom_btn_frame, text="Medium", font=("poppins", 15, 'bold'), fg_color="yellow", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2', command = sort_medium)
medium_btn.pack(pady = (0, 10))

easy_btn = ctk.CTkButton(custom_btn_frame, text="Easy", font=("poppins", 15, 'bold'), fg_color="Green", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2', command = sort_easy)
easy_btn.pack(pady = (0, 10))

all_btn = ctk.CTkButton(custom_btn_frame, text="Reset", font=("poppins", 15, 'bold'), fg_color="black", bg_color="white",
                         text_color="white", corner_radius=20, cursor = 'hand2', command=reset_all)
all_btn.pack(pady = (0, 10))

win.mainloop()