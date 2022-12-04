# Файл для создания моделей(таблиц) БД.
from database import Base
from sqlalchemy import Column, Integer, String, Float


# Класс создания таблицы в БД для записи импортов.
class Import(Base):
    __tablename__ = 'imports'

    id = Column(Integer, primary_key=True, index=True)
    link = Column(String)
    date_time = Column(String)


# Класс создания таблицы в БД для товаров.
class Products(Base):
    __tablename__ = 'products'

    category = Column(String)
    subcategory = Column(String)
    name = Column(String)
    current_price = Column(Float)
    raw_price = Column(Float)
    currency = Column(String)
    discount = Column(String)
    likes_count = Column(String)
    is_new = Column(String)
    brand = Column(String)
    brand_url = Column(String)
    codCountry = Column(String)
    variation_0_color = Column(String)
    variation_1_color = Column(String)
    variation_0_thumbnail = Column(String)
    variation_0_image = Column(String)
    variation_1_thumbnail = Column(String)
    variation_1_image = Column(String)
    image_url = Column(String)
    url = Column(String)
    id = Column(String, primary_key=True)
    model = Column(String)


# Класс для создания временной таблицы для товаров в БД
class TempProducts(Base):
    __tablename__ = 'temp_products'

    category = Column(String)
    subcategory = Column(String)
    name = Column(String)
    current_price = Column(Float)
    raw_price = Column(Float)
    currency = Column(String)
    discount = Column(String)
    likes_count = Column(String)
    is_new = Column(String)
    brand = Column(String)
    brand_url = Column(String)
    codCountry = Column(String)
    variation_0_color = Column(String)
    variation_1_color = Column(String)
    variation_0_thumbnail = Column(String)
    variation_0_image = Column(String)
    variation_1_thumbnail = Column(String)
    variation_1_image = Column(String)
    image_url = Column(String)
    url = Column(String)
    id = Column(String, primary_key=True)
    model = Column(String)
