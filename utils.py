from melipayamak import Api


def send_sms_code(mobile, code):
    username = '-'
    password = '-'
    api = Api(username, password)
    sms = api.sms()
    to = mobile
    _from = '-'
    text = f'Your code is {code}'
    response = sms.send(to, _from, text)
    print(response)
