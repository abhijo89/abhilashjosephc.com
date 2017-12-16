import requests
from bs4 import BeautifulSoup

s = requests.Session()
res = s.get("https://www.chavaramatrimony.com/CustomerLogin.aspx")
soup = BeautifulSoup(res.text)
vs = soup.find(attrs={"id": "__VIEWSTATE"}).get('value')
# __VIEWSTATEGENERATOR
vsg = soup.find(attrs={"id": "__VIEWSTATEGENERATOR"}).get('value')
data = {
    "ctl00$ContentPlaceHolder1$txtUsername": "CKNR76063",
    "ctl00$ContentPlaceHolder1$txtPassword": "PQH5F",
    "ctl00$ContentPlaceHolder1$lnklogin": "LOG IN",
    "__VIEWSTATE": vs,
    "__VIEWSTATEGENERATOR": vsg,
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "__VIEWSTATEENCRYPTED": "",
    "ctl00$Header$txtUsername": "",
    "ctl00$Header$txtPassword": "",
    "ctl00$Header$txtmail": "",
    "ctl00$Header$txtsearchbyid1": "",
    "ctl00$Header$TextBoxWatermarkExtender1_ClientState": ""
}
res = s.post("https://www.chavaramatrimony.com/CustomerLogin.aspx", data)

res = s.get("https://www.chavaramatrimony.com/Recomended_Matches.aspx")
print(res.text)
