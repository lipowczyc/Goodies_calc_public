
from tkinter import *
import datetime as dt
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials

GREY = "#cdc2ae"
LIGHT_GREY = "#ece5c7"
FONT_NAME = "Comic Sans MS"
FONT_COLOR = "#354259"
LABEL_COLOR = "#42032C"

# ------------------------FUNCTIONS----------------------------------- #
class GoodiesData:

    light_sheet = []
    current_data = []
    nicklist = []
    current_values = {}
    data_to_send = []
    credentialsy = {
      "type": "service_account",
      "project_id": "xxxxxxx",
      "private_key_id": "xxxxx",
      "private_key": "Xxxxxxxxx",
      "client_email": "xxx",
      "client_id": "xxx",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "xxxx"
    }
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        lightCreds = ServiceAccountCredentials.from_json_keyfile_dict(self.credentialsy)
        light_client = gspread.authorize(lightCreds)
        self.light_sheet = light_client.open("Goodies_Calc").sheet1
        self.current_data = self.light_sheet.get_all_records()
        self.get_nick_list(self.current_data)

    def start(self, parametry):
        self.get_data(parametry)
        # self.get_nick_list(self.current_data)
        self.send_data()


    def get_data(self, parametry):
        nickname = parametry["nickname"]
        uni_nickname = nickname.lower()


        today = dt.datetime.now()
        obrobione_today = today.strftime("%d/%m/%Y")
        # obrobiony_time = today.strftime("%X")

        current_values = self.get_user_rowdata(uni_nickname)


        if parametry["future_points"] == "":
            if current_values["futureRuneweekScore"] == "":
                f_points = 999
            else:
                f_points = int(current_values["futureRuneweekScore"])
            print(current_values)
        else:
            f_points = 500 #int(parametry["future_points"])

        if parametry["current_points"] == "":
            c_points = int(0 if current_values["currentRuneweekScore"] == '' else current_values["currentRuneweekScore"])
        else:
            c_points = int(parametry["current_points"])

        if parametry["maps"] == "":
            maps = int(current_values["maps"])
        else:
            maps = parametry["maps"]

        if parametry["blueprints"] == "":
            blueprints = current_values["blueprints"]
        else:
            blueprints = parametry["blueprints"]

        if parametry["horns"] == "":
            horns = current_values["horns"]
        else:
            horns = parametry["horns"]

        if parametry["peaches"] == "":
            peaches = current_values["peaches"]
        else:
            peaches = parametry["peaches"]

        self.data_to_send = {
                "nickname": nickname,
                "dateOfUpdate": obrobione_today,
                "futureRuneweekScore": f_points,
                "currentRuneweekScore": c_points,
                "left points": None,
                "maps": maps,
                "mp": None,
                "blueprints": blueprints,
                "bp": None,
                "horns": horns,
                "hp": None,
                "peaches": peaches,
            }

    def get_user_rowdata(self, user):
        goodies_data = self.current_data
        nick_list = self.nicklist

        # nr_wiersza = nick_list.index(user)
        nr_wiersza = self.find_in_list(user, nick_list)
        try:
            user_current_values = goodies_data[nr_wiersza]
        except IndexError:
            user_current_values = {
                    "nickname": "",
                    "dateOfUpdate": "",
                    "futureRuneweekScore": 0,
                    "currentRuneweekScore": 0,
                    "left points": None,
                    "maps": 0,
                    "mp": None,
                    "blueprints": 0,
                    "bp": None,
                    "horns": 0,
                    "hp": None,
                    "peaches": 0,
                }

        # print(user_current_values)
        return user_current_values

    def find_in_list(self, needle, haystack):
        needle_index = -1
        empty_row = -1
        idx = 0
        for cus in haystack:
            if cus == needle:
                return idx
            elif cus == '' and empty_row == -1:
                empty_row = idx
            idx += 1
        if empty_row != -1:
            needle_index = empty_row
        else:
            needle_index = idx
        return needle_index


    def get_nick_list(self, data):
        nick_list = []
        for cus in data:
            if "nickname" in cus.keys():
                nickname = cus["nickname"].lower()
                nick_list.append(nickname)
        self.nicklist = nick_list
        return nick_list

    def send_data(self):

        nr_wiersza = self.find_in_list(self.data_to_send["nickname"], self.nicklist) +2
        odp = self.light_sheet.update('B' + str(nr_wiersza), [list(self.data_to_send.values())])


        messagebox.showinfo(title=None, message="Thanks")
        exit()
    def checkWprowadzoneDane(self, user_input):
        listerr = []
        if user_input["nickname"] == "":
            messagebox.showwarning(title=None, message="You left empty field 'nickname'")
            return False
        if(user_input["future_points"] != "" and type(int(user_input["future_points"])) != int):
            messagebox.showwarning(title=None, message=f"{user_input['future_points']} is not a number")
            return False
        if(user_input["current_points"] != "" and type(int(user_input["current_points"])) != int):
            messagebox.showwarning(title=None, message=f"{user_input['current_points']} is not a number")
            return False

        return True

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Goodies Calc")
window.config(padx=20, pady=20, bg=GREY)



