from fastapi import APIRouter, HTTPException, status
import requests
import json
from schemas.auth import UserRequest, UserResponse
from core.settings import settings
from modules.token import Token


router = APIRouter()

token = Token()


@router.post("/create", response_model=UserResponse)
async def create_user(user: UserRequest):
    headers = {
        'Content-Type': 'application/json'
    }

    body = {
        'email': str(user.email),
        'password': user.password,
        'returnSecureToken': True
    }

    try:
        response = requests.post(
            url=f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={settings.fire_base_api_key}",
            headers=headers,
            data=json.dumps(body)
        )
        data = response.json()

        if 'error' in data:
            raise HTTPException(status_code=400, detail=data['error']['message'])

        jwt_token = token.create_access_token(
            {
                "email": str(user.email),
                "id": data["localId"]
            }
        )
        print(f"Token: {jwt_token}")
        return UserResponse(jwt_token=jwt_token)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=UserResponse)
async def login(user: UserRequest):
    headers = {
        'Content-Type': 'application/json'
    }

    body = {
        'email': str(user.email),
        'password': user.password,
        'returnSecureToken': True
    }

    try:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.fire_base_api_key}"
        response = requests.post(url, headers=headers, data=json.dumps(body))

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        user_data = response.json()

        if 'error' in user_data:
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        jwt_token = token.create_access_token(
            {
                "email": str(user.email),
                "id": user_data["localId"]
            }
        )

        return UserResponse(jwt_token=jwt_token)

    except requests.RequestException as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
