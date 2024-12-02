from fastapi.testclient import TestClient

from tator_bridge.tator_bridge import app

VALID_IMAGE_ID = 2819860
BAD_IMAGE_ID = 2819863240

client = TestClient(app)

def test_get_image():
    response = client.get(f"/media/{str(VALID_IMAGE_ID)}")
    assert response.status_code == 200
    assert isinstance(response.content, bytes)
    
def test_get_image_bad():
    response = client.get(f"/media/{str(BAD_IMAGE_ID)}")
    assert response.status_code == 404

    