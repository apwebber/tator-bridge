import sys

import pytest
from tator_bridge.helpers import get_media_url, get_media

VALID_IMAGE_ID = 2819860
BAD_IMAGE_ID = 2819863240

def test_get_media_url():
    url = get_media_url(VALID_IMAGE_ID)
    assert isinstance(url, str)
    
def test_get_media_url_bad():
    with pytest.raises(ValueError):
        get_media_url(BAD_IMAGE_ID)

def test_get_media():
    im = get_media(VALID_IMAGE_ID)
    assert isinstance(im, bytes)
    assert sys.getsizeof(im) > 4000
    
def test_get_media_bad():
    with pytest.raises(ValueError):
        get_media(BAD_IMAGE_ID)
