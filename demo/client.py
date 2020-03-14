import requests

while(True):
    val = input("Please enter your command:")
    val = val.split(" ")
    if val[0] == 'exit':
        print ("Thank you for using the rating system!")
        break
    elif val[0] == 'register':
        username = input("Please enter your username:")
        email = input("Please enter your email:")
        password = input("Please enter your password:")
        url = "http://zhiweiren1997.pythonanywhere.com/up/register/"
        data = {"username":username,"password":password}
        r = requests.post(url,data=data)
        if r.status_code == 200:
            print ("You have successfully registered!")
        else:
            print ("Registration error!")
    elif val[0] == 'login':
        url = "http://zhiweiren1997.pythonanywhere.com/up/login/"
        username = input("Please enter your username:")
        password = input("Please enter your password:")
        payload = {'username':username,'password':password}
        r = requests.post(url,data = payload)
        if r.status_code == 200:
            print (r.text)
            sessionid = r.headers['Set-Cookie'].split(";")[0]
        else:
            print (r.text)
        
    elif val[0] == 'test':
        pass
    elif val[0] == 'logout':
        url = "http://zhiweiren1997.pythonanywhere.com/up/logout/"
        headers = {'Cookie': sessionid}
        data = {"null":"null"}
        r = requests.post(url,data,headers=headers)
        print (r.text)
        for k,v in r.text.item():
            print (v)
    elif val[0] == 'list':
        url = "http://zhiweiren1997.pythonanywhere.com/up/modules/"
        r = requests.get(url)
        print (r.text)
    elif val[0] == 'view':
        url = "http://zhiweiren1997.pythonanywhere.com/up/allavg/"
        payload = {"data":"data"}
        r = requests.post(url)
        print (r.text)
    elif val[0] == 'average':
        url = "http://zhiweiren1997.pythonanywhere.com/up/avg/"
        p_id = val[1]
        module_id = val[2]
        payload = {"p_id":p_id,"module_id":module_id}
        r = requests.post(url,payload)
        print (r.text)
    elif val[0] == 'rate':
        professor = val[1]
        module = val[2]
        score = val[5]
        url = "http://zhiweiren1997.pythonanywhere.com/scores/"
        data = {"score":score,"professor":professor,"module":module}
        headers = {'Cookie': sessionid}
        r = requests.post(url,data,headers=headers)
        print (r.text)