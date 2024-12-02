from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
    
from tator_bridge.helpers import get_media

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/media/{media_id}")
@limiter.limit("10/minute")
def serve_tator_media(request: Request, media_id: str) -> Response:
    """
    Serves the image from tator with the given ID.

    Args:
        media_id (str): The media ID.

    Raises:
        HTTPException: If the media with that ID wasn't found.

    Returns:
        Response: The image.
    """
    try:
        im = get_media(media_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Media ID not found.")
    
    return Response(content=im, media_type="image/jpeg")
