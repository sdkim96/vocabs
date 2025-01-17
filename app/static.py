from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import FileResponse, Response
from fastapi import Request
from pathlib import Path

ROOT = Path(__file__).parent.parent

class UIMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        ui_dir = str(ROOT / "frontend/dist")

        if not request.url.path.startswith("/api") and not request.url.path.startswith("/docs") and not request.url.path.startswith("/redoc"):
            file_path = Path(ui_dir + request.url.path)
            if file_path.exists() and file_path.is_file():
                return FileResponse(path=file_path)
            else:
                index_file = Path(ui_dir + "/index.html")
                if index_file.exists() and index_file.is_file():
                    return FileResponse(path=index_file)
                return Response(content="Not Found", status_code=404)
        response = await call_next(request)
        return response