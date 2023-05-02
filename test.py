import requests

url = " http://127.0.0.1:5000/scrape?url=https://fr.aliexpress.com/item/32864744166.html?spm=a2g0o.productlist.main.81.1af436a9CnLUyE&algo_pvid=307358c7-0123-43b1-986b-565a57b0bb71&algo_exp_id=307358c7-0123-43b1-986b-565a57b0bb71-20&pdp_npi=3%40dis%21MAD%21189.64%21115.68%21%21%21%21%21%40211be72e16826161577145301d079b%2165514016856%21sea%21MA%21913694033&curPageLogUid=Rh1GDuEoG5bE&gatewayAdapt=glo2fra"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error: ", response.status_code)
