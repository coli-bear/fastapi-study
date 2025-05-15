from chapter.ch01.models import Question

# ch01. FastAPI 기초 다지기

> 참고 : [wikidocs - FastAPI](https://wikidocs.net/175950)

## FastAPI 의 기초

FastAPI 를 사용한 백엔드를 구현하기 전에 먼저 아래의 기초적인 내용을 정리해보겠다.

1. FastAPI 프로젝트 구조
2. Database 설정
3. Model
4. Domain
5. Frontend

## FastAPI 프로젝트 구조

먼저 이 책에서 제시하는 프로젝트의 구조는 아래와 같다 .

```text
├── main.py
├── database.py
├── models.py
├── domain
│   ├── answer
│   ├── question
│   └── user
└── frontend
```

먼저 각 파일과 디렉토리의 역할을 정리해보자.

### main.py

먼저 간단한 FastAPI 애플리케이션을 작성해보자.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}
```

위 코드에서 `app = FastAPI()` 를 이용해서 FastAPI 의 인스턴스를 생성해 주고 있는 FastAPI 의 핵심 객체로 해당 파일에서 프로젝트의 전체적인 환경을 설정할 수 있다.

### database.py

이 파일은 데이터베이스와 관련된 설정을 하는 파일로 이 파일에서는 데이터베이스를 사용하기 위한 정보를 데이터를 관리한다.

### models.py

먼저 여기서 모델 이라는 것에 대해 정의하고 넘어가겠다.

- 모델 : 관계형 데이터 베이스의 데이터를 프로그래밍에서 사용하는 객체의 형태로 변환하기 위한 것으로 테이블과 객체를 1:1로 맵핑하는 역할을 한다.
- ORM : Object Relational Mapping 의 약자로 객체와 관계형 데이터베이스의 데이터를 매핑하는 기술을 의미한다.

여기서는 프로젝트에서 데이터베이스의 테이블과 연결하기 위한 모델을 정의한다.

### domain

여기서는 도메인에 대한 구현부가 구현된다. 도메인 안에는 python package 형태로 각 도메인이 분리되어 등록된다.
여기에서는 CRUD, API 등 도메인을 동작시키기 위한 로직을 구현한다.

### frontend

FastAPI 를 이용해 구현한 API (RestAPI, HttpAPI) 를 호출하고, 브라우저 또는 모바일에서 사용자에게 제공하기 위한 프론트엔드 애플리케이션을 구현하는 디렉토리이다.

## Database 설정

앞서 설명한 것처럼 FastAPI 는 ORM 을 이용해서 데이터베이스와 연결할 수 있다. 이때 사용되는 파일들이 아래 두 개 이다.

- database.py
- models.py

그러면 이 두 파일을 이용해 간단하게 데이터베이스와 연동해 보겠다.

### 데이터베이스 구축

FastAPI 와 데이터베이스를 연결하기 위한 데이터베이스를 구축해보자 여기서는 PostgreSQL 을 사용했다.

먼저 도커와 도커 컴포즈를 이용해서 처리하겠다. 프로젝트 루트의 docker-compose.yaml 파일을 실행하며 된다.

- 도커컴포즈를 이용하는 이유는 도커 명령어를 치기 귀찮아서이므로 그냥 넘어가자.

```yaml
services:
  fastapi-postgres:
    image: postgres:latest
    container_name: fastapi-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: fastapi_db
```

일단 docker-compose.yaml 파일을 작성하고 아래 명령어로 실행한다.

```shell
docker-compose up -d
```

### FastAPI 와 PostgreSQL 연결

이제 FastAPI 와 PostgreSQL 을 연결하겠다. ORM 을 지원하는 라이브러리인 SQLAlchemy 라이브러리를 설치해보겠다.

```shell
pip install -U sqlalchemy 
pip list | grep SQLAlchemy 
SQLAlchemy        2.0.40
```

정상적으로 설치됐으므로 다음으로 database 와 연결을 해보겠다. database.py 파일에 아래와 같은 내용을 작성하겠다.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_SOURCE = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_SOURCE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

먼저 각각에 코드가 무슨 역할을 하는지에 대해서 정리해보자

`DATABASE_SOURCE = "postgresql://postgres:postgres@localhost:5432/fastapi_db"`

- 데이터베이스의 소스코드로 PostgreSQL 을 사용하고 있으며, localhost 의 5432 포트에 fastapi_db 라는 이름의 데이터베이스를 사용하겠다는 의미이다.

`engine = create_engine(DATABASE_SOURCE)`

- SQLAlchemy 에서 데이터베이스와 연결을 담당하는 엔진을 생성한다.

`SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`

- SQLAlchemy 에서 데이터베이스와 연결을 위한 세션을 생성한다.
- autocommit : 세션이 종료될 때 자동으로 커밋할지 여부를 설정한다. False 를 설정하면 데이터를 저장할 때 commit 을 해야만 저장된다 문제는 True 를 설정하였을 때
- autoflush : 세션이 종료될 때 자동으로 플러시할지 여부를 설정한다.
- bind : 연결할 데이터베이스 엔진을 설정한다.

`Base = declarative_base()`

- SQLAlchemy 에서 모델을 정의하기 위한 베이스 클래스를 생성한다.
- 모델을 정의할 때 이 클래스를 상속받아야 한다.

이렇게 데이터베이스를 연결한 Base 객체를 생성하였으니 models.py 에 모델을 작성해 보겠다.

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")

```

