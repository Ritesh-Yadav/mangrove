from services.authentication.authentication_service import AuthenticationService
from services.authentication.models import UserModel
from services.repository.connection import Connection
from services.repository.repository import Repository

class TestAuthenticationService:

    test_user_email = 'testuser@email.com'

    def setup(self):
        self.repository = Repository(Connection())

    def teardown(self):
        document = self.repository.load(self.test_user_email)
        self.repository.delete(document)


    def test_should_authenticate_user(self):
        service = AuthenticationService(self.repository)
        user = UserModel(id=self.test_user_email, email=self.test_user_email, password='password')
        service.create_user(user)
        user = service.authenticate_user(self.test_user_email, 'password')
        assert user


        
