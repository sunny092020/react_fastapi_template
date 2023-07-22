from app.db import models


def test_get_users(client, test_superuser, superuser_token_headers):
    response = client.get("/api/v1/users", headers=superuser_token_headers)
    assert response.status_code == 200

    users = response.json()

    # Assert that test_superuser is in the response
    assert any(user["email"] == test_superuser.email for user in users)


def test_delete_user(client, test_superuser, test_db, superuser_token_headers):
    before_delete_user_length = len(test_db.query(models.User).all())

    # verify user with id of test_superuser.id exists
    assert test_db.query(models.User).filter(models.User.id == test_superuser.id).first()

    response = client.delete(f"/api/v1/users/{test_superuser.id}", headers=superuser_token_headers)

    after_delete_user_length = len(test_db.query(models.User).all())

    assert response.status_code == 200
    assert before_delete_user_length - 1 == after_delete_user_length

    # verify no user with id of test_superuser.id exists
    assert not test_db.query(models.User).filter(models.User.id == test_superuser.id).first()


def test_delete_user_not_found(client, superuser_token_headers):
    response = client.delete("/api/v1/users/4321", headers=superuser_token_headers)
    assert response.status_code == 404


def test_edit_user(client, test_superuser, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": True,
        "first_name": "Joe",
        "last_name": "Smith",
        "password": "new_password",
    }

    response = client.put(
        f"/api/v1/users/{test_superuser.id}",
        json=new_user,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_user["id"] = test_superuser.id
    new_user.pop("password")
    assert response.json() == new_user


def test_edit_user_not_found(client, test_db, superuser_token_headers):
    new_user = {
        "email": "newemail@email.com",
        "is_active": False,
        "is_superuser": False,
        "password": "new_password",
    }
    response = client.put("/api/v1/users/1234", json=new_user, headers=superuser_token_headers)
    assert response.status_code == 404


def test_get_user(
    client,
    test_user,
    superuser_token_headers,
):
    response = client.get(f"/api/v1/users/{test_user.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == {
        "id": test_user.id,
        "email": test_user.email,
        "is_active": bool(test_user.is_active),
        "is_superuser": test_user.is_superuser,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
    }


def test_user_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/users/123", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_user_me(client, user_token_headers):
    response = client.get("/api/v1/users/me", headers=user_token_headers)
    assert response.status_code == 200


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    response = client.get("/api/v1/users/123")
    assert response.status_code == 401
    response = client.put("/api/v1/users/123")
    assert response.status_code == 401
    response = client.delete("/api/v1/users/123")
    assert response.status_code == 401


def test_unauthorized_routes(client, user_token_headers):
    response = client.get("/api/v1/users", headers=user_token_headers)
    assert response.status_code == 403
    response = client.get("/api/v1/users/123", headers=user_token_headers)
    assert response.status_code == 403