#  -------------Labels------------
label_title = Label(text="Goodies Calc Updater", fg="#ff4c29", font=(FONT_NAME, 15, "bold"), bg=GREY)
label_title.grid(column=0, row=0, sticky="E")
label_title.config(padx=5, pady=5)
label_rights = Label(text="©pff singularities, 2022", fg="#1e5128", bg=GREY)
label_rights.grid(column=1, row=0, sticky="E")
label_rights.config(padx=5, pady=5)

label_nickname = Label(text="Nickname in the game", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_nickname.grid(column=0, row=1, sticky="E")
label_nickname.config(padx=5, pady=5)

label_future_points = Label(text="How many points during RuneWeek \nare you going to get?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_future_points.grid(column=0, row=4, sticky="E")
label_future_points.config(padx=5, pady=5)
label_current_points = Label(text="How many points \nare you got so far?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_current_points.grid(column=0, row=5, sticky="E")
label_current_points.config(padx=5, pady=5)

label_maps = Label(text="How many maps \ndo you have?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_maps.grid(column=0, row=6, sticky="E")
label_maps.config(padx=5, pady=5)
label_blueprints = Label(text="How many blueprints?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_blueprints.grid(column=0, row=7, sticky="E")
label_blueprints.config(padx=5, pady=5)
label_horns = Label(text="How many ravens/pollens?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_horns.grid(column=0, row=8, sticky="E")
label_horns.config(padx=5, pady=5)
label_peaches = Label(text="How many peaches/briars?:", fg=LABEL_COLOR, font=(FONT_NAME, 15, "bold"), bg=GREY)
label_peaches.grid(column=0, row=9, sticky="E")
label_peaches.config(padx=5, pady=5)

# ------------Button & Entries & Spinboxes-----------

entry_nickname = Entry(width=17, fg=FONT_COLOR, font=(FONT_NAME, 15, "bold"), bg=LIGHT_GREY)
entry_nickname.focus()
entry_nickname.grid(column=1, row=1)

entry_future_points = Entry(width=17, fg=FONT_COLOR, font=(FONT_NAME, 15, "bold"), bg=LIGHT_GREY)
entry_future_points.focus()
entry_future_points.grid(column=1, row=4)
entry_current_points = Entry(width=17, fg=FONT_COLOR, font=(FONT_NAME, 15, "bold"), bg=LIGHT_GREY)
entry_current_points.focus()
entry_current_points.grid(column=1, row=5)

spinbox_map = Spinbox(from_=0, to=100, width=5)
spinbox_map.grid(column=1, row=6)
spinbox_blueprint = Spinbox(from_=0, to=100, width=5)
spinbox_blueprint.grid(column=1, row=7)
spinbox_horn = Spinbox(from_=0, to=100, width=5)
spinbox_horn.grid(column=1, row=8)
spinbox_peach = Spinbox(from_=0, to=100, width=5)
spinbox_peach.grid(column=1, row=9)
def zaje():
    gd = GoodiesData()
    user_params = {
        "nickname": entry_nickname.get(),
        "future_points": entry_future_points.get(),
        "current_points": entry_current_points.get(),
        "maps": spinbox_map.get(),
        "blueprints": spinbox_blueprint.get(),
        "horns": spinbox_horn.get(),
        "peaches": spinbox_peach.get(),
    }
    if gd.checkWprowadzoneDane(user_params):
        gd.start(user_params)
button_search = Button(text="Update", fg=FONT_COLOR, font=(FONT_NAME, 15, "bold"), width=17, bg=LIGHT_GREY, command=zaje)
button_search.grid(column=1, row=10)
button_search.config(padx=5, pady=5)

window.mainloop()
