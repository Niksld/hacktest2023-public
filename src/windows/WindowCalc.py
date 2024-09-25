import dearpygui.dearpygui as dpg

from windows.Window import Window
from math import sqrt


class WindowCalc(Window):
    def __init__(self, theme = None):
        super().__init__("calc", 300, 400, ["center", 0, 0], False, True, theme=theme, no_collapse=True, label="Kalkulačka", no_scrollbar=True)



        class Data():
            vc = ["0"]        # current calc value
            vm = ["0"]        # memory calc value
            op = [""]         # previous used operator

        class Strings():
            divisionByZero       = "err: division by 0"
            squareRootOfNegative = "err: sqrt of negative"
            memoHint             = "Memory field\nAlways contains 2nd operand"


        def callback_router(sender, app_data, user_data):
            if (user_data[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
                callback_numeric(user_data[0], Data.vc, user_data[1], Data.vm, user_data[2], Data.op)
            elif (user_data[0] == "."):
                callback_dot(user_data[0], Data.vc, user_data[1], Data.vm, user_data[2], Data.op)
            elif (user_data[0] in ["+", "-", "*", "/"]):
                callback_op(user_data[0], Data.vc, user_data[1], Data.vm, user_data[2], Data.op)
            elif (user_data[0] == "="):
                callback_equals(Data.vc, user_data[1], Data.vm, user_data[2], Data.op)
            elif (user_data[0] == "<-"):
                callback_delete(Data.vc, user_data[1])
            elif (user_data[0] == "C"):
                callback_clear(Data.vc, user_data[1], Data.vm, user_data[2], Data.op)
            elif (user_data[0] == "sqrt"):
                callback_sqrt(Data.vc, user_data[1], user_data[2], Data.op)
            elif (user_data[0] == "±"):
                callback_not(Data.vc, user_data[1])
            elif (user_data[0] == "¹"):
                callback_flip(Data.vc, user_data[1], user_data[2], Data.op)

        def callback_numeric(user_data, data_current, text_current, data_memo, text_memo, last_operator):
            if (last_operator[0] in ["+2", "-2", "*2", "/2", "###"]):
                callback_clear(data_current, text_current, data_memo, text_memo, last_operator)
            data_current[0] = string(data_current[0] + user_data)
            dpg.set_value(text_current, data_current[0])

        def callback_dot(user_data, data_current, text_current, data_memo, text_memo, last_operator):
            if (last_operator[0] in ["+2", "-2", "*2", "/2", "###"]):
                callback_clear(data_current, text_current, data_memo, text_memo, last_operator)
            new_string = data_current[0] + user_data
            if (validate(new_string)):
                data_current[0] = new_string
                dpg.set_value(text_current, data_current[0])

        def callback_op(user_data, data_current, text_current, data_memo, text_memo, last_operator):
            if (last_operator[0] in ["+", "-", "*", "/"]):
                callback_equals(data_current, text_current, data_memo, text_memo, last_operator)
            last_operator[0] = user_data
            data_memo[0] = data_current[0]
            dpg.set_value(text_memo, data_memo[0])
            data_current[0] = "0"
            dpg.set_value(text_current, data_current[0])

        def callback_equals(data_current, text_current, data_memo, text_memo, last_operator):
            if (len(last_operator[0]) > 1):
                if (last_operator[0] == "+2"):
                    data_current[0] = string(value(data_current[0]) + value(data_memo[0]))
                elif (last_operator[0] == "-2"):
                    data_current[0] = string(value(data_current[0]) - value(data_memo[0]))
                elif (last_operator[0] == "*2"):
                    data_current[0] = string(value(data_current[0]) * value(data_memo[0]))
                elif (last_operator[0] == "/2"):
                    data_current[0] = string(value(data_current[0]) / value(data_memo[0]))
            elif (len(last_operator[0]) == 1):
                temp = value(data_current[0])
                if (last_operator[0] == "+"):
                    data_current[0] = string(value(data_memo[0]) + temp)
                    last_operator[0] = "+2"
                elif (last_operator[0] == '-'):
                    data_current[0] = string(value(data_memo[0]) - temp)
                    last_operator[0] = "-2"
                elif (last_operator[0] == '*'):
                    data_current[0] = string(value(data_memo[0]) * temp)
                    last_operator[0] = "*2"
                elif (last_operator[0] == '/'):
                    if (temp == 0):
                        dpg.set_value(text_memo, Strings.divisionByZero)
                        last_operator[0] = ""
                        return
                    data_current[0] = string(value(data_memo[0]) / temp)
                    last_operator[0] = "/2"
                data_memo[0] = string(temp)
                dpg.set_value(text_memo, data_memo[0])
            dpg.set_value(text_current, data_current[0])

        def callback_delete(storage_data, text_field):
            if (len(storage_data[0]) < 2 or (len(storage_data[0]) < 3 and storage_data[0][0] == "-")):
                storage_data[0] = "0"
            else:
                storage_data[0] = storage_data[0][:-1]
            dpg.set_value(text_field, storage_data[0])

        def callback_clear(data_current, text_current, data_memo, text_memo, last_operator):
            data_current[0] = "0"
            data_memo[0] = "0"
            last_operator[0] = ""
            dpg.set_value(text_current, data_current[0])
            dpg.set_value(text_memo, data_memo[0])

        def callback_sqrt(data_current, text_current, text_memo, last_operator):
            if (value(data_current[0]) < 0):
                dpg.set_value(text_memo, Strings.squareRootOfNegative)
            else:
                data_current[0] = string(sqrt(value(data_current[0])))
                dpg.set_value(text_current, data_current[0])
                # last_operator[0] = "###"

        def callback_not(data_current, text_current):
            data_current[0] = string(-value(data_current[0]))
            dpg.set_value(text_current, data_current[0])

        def callback_flip(data_current, text_current, text_memo, last_operator):
            if (data_current[0] == "0"):
                dpg.set_value(text_memo, Strings.divisionByZero)
            else:
                data_current[0] = string(1 / value(data_current[0]))
                dpg.set_value(text_current, data_current[0])
                # last_operator[0] = "###"


        def string(x):
            # removes zeros at the beginning of string except for some number cases
            if (isinstance(x, str)):
                if (len(x) < 2):
                    return x
                counter = 0
                start = 0
                if (x[0] == "-"):
                    start = 1
                for i in range(start, len(x)):
                    if x[i] != '0':
                        break
                    counter += 1
                if (counter == len(x)):
                    counter -= 1
                if (x[counter] == '.'):
                    counter -= 1
                if (counter < 1):
                    return x
                if (start > 0):
                    return "-" + x[(counter + 1):]
                return x[counter:]
            # converts float to string without trailing zeros
            temp = str("{:.10f}".format(x)).rstrip("0")
            if (temp[len(temp) - 1] == "."):
                temp = temp[:-1]
            return temp

        def value(x):
            # convert string to float with additional cases
            if (x in ["", "-"]):
                return 0
            return float(x)

        def validate(input):
            try:
                value(input)
            except ValueError:
                return False
            return True

        input = dpg.add_input_text(default_value=0, width=-1, height=55, readonly=True, parent=self.tag)
        memo  = dpg.add_input_text(default_value=0, width=-1, height=55, readonly=True, parent=self.tag)
        buttons = ["<-"," ","C"," "," ","7","8","9","/"," ","4","5","6","*","¹", "1","2","3","-","±"," " ,"0",".","+","="]


        x,y, counter = 15,110,0
        for button in buttons:
            if counter == 5:
                x = 15
                y += 55
                counter = 0
            dpg.add_button(label=button, width=50, height=50, callback=callback_router, user_data=(button, input, memo), parent=self.tag, pos=[x,y], enabled=True if button != " " else False)

            x+=55
            counter += 1


