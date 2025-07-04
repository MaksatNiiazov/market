"""
Service for working with external product API.
"""
import base64
import enum
from enum import Enum
from http import HTTPStatus
from typing import Any
from uuid import UUID
from http import HTTPStatus
from typing import Any
import requests
from django.conf import settings
from pydantic import BaseModel


class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"


class ExternalProductCreateSchema(BaseModel):
    title: str
    supplier: str
    category_public_id: str
    brand: str | None = None
    sex: Sex | None = None
    description: str | None = None
    photo_path: str
    provider_id: str

    class Config:
        from_attributes = True


class ExternalProductVariantCreateSchema(BaseModel):
    sku: str
    base_price: float
    cost_price: float
    options_public_ids: list[str]
    photo_path: str
    quantity: int = 0

    class Config:
        from_attributes = True


class SourceService(str, enum.Enum):
    TANDA = "tanda"


class ExternalProductCreateRequest(BaseModel):
    information: ExternalProductCreateSchema
    variants: list[ExternalProductVariantCreateSchema]
    source_service: SourceService

    class Config:
        from_attributes = True


class OptionTypeResponse(BaseModel):
    id: int
    name: str
    code: str | None = None

    class Config:
        from_attributes = True


class OptionValueResponse(BaseModel):
    id: int
    value: str
    value_metadata: dict[str, Any] | None = None
    option_type: OptionTypeResponse

    class Config:
        from_attributes = True


class VariantOptionResponse(BaseModel):
    id: int
    option_value: OptionValueResponse

    class Config:
        from_attributes = True


class ProductVariantResponse(BaseModel):
    id: int
    public_id: UUID
    sku: str | None = None
    provider_sku: str | None = None
    price: float | None = None
    variant_options: list[VariantOptionResponse] = []
    quantity: int | None = 0
    is_defective: bool
    photos: list[str]


class ProductCreateResponse(BaseModel):
    id: int
    public_id: UUID
    title: str
    description: str | None = None
    slug: str
    base_price: float
    supplier: str
    brand: str | None = None
    sex: Sex | None = None
    category_id: int
    status: str
    photos: list[str] = []
    variants: list[ProductVariantResponse] = []
    provider_name: str
    provider_sku: str | None = None
    total_quantity: int = 0


def get_access_token() -> str:
    """
    Get access token from SSO service.

    Returns:
        str: Access token
    """
    client_id = settings.M2M_SSO_CLIENT_ID
    client_secret = settings.M2M_SSO_CLIENT_SECRET
    sso_token_url = settings.SSO_TOKEN_URL

    credential = f"{client_id}:{client_secret}"
    code = base64.b64encode(credential.encode("utf-8"))

    payload = {
        "grant_type": "client_credentials",
    }

    response = requests.post(
        sso_token_url,
        data=payload,
        timeout=20,
        headers={
            "Authorization": f"Basic {code.decode('utf-8')}",
            "Cache-Control": "no-cache",
        },
    )

    response_data = response.json()
    return response_data.get("access_token")


def create_external_product(product_data: ExternalProductCreateRequest) -> ProductCreateResponse:
    """
    Create product in external service.

    Args:
        product_data: Product data

    Returns:
        ExternalProductCreateResponse: Created product data
    """
    base_url = settings.EXTERNAL_PRODUCT_API_URL
    access_token = get_access_token()
    response = requests.post(
        f"{base_url}/api/external/products/",
        json=product_data.model_dump(),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != HTTPStatus.OK:
        message = f"Failed to create product in external service: {response.text}"
        raise ValueError(message)
<<<<<<< HEAD
    return ProductCreateResponse(**response.json())


=======

    return ProductCreateResponse(**response.json())

>>>>>>> cef0015ae8a7b7fd390bad6b092bca56d970e0fc
class ExternalProductUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    brand: str | None = None
    category_public_id: str | None = None

    class Config:
        from_attributes = True


def update_external_product(product_public_id: str, product_data: ExternalProductUpdateRequest) -> None:
    """Update product in external service."""
    base_url = settings.EXTERNAL_PRODUCT_API_URL
    access_token = get_access_token()
    response = requests.patch(
        f"{base_url}/api/external/products/{product_public_id}/",
        json=product_data.model_dump(exclude_none=True),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    if response.status_code != HTTPStatus.OK:
        message = f"Failed to update product in external service: {response.text}"
        raise ValueError(message)
