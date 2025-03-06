from melipayamak import Api


def send_sms_code(mobile, code):
    username = '09190978688'
    password = 'QPNCT'
    api = Api(username, password)
    sms = api.sms()
    to = mobile
    _from = '50002710078687'
    text = f'Your code is {code}'
    response = sms.send(to, _from, text)
    print(response)
