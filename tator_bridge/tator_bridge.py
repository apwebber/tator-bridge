import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response

from tator_bridge.helpers import get_media

app = FastAPI()


@app.get("/media/{media_id}")
def serve_tator_media(media_id: str):
    try:
        im = get_media(media_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Media ID not found.")
    
    return Response(content=im, media_type="image/jpeg")
