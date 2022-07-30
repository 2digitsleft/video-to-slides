from google.oauth2 import service_account
from config.settings import settings
from src.core.exceptions import AuthenticationError

class AuthManager:
    @staticmethod
    def get_credentials():
        """Get Google API credentials"""
        try:
            return service_account.Credentials.from_service_account_file(
                settings.SERVICE_ACCOUNT_FILE,
                scopes=settings.GOOGLE_SCOPES
            )
        except Exception as e:
            raise AuthenticationError(f"Failed to load credentials: {e}")
