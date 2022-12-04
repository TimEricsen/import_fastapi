from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
import schemas, database, models
import pandas as pd
import datetime

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI() # Создание API приложения


# Получаем базу данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Post запрос на импорт
@app.post('/import', tags=['Import'])
def post_import(request: schemas.Import, response: Response, db: Session = Depends(get_db)):
    try:
        reader = pd.read_csv(request.get_link)
        reader.drop_duplicates(subset=['id'])
        reader.to_sql(name='temp_products', con=database.engine, if_exists='replace', index=False)
        db.execute('''REPLACE INTO products SELECT * FROM temp_products''')
        db.commit()
        new_import = models.Import(link=request.get_link, date_time=datetime.datetime.now())
        db.add(new_import)
        db.commit()
        db.refresh(new_import)
        response.status_code = status.HTTP_201_CREATED
        return f'Импорт {new_import.id} по ссылке {new_import.link} выполнен успешно.'
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': f'При импорте по запросу: {request.get_link} произошла ошибка.',
                'detail': 'Ссылка не актуальна или файл повреждён.'}


# Get запрос на получение импорта
@app.get('/import/{id}', tags=['Import'])
def get_import(id, db: Session = Depends(get_db)):
    imprt = db.query(models.Import).filter(models.Import.id == id).first()
    if not imprt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Импорт не найден.')
    return f'Импорт {imprt.id} по запросу {imprt.link}'


# Get запрос на получение списка продуктов по переданным параметрам from и to
@app.get('/product', tags=['Products'])
def get_products(from_price: float = 0, to_price: float = 1000,  db: Session = Depends(get_db)):
    try:
        if from_price < to_price and from_price >= 0:
            products = db.query(models.Products).filter(models.Products.current_price >= from_price,
                                                        models.Products.current_price <= to_price).all()
            product_list = list(products)
            imprt = db.query(models.Import).order_by(models.Import.id.desc()).first()
            return {'last successful import': imprt.date_time[:19], 'products': product_list}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Данные невозможно обработать, неверный запрос.')
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Данные невозможно обработать, неверный запрос.')


# Delete запрос на удаление продукта по полученному id
@app.delete('/product/{id}', tags=['Products'])
def delete_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).delete(synchronize_session=False)
    db.commit()
    if product:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Продукт успешно удалён!')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Продукт с id {id} не найден.')


# Patch запрос на частичное обновление любых полей продукта, полученного по id
@app.patch('/product/{id}', tags=['Products'])
def update_product(id, request: schemas.UpdateProduct, db: Session = Depends(get_db)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Продукт с id {id} не найден.')
    product_data = request.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail='Информация о продукте успешно обновлена!')
