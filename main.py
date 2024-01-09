import os
import re
import time
import base64
import requests
import threading
import customtkinter
from fake_useragent import UserAgent
from PIL import Image, UnidentifiedImageError
from tkinter.filedialog import askopenfilename

icon = """
AAABAAEAMDAAAAEACACoDgAAFgAAACgAAAAwAAAAYAAAAAEACAAAAAAAAAkAAMMOAADDDgAAAAEAAAABAAAVAP8AHgr/AC0b/wAgDP8AFQH/ABYC/wAoFf8AIA3/AI2D/wDc2f8Awr3/AEs7/wBVRv8AzMj/AKWd/wAiD/8AKhf/AMfD/wD+/v8A////ANvY/wAzIf8A0s//AO3s/wA6Kf8AGAT/AGNV/wDi4P8Avbj/AIJ3/wD7+/8A2db/ACYT/wAXA/8A5eP/APz8/wCbk/8AGgb/AFdI/wDv7v8A9vb/AG5h/wDz8v8A9PT/AGVY/wBURf8A6ej/AP39/wAZBf8AiH7/APf3/wDh3/8APy7/ADgn/wDSzv8AKxn/ALSu/wDPy/8ANSP/ACkW/wDFwP8A19T/AD0s/wC1r/8AIQ7/AKqj/wDj4f8ASTn/AOjn/wCspf8Ai4H/AF1P/wBpXP8A8vH/AIR5/wBeUP8A8O//AGhb/wB4bP8A9fX/AI+G/wDW0/8A+fn/AIyC/wAbB/8AHAj/AMrG/wAkEf8AHQn/AI+F/wD4+P8AYlT/AOvq/wA+Lf8AfHH/AHdr/wAyIP8ALBr/ACUS/wBMPP8AQC//AKOb/wBTRP8A3dv/ADko/wDe3P8AcGT/AL65/wB+c/8A5+X/APPz/wBDM/8ANiX/AG1g/wBZS/8A3dr/ANDM/wCyrP8AY1b/ANTR/wBOP/8AMR//AO7t/wBYSv8AW03/AHpv/wAvHf8ANCL/AMO+/wBRQv8A393/AKKa/wDa1/8Ah33/AFBB/wCnoP8AyMT/APr6/wDo5v8ATD3/AJ2V/wB2av8APCv/ALOt/wChmf8AxsH/AJKJ/wB0aP8AIxD/AJiP/wBBMf8AoJj/ANHN/wB/dP8AKxj/ADcm/wBIOP8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJZqbnC1mb0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFSWlxRcK1paKpiZfiEAAAAAAAAAAAAAAAAAAAAA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
"""

def write_to_terminal(text):
    terminal.configure(state="normal")
    terminal.insert("end", f"{text}\n")
    terminal.configure(state="disabled")


def check_requisite(url, image):
    if not re.fullmatch(r"^https://[a-zA-Z0-9-_]+\.straw\.page$", url):
        preview_label.configure(image=None, text="Please enter a valid url!")
        return False
    if image == "":
        preview_label.configure(image=None, text="Please select an image!")
        return False
    return True

def get_cookies(url):
    ua = UserAgent()
    headers = {"user-agent": ua.random}

    write_to_terminal("[STATUS] Acquiring cookies...")
    response = requests.get(url, headers=headers)
    write_to_terminal("[SUCCESS] Cookies successfully get")
    return response.cookies.get_dict()


def send(url, image):
    url = url.get().rstrip('/')
    image = image.get()

    if not check_requisite(url, image):
        return

    API = url + "/gimmicks/canvas"

    with open(image, "rb") as f:
        im_bytes = base64.b64encode(f.read())
    im_b64 = im_bytes.decode("utf-8")

    payload = {"image": im_b64,
               "ret": "true"}

    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    response = requests.post(API, headers=headers, cookies=get_cookies(url), data=payload)
    if response.status_code == 200: # The api sends nothing on text for some reason, so this is the only way ( at least I think :p )
        print(response.text)
        write_to_terminal("[SUCCESS] Image successfully sent")
    else:
        write_to_terminal(f"[ERROR]: {response.text}")

    write_to_terminal("\n")
    write_to_terminal("Press any key to quit terminal :)")
    cache = terminal.get("0.0", "end")
    terminal.configure(state="normal")
    while terminal.get("0.0", "end") == cache:
        time.sleep(0.1)
    terminal.delete("0.0", "end")
    terminal.configure(state="disabled")
    terminal.place_forget()


