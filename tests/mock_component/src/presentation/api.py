from src.application.parser import parse_message

from fastapi import APIRouter, Response, status


router = APIRouter()


@router.get("/")
def ping():
    return Response(status_code=status.HTTP_200_OK)


@router.post("/parse_message/{message}")
def parse(message: str):
    result = parse_message(raw_str=message)
    return Response(status_code=status.HTTP_200_OK, content=result.content)
