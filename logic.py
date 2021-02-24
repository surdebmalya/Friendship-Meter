from PIL import Image, ImageFont, ImageDraw
from flask import request
import requests
import base64

def checking_whether_report_bug_clicked():
	name = str(request.form['name'])
	mail = str(request.form['email'])
	msg = str(request.form['message'])
	#print(name, mail, msg)
	#return "OK"
	requests.post('https://sending-data-to-web3forms.surdebmalya11.repl.co/post', json={"name":name, "mail":mail, "msg":msg})
	return "done"


def data_validity(data_1, data_2):
	data_1_valid = False
	temp_arr = []
	for j in data_1:
		temp_arr.append(ord(j))
	if len(temp_arr)==0:
		pass
	else:
		if len(set(temp_arr))==1 and temp_arr[0]==32:
			pass
		else:
			for i in data_1:
				if ord(i) >= 97 and ord(i) <= 122:
					data_1_valid = True
				else:
					if ord(i) >= 65 and ord(i) <= 90:
						data_1_valid = True
					else:
						if ord(i) == 32:
							data_1_valid = True
						else:
							data_1_valid = False
							break

	data_2_valid = False
	temp_arr = []
	for j in data_2:
		temp_arr.append(ord(j))
	if len(temp_arr)==0:
		pass
	else:
		if len(set(temp_arr))==1 and temp_arr[0]==32:
			pass
		else:
			for i in data_2:
				if ord(i) >= 97 and ord(i) <= 122:
					data_2_valid = True
				else:
					if ord(i) >= 65 and ord(i) <= 90:
						data_2_valid = True
					else:
						if ord(i) == 32:
							data_2_valid = True
						else:
							data_2_valid = False
							break

	return data_1_valid, data_2_valid


def spacing_controll(data_1, data_2):
    data_1_list = data_1.split()
    data_2_list = data_2.split()

    normalized_data_1 = " ".join(data_1_list)
    normalized_data_2 = " ".join(data_2_list)

    return normalized_data_1, normalized_data_2


def friendship_calculation(person1, person2):
    ultimate_string = ""
    for _ in range(len(person1)):
        ultimate_string += person1[_].upper()
    ultimate_string += " FRIENDS "
    for _ in range(len(person2)):
        ultimate_string += person2[_].upper()
    existing_letters = []
    for _ in range(len(ultimate_string)):
        if (ultimate_string[_]
                not in existing_letters) and (ultimate_string[_] != " "):
            existing_letters.append(ultimate_string[_])
    counting = []
    for _ in range(len(existing_letters)):
        current_letter = existing_letters[_]
        count = 0
        for k in ultimate_string:
            if current_letter == k:
                count += 1
        counting.append(count)
    value = 0
    index = 0
    for _ in range(len(counting) - 1, -1, -1):
        value += int(counting[_]) * pow(10, index)
        index += 1
    while value > 100:
        temp = []
        isEven = False
        if len(counting) % 2 == 0:
            isEven = True
        current_position = 0
        for _ in range(len(counting) // 2):
            current_position = _
            first_value = counting[_]
            last_value = counting[-(_ + 1)]
            temp.append(first_value + last_value)
        if not (isEven):
            temp.append(counting[current_position + 1])
        counting = temp
        value = 0
        index = 0
        for _ in range(len(counting) - 1, -1, -1):
            value += int(counting[_]) * pow(10, index)
            index += 1
    return str(value) + "%"


def update_img_locally(data_1, data_2, result):
    im = Image.open('static/bg.PNG')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('DejaVuSansMono.ttf', 40, encoding='unic')
    textToDraw = "Friendship Between\n" + data_1 + "\n&\n" + data_2 + "\n" + result
    draw.multiline_text((250, 150),
                        textToDraw, (255, 255, 255),
                        font=font,
                        stroke_width=1,
                        align='center')
    im.save("temp/temp_image.PNG")


def upload_imgbb_server():
    with open("temp/temp_image.PNG", "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": '********',
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
    return res.json()['data']['url']
