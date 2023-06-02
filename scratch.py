import requests
import json
import pathlib

# def download_images():
#     # with open("launches.json") as f:
#     response = requests.get('https://ll.thespacedevs.com/2.0.0/launch/upcoming')
#     save_file = open("launches.json", "w")  
#     json.dump(response.json(), save_file)  
#     save_file.close()  

# download_images()

with open("launches.json") as f:
    # Ensure directory exists
    pathlib.Path("images").mkdir(parents=True, exist_ok=True)

    launches = json.load(f)
    image_urls = [launch["image"] for launch in launches["results"] ]
    for url in image_urls:
    # try:
        response = requests.get(url)
        image_name = url.split("/")[-1]
        target_file =  f"images/{image_name}"
        with open (target_file, "wb" ) as target:
            # print(target_file)
            target.write(response.content)
        print(f"Downloaded {url} to {target_file}")

    # except :
    #     print(f"{url} appears to be an invalid URL or Could not connect to {url}")
    