Item 클레스에 Base 객체를 상속받고 `__tablename__` 속성에 테이블의 이름을 지정해준다.

- `__tablename__` : 테이블의 이름을 지정하는 속성으로 반드시 지정해줘야 한다.
- `Column` : 테이블의 컬럼을 정의하는 속성으로 각 컬럼의 이름과 데이터 타입을 지정해준다.
- `Integer`, `String`, `Text`, `DateTime` : 데이터 타입을 지정하는 속성으로 각각 정수형, 문자열형, 텍스트형, 날짜형을 의미한다.
- `primary_key` : 기본키를 지정하는 속성으로 True 를 설정하면 해당 컬럼이 기본키로 설정된다.
- `nullable` : 해당 컬럼이 NULL 값을 허용하는지 여부를 설정하는 속성으로 True 를 설정하면 NULL 값을 허용한다.
- `ForeignKey` : 외래키를 지정하는 속성으로 해당 컬럼이 외래키로 설정된다.
- `relationship` : 관계를 설정하는 속성으로 해당 모델과 다른 모델 간의 관계를 설정한다.
- `backref` : 역참조를 설정하는 속성으로 해당 모델에서 다른 모델을 참조할 때 사용된다.

모델에 대한 관계가 생겼으므로 관계를 표현할 때 어떻게 표현하는지에 대해서 정리해보겠다.

먼저 `question_id` 컬럼은 `question` 테이블의 `id` 컬럼을 참조하는 외래키로 설정되어 있다.

- `ForeignKey("question.id")` : question 테이블의 id 컬럼을 참조하는 외래키로 설정한다.

relationship() 메서드는 Question 모델과 Answer 모델 간의 관계를 설정하는 메서드로, Answer 모델에서 Question 모델을 참조할 때 사용된다.

- backref="answers" : Question 모델에서 Answer 모델을 참조할 때 사용되는 속성으로, Question 모델에서 Answer 모델을 참조가 가능해진다.

여기서는 이정도만 정리하고 나중에 SQLAlchemy 에 대해서 더 공부하고 정리하겠다.

### 모델로 테이블 생성하기

이제 모델을 이용해서 테이블을 생성해보겠다.

- 여기서는 `alembic` 이라는 라이브러리를 이용해서 테이블을 생성하겠다.

```shell
pip install -U alembic
```

alembic 은 SQLAlchemy 의 마이그레이션 도구로 데이터베이스의 스키마를 관리하는 도구이다. 마이그레이션을 하기 전 먼저 초기화 작업을 해보겠다.

- chapter.ch01 디렉토리로 이동한 후 아래 명령어를 실행한다.

```shell
alembic init migrations
  Creating directory 'FastAPIProject/example/chapter/ch01/migrations' ...  done
  Creating directory 'FastAPIProject/example/chapter/ch01/migrations/versions' ...  done
  Generating FastAPIProject/example/chapter/ch01/migrations/script.py.mako ...  done
  Generating FastAPIProject/example/chapter/ch01/migrations/env.py ...  done
  Generating FastAPIProject/example/chapter/ch01/migrations/README ...  done
  Generating FastAPIProject/example/chapter/ch01/alembic.ini ...  done
  Please edit configuration/connection/logging settings in 'FastAPIProject/example/chapter/ch01/alembic.ini' before proceeding.

```

실행하면 프로젝트 root 하위에 migrations 디렉토리와 alembic.ini 파일이 생성된 것을 확인할 수 있다.

alembic.ini 파일은 alembic 의 설정파일로 데이터베이스의 연결정보를 설정할 수 있다.

