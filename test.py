import customtkinter as ctk
app = ctk.CTk()
app.geometry("500x500")
scrollable_frame = ctk.CTkScrollableFrame(master = app, corner_radius = 10, label_text = " ", label_fg_color = "transparent")
object_in_frame = ctk.CTkLabel(master = scrollable_frame, text = "I`m in", fg_color = "transparent")
object_out_of_frame = ctk.CTkLabel(master = scrollable_frame, text = "I`m out", fg_color = 'transparent')
scrollable_frame.place(x = 150, y = 150)
object_in_frame.pack(pady = 10)
object_out_of_frame.pack(pady = 10)
app.mainloop()