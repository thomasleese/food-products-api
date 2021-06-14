def test_app(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://localhost")
    from food_products_api.worker import app

    assert app
