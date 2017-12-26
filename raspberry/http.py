import requests

def classify(file_name):
    url = 'http://192.168.0.133:5000/classify/'
    file = open(file_name,'rb')
    r = requests.post(url,files={'image':file}, data={'file_name':file_name})
    return r.text