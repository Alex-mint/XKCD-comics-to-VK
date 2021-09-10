import os
import requests
import random

from dotenv import load_dotenv


def get_comics_amount():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.status_code
    response = response.json()
    return response["num"]


def fetch_comics(path):
    comics_number = get_comics_amount()
    choice_comics = random.randint(1, comics_number)
    url = f"https://xkcd.com/{choice_comics}/info.0.json"
    response = requests.get(url)
    response.status_code
    response = response.json()
    link = response["img"]
    download_image(link, path)
    comments = response["alt"]
    return comments


def download_image(link, path):
    response = requests.get(link)
    response.status_code
    with open(path, "wb") as file:
        file.write(response.content)


def get_upload_url(vk_token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": vk_token,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    response.status_code
    upload_url = response.json()["response"]["upload_url"]
    return upload_url


def send_image_to_vk(upload_url):
    with open('comics.png', 'rb') as file:
        files = {
            "photo": file,
        }
        response = requests.post(upload_url, files=files)
        response.status_code
        response = response.json()
        server = response["server"]
        photo = response["photo"]
        image_hash = response["hash"]
        return server, photo, image_hash


def save_image_in_vk(vk_token,server, photo, image_hash):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": vk_token,
        "photo": photo,
        "server": server,
        "hash": image_hash,
        "v": "5.131"
    }
    response = requests.post(url, params=params)
    response.status_code
    response = response.json()["response"][0]
    owner_id = response["owner_id"]
    media_id = response["id"]
    return owner_id, media_id


def publishing_comics(vk_token, client_id, group_id, message):
    upload_url = get_upload_url(vk_token)
    server, photo, image_hash = send_image_to_vk(upload_url)
    owner_id, media_id = save_image_in_vk(vk_token, server, photo, image_hash)
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": vk_token,
        "owner_id": int(f"-{group_id}"),
        "from_group": client_id,
        "attachments": f"photo{owner_id}_{media_id}",
        "message": message,
        "v": "5.131"
    }
    response = requests.post(url, params=params)
    response.status_code


def main():
    load_dotenv()
    group_id = os.getenv("GROUP_ID")
    path = "comics.png"
    client_id = os.getenv("CLIENT_ID")
    vk_token = os.getenv("VK_TOKEN")
    message = fetch_comics(path)
    publishing_comics(vk_token, client_id, group_id, message)
    os.remove(path)


if __name__ == "__main__":
    main()