alembic.ini 파일을 열어보면 많은 내용이 있지만 일단 database 연결을 위한 부분만 수정하겠다.

```ini
[alembic]
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/fastapi_db
```

이제 alembic 이 참조할 모델을 연결하기 위해 migrations/env.py 파일을 수정하겠다.

```python
import chapter.ch01.models as models  # chapter 내부에 경로가 있으므로 chapter.ch01.models 로 import

...

target = models.Base.metadata

...

```

### 리비전 파일 생성하기

이제 리비전 파일을 생성해 보겠다

> 리비전 파일 : 데이터베이스의 스키마를 관리하기 위한 파일로 데이터베이스의 스키마를 변경할 때마다 리비전 파일을 생성해야 한다. alembic 을 이용해서 리비전 파일을 생성하면 migrations 디렉터리에
> 저장된다.

```shell
alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'question'
INFO  [alembic.autogenerate.compare] Detected added table 'answer'
  Generating FastAPIProject/example/chapter/ch01/migrations/versions/7d109f030d9b_.py ...  done

```

위와 같이 리비전 파일이 생성된 것을 확인할 수 있으며, migrations/versions 디렉토리 안에 리비전 파일이 생성된 것을 확인할 수 있다.

> 여기서 만약 psycopg2 라이브러리가 설치되어 있지 않다면 아래 명령어로 설치하자.
> - python과 postgresql 을 연결하기 위한 python 드라이버이다.
> ```shell 
> pip install psycopg2-binary
> ```

alembic 없이 테이블을 생성할 수 있지만 테이블이 없는경우에만 테이블을 생성하고, 변경관리가 불가능하여 이 책에서는 alembic 을 사용했음을 알아두자.

### 테이블 생성하기

이제 리비전 파일을 이용해서 테이블을 생성해보겠다.

```shell
alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 7d109f030d9b, empty message
```

이제 테이블이 정상적으로 생성됐는지 알아보자

- DBMS 툴을 이용해서 fastapi_db 데이터베이스에 접속한 후 아래 쿼리를 실행해보자.

```sql
SELECT *
FROM information_schema.tables
WHERE table_schema = 'public';
```

| table_catalog | table_schema | table_name      | 
|---------------|--------------|-----------------|
| fastapi_db    | public       | alembic_version |
| fastapi_db    | public       | question        |
| fastapi_db    | public       | answer          |

위와 같이 테이블이 생성된 것을 알 수 있다 그 중 alembic_version 테이블은 alembic 이 데이터베이스를 변경, 관리하기 위한 테이블로 migrations/versions 에 있는 리비전 파일의
리비전 번호가 저장되어 있다.

## Model

alembic 을 이용했으니 이제 모델을 이용해서 데이터를 처리해보도록 하겠다. (파이썬 인터프리터 이용)

> chapter/ch01 디렉토리로 이동한 후 아래 명령어를 실행한다.

```shell
cd chapter/ch01
python
````

### Insert

```python 
from database import SessionLocal
from models import Question, Answer
from datetime import datetime

q = Question(subject="질문 제목", content="질문 내용", create_date=datetime.now())

