# import os
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# from app import AppFactory


# # @pytest.fixture
# # def client():
# #     app_class = WebApp(test = True)
# #     app_class.app.config["TESTING"] = True
# #     with app_class.app.test_client() as client:
# #         yield client

# # @pytest.mark.skip()
# # def test_index_get(client):
# #     response = client.get("/")
# #     assert response.status_code == 200

# # @pytest.mark.skip()
# # def test_login_get(client):
# #     response = client.get("/login")
# #     assert response.status_code == 200

# # @pytest.mark.skip()
# # def test_login_post(client):
# #     # Check that the login works
# #     username = "ben"
# #     password = "123"

# #     # client.
# #     # q.return_value = []
# #     # response = client.post(
# #     #     "/login",
# #     #     data={"username": username, "password": password},
# #     #     follow_redirects=False,
# #     # )
# #     # assert response.status_code == 200
# #     # assert b"User not found" in response.data

# #     # q.return_value = "asdf"
# #     # response = client.post(
# #     #     "/login",
# #     #     data={"username": username, "password": password},
# #     #     follow_redirects=False,
# #     # )
# #     # assert response.status_code == 200
# #     # assert b"Incorrect password." in response.data

# #     # q.return_value = "123"
# #     # response = client.post(
# #     #     "/login",
# #     #     data={"username": username, "password": password},
# #     #     follow_redirects=False,
# #     # )
# #     # assert response.status_code == 200
# #     # assert b"Incorrect password." in response.data

# # @pytest.mark.skip()
# # def test_register_get(client):
# #     response = client.get("/register")
# #     assert response.status_code == 200

# # @pytest.mark.skip()
# # def test_create_get(client):
# #     # Not logged in
# #     response = client.get("/create")
# #     assert response.status_code == 302
# #     assert "/login" in response.headers["Location"]

# #     with client.session_transaction() as sess:
# #         sess["username"] = "fake"
# #     response = client.get("/create")
# #     assert response.status_code == 200


# # # def test_login_
