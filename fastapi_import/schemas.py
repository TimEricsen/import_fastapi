# Файл для всех 'request body' (тело запроса)
from pydantic import BaseModel
from typing import Optional


# Саоздание тела запроса ссылки
class Import(BaseModel):
    get_link: str  # Название(произвольное): тип


# Создание тела обновления полей продукта
class UpdateProduct(BaseModel):
    name: Optional[str] = None
    current_price: Optional[float] = None
    raw_price: Optional[float] = None
    currency: Optional[str] = None
    discount: Optional[str] = None
    likes_count: Optional[str] = None
    is_new: Optional[str] = None
    brand: Optional[str] = None
    brand_url: Optional[str] = None
    codCountry: Optional[str] = None
    variation_0_color: Optional[str] = None
    variation_1_color: Optional[str] = None
    variation_0_thumbnail: Optional[str] = None
    variation_0_image: Optional[str] = None
    variation_1_thumbnail: Optional[str] = None
    variation_1_image: Optional[str] = None
    image_url: Optional[str] = None