db = SessionLocal()
db.add(q)
db.commit()
```

코드를 하나씩 살펴보자

- SessionLocal() : database.py 에서 정의한 세션을 생성한다.
- add() : 세션에 데이터를 추가한다.
- commit() : 세션에 추가한 데이터를 데이터베이스에 반영한다.

데이터가 정상적으로 반영됐는지 확인하기 위해서 dbms tool 또는 아래와 같은 명령어로 확인한다. 

```python
q.id
# 결과 1
```

모델을 생성할 때 Column 의 인자값으로 `autoincrement` 을 설정하면 자동으로 증가하는 값을 설정할 수 있으며, 기본값은 `autoincrement='auto'` 이다.
즉, 데이터가 반영될 때마다 primary key 값이 자동으로 증가한다는 것이다.

```python
q2 = Question(subject="질문 제목2", content="질문 내용2", create_date=datetime.now())
q2.id # 결과 없음
db.add(q2)
q2.id # 결과 없음
db.commit()
q2.id # 결과 2
```

위 코드에서 알 수 있는 사실은 `audoincrement`는 commit 이 호출되는 시점(Database 반영되는 시점) 에 처리된다는 것을 알 수 있다. 

### Select

데이저장했으니 이제 데이터를 조회해보자.

```python
questions = db.query(Question).all() # ---> (1)
questions 
# [<models.Question object at 0x106e55940>, <models.Question object at 0x106c87b10>]
question_1 = db.query(Question).get(1) # ---> (2)
question_1
# <models.Question object at 0x106e55940>
```

- (1) 전체 데이터 조회
  - db.query(Question) : Question 테이블을 조회한다.
  - all() : 조회한 데이터를 모두 가져온다.
- (2) 특정 데이터 조회
  - db.query(Question).get(1) : Question 테이블에서 id 가 1 인 데이터를 조회한다.
  - get() : 특정 데이터를 조회한다.
  - 주의 : 여기서 get() 메서드는 SQLAlchemy 현재 학습중인 라이브러리 버전에서는 deprecated 되었다. 이 부분은 SQLAlchemy 학습할때 다시 정리하자.

여기서 원하는 데이터를 필터링해서 조회하고 싶을 때는 아래와 같이 사용하면 된다. 
```python
db.query(Question).filter(Question.subject.like('%2%')).all()
# [<models.Question object at 0x106c87b10>]
```

### Update

데이터 수정은 간단하다. 데이터를 조회하고, 변경하고, commit() 하면 된다.

```python 
update_q = db.query(Question, 2)
update_q.subject = "FastAPI Update Subject"
db.commit()
```

### Delete

데이터를 삭제해보겠다. 

```python
delete_q = db.query(Question).get(2)
db.delete(delete_q)
db.commit()
db.query(Question).all()
# [<models.Question object at 0x106e55940>]
```

데이터가 삭제된 것을 확인할 수 있다. 

### Relationship Insert, Select

이제 연관관계가 있는 데이터를 입력해서 저장하고조회해보겠다. 

```python
q = db.query(Question).first()
a = Answer(content="답변 내용", create_date=datetime.now(), question=q)
db.add(a)
db.commit()
a.id # 결과 1
q.answers # 결과 [<models.Answer object at 0x106e57230>]
a.question # 결과 <models.Question object at 0x106e55940>
```

Answer 을 생성할 때 Question 을 참조하여 생성하고, commit() 을 하면 Answer 의 id 가 자동으로 증가한다.
- q.answers : Question 모델에서 Answer 모델을 참조할 때 사용된다.
- a.question : Answer 모델에서 Question 모델을 참조할 때 사용된다.

각 모델에서 서로를 참조하여 조회가 가능하다는 것을 확인했다. 실제 모델을 만들때 Question 모델에는 Answer 모델을 참조하지 않았다. 하지만 실제로는 조회가 가능한데 이는 `backref` 속성을 설정해서 역관계도 참조가 가능하도록 설정이 되어있기 때문이다. 

## Domain 

Model 을 이용해서 Database 와 연결하고, CRUD 가 정상적으로 동작되는 것을 확인했으니 이제 도메인을 구현해 보겠다. 

이때 구현해야 하는 목록은 다음과 같다. 

- HTTP API : Pydantic 을 이용하여 Response, Request Body 를 정의한다. 
- Router : FastAPI 의 Router 를 이용하여 API 를 구현하고, FastAPI 의 main.py 에 등록한다.
- CRUD: 실제로 데이터를 처리하기 위한 CRUD 을 구현한다.

이떼 FastAPI 의 Depends 를 이용하여 Session 에 대해서 의존성을 주입하여 사용하겠다. 

- DI(Dependency Injection) : 의존성 주입을 이용하여 FastAPI 의 Session 을 주입받아 사용한다.

먼저 Router 를 구현하기 전에 아래 명령어를 통해 백엔드 서버를 구동하자. 

```shell
uvicorn main:app --reload
```

### Router 

먼저 Question 을 처리하기 위한 API 를 만들어 보겠다. 

모듈을 별도로 구성하지 않고 `domain` 하위에 router 파일을 구성하겠다. 

- domain/question_router.py

해당 파일을 생성하고 아래와 같이 코드를 작성하자. 

```python 
from fastapi import APIRouter

from database import SessionLocal
from models import Question

router = APIRouter(prefix="/question")


@router.get("/list")
def question_list():
    db = SessionLocal()
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    db.close()
    return _question_list

