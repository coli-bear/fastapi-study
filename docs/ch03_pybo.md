# 파이보 서비스 개발

이제 wikidocs 에서 제공하는 토이프로젝트인 파이보를 구현하자.

여기서는 기본적인 내용은 커밋 이력을 확인하고, 주요한 내용만 정리하겠다.

## Navigation Bar

따로 정리하지 않으며, 아래 변경 이력을 확인

### Source Code Commit History

> - [Pybo Navigation Bar Frontend](https://github.com/coli-bear/fastapi-study/commit/bbda526ac50af8ac5a40f308d973695f689fd8cf)
> - [Pybo Navigation Bar Backend](https://github.com/coli-bear/fastapi-study/commit/10eff0477f1116de8b79189cf426767bbfad963e)

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

이제 router 를 등록해서 API 구현부를 최종적으로 완성하겠다. 이는 위 커밋 이력을 확인하면 된다.

