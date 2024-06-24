import tkinter as tk
from tkinter import PhotoImage, Canvas, Tk ,filedialog
from PIL import Image, ImageTk
import pygame
import sys

# Tạo cửa sổ chính
root = tk.Tk()
root.title('Chúc bé ngủ ngon')

# Đặt hình ảnh làm background
canvas = tk.Canvas(root, width=1800, height=400, bg='#7CFC00')
canvas.pack()
canvas.focus_set()

# Vẽ các dòng nhạc
num_lines = 5
line_spacing = 20
top_margin = 150

for i in range(num_lines):
    y_position = top_margin + i * line_spacing
    canvas.create_line(50, y_position, 1550, y_position, fill='black', width=2)
# Vẽ các dòng nhạc bass
bass_top_margin = 250

# Vẽ khóa Sol và khóa Fa
treble_clef = canvas.create_text(120, top_margin + 1.5 * line_spacing, text="𝄞", fill='black', font=("Segoe UI Symbol", 92))

# bass_clef = canvas.create_text(30, bass_top_margin + 2 * line_spacing, text="𝄢", fill='white', font=("Arial", 32))

# Tạo dòng chỉ báo (cursor) cố định
cursor_end = canvas.create_rectangle(200, top_margin - 60, 205, bass_top_margin + 4 * line_spacing -33, fill='cyan')
cursor_check = canvas.create_rectangle(775, top_margin - 60, 780, bass_top_margin + 4 * line_spacing -33, fill='cyan')
# Thiết lập cursor không hiển thị
canvas.itemconfig(cursor_end, outline="", fill="")


# Danh sách để lưu trữ các block và thông tin liên quan
blocks = []

# Hàm để tạo block cho mỗi nốt nhạc

def create_block(note, time_to_appear, y_position):
    x_position = 4390 - time_to_appear * 50  # Vị trí x phụ thuộc vào thời gian xuất hiện
    block = canvas.create_text(x_position, y_position, text="♩", fill='black', font=("Segoe UI Symbol", 70),tags=('note',))
    #ledger_line = canvas.create_line(x_position - 20, y_position +30, x_position + 20, y_position +30, fill='black', width=2)
    blocks.append((block, y_position))
    #blocks.append((ledger_line, y_position))
    create_ledger_line( x_position,y_position, top_margin)
    

# def create_ledger_line(x_position, y_position, top_margin):
#     # Kiểm tra xem nốt nhạc có cần dòng kẻ phụ không
#     if y_position < top_margin or y_position > 200:
#         ledger_line = canvas.create_line(x_position - 20, y_position +30, x_position + 20, y_position +30, fill='black', width=2,tags=('line_note',))
#         blocks.append((ledger_line, y_position))
def create_ledger_line(x_position, y_position, top_margin):
    # Kiểm tra xem nốt có cần dòng kẻ phụ không
    if 220 >= y_position > 210:
        ledger_line = canvas.create_line(x_position - 20, y_position + 30, x_position + 15, y_position + 30, fill='black', width=2,tags=('line_note',))
        blocks.append((ledger_line, y_position))
    if 230 >= y_position > 220:
        ledger_line = canvas.create_line(x_position - 15, y_position + 20, x_position + 20, y_position + 20, fill='black', width=2,tags=('line_note',))
        blocks.append((ledger_line, y_position))
    if 242 >= y_position > 230:
        ledger_line1 = canvas.create_line(x_position - 15, y_position + 30, x_position + 15, y_position + 30, fill='black', width=2,tags=('line_note',))
        ledger_line2 = canvas.create_line(x_position - 15, y_position + 10, x_position + 15, y_position + 10, fill='black', width=2,tags=('line_note',))
        blocks.append((ledger_line1, y_position))
        blocks.append((ledger_line2, y_position))

def move_blocks():
    if not pause:
        for block, y_position in blocks:
            canvas.move(block, -10, 0)  # Di chuyển mỗi block sang trái 10 pixels
    root.after(100, move_blocks)

def update_end():
    global miss_count
    # Tìm tất cả các items chồng lấp với cursor
    overlapping_items = canvas.find_overlapping(145, top_margin - 60, 150, bass_top_margin + 4 * line_spacing -33)
    
    for item in overlapping_items:
        # Kiểm tra xem item có phải là nốt nhạc không (ví dụ: kiểm tra tag hoặc kiểu của item)
        if is_note_item(item):
            tags = canvas.gettags(item)  # Lấy tất cả tags của item
            if 'miss' in tags:
                miss_count += 1  # Tăng biến đếm nếu tag là 'miss'
            ## Xóa item nốt nhạc khỏi canvas
            canvas.delete(item)
    canvas.after(100, update_end)
    # return miss_count

