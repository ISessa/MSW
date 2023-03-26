import requests
import emoji


def day_place(web_str,n):
    start = web_str.find(f"data-forecast-day='{n}'")
    end = web_str.find(f"data-forecast-day='{n+1}'")
    if end == -1:
        end = len(web_str)

    return start, end


def count_stars(type_str,web_str,start,finish):
    n_type = 0
    for j in range(1, 50):
        type = web_str.find(f'li class="{type_str}',start,finish)
        if type > 0:
            n_type += 1
            start = type + 1
        else:
            break

    return n_type


def send_to_telegram(message):

    apiToken = '6255878974:AAF8zKS_MvKm9zo8OkJvLnTA1veNFzxpV5Q'
    chatID = '828373435'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def analyze_stars(web_str,day):
    s_day_n,e_day_n = day_place(web_str,day)
    active = count_stars("active",web_str,s_day_n,e_day_n)
    inactive = count_stars("inactive",web_str,s_day_n,e_day_n)
    placeholder = count_stars("placeholder",web_str,s_day_n,e_day_n)

    return active,inactive,placeholder


def def_days(web_str):
    days = ["", "","","","","",""]
    start = 0
    for day in range(7):
        day_string = web_str.find("table-header-title",start)
        day_string += 20
        while web_str[day_string] != ' ':
            days[day] += web_str[day_string]
            day_string += 1
        start = day_string
    days[0],days[1] = "Today","Tomorrow"

    return days


def format_text_to_send(web_str,number_of_days):
    days = def_days(web_str)
    message_to_print = emoji.emojize("Hey surfer! 🏄\n")
    active_count,inactive_count = 0,0
    for count,day in enumerate(days):
        active,inactive,placeholder = analyze_stars(web_str,(count+1))
        active_count += active
        inactive_count += inactive
        day_string = emoji.emojize(f"{day} there will be {active}") + emoji.emojize(f":glowing_star: and ") + emoji.emojize(f"{inactive}:star: \n")
        message_to_print += day_string
        if count == (number_of_days - 1):
            break
    message_to_print += "(Everyday there are max 48 stars in total each day)"

    return message_to_print,active_count,inactive_count


def main():

    url = 'https://magicseaweed.com/Backdoor-Haifa-Surf-Report/3987/'
    r = requests.get(url)
    text = r.text

    number_of_days = 3
    message_to_print,active_flag,inactive_flag = format_text_to_send(text,number_of_days)
    if active_flag != 0 and inactive_flag != 0:
        send_to_telegram(message_to_print)

    return

if __name__ == "__main__":
    main()