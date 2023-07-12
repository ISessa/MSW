import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import emoji


def send_to_telegram(message):
    apiToken = '6255878974:AAF8zKS_MvKm9zo8OkJvLnTA1veNFzxpV5Q'
    chatID = '828373435'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def analyze_url_data(url):
    def cut_relevant_part(full_status_str):
        str_start = full_status_str.find('>')
        str_end = full_status_str.find('<', 1)
        relevant_status_str = full_status_str[str_start + 1:str_end]

        return relevant_status_str

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)
    driver.get(url)

    statuses = driver.find_elements("xpath", "//div[contains(@class, 'RatingsCell')][.//span]")
    for i, status in enumerate(statuses):
        status_str = status.get_attribute("innerHTML")
        statuses[i] = cut_relevant_part(status_str)

    days = driver.find_elements("xpath", "//div[contains(@class, 'TableDayContainer_dayHeading')][.//h6]")
    for i, day in enumerate(days):
        day_str = day.get_attribute("innerHTML")
        days[i] = cut_relevant_part(day_str)

    driver.close()

    return statuses, days


def format_message(conditions, days):
    message_to_print = emoji.emojize("Hey surfer! 🏄\n "
                                     "In the next three evenings the conditions will be:\n"
                                     f"{days[0]}: {conditions[2]}\n"
                                     f"{days[1]}: {conditions[5]}\n"
                                     f"{days[2]}: {conditions[8]}\n")
    for i, condition in enumerate(conditions):
        if condition == "FAIR" and (i % 3) == 2:
            message_to_print += f"\n{days[int((i + 1) / 3)]}, evening you should go surf.\n"
        elif condition == "GOOD" or condition == "FAIR TO GOOD":
            if (i % 3) == 0:
                time_of_day = "morning"
            elif (i % 3) == 1:
                time_of_day = "noon"
            elif (i % 3) == 2:
                time_of_day = "evening"
            else:
                time_of_day = "error"
            message_to_print += f"\n{days[int((i + 1) / 3)]}, {time_of_day} the waves are fucking awsome!!\n"

    return message_to_print


def main():
    url = 'https://www.surfline.com/surf-report/bat-galim/584204204e65fad6a7709139?view=table'
    # url = 'https://www.surfline.com/surf-report/la-perouse-bay/5842041f4e65fad6a7708de2?view=table' #its in hawaii
    conditions, days = analyze_url_data(url)
    message = format_message(conditions, days)
    send_to_telegram(message)

    return


if __name__ == "__main__":
    main()
