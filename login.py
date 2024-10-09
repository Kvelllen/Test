from tkinter import *

# Project packages
import sql

class LoginWindow:
    def __init__(self):
        self.login_success = False
        self.background_color = '#383257'
        self.create_login_window()


    def format_string(self, string, bad_characters):
        for char in bad_characters:
            string = string.replace(char, '')
        return string


    def login_func(self):
        login = self.entry_login.get()
        password = self.entry_password.get()

        # Label for displaying error messages
        self.label_error = Label(self.frame, text="Incorrect login or password",
                                 font=("Arial", 13), background=self.background_color,
                                 fg='#b2a3ff')

        try:
            if login and password:
                stored_password = self.format_string(str(sql.execute_query(
                    f"SELECT login_password FROM managers WHERE manager_name = '{login}'"
                )), ['[', '(', ',', ')', ']', '\''])

                if password == stored_password:
                    self.login_success = True
                    print(f">> Login successful.")
                    print(f">> Logged in as {login}.")
                    self.window.destroy()
                else:
                    print(f">> Incorrect login or password.")
                    self.label_error.place(x=65, y=130)
            else:
                print(f">> Please enter both login and password.")
                self.label_error.place(x=65, y=130)
        except Exception as e:
            print(f">> Error occurred: {e}")
            self.label_error.place(x=65, y=130)


    def create_login_window(self):
        self.window = Tk()
        self.window['bg'] = '#241f40'
        self.window.title("Login")
        self.window.wm_attributes('-alpha', 0.97)
        self.window.geometry('350x230+%d+%d' % ((self.window.winfo_screenwidth() / 2) - (350 / 2),
                                                 (self.window.winfo_screenheight() / 2) - ((250 + 30) / 2)))
        self.window.resizable(width=False, height=False)

        self.frame = Frame(self.window, bg=self.background_color)
        self.frame.place(x=10, y=10, relwidth=0.945, relheight=0.9)


        label_title = Label(self.frame, text="OrderBase", font=("Arial", 20),
                            background=self.background_color, fg='#b2a3ff')
        label_title.place(x=100, y=5)


        Label(self.frame, text="Login:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff').place(x=46, y=59)
        self.entry_login = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_login.place(x=100, y=60)


        Label(self.frame, text="Password:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff').place(x=15, y=99)
        self.entry_password = Entry(self.frame, show='*', bg='#543ec7', font=("Arial", 13))  # Hide password input
        self.entry_password.place(x=100, y=100)


        login_button = Button(self.frame, text="Login", bg='#695f9e', fg='#27016e',
                              activebackground="#2108a3", command=self.login_func)
        login_button.place(x=150, y=165)

        self.window.mainloop()


if __name__ == "__main__":
    LoginWindow()