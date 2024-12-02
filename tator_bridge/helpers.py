import datetime
import io
import os
import requests
import tator
from tator.openapi.tator_openapi.exceptions import ApiException
from cachier import cachier

PRESIGNED_VAL_SECONDS = 43200
IMAGE_CACHE_DAYS = 30

def get_tator_url() -> str:
    return os.environ["tator_url"]


def get_token() -> str:
    return os.environ["tator_token"]

def get_tator_api() -> tator.api:
    return tator.get_api(get_tator_url(), get_token())

@cachier(stale_after=datetime.timedelta(seconds=PRESIGNED_VAL_SECONDS))
def get_media_url(media_id: int) -> str:
    api = get_tator_api()
    
    try:
        m = api.get_media(media_id, presigned=PRESIGNED_VAL_SECONDS)
    except ApiException:
        raise ValueError("Unknown media ID")
    
    images = m.media_files.image
    images = [i for i in images if i.mime == 'image/jpeg']
    return images[0].path

@cachier(stale_after=datetime.timedelta(days=IMAGE_CACHE_DAYS))
def get_media(media_id: int) -> bytes:
    url = get_media_url(media_id)
    return requests.get(url).content