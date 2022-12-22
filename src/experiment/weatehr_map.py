from requests import request

headers = {
    "Accept": "application/json",
    "X-IBM-Client-Id": "6669c0fc737fbddf713bcdfa29b3b6ff",
    "X-IBM-Client-Secret": "866d29562ee1974a457ead8524d45d41"
}

#order_id = "o140350685783"
order_id = "o103308197002"

response = request(
    "GET",
    f"https://api-metoffice.apiconnect.ibmcloud.com/map-images/1.0.0/orders/{order_id}/latest",
    headers=headers)

print(f"{response.content}")

headers2 = {
    "Accept": "image/png",
    "X-IBM-Client-Id": "6669c0fc737fbddf713bcdfa29b3b6ff",
    "X-IBM-Client-Secret": "866d29562ee1974a457ead8524d45d41"
}

parameters = {
    "includeLand": "true"
}

file_id = "temperature_at_surface_ts21_2022121212"
url = f"https://api-metoffice.apiconnect.ibmcloud.com/map-images/1.0.0/orders/{order_id}/latest/{file_id}/data"

response = request(
    "GET",
    url,
    headers=headers2)

f = open("test.png", "wb")
f.write(response.content)
f.close()
