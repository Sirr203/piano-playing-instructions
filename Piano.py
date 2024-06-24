import tkinter as tk
from tkinter import filedialog, Label, PhotoImage
import tkinter.font as font
import subprocess

# Tạo cửa sổ chính
root = tk.Tk()
root.title('Giao diện người dùng')
root.geometry("1024x700+250+50")

# Tải hình ảnh làm nền
bg_image = PhotoImage(file="back_ground.png")

# Hiển thị hình ảnh làm nền
background_label = Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Hàm để chạy file Python khác
def run_song_file(file_name):
    try:
        # Sử dụng subprocess để chạy file Python khác
        subprocess.run(["python", file_name])
    except Exception as e:
        print(f"Error: {e}")


# Nút để chọn và chạy bài nhạc 1
button_song1 = tk.Button(root, text="Một con vịt",bg="#7CFC00",fg="#333" ,activebackground="#326500",command=lambda: run_song_file("play_piano_music/Một con vịt.py"),width=20, height=2)
button_song1.pack(pady=10,anchor="nw")

# button_song1 = tk.Button(root, text="Một con vịt", bg="#7CFC00", fg="#333", activebackground="#326500", command=lambda: run_song_file("play_piano_music/Một con vịt.py"), width=20, height=2)
# button_song1.config(width=10, height=2, borderwidth=10, relief="solid", bd=0, highlightthickness=0, padx=0, pady=0, font=("Arial", 16))
# button_song1.pack(pady=10, anchor="nw")



# Nút để chọn và chạy bài nhạc 2
button_song2 = tk.Button(root, text="Chúc bé ngủ ngon", bg="#7CFC00",fg="#333" ,activebackground="#326500",command=lambda: run_song_file("play_piano_music/Chúc bé ngủ ngon.py"),width=20, height=2)
button_song2.pack(pady=10,anchor="nw")

#Exit
button_exit = tk.Button(root, text="Tắt chương trình", bg="#7CFC00",fg="#333" ,activebackground="#326500",command=root.destroy,width=20, height=2)
button_exit.pack(pady=10,anchor="nw")

root.mainloop()