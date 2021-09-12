import os
import requests
import random

from dotenv import load_dotenv


def get_comics_amount():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response["num"]


def download_random_comics(path):
    comics_number = get_comics_amount()
    random_comics = random.randint(1, comics_number)
    url = f"https://xkcd.com/{random_comics}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    link = response["img"]
    download_image(link, path)
    comments = response["alt"]
    return comments


def download_image(link, path):
    response = requests.get(link)
    response.raise_for_status()
    with open(path, "wb") as file:
        file.write(response.content)


def get_upload_url(vk_token):
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": vk_token,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    if response.get("error"):
        raise requests.HTTPError(response["error"]["error_msg"])
    upload_url = response["response"]["upload_url"]
    return upload_url


def send_image_to_vk(upload_url, path):
    with open(path, "rb") as file:
        files = {
            "photo": file,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    response = response.json()
    if response.get("error"):
        raise requests.HTTPError(response["error"]["error_msg"])
    server = response["server"]
    photo = response["photo"]
    image_hash = response["hash"]
    return server, photo, image_hash


def save_image_in_vk(vk_token, server, photo, image_hash):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": vk_token,
        "photo": photo,
        "server": server,
        "hash": image_hash,
        "v": "5.131"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()
    if response.get("error"):
        raise requests.HTTPError(response["error"]["error_msg"])
    response = response["response"][0]
    owner_id = response["owner_id"]
    media_id = response["id"]
    return owner_id, media_id


def publish_comics(vk_token, client_id, group_id, message, path):
    upload_url = get_upload_url(vk_token)
    server, photo, image_hash = send_image_to_vk(upload_url, path)
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
    response.raise_for_status()
    response = response.json()
    if response.get("error"):
        raise requests.HTTPError(response["error"]["error_msg"])


def main():
    path = "comics.png"
    load_dotenv()
    group_id = os.getenv("GROUP_ID")
    client_id = os.getenv("CLIENT_ID")
    vk_token = os.getenv("VK_TOKEN")
    try:
        message = download_random_comics(path)
        publish_comics(vk_token, client_id, group_id, message, path)
    except requests.HTTPError():
        print("requests.HTTPError")
    finally:
        os.remove(path)


if __name__ == "__main__":
    main()