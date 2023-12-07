import logging

import pyrebase
import firebase_admin
from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from source.config.settings import FIREBASE_CONFIG
from source.schemas.AuthenticationSchemas import SignUpSchema, LoginSchema

if not firebase_admin._apps:
    cred = credentials.Certificate("/Users/lucyvelasco/PycharmProjects/jus_crawler/serviceAccount.json")
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/cadastro")
async def create_an_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        return JSONResponse(content={"message": f"User account created successfuly for user {user.uid}"},
                            status_code=201
                            )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail=f"Account already created for the email {email}"
        )


@router.post("/login")
async def create_access_token(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email,
            password=password
        )
        token = user['idToken']
        return JSONResponse(
            content={
                "token": token
            }, status_code=200
        )
    except HTTPException:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )


@router.post("/ping")
async def validate_token(request: Request):
    headers = request.headers
    jwt = headers.get('authorization')

    user = auth.verify_id_token(jwt)

    return user['user_id']