def parallel(url, image):
    terminal.place(x=290, y=0)
    threading.Thread(target=send, args=(url, image)).start()


def select_image():
    path = askopenfilename(initialdir=os.getcwd(),
                           title="Select an image file")
    if path != "":
        input_image_path.set(path)
        try:
            img = Image.open(input_image_path.get())
            if not img.is_animated:
                preview_image = customtkinter.CTkImage(dark_image=img,size=(350, 350))
                preview_label.configure(image=preview_image, text="")
            else:
                preview_image = customtkinter.CTkImage(dark_image=img,size=(350, 350))
                preview_label.configure(image=preview_image, text="GIF is bad on tkinter, pretend it works :)")
        except UnidentifiedImageError:
            preview_label.configure(text="Nice choice :p")

# Create icon file and set it as icon then delete it, for simplistic
icondata = base64.b64decode(icon)
tempFile = "icon.ico"
with open(tempFile, "wb") as f:
    f.write(icondata)

window = customtkinter.CTk()
window.geometry("640x350")
window.title("straw.page Image sender")
window.iconbitmap("icon.ico")
window.resizable(False, False)
customtkinter.set_appearance_mode("dark")

os.remove("icon.ico")

input_url = customtkinter.StringVar()
input_image_path = customtkinter.StringVar()

selection_frame = customtkinter.CTkFrame(master=window, fg_color="#141414")
inner_frame1 = customtkinter.CTkFrame(master=selection_frame, fg_color="transparent")
inner_frame2 = customtkinter.CTkFrame(master=selection_frame, fg_color="transparent")
inner_frame3 = customtkinter.CTkFrame(master=selection_frame, fg_color="transparent")

url_entry_label = customtkinter.CTkLabel(master=inner_frame1,
                                         text="1. Enter straw.page URL",
                                         font=("calibri", 18, "bold"),
                                         )
url_entry_label.pack(pady=10)
url_entry = customtkinter.CTkEntry(master=inner_frame1,
                                   font=("consolas", 14),
                                   textvariable=input_url,
                                   corner_radius=0,
                                   border_width=1,
                                   height=40,
                                   )
url_entry.pack(fill='x')
# ~copied~ inspired by https://www.youtube.com/watch?v=u8Em9OQJXaI
select_image_button_label = customtkinter.CTkLabel(master=inner_frame2,
                                         text="2. Select an image",
                                         font=("calibri", 18, "bold"),
                                         )
select_image_button_label.pack(pady=10)
select_image_button = customtkinter.CTkButton(master=inner_frame2,
                                              text="S E L E C T",
                                              text_color="#ffcc66",
                                              fg_color="#141414",
                                              command=select_image,
                                              height=40,
                                              corner_radius=0
                                              )
select_image_button.pack(fill='x')
select_image_button.bind("<Enter>", lambda event: select_image_button.configure(text_color="#141414", fg_color="#ffcc66"))
select_image_button.bind("<Leave>", lambda event: select_image_button.configure(text_color="#ffcc66", fg_color="#141414"))

send_button_label = customtkinter.CTkLabel(master=inner_frame3,
                                         text="3. Profit",
                                         font=("calibri", 18, "bold"),
                                         )
send_button_label.pack(pady=10)
send_button = customtkinter.CTkButton(master=inner_frame3,
                                      height=40,
                                      text="S E N D",
                                      text_color="#25dae9",
                                      fg_color="#141414",
                                      corner_radius=0,
                                      command=lambda: parallel(input_url, input_image_path),
                                      )
send_button.pack(fill='x')
send_button.bind("<Enter>", lambda event: send_button.configure(text_color="#141414", fg_color="#25dae9"))
send_button.bind("<Leave>", lambda event: send_button.configure(text_color="#25dae9", fg_color="#141414"))

inner_frame1.pack(expand=True, fill="both")
inner_frame2.pack(expand=True, fill="both")
inner_frame3.pack(expand=True, fill="both")
selection_frame.pack(side="left", fill="both", expand=True)

preview_label = customtkinter.CTkLabel(master=window,
                                       text="Image preview...",
                                       font=("consolas", 12),
                                       width=350,
                                       height=350,
                                       )
preview_label.pack(side="left")
terminal = customtkinter.CTkTextbox(master=window,
                                    width=350,
                                    height=350,
                                    font=("consolas", 14),
                                    state="disabled",
                                    )

window.mainloop()
