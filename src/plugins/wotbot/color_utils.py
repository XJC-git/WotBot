def set_power_color(input):
    num = int(input)
    if num < 500:
        return "#FE7903"
    elif num < 700:
        return "#44B300"
    elif num < 900:
        return "#02C9B3"
    elif num < 1100:
        return "#D042F3"
    else:
        return "#A00DC5"

def set_win_color(input):
    num = input
    if input is str and input.__contains__("%"):
        num = num.replace('%','')
    num = int(num)
    if num < 45:
        return "#FE7903"
    elif num < 48:
        return "#44B300"
    elif num < 50:
        return "#02C9B3"
    elif num < 53:
        return "#D042F3"
    else:
        return "#A00DC5"