def update_miss():

    overlapping_items_check_colour = canvas.find_overlapping(700, top_margin - 60, 730, bass_top_margin + 4 * line_spacing -33)
    for icolour in overlapping_items_check_colour:
        if note_uncheck(icolour):
            # Đổi tag của nốt nhạc khi đi qua cursor
            canvas.itemconfig(icolour, fill='red')
        if line(icolour):
            canvas.itemconfig(icolour, fill='red')

    overlapping_items_check = canvas.find_overlapping(600, top_margin - 60, 700, bass_top_margin + 4 * line_spacing -33)
    #overlapping_items_check_colour = canvas.find_overlapping(700, top_margin - 60, 765, bass_top_margin + 4 * line_spacing -33)
    for icheck in overlapping_items_check:
        if note_uncheck(icheck):
            #canvas.itemconfig(icheck, fill='red')
            canvas.itemconfig(icheck, tags=('miss',))
        # if line(icheck):
        #     canvas.itemconfig(icheck, tags=('miss',))
    

    canvas.after(100, update_miss)


def is_note_item(item):
    tags = canvas.gettags(item)
    return 'note' in tags or 'pass' in tags or 'miss' in tags or 'line_note' in tags

def note_uncheck(item):
    tags = canvas.gettags(item)
    return 'note' in tags

def line(item):
    tags = canvas.gettags(item)
    return 'line_note' in tags


# Hàm để tạo các block từ sheet music
def create_blocks_from_sheet(sheet):
    for note_info in sheet:
        note, time_to_appear = note_info
        y_position = note_to_position(note)
        create_block(note, time_to_appear, y_position)

def end_program():
    # Hiển thị dòng chữ "Finish" trên canvas
    canvas.create_text(800, 300, text="Finish", fill='black', font=("Segoe Script", 80))
    # Đợi 2 giây (2000ms) rồi tắt chương trình
    root.after(2000, root.destroy)


def check_end():
    global miss_count
    remaining_notes = canvas.find_withtag('note')
    passed_notes = canvas.find_withtag('pass')
    miss_note = canvas.find_withtag('miss')
    line = canvas.find_withtag('line')
    if not remaining_notes and not passed_notes and not miss_note and not line:
        if miss_count == 0 :
        # Không còn nốt nhạc, gọi hàm end_program
            #os.system("main.py")
            end_program()
        else :
            canvas.create_text(800, 300, text='Restarting', fill='black', font=("Segoe Script", 80), tags='restart_text')
            reset_program()

    else:
        # Nếu vẫn còn nốt nhạc, tiếp tục kiểm tra sau mỗi khoảng thời gian
        canvas.after(100, check_end)


def reset_program():
    root.after(2000, lambda: canvas.delete('restart_text'))
    # Xóa tất cả các nốt nhạc và thiết lập lại trạng thái ban đầu của chương trình
    canvas.delete('note')
    canvas.delete('pass')
    canvas.delete('miss')
    canvas.delete('line_note')
    # Thêm mã để khởi tạo lại các nốt nhạc và bắt đầu chương trình
    pygame.mixer.music.play(0)
    create_blocks_from_sheet(sheet_music)
    update_miss()
    update_end()
    check_miss()
    check_end()
    root.mainloop()

def check_miss():
    miss_notes = canvas.find_withtag('miss')
    if len(miss_notes) >= 3:
        # Nếu có ít nhất 3 nốt có tag 'miss', reset chương trình
        canvas.create_text(800, 300, text='Restarting', fill='black', font=("Segoe Script", 80), tags='restart_text')
        # Chờ trong 2 giây rồi reset chương trình
        reset_program()
    else:
        # Nếu vẫn còn nốt nhạc, tiếp tục kiểm tra sau mỗi khoảng thời gian
        canvas.after(100, check_miss)

# Định nghĩa các hàm initialize_notes và start_program theo yêu cầu của chương trình của bạn


