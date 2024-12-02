import datetime
import os
import requests
import tator
from tator.openapi.tator_openapi.exceptions import ApiException
from cachier import cachier
from dotenv import load_dotenv

PRESIGNED_VAL_SECONDS = 43200

load_dotenv()

def get_tator_url() -> str:
    return os.environ["tator_url"]

def get_token() -> str: 
    return os.environ["tator_token"]

def get_tator_api() -> tator.api:
    return tator.get_api(get_tator_url(), get_token())

@cachier(stale_after=datetime.timedelta(seconds=PRESIGNED_VAL_SECONDS))
def get_media_url(media_id: int) -> str:
    """
    Get the media URL. Returns the first url with image/jpeg mime type.
    Uses cachier to cache the URl.

    Args:
        media_id (int): Tator media ID

    Raises:
        ValueError: If tator can't find the media with the given ID

    Returns:
        str: The url to the media
    """
    api = get_tator_api()
    
    try:
        m = api.get_media(media_id, presigned=PRESIGNED_VAL_SECONDS)
    except ApiException:
        raise ValueError("Unknown media ID")
    
    images = m.media_files.image
    images = [i for i in images if i.mime == 'image/jpeg']
    return images[0].path

def get_media(media_id: int) -> bytes:
    """
    Fetches the media with the given ID.

    Args:
        media_id (int): The media ID

    Returns:
        bytes: The image as bytes
    """
    url = get_media_url(media_id)
    return requests.get(url).content