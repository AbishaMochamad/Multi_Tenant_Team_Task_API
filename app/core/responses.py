from app.models.commons import ServerErrorResponse

server_error_response = {
    500: {"model": ServerErrorResponse, "detail": "Internal server error."}
}
