import requests
from bs4 import BeautifulSoup
from etext import send_sms_via_email, send_mms_via_email
from PIL import Image

def get_cookies_of_the_week():
    sub = []
    file_path = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = r"https://crumblcookies.com/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # imgElement1 = soup.find_all('img', alt="A delicious cookie")[1::2][0].attrs['src']
    # file_path.append(imgElement1)
    # imgElement2 = soup.find_all('img', alt="A delicious cookie")[1::2][1].attrs['src']
    # file_path.append(imgElement2)
    # imgElement3 = soup.find_all('img', alt="A delicious cookie")[1::2][2].attrs['src']
    # file_path.append(imgElement3)
    # imgElement4 = soup.find_all('img', alt="A delicious cookie")[1::2][3].attrs['src']
    # file_path.append(imgElement4)
    # imgElement5 = soup.find_all('img', alt="A delicious cookie")[1::2][4].attrs['src']
    # file_path.append(imgElement5)
    # imgElement6 = soup.find_all('img', alt="A delicious cookie")[1::2][5].attrs['src']
    # file_path.append(imgElement6)

    for i in range(6):
        div = soup.find_all('li')[:6][i]
        txtElement = div.attrs
        name = str(txtElement['id'])
        name = name.replace("individual-cookie-flavor-", '')
        # print(name)
        sub.append(name)

        imgElement = soup.find_all('img', alt="A delicious cookie")[1::2][i].attrs['src']
        file_path.append(imgElement)
        # print(imgElement)
        response = requests.get(imgElement)
        with open('temp'+str(i+1)+'.png', 'wb') as file:
            file.write(response.content)

        resize = Image.open('temp'+str(i+1)+'.png')
        resize = resize.resize((300, 300), Image.ANTIALIAS)
        resize.save('temp'+str(i+1)+'.png', optimize=True, quality=95)


    return sub



def main():
    numbers = ["8015648117", "8016287366"
        , "8018666334", "3855526569", "8016986422"
               ]
    with open('keys.txt', 'r') as file:
        key = file.read()
    for number in numbers:
        if number == "8018666334":
            p = "Verizon"
        elif number == "8016986422":
            p = "Verizon"
        elif number == "3855526569":
            p = "Verizon"
        else:
            p = "AT&T"

        try:
            sub = get_cookies_of_the_week()
            messageInit = "Please be patient, it may take a second for all 5 of the weekly cookies to send."
            provider = p
            message = ""

            sender_credentials = ("nathans.robot.assistant@gmail.com", key)

            mime_maintype = "image"
            mime_subtype = "png"

            file_path = 'temp.png'

            send_mms_via_email(
                number,
                messageInit,
                file_path,
                mime_maintype,
                mime_subtype,
                provider,
                sender_credentials,
                subject="Here are the Crumbl cookies for this week:"
            )

            print(f'Successfully sent title to: {number}')

            for j in range(5):

                file_path = "temp"+str(j+2)+".png"

                send_mms_via_email(
                    number,
                    message,
                    file_path,
                    mime_maintype,
                    mime_subtype,
                    provider,
                    sender_credentials,
                    subject=str(sub[j+1])
                )

                print(f'Successfully sent message to: {number}')

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()