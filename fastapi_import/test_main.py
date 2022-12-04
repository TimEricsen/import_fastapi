from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_import():
    r = client.get('/import/1')
    assert r.status_code == 200
    assert r.json() == 'Импорт 1 по запросу https://query.data.world/s/s5gt6acvtmeahnaha2epnhlnxdiw3e'


def test_get_product():
    r = client.get('/product?from_price=15&to_price=14')
    assert r.status_code == 400
    assert r.json() == {
        'detail': 'Данные невозможно обработать, неверный запрос.'
    }


def test_delete_product():
    r = client.delete('/product/123123')
    assert r.status_code == 404
    assert r.json() == {
        'detail': 'Продукт с id 123123 не найден.'
    }