def handle_space_press(event):
    overlapping_items = canvas.find_overlapping(770, top_margin - 60, 780, bass_top_margin + 4 * line_spacing -33)
    
    for item in overlapping_items:
            # Kiểm tra xem item có phải là nốt nhạc không (ví dụ: kiểm tra tag hoặc kiểu của item)
            if is_note_item(item):
                # Xóa item nốt nhạc khỏi canvas
                canvas.delete(item)
    canvas.after(100, update_end)

# Hàm tạm dừng và tiếp tục
pause = False
def toggle_pause():
    global pause
    pause = not pause
    if pause:
        pause_button.config(text="Tiếp tục")
        pygame.mixer.music.pause()
    else:
        pause_button.config(text="Tạm dừng")
        pygame.mixer.music.unpause()

# Hàm reset lại
def reset():
    global blocks, pause
    pause = True
    pause_button.config(text="Tạm Dừng")
    for block, y_position in blocks:
        canvas.delete(block)
    blocks = []
    if sheet_music:
        create_blocks_from_sheet(sheet_music)
    pygame.mixer.music.play(0)  # Chơi từ đầu
    pause = False

def exit_program():
    sys.exit()


        
# Hàm để chuyển đổi ký hiệu nốt nhạc thành vị trí trên dòng nhạc
def note_to_position(note):
    note_positions = {
        'D4': top_margin + 6   * line_spacing,
        'E4': top_margin + 5.5 * line_spacing,
        'F4': top_margin + 5   * line_spacing,
        'B4': top_margin + 4.5 * line_spacing,
        'A4': top_margin + 4   * line_spacing,
        'C5': top_margin + 3.5 * line_spacing,
        'D5': top_margin + 3   * line_spacing,
        'E5': top_margin + 2.5 * line_spacing,
        'F5': top_margin + 2   * line_spacing,
        'B5': top_margin + 1.5 * line_spacing,
        'A5': top_margin + 1   * line_spacing,
        
    }

    return note_positions.get(note, top_margin + 2 * line_spacing)

# Ví dụ sheet music cho "1 con vịt"
sheet_music_dict = {
    "list_music/ngungon.mp3":[
    ('G5', 52), ('E5', 50.6), ('C5', 49), ('E5', 48), ('E5', 46.5), ('F5', 45.5), ('E5', 45), ('C5', 43.5), # Sol Mi do Mi Mi Fa Mi do
    ('C5', 41), ('A5', 40.5), ('A5', 39), ('G5', 37.5), ('E5', 36), ('F5', 35), ('E5', 34), ('D4', 33), ('D4', 32), # Do La La Sol Mi Fa Mi Re Re
    ('G5', 28.8), ('E5', 27.3), ('C5', 26), ('E5', 24.5), ('E5', 23), ('F5', 22), ('E5', 21.2), ('C5', 20.2), # Sol Mi do Mi Mi Fa Mi do
    ('A4', 17), ('C5', 16), ('A4', 14), ('C5', 13), ('B4', 11.5), ('C5', 10.5), ('B4', 9.5), ('D5', 8.5), ('C5', 8), # La do la do xi do xi Re do
    ('A4', 5.5), ('C5', 3.5), ('A4', 2.5), ('C5', 1), ('A4', -0.5), ('B4', -2), ('C5', -3.5) ]# La do la do la xi do
}
# Tạo các block từ sheet music

miss_count = 0
initial_song = "list_music/ngungon.mp3"
sheet_music = sheet_music_dict[initial_song]

create_blocks_from_sheet(sheet_music)

pygame.init()
pygame.mixer.music.load(initial_song)
pygame.mixer.music.play()

# Tạo menu
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="Tùy chọn", menu=file_menu)
file_menu.add_command(label="Tạm Dừng", command=toggle_pause)
file_menu.add_command(label="Chơi lại", command=reset)
file_menu.add_command(label="Quay lại menu", command=reset)
# Nút tạm dừng
pause_button = tk.Button(root, text="Tạm Dừng", command=toggle_pause)
pause_button.pack(side=tk.LEFT)

# Nút reset
reset_button = tk.Button(root, text="Chơi lại", command=reset)
reset_button.pack(side=tk.LEFT)

# Nút tắt
exit_button = tk.Button(root, text="Quay lại menu", command=exit_program)
exit_button.pack(side=tk.LEFT)






move_blocks()
canvas.bind('<space>', handle_space_press)
update_miss()
update_end()
check_miss()
check_end()
root.mainloop()
