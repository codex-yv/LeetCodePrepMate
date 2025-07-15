from tkinter import *
from PIL import Image, ImageTk
import os
import customtkinter as ctk
from tkinter import ttk
from utils import helper

all_data_by_id = helper.getDatabyId()

def on_enter_search(event):
    global all_data_by_id
    entry_val = search_entry.get()
    FindClass = helper.FindDataByID()
    r_val = FindClass.findDatabyId(k=entry_val, s=all_data_by_id)

    if r_val is None:
        q_name.configure(text = FindClass.question)
        q_type_val.configure(text = FindClass.difficulty)
        q_accept_val.configure(text = FindClass.acceptance)
        ttl_companies.configure(text = f"Total Companies:{FindClass.total}")
        q_link.configure(text = FindClass.link)


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
info_frame.place(x = 460, y = 50)

search_entry = ctk.CTkEntry(info_frame, font=("poppins", 15), fg_color="white", bg_color="white", border_width=1, border_color="black",
                            placeholder_text="Search Question Number", height=40, width=300, corner_radius=20)
search_entry.pack(side = 'top', anchor = 'n', pady = 20)

search_entry.bind("<Return>", on_enter_search)

ques_info_frame = ctk.CTkFrame(info_frame, fg_color="white", height=150, corner_radius=20, border_width=1, border_color="black")
ques_info_frame.propagate(False)
ques_info_frame.pack(fill=X, expand=True, padx=10, pady=10)

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

dashboard_frame3 = ctk.CTkFrame(main_canvas, bg_color="white", fg_color="white", width=700, height=270,
                                border_width=1, border_color='black')
dashboard_frame3.place(x = 20, y = 315)

# companies = ["Apple", "Google", "Microsoft", "Amazon", "Meta"]


# # Define Treeview
# columns = ("SLNO", "Companies")
# tree = ttk.Treeview(dashboard_frame3, columns=columns, show="headings")

# # Define headings
# tree.heading("SLNO", text="SLNO")
# tree.heading("Companies", text="Companies")

# # Define column widths
# tree.column("SLNO", width=50, anchor=CENTER)
# tree.column("Companies", width=200, anchor=W)

# # Insert companies with auto SLNO
# for idx, name in enumerate(companies, start=1):
#     tree.insert("", END, values=(idx, name))

# # Add Treeview to Frame
# tree.pack(fill=BOTH, expand=True)

infolabel = ctk.CTkLabel(dashboard_frame3, text="To see data search companies or Question Number",
                         font=("poppins", 18), fg_color="white", bg_color="white", text_color="black")
infolabel.pack(padx = 140, pady = 120)


custom_btn_frame = ctk.CTkFrame(main_canvas, fg_color="white", height=270, width=160)
custom_btn_frame.propagate(False)
custom_btn_frame.place(x = 730, y = 315)

sort_label = ctk.CTkLabel(custom_btn_frame, text="Sort by:", font=("poppins", 18, 'bold'), fg_color="white",
                          bg_color="white", text_color="Black")
sort_label.pack(pady = (20, 50))

hard_btn = ctk.CTkButton(custom_btn_frame, text="Hard", font=("poppins", 15, 'bold'), fg_color="red", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2')
hard_btn.pack(pady = (0, 10))


medium_btn = ctk.CTkButton(custom_btn_frame, text="Medium", font=("poppins", 15, 'bold'), fg_color="yellow", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2')
medium_btn.pack(pady = (0, 10))

easy_btn = ctk.CTkButton(custom_btn_frame, text="Easy", font=("poppins", 15, 'bold'), fg_color="Green", bg_color="white",
                         text_color="black", corner_radius=20, cursor = 'hand2')
easy_btn.pack(pady = (0, 10))

win.mainloop()