from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

# Project packages
import classes
import sql

# GUI FUNCTIONS --------------------------------------------------------------------------


class APIWindow:
    def __init__(self):
        self.background_color = '#383257'
        self.create_api_window()


    # Очистити поле для виводу інформації
    def delete(self):
        labelDelete = Label(self.frame, text="                 ",
                            font=("Calibri", 220), background=self.background_color, fg='#b2a3ff')
        labelDelete.place(x=5, y=570)


    # Вирахувати ціну згідно з типом склотари
    def calc_price(self):
        labelDelete0 = Label(self.frame, text="                               ",
                             font=("Calibri", 13), background=self.background_color, fg='#b2a3ff')
        labelDelete0.place(x=135, y=135)
        multiplier = 0
        type_ = str(self.entry_type.get())
        amount = int(self.entry_amount .get())
        if type_ == 'A':
            multiplier = 100
        elif type_ == 'B':
            multiplier = 70
        elif type_ == 'C':
            multiplier = 50
        else:
            multiplier = 0
        priceCalc = multiplier * amount
        label30 = Label(self.frame, text="{price} $".format(price=priceCalc), font=("Arial", 13),
                        background=self.background_color,
                        fg='#b2a3ff')
        label30.place(x=136, y=135)

        return priceCalc


    # Створити нове замовлення
    def create(self):
        try:
            typeField = self.entry_type.get()
            amountField = self.entry_amount.get()

            # Validate amountField
            if not amountField.isdigit():
                raise ValueError("Amount must be a positive integer.")
            amountField = int(amountField)

            entry_price = self.calc_price()

            priceField = entry_price
            managerField = classes.Manager(
                self.entry_managerName.get(),
                self.entry_managerAdress.get(),
                self.entry_managerTelephone.get()
            )
            customerField = classes.Customer(
                self.entry_customerName.get(),
                self.entry_customerAdress.get(),
                self.entry_customerTelephone.get()
            )

            currentDate = classes.Order.setDateCreation()
            currentOrder = classes.Order(
                None, typeField, amountField, priceField,
                managerField, customerField, currentDate, None
            )

            # Create table if it doesn't exist
            sql.execute_non_query('''CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                type VARCHAR(1) NOT NULL,
                amount INT NOT NULL,
                price INT NOT NULL,
                manager_name VARCHAR(50) NOT NULL,
                station_adress VARCHAR(100) NOT NULL,
                manager_telephone VARCHAR(20) NOT NULL,
                customer_name VARCHAR(50) NOT NULL,
                customer_adress VARCHAR(100) NOT NULL,
                customer_telephone VARCHAR(20) NOT NULL,
                creation_time TIMESTAMP NOT NULL,
                completion_time TIMESTAMP
            );''')

            # Insert order
            sql.execute_non_query(f'''INSERT INTO orders(type, amount, price, 
                manager_name, station_adress, manager_telephone, 
                customer_name, customer_adress, customer_telephone, 
                creation_time)
            VALUES
                ('{typeField}', {amountField}, {priceField},
                '{managerField.name}', '{managerField.adress}', '{managerField.telephone}',
                '{customerField.name}', '{customerField.adress}', '{customerField.telephone}',
                '{currentDate}')
            ON CONFLICT(id)
            DO UPDATE SET
                type = EXCLUDED.type,
                amount = EXCLUDED.amount,
                price = EXCLUDED.price,
                manager_name = EXCLUDED.manager_name,
                station_adress = EXCLUDED.station_adress,
                manager_telephone = EXCLUDED.manager_telephone,
                customer_name = EXCLUDED.customer_name,
                customer_adress = EXCLUDED.customer_adress,
                customer_telephone = EXCLUDED.customer_telephone,
                creation_time = EXCLUDED.creation_time,
                completion_time = EXCLUDED.completion_time;''')

            classes.Order.globalID = sql.execute_query('SELECT MAX(id) FROM orders;')
            currentOrder.id = classes.Order.globalID
            print(f"> Order №{currentOrder.id} created.")

        except ValueError as ve:
            messagebox.showwarning(title="Warning", message=str(ve))
        except Exception as e:
            messagebox.showwarning(title="Warning", message="An error occurred: " + str(e))


    # Видалити зайві символи при виводі даних замовлення
    def format_string(self, string, bad_characters):
        for i in bad_characters:
            string = string.replace(i, '')
        return string


    # Вивести інформацію по створенному замовленню на екран
    def get(self):
        self.delete()
        check = False
        bad_characters = ['[', '(', '\'', ')', ']', 'datetime', '.', ',']
        try:
            if self.format_string(str(sql.execute_query(f'SELECT id FROM orders WHERE id={self.entry_getOrder.get()}')),
                            bad_characters) != '':
                check = True
            label15 = Label(self.frame,
                            text=f"Order №{self.format_string(str(sql.execute_query(f'SELECT id FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                            font=("Calibri", 18), background=self.background_color, fg='#b2a3ff')
            label15.place(x=15, y=570)

            label16 = Label(self.frame,
                            text=f"Type: {self.format_string(str(sql.execute_query(f'SELECT type FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                            font=("Calibri", 11), background=self.background_color, fg='#b2a3ff')
            label16.place(x=15, y=605)

            label17 = Label(self.frame,
                            text=f"Amount (kg): {self.format_string(str(sql.execute_query(f'SELECT amount FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                            font=("Calibri", 11), background=self.background_color, fg='#b2a3ff')
            label17.place(x=15, y=630)

            label3 = Label(self.frame,
                           text=f"Creation date: {self.format_string(str(sql.execute_query(f'SELECT creation_time FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                           font=("Calibri", 11), background=self.background_color, fg='#b2a3ff')
            label3.place(x=15, y=655)

            label18 = Label(self.frame,
                            text=f"Price (USD): {self.format_string(str(sql.execute_query(f'SELECT price FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                            font=("Calibri", 11), background=self.background_color, fg='#b2a3ff')
            label18.place(x=15, y=680)

            label19_0 = Label(self.frame, text=f"Manager", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
            label19_0.place(x=15, y=710)
            label19_1 = Label(self.frame,
                              text=f"Name: {self.format_string(str(sql.execute_query(f'SELECT manager_name FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label19_1.place(x=15, y=740)
            label19_2 = Label(self.frame,
                              text=f"Adress: {self.format_string(str(sql.execute_query(f'SELECT station_adress FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label19_2.place(x=15, y=765)
            label19_3 = Label(self.frame,
                              text=f"Telephone: {self.format_string(str(sql.execute_query(f'SELECT manager_telephone FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label19_3.place(x=15, y=790)

            label20_0 = Label(self.frame, text=f"Customer", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
            label20_0.place(x=15, y=820)
            label20_1 = Label(self.frame,
                              text=f"Name: {self.format_string(str(sql.execute_query(f'SELECT customer_name FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label20_1.place(x=15, y=850)
            label20_2 = Label(self.frame,
                              text=f"Adress: {self.format_string(str(sql.execute_query(f'SELECT customer_adress FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label20_2.place(x=15, y=875)
            label20_3 = Label(self.frame,
                              text=f"Telephone: {self.format_string(str(sql.execute_query(f'SELECT customer_telephone FROM orders WHERE id={self.entry_getOrder.get()}')), bad_characters)}",
                              font=("Arial", 11), background=self.background_color, fg='#b2a3ff')
            label20_3.place(x=15, y=900)

            if not check:
                label15 = Label(self.frame, text="Entered order does not exist", font=("Calibri", 16),
                                background=self.background_color,
                                fg='#b2a3ff')
                label15.place(x=15, y=575)
        except ValueError as err:
            label15 = Label(self.frame, text="Entered order does not exist", font=("Calibri", 16),
                            background=self.background_color,
                            fg='#b2a3ff')
            label15.place(x=15, y=575)


    # Спеціальні функції: функції, згідні з завданням, відмічені, як (--)
    def special_box_functions(self):
        functionChoice = self.choice_box_functions.get()
        match functionChoice:

            case "Get orders":
                box = ttk.Combobox(values=sql.execute_query("SELECT * FROM orders;"), state="readonly",
                                   font=("Arial", 22))
                box.place(x=20, y=480)

            case "-- Customers list":
                try:
                    box = ttk.Combobox(values=sql.execute_query("SELECT * FROM customers;"), state="readonly",
                                       font=("Arial", 22))
                    box.place(x=20, y=480)
                except IndexError as err:
                    pass

            case "-- Most popular type":
                try:
                    box = ttk.Combobox(values=sql.execute_query(
                        "SELECT type, COUNT(*) AS order_count FROM orders GROUP BY type ORDER BY order_count DESC;"),
                                       state="readonly", font=("Arial", 22))
                    box.place(x=20, y=480)
                except ValueError as err:
                    pass

            case "-- Average amount":
                try:
                    box = ttk.Combobox(values=sql.execute_query(
                        "SELECT 'Overall' AS type, AVG(amount) AS average_amount FROM orders UNION ALL SELECT type, AVG(amount) AS average_amount FROM orders GROUP BY type ORDER BY average_amount DESC;"),
                                       state="readonly", font=("Arial", 22))
                    box.place(x=20, y=480)
                except ValueError as err:
                    pass

            case "-- Most expensive order":
                try:
                    box = ttk.Combobox(
                        values=sql.execute_query("SELECT * FROM orders ORDER BY price DESC LIMIT 15;"),
                        state="readonly", font=("Arial", 22))
                    box.place(x=20, y=480)
                except IndexError as err:
                    pass

            case "-- Customer, who paid the most":
                try:
                    box = ttk.Combobox(values=sql.execute_query(
                        "SELECT customer_name, SUM(price) AS total_paid FROM orders GROUP BY customer_name ORDER BY total_paid DESC LIMIT 15;"),
                                       state="readonly", font=("Arial", 22))
                    box.place(x=20, y=480)
                except ValueError as err:
                    pass
            case _:
                pass


    def create_api_window(self):
        # MAIN PART --------------------------------------------------------------------------

        self.window = Tk()
        self.window['bg'] = '#241f40'
        self.window.title("OrderBase")
        self.window.wm_attributes('-alpha', 0.97)
        self.window.geometry('385x970+%d+%d' % (
        (self.window.winfo_screenwidth() / 2) - (385 / 2), (self.window.winfo_screenheight() / 2) - ((970 + 30) / 2)))
        self.window.resizable(width=False, height=False)
        self.frame = Frame(self.window, bg=self.background_color)
        self.frame.place(x=10, y=10, relwidth=0.945, relheight=0.97)

        frame1 = Frame(self.window, bg='#383275')
        frame1.place(x=10, y=415, relwidth=0.945, relheight=0.02)
        frame2 = Frame(self.window, bg='#383275')
        frame2.place(x=10, y=526, relwidth=0.945, relheight=0.02)

        label1 = Label(self.frame, text="OrderBase", font=("Arial", 20), background=self.background_color, fg='#b2a3ff')
        label1.pack()

        # END OF MAIN PART --------------------------------------------------------------------------

        # INPUT --------------------------------------------------------------------------

        label14 = Label(self.frame, text="Order", font=("Arial", 15), background=self.background_color, fg='#b2a3ff')
        label14.place(x=25, y=50)

        label2 = Label(self.frame, text="Type:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label2.place(x=25, y=85)
        self.entry_type = ttk.Combobox(values=classes.Order.types, state="readonly", font=("Arial", 11))
        self.entry_type.place(x=150, y=95)

        label4 = Label(self.frame, text="Amount (kg):", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label4.place(x=25, y=110)
        self.entry_amount = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_amount.place(x=140, y=110)

        label5 = Label(self.frame, text="Price (USD):", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label5.place(x=25, y=135)

        label6 = Label(self.frame, text="Manager", font=("Arial", 15), background=self.background_color, fg='#b2a3ff')
        label6.place(x=25, y=170)

        label7 = Label(self.frame, text="Name:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label7.place(x=25, y=200)
        self.entry_managerName = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_managerName.place(x=140, y=200)

        label8 = Label(self.frame, text="Adress:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label8.place(x=25, y=225)
        self.entry_managerAdress = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_managerAdress.place(x=140, y=225)

        label9 = Label(self.frame, text="Telephone:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label9.place(x=25, y=250)
        self.entry_managerTelephone = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_managerTelephone.place(x=140, y=250)

        label10 = Label(self.frame, text="Customer", font=("Arial", 15), background=self.background_color, fg='#b2a3ff')
        label10.place(x=25, y=285)

        label11 = Label(self.frame, text="Name:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label11.place(x=25, y=315)
        self.entry_customerName = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_customerName.place(x=140, y=315)

        label12 = Label(self.frame, text="Adress:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label12.place(x=25, y=340)
        self.entry_customerAdress = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_customerAdress.place(x=140, y=340)

        label13 = Label(self.frame, text="Telephone:", font=("Arial", 13), background=self.background_color, fg='#b2a3ff')
        label13.place(x=25, y=365)
        self.entry_customerTelephone = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_customerTelephone.place(x=140, y=365)

        # END OF INPUT --------------------------------------------------------------------------

        # GUI BUTTONS --------------------------------------------------------------------------

        create_button = Button(self.frame, text="Add Order", bg='#695f9e', fg='#27016e', activebackground="#2108a3",
                               command=self.create)
        create_button.place(x=260, y=50)

        price_button = Button(self.frame, text="Calculate", bg='#695f9e', fg='#27016e', activebackground="#2108a3",
                              command=self.calc_price)
        price_button.place(x=265, y=135)

        get_button = Button(self.frame, text="Get Order", bg='#695f9e', fg='#27016e', activebackground="#2108a3",
                            command=self.get)
        get_button.place(x=25, y=545)
        self.entry_getOrder = Entry(self.frame, bg='#543ec7', font=("Arial", 13))
        self.entry_getOrder.place(x=100, y=546)

        function_button = Button(self.frame, text="Function apply", bg='#695f9e', fg='#27016e', activebackground="#2108a3",
                                 command=self.special_box_functions)
        function_button.place(x=25, y=434)
        self.choice_box_functions = ttk.Combobox(values=classes.Order.specialFunctionsList, state="readonly",
                                            font=("Arial", 11))
        self.choice_box_functions.place(x=130, y=445)

        # END OF GUI BUTTONS --------------------------------------------------------------------------

        self.window.mainloop()

if __name__ == "__main__":
    APIWindow()