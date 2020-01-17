"""
Tests for jwt flask app.
"""
import os
import json
import pytest

import src.api as api

SECRET = "TestSecret"
TOKEN_ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qVXlOems0TmpSRE4wRkdNVVJCTkVaQk1FSkNSa1UzTURnelJrTXhNVGN5UWpReVFqVXhNQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQta3ppbm1yLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTIwMDFkNmRhMjI0NjBlYTI4ZDk1ZjgiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTc5MjQ5Njk5LCJleHAiOjE1NzkyNTY4OTksImF6cCI6IkliZG52U1NtdElldFUwMkhqS01DeDA4YWl5cWxVUk93Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.S8U3K_2ZWUR_yqXPzkn_lnN1dgpGvlmu4xnURozeOnmrh8bGFt3EDwH7QWkZ_KUz6Euecr0bIpxEtfX0DOSp7p_fpnSkpu8Avjir-fkURAX8g5YLubt4OM8ogDVmv-McjY5D5mJv0cjGh5zD237EpJxUVvqEZx1rsUCBVf7ffp7zwHK5DkqjttJUmi45tHrw4lqBW-095ToHPVqN5wsRidjNsvqY_7hyD7VOqRnDhuZ-0hzBxUl2P_Mq70XsV-Vla_WJ1xq7pUcTd8L1uZ33BMNcZY39b_lNYNqVgSc_DocVdXnKFpQO7cFaFyVTbnvas3D1EMCtVq8wx0X-8pU6WA"
TOKEN_DIRECTOR = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qVXlOems0TmpSRE4wRkdNVVJCTkVaQk1FSkNSa1UzTURnelJrTXhNVGN5UWpReVFqVXhNQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQta3ppbm1yLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTFkOTE3NGJhZTA0YzBkYmVjNTY2ZmMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTc5MjQ5OTg2LCJleHAiOjE1NzkyNTcxODYsImF6cCI6IkliZG52U1NtdElldFUwMkhqS01DeDA4YWl5cWxVUk93Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.OMonJhtzEm-KFU3tODXaoQ5lJ_Q0MjVAc1lu-x-r8p2e6EEROi0mDm8qb-KpNgQEsuCjHW8ui1OgfT_xRrw0q3_SRHfAQ7uq2i1Dc8PaVbE9hcrAWN0X4xSwxjnnJJ_vytjYO41VCqrVEaCOzy57XURDtxnGLy8ZBCKbMkDsyBWtgj5Ekzqcm9fsS_UW8I6JKaO2tVR8f1lnVBDgXXIiT2gxajfF3bUjleHAoU069G6dcN4CBIN3pND_cQoAn6MRvD-Cd211MQA9G4qdcuJQ_6ZTbT5pCWIK2Yf4gfI82dveEq4NvSUuf0a7Xt833dQ4fFUhkopymJXIEFlh4_wFCA"
TOKEN_PRODUCER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qVXlOems0TmpSRE4wRkdNVVJCTkVaQk1FSkNSa1UzTURnelJrTXhNVGN5UWpReVFqVXhNQSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQta3ppbm1yLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTFkOTE5YmU5Y2RlMTBlN2JlYmE1ZTgiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNTc5MjQ5NjA2LCJleHAiOjE1NzkyNTY4MDYsImF6cCI6IkliZG52U1NtdElldFUwMkhqS01DeDA4YWl5cWxVUk93Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.FodeK276KEilIZ34Ot1r0dS7At4ejgz6PXgCOz0woerdfF7li6SFovCmnjMPKNvLU9yGC_gOuVjFAv-5A_aDSRZ1_z2-PCfAXE58id4y892JLKhgituwf1iHbDkPpRTGK7ZkDe3spf2rG75O7flTZpVFORTbR3ykkf-6HSuUX6uSaJ4trlSHF-zmDnd1QveIYaIS4bU82aBtBJ8jXHDTltjZoOLatpZU6qgTyENFyc62mkZn-tXUXytUAyWu01rMvQMeZp4FbKopWPCXygvsc4MWT6vPfO53n3RPy_Q4HTX75uJU8TvgjlLIJB1_i0wual-cTXbW3VUEc-Fa1LUCJg"

EMAIL_ASSISTANT = "faintromion@gmail.com"
EMAIL_DIRECTOR = "inatchenator@gmail.com"
EMAIL_PRODUCER = "kzinmr109@gmail.com"

PASSWORD_ASSISTANT = "Triela109"
PASSWORD_DIRECTOR = "Triela109"
PASSWORD_PRODUCER = "Triela109"


