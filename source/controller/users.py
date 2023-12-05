import pyrebase
import firebase_admin
from fastapi import APIRouter
from firebase_admin import credentials
from source.config.settings import FIREBASE_CONFIG
from source.schemas.AuthenticationSchemas import SignUpSchema

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
    pass


@router.post("/login")
async def create_access_token():
    pass


@router.post("/ping")
async def validate_token():
    pass
