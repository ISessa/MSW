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


def format_text_to_send(web_str):
    days = ["Today", "Tomorrow", "2d from now"]
    message_to_print = emoji.emojize("Hey surfer! 🏄\n")
    placeholder_tot_count = 0
    for count,day in enumerate(days):
        active,inactive,placeholder = analyze_stars(web_str,(count+1))
        placeholder_tot_count += placeholder
        day_string = emoji.emojize(f"{day} there will be {active}") + emoji.emojize(f":glowing_star: and ") + emoji.emojize(f"{inactive}:star: \n")
        message_to_print += day_string
    message_to_print += "(Everyday there are max 48 stars in total)"

    return message_to_print,placeholder_tot_count


def main():

    url = 'https://magicseaweed.com/Backdoor-Haifa-Surf-Report/3987/'
    r = requests.get(url)
    text = r.text

    message_to_print,placeholder_flag = format_text_to_send(text)
    max_placeholders = 144 #Max stars in 3 days is 144. If n of days change or n of stars change per day - make sure to chane format_text_to_send as well
    if placeholder_flag != max_placeholders:
        send_to_telegram(message_to_print)

    return

if __name__ == "__main__":
    main()
