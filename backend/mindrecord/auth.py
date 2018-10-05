import datetime
from typing import List, Optional
import bson
import jwt
import bcrypt

from mindrecord.utils import Request, JsonResponse, Status, HTTPError, allow_methods, allow_cors
from mindrecord.app import config, db


__all__ = ['User', 'Roles', 'AuthError', 'get_auth_token', 'get_auth_token_payload',
           'create_access_token', 'get_user_from_request', 'requires_auth', 'auth_view', 'verify_email_view']

db_users = db['users']
db_revoked_tokens = db['revoked_tokens']


class Roles(object):
    # No token
    UNAUTHORIZED = 'unauthorized'

    # With token, but no credentials (login:password)
    ANONYMOUS = 'anonymous'

    # With token, with credentials
    USER = 'user'

    # Admin (utility)
    ADMIN = 'admin'


class User(object):
    id = None
    role = Roles.UNAUTHORIZED

    def __init__(self, identifier: Optional[str], role=Roles.USER):
        self.id = identifier
        self.role = role

    @property
    def is_guest(self) -> bool:
        return self.role == Roles.UNAUTHORIZED or self.id is None

    @property
    def is_authorized(self) -> bool:
        return self.role != Roles.UNAUTHORIZED and self.id is not None

    @classmethod
    def create_anonymous(cls) -> 'User':
        new_id = str(bson.objectid.ObjectId()) + '_anon'
        return User(new_id, Roles.ANONYMOUS)

    @classmethod
    def create_guest(cls) -> 'User':
        return User(identifier=None, role=Roles.UNAUTHORIZED)


class AuthError(HTTPError):
    def __init__(self, message, status_code=Status.UNAUTHORIZED):
        super().__init__(status_code=status_code, message=message)


def get_auth_token(request: Request, raise_if_none=True):
    auth_header = request.get_header_value('Authorization', None)
    if not auth_header:
        if raise_if_none:
            raise AuthError('Token is missing')
        return None

    parts = auth_header.split(' ')
    if len(parts) != 2:
        raise AuthError('Invalid token')

    if parts[0].lower() != 'bearer':
        raise AuthError('Bearer token required')

    return parts[1]


def get_payload(token: str):
    try:
        return jwt.decode(token, config.JWT_SECRET, issuer=config.JWT_ISSUER, algorithms=[config.JWT_ALGORITHM])
    except jwt.InvalidTokenError as err:
        raise AuthError('Invalid token: {0}'.format(err.args[0]))


def get_auth_token_payload(request: Request, raise_if_none=True):
    token = get_auth_token(request, raise_if_none=raise_if_none)
    if not token:
        if raise_if_none:
            raise AuthError('Token is missing')
        return None
    return get_payload(token)


def create_access_token(user: User):
    return create_user_token(user=user, expire_seconds=config.JWT_ACCESS_EXPIRATION_SECONDS, kind='access')


def create_refresh_token(user: User):
    return create_user_token(user=user, expire_seconds=config.JWT_REFRESH_EXPIRATION_SECONDS, kind='refresh')


def create_email_token(user: User):
    return create_user_token(user=user, expire_seconds=config.JWT_EMAIL_CONFIRMATION_SECONDS, kind='email')


def create_user_token(user: User, kind: str, encoding='utf-8', expire_seconds=60 * 60 * 24):
    iat = datetime.datetime.utcnow()  # Issued at
    exp = iat + datetime.timedelta(seconds=expire_seconds)  # Expire at

    payload = {
        'iat': iat,
        'exp': exp,
        'iss': config.JWT_ISSUER,
        config.JWT_USER_ID_CLAIM: user.id,
        config.JWT_ROLE_CLAIM: user.role,
        config.JWT_KIND_CLAIM: kind
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM).decode(encoding)


def get_user_from_request(request: Request, raise_if_no_token=False):
    return get_user_from_token(get_auth_token(request, raise_if_none=raise_if_no_token))


def get_user_from_token(token: str=None, kind='access'):
    if not token:
        return User.create_guest()

    token_payload = get_payload(token)
    token_kind = token_payload.get(config.JWT_KIND_CLAIM, None)
    role = token_payload.get(config.JWT_ROLE_CLAIM, Roles.ANONYMOUS)
    user_id = token_payload.get(config.JWT_USER_ID_CLAIM, None)
    if not token_kind or not user_id:
        raise AuthError('Invalid token')
    if kind != token_kind:
        raise AuthError('Invalid token')
    return User(identifier=user_id, role=role)


