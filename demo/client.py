import requests
import prettytable as pt
url_h = "http://127.0.0.1:8000/"
#Initializing sessionid
sessionid = None
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
        url = url_h + "up/register/"
        data = {"username":username,"password":password,"email":email}
        r = requests.post(url,data=data)
        print (r.text)
    elif val[0] == 'login':
        url = url_h + "up/login/"
        username = input("Please enter your username:")
        password = input("Please enter your password:")
        payload = {'username':username,'password':password}
        r = requests.post(url,data = payload)
        if r.status_code == 200:
            print (r.text)
            sessionid = r.headers['Set-Cookie'].split(";")[0]
        else:
            print ("You may enter the wrong username or password!")

    elif val[0] == 'logout':
        url = url_h + "up/logout/"
        headers = {'Cookie': sessionid}
        data = {"null":"null"}
        r = requests.post(url,data,headers=headers)
        print (r.text)
        #Set sessionid to None
        sessionid = None
    elif val[0] == 'list':
        url = url_h + "up/modules/"
        r = requests.get(url)
        #Formatting the message to let prettytable output it
        text = str(r.text).strip('"') #remove "
        text = text.split("\\n")#Notice that the last element is empty
        #Split the message by ;
        for i in range(len(text)):
            text[i] = text[i].split(";")
        tb = pt.PrettyTable()
        #text[0] is the table header
        tb.field_names = text[0]
        #The last row will only have one element
        for i in text[1:-1]:
            tb.add_row(i)
        #Print the prettytable
        print (tb)
    elif val[0] == 'view':
        url = url_h + "up/allavg/"
        payload = {"data":"data"}
        r = requests.post(url)
        r = r.text.strip('"').split(";")
        for i in r:
            print(i)
    elif val[0] == 'average':
        url = url_h + "up/avg/"
        p_id = val[1]
        module_id = val[2]
        payload = {"p_id":p_id,"module_id":module_id}
        r = requests.post(url,payload)
        print (r.text.strip('"'))
    elif val[0] == 'rate':
        professor = val[1]
        module = val[2]
        year = val[3]
        semester = val[4]
        score = val[5]
        url = url_h + "scores/"
        data = {"score":score,"professor":professor,"module":module,"semester":semester,"year":year}
        if sessionid is not None:
            headers = {'Cookie': sessionid}
            r = requests.post(url,data,headers=headers)
            if r.status_code == 201:
                print ("Rating successful!")
            else:
                print ("Rating error!")
        else: 
            print ("You havn't logged in yet!")
    else:
        print ("You havn't print the correct commands!\n")