```

- router : FastAPI 의 Router 를 생성한다. 여기서 생성된 라우터를 FastAPI 앱에 등록해야만 라우팅 기능이 동작한다. 
- prefix : API 의 prefix 를 설정한다.
  - 실제 API 요청시 `/question/list` 로 요청이 들어온다.
- @router.get("/list") : GET 방식의 API 를 생성한다.

코드를 살펴보면 `db.close()` 를 통해서 사용한 세션을 커넥션 풀에 반환하고 있다. 세션을 종료하는것으로 오해하지 말자. 

이렇게 생성된 router 객체는 FastAPI 앱에 등록해야한다. 아래와 같이 main.py 에 등록하자. 

```python
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain import question_router
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router.router)
```

- `origins` : 허용할 도메인을 설정한다.
- `app.add_middleware` : FastAPI 앱에 CORS 미들웨어를 추가한다.
  - `allow_origins` : 허용할 도메인을 설정한다.
  - `allow_credentials` : 쿠키를 허용할지 여부를 설정한다.
  - `allow_methods` : 허용할 HTTP 메서드를 설정한다.
  - `allow_headers` : 허용할 HTTP 헤더를 설정한다.
- `app.include_router(question_router.router)` : FastAPI 앱에 router 를 등록한다.

이제 서 Question API 가 정상적으로 동작하는지 확인해보자.

```shell
curl -X GET "http://localhost:8000/question/list"
[{"create_date":"2025-05-15T12:41:22.822039","subject":"질문 제목","content":"질문 내용","id":1}]
```

정상적으로 동작하는 것을 확인하였다. 브라우저에서 아래의 URL 로 접근해보자. 

- http://localhost:8000/docs#/

이는 FastAPI 에서 제공하는 Swagger API 문서이다. 여기서 API 요청 테스트가 가능하기도 하니 유용하게 사용할 수 있다.

> 사진은 캡처하지 않았으니 직접 들어가서 확인해 볼 것

### DI(Dependency Injection)

FastAPI 에서 제공하는 DI 를 이용해서 데이터베이스 세션의 생성과 반환을 자동화 할 수 있다. 아래 코드를 살펴보자. 

- database.py

```python
import contextlib

@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- `contextlib` : 파이썬 표준 라이브러리로 컨텍스트 매니저를 제공하는 모듈이다.
- `contextmanager` : 컨텍스트 매니저를 생성하는 데코레이터이다.

이렇게 등록된 get_db 는 with 문과 함께 사용할 수 있다. 

```python
with get_db() as db:
    # using db session 
    pass 
```

이제 `question_router`에서 `get_db`를 with 문으로 사용하도록 변경하겠다. 

```python
from fastapi import APIRouter

from database import SessionLocal, get_db # get_db 추가
from models import Question

router = APIRouter(prefix="/question")


@router.get("/list")
def question_list():
    with get_db() as db: # get_db 와 with 문을 이용해서 세션 객체를 자동으로 생성하고 반환한다.
        _question_list = db.query(Question).order_by(Question.create_date.desc()).all()

    return _question_list
```

이제 `db.close()` 를 호출하지 않아도 세션이 자동으로 종료된다.

이보다 더 효율적으로 사용하는 방법은 FastAPI 에서 제공하는 `Depends`를 사용하는 방법이다. 

아래와 같이 `Depends`를 이용해서 의존성을 주입하도록 변경하였다. 

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Question

router = APIRouter(prefix="/question")


# @router.get("/list")
# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#
#     return _question_list

@router.get("/list")
def question_list(db: Session = Depends(get_db)):
    return db.query(Question).order_by(Question.create_date.desc()).all()
```

- `Depends` : FastAPI 에서 제공하는 의존성 주입을 위한 클래스이다.  
- `db: Session = Depends(get_db)` : db 파라미터에 get_db() 를 의존성 주입한다.

`Depends`는 매개변수로 전달받은 함수를 호출하여 그 결과를 반환하는 역할을 한다. 여기까지 구현한 코드에서 주의해야할 점은 `@contextlib.contextmanager` 이다. 해당 라이브러리를 사용하면 get_db 의 값이 `contextlib._GeneratorContextManager` 객체를 반환한다. 이렇게 되면 FastAPI 의 종속성 주입이 제대로 동작하지 않을 수 있기 때문에 `get_db`에서 `@contextlib.contextmanager` 를 제거해야 한다. 

`database.py` 의 최종적인 모습은 다음과 같다. 

- auto_commit 데코레이터는 나중에 사용하려고 만들어 놓은거니 무시하고 넘어가자. ₩

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_SOURCE = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_SOURCE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def auto_commit(func):
    def wrapper(*args, **kwargs):
        try:
            db = kwargs.get('db')
        except AttributeError:
            raise AttributeError('You need to define db attribute')

        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise e
    return wrapper

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