def requires_auth(permit_roles: List[str]=(Roles.UNAUTHORIZED, ), allowed_roles: List[str]=None):
    def decorator(fn):
        def wrapper(request: Request, *args, **kwargs):
            user = get_user_from_request(request)

            if permit_roles is not None and user.role in permit_roles:
                raise HTTPError(Status.UNAUTHORIZED)

            if allowed_roles is not None and user.role not in allowed_roles:
                raise HTTPError(Status.UNAUTHORIZED)

            return fn(request, *args, **kwargs)
        return wrapper
    return decorator


def tokens_response(user: User, status_code=200):
    return JsonResponse({
        'access_token': create_access_token(user),
        'access_token_expiration': config.JWT_ACCESS_EXPIRATION_SECONDS,
        'refresh_token': create_refresh_token(user),
        'refresh_token_expiration': config.JWT_REFRESH_EXPIRATION_SECONDS,
    }, status_code=status_code)


@allow_cors()
@allow_methods('GET', 'POST', 'DELETE')
def auth_view(request: Request):
    if request.method == 'POST':
        user = get_user_from_request(request)
        if user.is_authorized:
            # User is already AUTHORIZED
            # Try to refresh tokens
            raise HTTPError(Status.BAD_REQUEST, message='Already logged in')

        refresh_token = request.data.get('refresh_token', None)
        if refresh_token is not None:
            revoked_token = db_revoked_tokens.find_one({'token': refresh_token[0]})
            if revoked_token is not None:
                raise HTTPError(Status.BAD_REQUEST)
            user = get_user_from_token(refresh_token)
            db_revoked_tokens.insert_one({'token': refresh_token})
            return tokens_response(user)

        email = request.data.get('email', None)  # type: str
        password = request.data.get('password', None)  # type: str

        if email:
            if isinstance(email, list):
                email = email[0]
            email = email.strip()
        if password:
            if isinstance(password, list):
                password = password[0]
            password = password.strip()

        """ Anonymous auth """
        if not email and not password:
            if not config.AUTH_ALLOW_ANONYMOUS:
                raise HTTPError(Status.BAD_REQUEST, 'email and password should be set')

            user_id = db_users.insert_one({
                'role': Roles.ANONYMOUS,
                'created': datetime.datetime.utcnow()
            }).inserted_id

            user = User(str(user_id), Roles.ANONYMOUS)
            return tokens_response(user, status_code=Status.CREATED)

        """ Email-based auth """
        existing_user = db_users.find_one({'email': email})
        if existing_user is None:
            """ New user registration """
            hashed_pwd = bcrypt.hashpw(password=password.encode('utf-8'),
                                       salt=bcrypt.gensalt(config.AUTH_BCRYPT_ROUNDS))
            user_id = db_users.insert_one({
                'email': email,
                'password': hashed_pwd,
                'role': Roles.USER,
                'created': datetime.datetime.utcnow(),
                'verified': False
            }).inserted_id

            user = User(str(user_id), Roles.USER)

            email_verification_token = create_email_token(user)
            # Todo: send email verification token
            print('/verify-email?token={}'.format(email_verification_token))

            return tokens_response(user, status_code=Status.CREATED)

        """ Existing user auth """
        if bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
            user = User(str(existing_user['_id']), existing_user['role'])
            return tokens_response(user, status_code=Status.OK)

        raise HTTPError(Status.BAD_REQUEST)
    if request.method == 'DELETE':
        # TODO: Implement logout and token revoke
        raise HTTPError(Status.NOT_IMPLEMENTED)


@allow_methods('GET')
def verify_email_view(request: Request):
    token = request.data.get('token', None)
    if token is not None:
        user = get_user_from_token(token[0], kind='email')
        existing_user = db_users.find_one({'_id': bson.ObjectId(user.id)})
        if not existing_user:
            raise HTTPError(Status.BAD_REQUEST)

        # If verified already
        if existing_user.get('verified', False):
            raise HTTPError(Status.BAD_REQUEST, 'Token was already used')

        db_users.update_one({'_id': bson.ObjectId(user.id)}, {'$set': {'verified': True}})
        return JsonResponse({'message': 'Your email has been verified successfully!'})
    raise HTTPError(Status.BAD_REQUEST)
