from django.conf import settings
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timezone
import requests
import json

logger = logging.getLogger(__name__)

# check key in dictionary(nested dictionary)
def find_key(dictionary, target_key):
    if not isinstance(dictionary, dict):
        return False
    if target_key in dictionary:
        return True
    for value in dictionary.values():
        if isinstance(value, dict) and find_key(value, target_key):
            return True
    return False


class ZitadelBaseService:
    """base class for request to zitadel"""

    def __init__(self):
        self.base_url = getattr(settings, 'ZITADEL_BASE_URL', '')
        self.private_key_token = getattr(settings, 'PERSONAL_ACCESS_TOKEN', '')
        self.session_time = getattr(settings, 'SESSION_TIME', 3600)

    def _make_request(self, method: str, endpoint: str, payload: Optional[Dict] = None,
                      params: Optional[Dict] = None) -> Optional[Dict]:

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.private_key_token}',
            'Accept': 'application/json'
        }
        data = json.dumps(payload) if payload else None
        try:
            response = requests.request(method, url, headers=headers, data=data, params=params)
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.RequestException as e:
            logger.error(f"Zitadel API error: {str(e)} - URL: {url}")
            return None


class ZitadelSessionService(ZitadelBaseService):
    """class for handle sessions with zitadel CRUD"""

    def create_session(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """create session with zitadel"""
        endpoint = "/v2/sessions"
        payload = {
            "checks": {
                "user": {"loginName": f"{username}@mail.erp.hoshro.com"}, 
                "password": {"password": password}
            },
            "lifetime": f"{self.session_time}s"
        }
        return self._make_request("POST", endpoint, payload)

    def update_session(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """update session with zitadel"""
        raise NotImplementedError("Session update not implemented yet")

    def delete_session(self, session_id: str, session_token: str) -> bool:
        """delete session with zitadel"""
        endpoint = f"/v2/sessions/{session_id}"
        payload = {"sessionToken": session_token}
        response = self._make_request("DELETE", endpoint, payload)
        return response is not None

    def get_user_info_by_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        get user info by session with zitadel
        convert expiration date to tehran time
        check expiration session
        """
        endpoint = f"/v2/sessions/{session_id}"
        response_data = self._make_request("GET", endpoint)
        if not response_data:
            return None
        try:
            return response_data
            # expiration_str = response_data["session"]["expirationDate"]
            # expiration_utc = datetime.fromisoformat(expiration_str.replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
            # tehran_tz = pytz.timezone("Asia/Tehran")
            # expiration_tehran = expiration_utc.astimezone(tehran_tz)
            # current_time_tehran = datetime.now(tehran_tz)
            # if current_time_tehran < expiration_tehran:
            #     return response_data
            # return None
        except KeyError as e:
            logger.error(f"Missing key in session response: {str(e)}")
            return None

class ZitadelUserService(ZitadelBaseService):
    """class for handle users with zitadel CRUD"""

    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """create user with data user with zitadel"""
        required_fields = ["username", "email", "givenName", "familyName", "phone", "password"]
        for field in required_fields:
            if not find_key(user_data, field): # check keys are in user data
                raise ValueError(f"{field} is required.")

        endpoint = "/v2/users/human"
        payload = {
            "username": user_data["username"],
            "organization": {
                "orgId": "332484472068961027",  
            },
            "profile": {
                "givenName": user_data["givenName"],
                "familyName": user_data["familyName"],
            },
            "email": {
                "email": user_data["email"],
                "isVerified": True
            },
            "phone": {
                "phone": user_data["phone"],
                "isVerified": True
            },
            "password": {
                "password": user_data["password"],
                "changeRequired": False
            },
            "metadata": [
                {"key": "national_id", "value": user_data["username"]}
            ]
        }
        return self._make_request("POST", endpoint, payload)

    def delete_user(self, user_id: str) -> bool:
        """delete user with zitadel"""
        endpoint = f"/v2/users/{user_id}"
        response = self._make_request("DELETE", endpoint)
        return response is not None

    def get_user_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """get user by user id with zitadel"""
        endpoint = f"/v2/users/{user_id}"
        return self._make_request("GET", endpoint)

    def update_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """update user with data user with zitadel"""
        required_fields = ["userId", "username", "givenName", "familyName", "phone"]
        for field in required_fields:
            if not find_key(user_data, field): # check keys are in user data
                raise ValueError(f"{field} is required.")

        endpoint = f"/v2/users/human/{user_data['userId']}"
        payload = {
            "username": user_data["username"],
            "human": {
                "profile": {
                    "givenName": user_data["givenName"],
                    "familyName": user_data["familyName"],
                },
                "phone": {"phone": user_data["phone"], "isVerified": True}
            }
        }
        return self._make_request("PUT", endpoint, payload)


class ZitadelAuthorizationsService(ZitadelBaseService):
    """class for handle authorizations roles with zitadel"""

    def create_authorizations(self, user_id, projectId, roleKeys): # TODO: roles create one time?
        """create authorizations roles with zitadel"""
        endpoint = f"/management/v1/users/{user_id}/grants"
        payload = {
            "projectId": projectId,
            "organizationId": "",
            "roleKeys": roleKeys
        }
        return self._make_request("POST", endpoint, payload)

    def search_authorizations(self, user_id: str) -> Optional[Dict[str, Any]]:
        """gave userid and return info and roles user with zitadel"""
        endpoint = "/management/v1/users/grants/_search"
        payload = {
            "query": {
                "offset": "0",
                "limit": 100,
                "asc": True
            },
            "queries": [
                {
                    "userIdQuery": {
                        "userId": user_id
                    }
                }
            ]
        }
        return self._make_request("POST", endpoint, payload)

    def remove_authorizations(self, user_id: str, grant_id: str) -> Optional[Dict[str, Any]]:
        """remove role from user with zitadel"""
        endpoint = f"/management/v1/users/{user_id}/grants/{grant_id}"
        return self._make_request("DELETE", endpoint)

























from typing import Optional, Tuple
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from dataclasses import dataclass
from .zitadel_service import ZitadelSessionService
from .models import Session


@dataclass
class AuthCredentials:
    token_id: str
    session_id: str


class ZAuthentication(BaseAuthentication):
    """
    authenticate class with zitadel
    extract token_id from request
    extract session_id from database
    get user info from zitadel
    get user from database
    return user and z_user(user info from zitadel)
    """

    class AuthErrorMessages:
        """authentication error messages"""
        def __init__(self):
            pass

        MISSING_TOKEN = "Missing Token-ID header"
        MISSING_SESSION = "Missing Session-ID header"
        SESSION_EXPIRED = "Session expired"
        INVALID_USER_INFO = "Invalid user info structure"
        USER_NOT_FOUND = "User not found"
        INVALID_TOKEN = "Invalid or expired token"

    def _extract_credentials(self, request) -> AuthCredentials:
        """
        extract token_id from request 
        return AuthCredentials(token_id, session_id)
        """
        token_id = request.META.get('HTTP_TOKEN_ID')

        if not token_id:
            raise AuthenticationFailed(self.AuthErrorMessages.MISSING_TOKEN)
        try:
            session_id = Session.objects.get(token_id=token_id)
        except Session.DoesNotExist:
            raise AuthenticationFailed(self.AuthErrorMessages.INVALID_TOKEN)
        return AuthCredentials(token_id=token_id, session_id=session_id.session_id)

    def _validate_user_info(self, user_info: dict) -> str: # TODO: can change name func to get_user_id
        """validate user info from zitadel and extract user id"""
        try:
            return user_info["session"]["factors"]["user"]["id"] # extract user id
        except (KeyError, TypeError):
            raise AuthenticationFailed(self.AuthErrorMessages.INVALID_USER_INFO)

    def _get_user(self, user_id: str) -> User:
        """get user from database"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(self.AuthErrorMessages.USER_NOT_FOUND)


    def authenticate(self, request) -> Optional[Tuple[User, str]]:
        """authenticate user with zitadel"""
        credentials = self._extract_credentials(request) 

        zitadel = ZitadelSessionService()
        user_info = zitadel.get_user_info_by_session(credentials.session_id)

        if not user_info:
            raise AuthenticationFailed(self.AuthErrorMessages.SESSION_EXPIRED)

        user_id = self._validate_user_info(user_info)
        user = self._get_user(user_id)

        return user, credentials.session_id









from rest_framework import permissions

from app_auth.zitadel_service import ZitadelAuthorizationsService


# class ZPermission review roles users with zitadel
    # if user have that role return → True
    # if user not authenticated or not have that role return → False


class ZPermission(permissions.BasePermission):
    """
    Permission check with Zitadel.

    - False → user not authenticated
    - True  → no role_key required
    - False → authorizations missing/invalid
    - True  → role_key found in roleKeys
    - False → role_key not in roleKeys or any error
    """
    def __init__(self, extra_data=None):
        self.extra_data = extra_data or {}

    def has_permission(self, request, view):
        required_roles = self.extra_data.get('role_key', '')
        if not required_roles: 
            return True 
        
        if not isinstance(required_roles, list):
            return False
            
        zitadel = ZitadelAuthorizationsService()
        try:
            authorizations = zitadel.search_authorizations(request.user.username)
            if not authorizations or 'result' not in authorizations:
                return False 
            result = authorizations['result']
            if not result or len(result) == 0:
                return False 
            user_role_keys = result[0].get('roleKeys', [])
            if not isinstance(user_role_keys, list):
                return False 
            
            # Check if user has any of the required roles
            return any(role in user_role_keys for role in required_roles)
        except (IndexError, KeyError, TypeError, AttributeError):
            return False 
        except Exception as e:
            return False