@pytest.fixture
def client():
    os.environ["JWT_SECRET"] = SECRET
    api.app.config["TESTING"] = True
    client = api.app.test_client()

    yield client


# def test_auth(client):
#     body = {"email": EMAIL, "password": PASSWORD}
#     response = client.post(
#         "/auth", data=json.dumps(body), content_type="application/json"
#     )

#     assert response.status_code == 200
#     token = response.json["token"]
#     assert token is not None


def test_get_actors_failure(client):
    response = client.get("/actors")
    assert response.status_code == 401


def test_post_actors_failure(client):
    response = client.post("/actors")
    assert response.status_code == 401


def test_patch_actors_failure(client):
    response = client.patch("/actors/1")
    assert response.status_code == 401


def test_delete_actors_failure(client):
    response = client.delete("/actors/1")
    assert response.status_code == 401


def test_get_movies_failure(client):
    response = client.get("/movies")
    assert response.status_code == 401


def test_post_movies_failure(client):
    response = client.post("/movies")
    assert response.status_code == 401


def test_patch_movies_failure(client):
    response = client.patch("/movies/1")
    assert response.status_code == 401


def test_delete_movies_failure(client):
    response = client.delete("/movies/1")
    assert response.status_code == 401


# assistant role


def test_get_actors_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.get("/actors", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["actors"]) > 0


def test_post_actors_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.post("/actors", headers=headers, content_type="application/json")
    assert response.status_code == 401


def test_patch_actors_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.patch(
        "/actors/1", headers=headers, content_type="application/json"
    )
    assert response.status_code == 401


def test_delete_actors_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.delete(
        "/actors/1", headers=headers, content_type="application/json"
    )
    assert response.status_code == 401


def test_get_movies_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.get("/movies", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["movies"]) > 0


def test_post_movies_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.post("/movies", headers=headers, content_type="application/json")
    assert response.status_code == 401


def test_patch_movies_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.patch(
        "/movies/1", headers=headers, content_type="application/json"
    )
    assert response.status_code == 401


def test_delete_movies_assistant(client):
    headers = {"Authorization": f"Bearer {TOKEN_ASSISTANT}"}
    response = client.delete(
        "/movies/1", headers=headers, content_type="application/json"
    )
    assert response.status_code == 401


# producer role


def test_get_actors_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    response = client.get("/actors", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["actors"]) > 0


def test_post_actors_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    body = {"name": "Kazuki Inamura", "age": 28, "gender": "male"}
    response = client.post(
        "/actors",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_patch_actors_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    body = {"name": "Ramunai Kizuka"}
    response = client.patch(
        "/actors/2",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_actors_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    response = client.delete(
        "/actors/2", headers=headers, content_type="application/json"
    )
    assert response.status_code == 200


def test_get_movies_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    response = client.get("/movies", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["movies"]) > 0


def test_post_movies_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    body = {"title": "Casting Agency", "release_date": "01/17/20"}
    response = client.post(
        "/movies",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_patch_movies_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    body = {"title": "Agency Casting"}
    response = client.patch(
        "/movies/2",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_movies_producer(client):
    headers = {"Authorization": f"Bearer {TOKEN_PRODUCER}"}
    response = client.delete(
        "/movies/2", headers=headers, content_type="application/json"
    )
    assert response.status_code == 200


# director role


def test_get_actors_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    response = client.get("/actors", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["actors"]) > 0


def test_post_actors_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    body = {"name": "Kazuki Inamura", "age": 28, "gender": "male"}
    response = client.post(
        "/actors",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_patch_actors_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    body = {"name": "Ramunai Kizuka"}
    response = client.patch(
        "/actors/2",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_actors_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    response = client.delete(
        "/actors/2", headers=headers, content_type="application/json"
    )
    assert response.status_code == 200


def test_get_movies_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    response = client.get("/movies", headers=headers, content_type="application/json")
    assert response.status_code == 200
    assert len(response.json["movies"]) > 0


def test_post_movies_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    body = {"title": "Casting Agency", "release_date": "01/17/20"}
    response = client.post(
        "/movies",
        headers=headers,
        data=json.dumps(body),
        content_type="application/json",
    )
    assert response.status_code == 401


def test_delete_movies_director(client):
    headers = {"Authorization": f"Bearer {TOKEN_DIRECTOR}"}
    response = client.delete(
        "/movies/1", headers=headers, content_type="application/json"
    )
    assert response.status_code == 401
