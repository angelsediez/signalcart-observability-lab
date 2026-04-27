def test_product_order_and_checkout_flow(client):
    product_response = client.post(
        "/products",
        json={
            "name": "Demo Keyboard",
            "price": 49.99,
            "stock": 10,
        },
    )

    assert product_response.status_code == 201
    product = product_response.json()

    order_response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": product["id"],
                    "quantity": 2,
                }
            ]
        },
    )

    assert order_response.status_code == 201
    order = order_response.json()

    assert order["status"] == "created"
    assert order["total"] == 99.98

    checkout_response = client.post(
        "/checkout",
        json={"order_id": order["id"]},
    )

    assert checkout_response.status_code == 200
    checkout = checkout_response.json()

    assert checkout["status"] == "checked_out"
    assert checkout["total"] == 99.98
    assert checkout["message"] == "checkout completed"


def test_order_creation_rejects_missing_product(client):
    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": 999,
                    "quantity": 1,
                }
            ]
        },
    )

    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]
