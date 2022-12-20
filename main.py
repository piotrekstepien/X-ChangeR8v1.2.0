from datetime import date
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import functions
from functions import *


def get_currency_exchange_rate():

    def update_plot(data1, data2):
        axes = fig.axes
        axes[0].cla()
        x = data1
        y = data2
        axes[0].plot(x,y,"r-")
        axes[0].xaxis.set_major_locator(plt.MaxNLocator(5))
        axes[0].grid()
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack()

    def create_window():
        list_of_currencies = ["USD", "EUR", "BGN", "PLN", "NOK"]
        layout = [
            [sg.Combo(list_of_currencies, default_value="USD", key="-CURRENCY1-"), sg.Text("to"),
             sg.Combo(list_of_currencies, default_value="EUR", key="-CURRENCY2-"), sg.Text("from"),
             sg.Input(key="-CALENDAR_INPUT_FROM-", enable_events=True, visible=False),
             sg.CalendarButton(button_text=today, target="-CALENDAR_INPUT_FROM-", key="-DATEFROM-", format=("%Y-%m-%d"),
                               enable_events=True),
             sg.Text("to"), sg.Input(key="-CALENDAR_INPUT_TO-", enable_events=True, visible=False),
             sg.CalendarButton(button_text=today, target="-CALENDAR_INPUT_TO-", key="-DATETO-", format=("%Y-%m-%d"),
                               enable_events=True),sg.Push(),
             sg.Button("SUBMIT", size = (7,1))],
            [sg.Text("Today's exchange rate: ", font="14"), sg.Text(key="-TODAYRATE-", enable_events=True), sg.Push(),
             sg.Button("RESET", key = "-AGAIN-", enable_events=True, size=(7,1))],
            [sg.Canvas(key="-CANVAS-")]
        ]
        return sg.Window("X-changeR8 V1.1.1", layout, finalize=True)

    today = str(date.today())
    date_to = today

    window = create_window()

    fig = plt.figure(figsize = (5,4))
    fig.add_subplot(111).plot([],[])
    figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

    while True:
        event, values = window.read(timeout=5)
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-CALENDAR_INPUT_FROM-":
            date_from = values[
                "-CALENDAR_INPUT_FROM-"]
            window["-DATEFROM-"].update(text=date_from)
            window.refresh()
        if event == "-CALENDAR_INPUT_TO-":
            date_to = values[
                "-CALENDAR_INPUT_TO-"]
            window["-DATETO-"].update(text=date_to)
            window.refresh()
        if event == "SUBMIT":
            currency1 = values["-CURRENCY1-"]
            currency2 = values["-CURRENCY2-"]
            if currency1 != "PLN" and currency2 != "PLN":
                url1 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency1}/{date_from}/{date_to}"
                url2 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency2}/{date_from}/{date_to}"
                if get_exchange_data_from_nbp(url1) is None or get_exchange_data_from_nbp(url2) is None:
                    window.close()
                    get_currency_exchange_rate()
                first_currency = get_currency_as_list(url1)
                second_currency = get_currency_as_list(url2)
            else:
                url1 = pln_chosen(currency1, currency2, date_from, date_to)
                if currency1 == "PLN":
                    first_currency = only_ones(url1)
                    second_currency = get_currency_as_list(url1)
                else:
                    first_currency = get_currency_as_list(url1)
                    second_currency = only_ones(url1)
            # today rate:
            today_exchange_rate = round(first_currency[-1] / second_currency[-1], 4)
            window["-TODAYRATE-"].update(today_exchange_rate)

            currency = get_currency_ratio(first_currency, second_currency)

            update_plot(get_date_list(url1), currency)

    window.close()


get_currency_exchange_rate()
