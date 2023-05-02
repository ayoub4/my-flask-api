import requests

url = " http://127.0.0.1:5000/scrape?url=https://fr.aliexpress.com/item/1005003082438274.html?spm=a2g0o.detail.1000014.55.6ec9G9ATG9AT3p&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40000.326746.0&scm_id=1007.40000.326746.0&scm-url=1007.40000.326746.0&pvid=2f9c2c0d-598a-41db-9421-40e79d530a86&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40000.326746.0,pvid:2f9c2c0d-598a-41db-9421-40e79d530a86,tpp_buckets:668%232846%238111%23466&pdp_npi=3%40dis%21EUR%215.03%214.03%21%21%21%21%21%402103246616812138165248249e0bd6%2112000023973107639%21rec%21FR%214452666233"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Error: ", response.status_code)
