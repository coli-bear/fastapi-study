# 파이보 서비스 개발

이제 wikidocs 에서 제공하는 토이프로젝트인 파이보를 구현하자.

여기서는 기본적인 내용은 커밋 이력을 확인하고, 주요한 내용만 정리하겠다.

## Navigation Bar

따로 정리하지 않으며, 아래 변경 이력을 확인

### Source Code Commit History

> - [Pybo Navigation Bar Frontend](https://github.com/coli-bear/fastapi-study/commit/20e3537b28e96e92dc0b1aaee3491eacdd3b7bbc)
> - [Pybo Navigation Bar Backend](https://github.com/coli-bear/fastapi-study/commit/faa24be551202d9ce35d56bcede772c2aa04292f)

## Pybo User

### Source Code Commit History

> - [Pybo User Frontend]()
> - [Pybo User Backend]()

#### User Model

사용자 모델을 다음과 같이 정의하였다.

- models.py

```python
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

생성된 모델을 RDBMS 에 반영하기 위한 리비전 파일을 생성하겠다.

```shell
alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.ddl.postgresql] Detected sequence named 'answer_id_seq' as owned by integer column 'answer(id)', assuming SERIAL and omitting
  Generating /Users/geontae/PycharmProjects/FastAPIProject/example/migrations/versions/7f008731ea15_.py ...  done
```

생성된 리비전파일을 적용해보자

```shell
alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 7d109f030d9b -> 7f008731ea15, empty message
```

DBMS 툴에서 실제 적용 됐는지 확인하면 정상적으로 적용이 된 것을 확인할 수 있다.

### Sign Up

사용자 등록을위한 API 명세는 다음과 같다.

```http request
GET /api/user/signup
content-type: application/json
accept: application/json

{
  "username": "testuser",
  "password": "testpassword",
  "confirm_password": "testpassword",
  "email": "test@mail.com"
}
```

여기서 필드를 보면 email 필드가 있다. 이는 별도의 validator 를 설치해서 사용해야 한다.

```shell
pip install "pydentic[email]"
  Downloading pydentic-0.0.1.dev3-py3-none-any.whl.metadata (6.1 kB)
WARNING: pydentic 0.0.1.dev3 does not provide the extra 'email'
Collecting python-stdnum>=1.16 (from pydentic[email])
  Downloading python_stdnum-2.1-py3-none-any.whl.metadata (18 kB)
Downloading pydentic-0.0.1.dev3-py3-none-any.whl (6.9 kB)
Downloading python_stdnum-2.1-py3-none-any.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 9.5 MB/s eta 0:00:00
Installing collected packages: python-stdnum, pydentic
Successfully installed pydentic-0.0.1.dev3 python-stdnum-2.1
```

이를 설치한 후 다음과 같이 생성을 위한 Schema 를 정의했다.

- models/user/user_schema.py

```python
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo


class UserCreateSchema(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: EmailStr

    @field_validator("username", "password", "confirm_password", "email")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")
        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_password(cls, value: str, info: FieldValidationInfo) -> str:
        if 'password' in info.data and info.data['password'] != value:
            raise ValueError("Password and confirm password do not match.")

        return value
```

먼저 not_empty 를 이용하여 빈 값에 대한 검증을 진행했으며, validate_password 에서 패스워드 검증을 진행했다. pydentic 의 EmailStr 를 사용하여 이메일 형식을 검증할 수 있다.

이제 사용자 등록을 함수를 구현하겠다. 여기서 중요한 요구사항이 하나 있다. 사용자 등록시 패스워드는 노출이 안되도록 보안사항을 적용해야한다 이때 단방향 알고리즘을 이용해서 암호화하게 되며 이는 passlib 를
이용해서 처리할 수 있다. 먼저 passlib 를 설치하자.

> 참고 : 여기서는 passlib 의 bcrypt 알고리즘을 사용했다. 일반적으로 엔트로피와 암호화 수준을 맞추기 위해서는 bcrypt보다 더 강력한 알고리즘을 사용하는 것이 좋지만, 여기서는 단순히 예시로
> bcrypt 를 사용했다.

```shell
pip install "passlib[bcrypt]"
Collecting passlib[bcrypt]
  Downloading passlib-1.7.4-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting bcrypt>=3.1.0 (from passlib[bcrypt])
  Using cached bcrypt-4.3.0-cp39-abi3-macosx_10_12_universal2.whl.metadata (10 kB)
Downloading passlib-1.7.4-py2.py3-none-any.whl (525 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 525.6/525.6 kB 6.4 MB/s eta 0:00:00
Using cached bcrypt-4.3.0-cp39-abi3-macosx_10_12_universal2.whl (498 kB)
Installing collected packages: passlib, bcrypt
Successfully installed bcrypt-4.3.0 passlib-1.7.4
```

- domain/user/user_crud.py

```python
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import auto_commit
from domain.user.user_schema import UserCreateSchema
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auto_commit
def create_user(db: Session, user: UserCreateSchema):
    _crypted_password = pwd_context.hash(user.password)
    user = User(username=user.username, password=_crypted_password, email=user.email)
    db.add(user)
```

이제 router 를 등록해서 API 구현부와 UI를 최종적으로 완성하겠다. 이는 위 커밋 이력을 확인하면 된다.

> 백엔드에 약간의 오류가 있어 아래 커밋이력을 확인해서 router 의 코드를 변경하자
> - [Pybo User Backend 오류 수정](https://github.com/coli-bear/fastapi-study/commit/89984e3ebc470ae968a757d5f9404d59cd3d9fb1)

### Sign In

사용자 로그인을 위한 API 명세는 다음과 같다. 로그인에서는 OAuth2 인증을 사용할 예정이며 fastapi 의 security 모듈을 사용해서 제공한다.

```http request
POST http://localhost:8000/api/user/signin
accept: application/json 
Content-Type: application/x-www-form-urlencoded

{
    "grant_type": "password",
    "username": "username",
    "password": "1234",
    "scope": "",
    "client_id": "string",
    "client_secret": "string"
}
```

로그인 API 는 사용자 등록과는 다르게 패스워드 검증이 필요하다. 이를 위해서 먼저 사용자 정보를 조회하고, 조회된 사용자 정보의 패스워드를 검증해야 한다.
아래는 로그인 응답 명세이다.

| field        | description        |
|--------------|--------------------|
| access_token | 로그인 성공시 발급되는 토큰    |
| token_type   | 토큰 타입, Bearer 로 고정 |
| username     | 로그인한 사용자 이름(ID)    |

이렇게 로그인 API 를 이용해서 로그인을 하게 되면 access_token 을 발급하게 되며, 이를 통해 API 호출에 대한 인증을 처리할 수 있다.

- domain/user/user_crud.py

```python
class UserTokenSchema(BaseModel):
    access_token: str
    token_type: str
    username: str
```

- domain/user/user_crud.py

```python
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
```

사용자 로그인 정보를 받는 router 는 fastapi.security 의 OAuth2PasswordRequestForm 을 이용할 예정이며, 토큰 발급/검증을 위해서는 다음과 같은 라이브러리를 설치해야한다

- python-multipart: OAuth2PasswordRequestForm 을 사용하기 위해 필요

```shell
pip install python-multipart
Collecting python-multipart
  Downloading python_multipart-0.0.20-py3-none-any.whl.metadata (1.8 kB)
Downloading python_multipart-0.0.20-py3-none-any.whl (24 kB)
Installing collected packages: python-multipart
Successfully installed python-multipart-0.0.20
```

- python-jose: JWT 토큰을 발급/검증하기 위해 필요

```shell
pip install "python-jose[cryptography]"
Requirement already satisfied: python-jose[cryptography] in ./.venv/lib/python3.13/site-packages (3.5.0)
Requirement already satisfied: ecdsa!=0.15 in ./.venv/lib/python3.13/site-packages (from python-jose[cryptography]) (0.19.1)
Requirement already satisfied: rsa!=4.1.1,!=4.4,<5.0,>=4.0 in ./.venv/lib/python3.13/site-packages (from python-jose[cryptography]) (4.9.1)
Requirement already satisfied: pyasn1>=0.5.0 in ./.venv/lib/python3.13/site-packages (from python-jose[cryptography]) (0.6.1)
Collecting cryptography>=3.4.0 (from python-jose[cryptography])
  Downloading cryptography-45.0.3-cp311-abi3-macosx_10_9_universal2.whl.metadata (5.7 kB)
Collecting cffi>=1.14 (from cryptography>=3.4.0->python-jose[cryptography])
  Downloading cffi-1.17.1-cp313-cp313-macosx_11_0_arm64.whl.metadata (1.5 kB)
Collecting pycparser (from cffi>=1.14->cryptography>=3.4.0->python-jose[cryptography])
  Downloading pycparser-2.22-py3-none-any.whl.metadata (943 bytes)
Requirement already satisfied: six>=1.9.0 in ./.venv/lib/python3.13/site-packages (from ecdsa!=0.15->python-jose[cryptography]) (1.17.0)
Downloading cryptography-45.0.3-cp311-abi3-macosx_10_9_universal2.whl (7.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.1/7.1 MB 6.5 MB/s eta 0:00:00
Downloading cffi-1.17.1-cp313-cp313-macosx_11_0_arm64.whl (178 kB)
Downloading pycparser-2.22-py3-none-any.whl (117 kB)
Installing collected packages: pycparser, cffi, cryptography
Successfully installed cffi-1.17.1 cryptography-45.0.3 pycparser-2.22

```

이제 구현해보자

- domain/user/user_router.py

```python
@router.post("/signin", response_model=UserTokenSchema)
def user_signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.exists_user(db=db, user=form_data.username)
    password_verified = user_crud.pwd_context.verify(form_data.password, user.password)
    if not user and not password_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 이름 또는 비밀번호가 잘못되었습니다.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # JWT 토큰 생성
    data = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return UserTokenSchema(access_token=access_token, token_type="bearer", username=user.username)
```

