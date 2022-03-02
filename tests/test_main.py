from fastapi.testclient import TestClient
import pymongo

from app.config import settings
from app.main import app


class TestMain:

    user_data = {
        "email": "testuser@testing.com",
        "password": "testpswd"
        }
    wrong_user_data = {
        "email": "wronguser@testing.com",
        "password": "wrongpswd"
        }
    access_token = ""
    wrong_access_token = "your.ad.could.be.here"
    link_id = ""
    url_1 = "http://test.com"
    url_2 = "http://test2.com"
    updated_url = "http://test.org"
    user_id = ""

    test_client = None
    test_db = None
    test_users = None
    test_links = None

    @classmethod
    def setup_class(cls):
        cls.test_client = pymongo.MongoClient(settings.MONGODB_CONNECTION_URL)
        cls.test_db = cls.test_client[settings.MONGO_DB]
        cls.test_users = cls.test_db["users"]
        cls.test_links = cls.test_db["links"]


    @classmethod
    def teardown_class(cls):
        cls.test_users.drop()
        cls.test_links.drop()

    def test_sign_up(self):
        self.setup_class()
        with TestClient(app) as client:
            response = client.post(
                "/api/users/sign_up",
                json=self.user_data
                )
        setattr(TestMain, 'user_id', response.json()["id"])
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

    def test_wrong_sign_up(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/users/sign_up",
                json=self.user_data
                )
        assert response.status_code == 200
        assert response.json()["status"] == "Fail"
        assert response.json()["detail"] == "This e-mail is used"

    def test_log_in(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/auth/log_in",
                json=self.user_data
                )
        setattr(TestMain, 'access_token', response.json()["access_token"])
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"

    def test_wrong_log_in(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/auth/log_in",
                json=self.wrong_user_data
                )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect e-mail or password"

    def test_create_link(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/links/",
                headers={"token": self.access_token},
                json={"url": self.url_1}
                )
            response_2 = client.post(
                "/api/links/",
                headers={"token": self.access_token},
                json={"url": self.url_2}
                )
        setattr(TestMain, 'link_id', response.json()["id"])
        assert response.status_code == 200
        assert response_2.status_code == 200
        assert response.json()["status"] == "OK"
        assert response_2.json()["status"] == "OK"

    def test_create_existing_link(self):
        with TestClient(app) as client:
            response = client.post(
                "/api/links/",
                headers={"token": self.access_token},
                json={"url": self.url_1}
                )
        assert response.status_code == 200
        assert response.json()["status"] == "Fail"
        assert response.json()["detail"] == "This URL is registered"

    def test_get_links(self):
        with TestClient(app) as client:
            response = client.get(
                "/api/links",
                headers={"token": self.access_token}
                )

        assert response.status_code == 200
        assert response.json()[0]["url"] == self.url_1
        assert response.json()[0]["owner"] == response.json()[1]["owner"] == self.user_id
        assert response.json()[1]["url"] == self.url_2


    def test_wrong_token(self):
        with TestClient(app) as client:
            response = client.get(
                "/api/links/",
                headers={"token": self.wrong_access_token}
                )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_get_link(self):
        with TestClient(app) as client:
            response = client.get(
                "/api/links/"+str(self.link_id),
                headers={"token": self.access_token}
                )
        assert response.status_code == 200
        assert response.json()["url"] == self.url_1

    def test_update_link(self):
        with TestClient(app) as client:
            response = client.patch(
                "/api/links/"+str(self.link_id),
                headers={"token": self.access_token},
                json={"url": self.updated_url}
            )
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

    def test_wrong_update_link(self):
        with TestClient(app) as client:
            response = client.patch(
                "/api/links/"+str(self.link_id),
                headers={"token": self.access_token},
                json={"url": self.updated_url}
            )
        assert response.status_code == 200
        assert response.json()["status"] == "Fail"
        assert response.json()["detail"] == "This URL is registered"

    def test_delete_link(self):
        with TestClient(app) as client:
            response = client.delete(
                "/api/links/"+self.link_id,
                headers={"token": self.access_token}
            )
        assert response.status_code == 200
        assert response.json()["status"] == "OK"

    def test_delete_user(self):
        with TestClient(app) as client:
            response = client.delete(
                "/api/users/delete",
                headers={"token": self.access_token}
            )
        assert response.status_code == 200
        assert response.json()["status"] == "OK"
        self.teardown_class()
