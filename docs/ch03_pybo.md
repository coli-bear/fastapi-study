from domain.answer.answer_schema import AnswerCreateSchemafrom sqlalchemy import DateTime

# 파이보 서비스 개발

이제 wikidocs 에서 제공하는 토이프로젝트인 파이보를 구현하자.

여기서는 기본적인 내용은 커밋 이력을 확인하고, 주요한 내용만 정리하겠다.

## Store

이어서 Store를 구현하겠다. Store 는 로컬 스토리지에 저장되는 데이터를 관리하며, 로그인정보, 페이지 정보등 사용자가 웹 서비스를 사용하는데 필요한 영속적인 데이터를 관리하는데 사용한다.

- frontend/src/lib/store.js

```javascript
import {writable} from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const parsed = storedValueStr != null ? JSON.parse(storedValueStr) : initValue;
    const store = writable(parsed);
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_signed = persist_storage("is_signed", false)
```

- page: 현재 페이지 정보를 관리하는 store
- access_token: 로그인 시 발급받은 토큰을 관리하는 store
- username: 로그인한 사용자의 이름을 관리하는 store
- is_signed: 로그인 상태를 관리하는 store

이제 이를 활용한 화면을 구현해보겠다.

## Navigation Bar

파이보 서비스의 네비게이션 바를 구현하겠다. 여기서는 Svelte SPA Router 를 사용하여 페이지 이동을 처리한다.

- frontend/src/components/NavigationBar.svelte

```sveltehtml

<script>
    import {link} from "svelte-spa-router";
    import {page} from "../lib/store.js";

    console.log(page)
</script>

<!-- Navigation bar -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/question" on:click="{() => {$page = 0}}">Pybo</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"/>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a use:link class="nav-link" href="#/signup">회원가입</a>
                </li>
                <li class="nav-item">
                    <a use:link class="nav-link" href="#/signin">로그인</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

이제 네비게이션 바와 페이지 이동을 위한 링크를 추가 하자

> 아래 코드에 moment.js 를 사용하여 날짜 형식을 처리한다. moment.js 는 날짜와 시간을 다루는 라이브러리로, 다양한 형식으로 날짜를 출력할 수 있다. 여기서는 한국어 로케일을 설정하여 날짜를
> 한국어로 출력한다.

- frontend/src/routes/Question.svelte

```sveltehtml

<script>
    import moment from "moment/min/moment-with-locales"

    moment.locale('ko')
    import {page} from "../lib/store"

    // 네비게이션 바 컴포넌트 임포트
    import Navigation from "../components/Navigation.svelte";

    // 페이징 처리를 위한 변수 선언
    let size = 10
    let total = 0
    let pages = [];

    let question_list = []

    $: total_page = Math.ceil(total / size)

    // 페이지 번호 범위 총 10개 표시를 위한 함수 추가 
    function get_pagination_range(page_number = 0, size = 10, total = 0) {
        if (total === 0) return [];
        let _total_page = Math.ceil(total / size)
        const visiblePages = 10;

        // 0-based page index를 1-based 페이지 번호로 변환
        const currentPage = page_number + 1;

        let start = currentPage - Math.floor(visiblePages / 2);
        let end = currentPage + Math.floor(visiblePages / 2) - 1;

        if (start < 1) {
            start = 1;
            end = Math.min(visiblePages, _total_page);
        }

        if (end > _total_page) {
            end = _total_page;
            start = Math.max(1, _total_page - visiblePages + 1);
        }

        const range = [];
        for (let i = start; i <= end; i++) {
            range.push(i);
        }

        return range;
    }

    // 페이지 번호에 해당하는 질문 목록을 가져오는 함수 수정
    function get_question_list(_page) {
        let params = {
            page: _page,
            size: size
        }
        fastapi('GET', '/api/question/list', params, (json) => {
            total = json.total
            question_list = json.questions
            $page = _page
            pages = get_pagination_range($page, size, total)
        })
    }

    $: get_question_list($page)
</script>
<!-- 네비게이션 바 추가 -->
<Navigation/>
<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th>제목</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
            <tr>
                <td>{ total - ($page * size) - i }</td>
                <td>
                    <a use:link href="/question/{question.id}">{question.subject}</a>
                    {#if question.answers.length > 0 }
                        <span class="text-danger small mx-2">{question.answers.length}</span>
                    {/if}
                </td>
                <!-- 작성일시 포멧 변경 -->
                <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
            </tr>
        {/each}
        </tbody>
    </table>
    <!-- Pagination Start -->
    <ul class="pagination justify-content-center">
        <li class="page-item">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( 0)}">처음</button>
        </li>
        <li class="page-item {$page <= 0 && 'disabled'}">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( $page-1)}">이전</button>
        </li>

        <!-- Page Number Display -->
        {#each pages as p}
            <li class="page-item {p - 1 === $page && 'active'}">
                <button on:click={() => get_question_list(p - 1)} class="page-link">{p}</button>
            </li>
        {/each}
        <!-- Next Button -->
        <li class="page-item {$page >= total_page -1  && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
        </li>
        <li class="page-item">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( total_page -1)}">마지막</button>
        </li>
    </ul>
    <!-- Pagination End -->
    <a use:link href="/question/create/" class="btn btn-primary">질문 등록하기</a>
</div>
```

위 코드에서 주석되어있는 부분을 참고하여 Question.svelte 파일을 수정 하자.

> 이 부분을 로그인 구현 후 정리해서 조금 대충 정리 되었다.

## Pybo User

### User Model

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

이제 router 를 등록해서 API 구현부와 UI를 최종적으로 완성하겠다.

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

이제 사용자 로그인과 로그아웃을 위한 UI 를 구현하겠다. 이때 주의해야할 점이 있는데 로그인요청시 헤더는 `application/x-www-form-urlencoded` 로 요청해야 한다. 이는 OAuth2의
규칙이다. 이에 필요한 패키지를 설치하자.

```shell
npm install qs 
```

다음으로 API 요청을 위한 fastapi 함수를 수정하겠다.

- frontend/src/lib/api.js

```javascript
import qs from "qs"

...

function default_options(method, params, content_type = 'application/json') {
    let options = {
        method: method,
        headers: {
            'Content-Type': content_type,
            'Accept': content_type
        }
    }
    if (method !== 'get') {
        options['body'] = JSON.stringify(params);
    }
    return options
}

function signin_options(params) {
    return {
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        },
        body: qs.stringify(params)
    }
}

export const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation.toLowerCase();
    let _url = _generate_url(method, url, params);
    let options = operation === 'signin' ? signin_options(params) : default_options(method, params);

...
}
```

먼저 로그인 요청과 일반 요청을 구분 하기 위해 두 함수를 정의했다.

- signin_options: 로그인 요청을 위한 옵션을 정의
- default_options: 일반 요청을 위한 옵션을 정의

이제 로그인 화면을 구현 해보자

- frontend/src/routes/UserSignIn.svelte

```sveltehtml

<script>
    import {push} from "svelte-spa-router";
    import {fastapi} from "../lib/api.js";
    import Error from "../components/Error.svelte";

    let error = {detail: []}
    let signin_username = "";
    let signin_password = "";

    function sign_error(json) {
        error = json;
    }

    function signin_success_callback(json) {
        push("/question")
    }

    function signin(event) {
        event.preventDefault()
        let url = "/api/user/signin"
        let params = {
            username: signin_username,
            password: signin_password
        }
        fastapi('signin', url, params, signin_success_callback, sign_error)
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Sign In</h5>
    <Error error={error}/>
    <form method="post">
        <div class="mb-3">
            <label for="username">username</label>
            <input type="text" class="form-control" id="username" bind:value="{signin_username}">
        </div>
        <div class="mb-3">
            <label for="password">password</label>
            <input type="password" class="form-control" id="password" bind:value="{signin_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{signin}">Sign In</button>
    </form>
</div>
```

fastapi 첫 인자를 signin 으로 설정했다. 이는 fastapi 함수에서 signin_options 함수를 호출하게 된다.
이제 로그인 화면에서 로그인을 하면 토큰을 발급받게 되고, 이를 통해 API 호출시 인증을 처리할 수 있다.

## Sign Out

이제 네비게이션 바에 로그인 상태를 표시하고 로그아웃 기능을 추가하자

```sveltehtml

<script>
    import {link} from "svelte-spa-router";
    import {access_token, is_signed, page, username} from "../lib/store.js";
</script>

<!-- Navigation bar -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/question" on:click="{() => {$page = 0}}">Pybo</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"/>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- Navigation Bar Sign In 처리 시작 -->
                {#if $is_signed}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signin" on:click={()=>{
                            $access_token = "";
                            $username = "";
                            $is_signed = false;
                        }}>로그아웃 ({$username})</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signup">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signin">로그인</a>
                    </li>
                {/if}
                <!-- Navigation Bar Sign In 처리 끝 -->
            </ul>
        </div>
    </div>
</nav>
```

주석 부분을 참고하여 코드를 수정하면 된다. 로그인 완료시 네비게이견 바를 수정하여 로그인 상태를 표시하고 로그아웃 기능을 추가했다. 로그아웃시에는 로컬 스토리지에 저장된 로그인 정보를 초기화한다.

## Question/Answer 글쓴이

질문과 답변 작성한 사람을 저장하기 위해서는 질문과 답변에 사용자 정보를 맵핑해야 할 것이다. 그러면 API 요청시 사용자 정보는 어떻게 가져올까? 기본적으로 RestAPI 에서는 세션에 데이터를 저장하는것이 아닌
별도의 방법으로 관리하게 된다. 여기서는 JWT 토큰의 payload 에서 username 을 가져와 처리할 것이다.

> 스케일 아웃에 의한 서버간 세션 공유가 불가능 한 경우에는 JWT 토큰을 이용해서 사용자 정보를 관리한다. 더 나아가 보안상의 이유로 주요정보는 별도의 DBMS 또는 Redis 와 같은 인메모리 DBMS 에
> 저장하고 JWT 토큰에는 사용자 ID 만 저장하는 방법도 있다.

### 사전작업

먼저 SQLite 에서 ORM 사용시 발생하는 문제가 있다. 이를 해결하기 위해 아래와 같이 코드를 수정해주자

> 프로젝트에서는 PostgreSQL 을 사용하기 때문에 문제가 발생하지는 않는다.

- database.py

```python
from sqlalchemy import MetaData

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)
```

위 naming_convention 은 RDBMS 컨벤션으로 주로 위와같이 정의해서 사용한다. sqlalchemy 에서 자동으로 생성된 규칙을 보면 아래와 같이 정의되어 있는것을 확인할 수 있다. 이를 맞추기 위해
위 코드를 적용하는게 좋아보인다.

- `answer_question_id_fkey` : 답변 테이블에서 질문 테이블을 참조하기 위한 외래키 이름 sqlalchemy 에서 자동으로 생성된 이름이다.

이제 env.py 에서 SQLite 마이그레이션을 위한 설정을 추가하겠다.

- migrations/env.py

```python
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )


def run_migrations_online() -> None:
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
        )

```

위와 같이 render_as_batch=True 를 설정하면 SQLite 에서도 마이그레이션을 적용할 수 있다.

> 참고 : `render_as_batch=True`의 의미 <br/>
> `Alembic` 에서 사용하는 옵션으로 SQLite 와 같이 일부 제약이 있는 데이터베이스에서 제약조건이 있는 메이그레이션을 가능하게 해주는 설정 <br/>
> - ALTER TABLE 명령을 직접 실행하지 않고 `배치모드`로 처리하도록 설정하는 옵션
> - SQLite는 ALTER TABLE 로 컬럼 삭제, 타입 변경, 제약조건 수정 등 직접 가능하지 않음 (스키마 변경 지원 X)
>
> 이 옵션을 설정하면 Alembic 은 다음과 같은 방식으로 동작한다.
> 1. 기존 테이블 내용 백업
> 2. 새로운 테이블 생성 (변경 사항 반영)
> 3. 데이터를 새로운 테이블로 복사
> 4. 기존 테이블 삭제
> 5. 새로운 테이블의 이름을 원래대로 변경
>
> 즉 간접적인 방식으로 우회해서 테이블의 스키마를 변경하게 된다. 이는 SQLite 를 사용하는 프로젝트에서 마이그레이션이 복잡한 경우에 필요하다.

이제 적용해보겠다.

```shell
alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'question_id_seq' as owned by integer column 'question(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'answer_id_seq' as owned by integer column 'answer(id)', assuming SERIAL and omitting
  Generating /Users/geontae/PycharmProjects/FastAPIProject/example/migrations/versions/7e8669dcfeea_.py ...  done
```

이렇게 생성된 `eb7657820ed0_.py` 리비전 파일을 확인해 보자

```python
def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.drop_constraint('user_username_key', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')
        batch_op.create_unique_constraint('user_username_key', ['username'])
        batch_op.create_unique_constraint('user_email_key', ['email'])
```

기존에 만들었던 `user_email_key`, `user_username_key` 제약조건을 제거하고, 새로운 제약조건 `uq_user_email`, `uq_user_username` 를 추가하는 것을 확인할 수
있다.

##### 동작순서

1. 기존 제약조건 제거
2. 새로운 제약조건 추가

이제 이 리비전 파일을 적용해 보자

```shell
alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 7f008731ea15 -> 7e8669dcfeea, empty message
```

### 사용자 맵핑

이제 질문과 답변에 사용자 정보를 맵핑하기 위해서 다음과 같이 모델을 수정하겠다.

- models.py

```python
class Question(Base):
    __tablename__ = "question"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # 추가
    user = relationship("User", backref="question_users")  # 추가


class Answer(Base):
    __tablename__ = "answer"

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # 추가
    user = relationship("User", backref="answer_users")  # 추가

```

이제 리비전 파일을 생성하고 적용하겠다.

- 이를 적용하기 전에 먼저 데이터를 삭제하자. 위에서 ForeignKey 를 nullable=False 로 설정했기 때문에 기존에 데이터가 있는 상태에서 적용하면 오류가 발생한다. 따라서 먼저 데이터를 삭제하고
  적용해야 한다.

```shell
alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'answer_id_seq' as owned by integer column 'answer(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected added column 'answer.user_id'
INFO  [alembic.autogenerate.compare] Detected added foreign key (user_id)(id) on table answer
INFO  [alembic.autogenerate.compare] Detected added column 'question.user_id'
INFO  [alembic.autogenerate.compare] Detected added foreign key (user_id)(id) on table question
  Generating /Users/geontae/PycharmProjects/FastAPIProject/example/migrations/versions/4347f84829f1_.py ...  done

alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 7e8669dcfeea -> 4347f84829f1, empty message
```

사용자 정보를 맵핑하기 위한 기본적인 작업을 완료했다 이제 질문과 답변 작성시 글쓴이 정보를 가져와보겠다. 그 절차는 아래와 같다.

1. 프론트엔드에서 로그인 성공 후 액세스토큰을 저장
2. 백엔드 API 호출시 헤더 정보에 액세스 토큰을 포함하여 요청
3. 백엔드에서 액세스 토큰을 분석하여 사용자명 취득
4. 사용자명으로 사용자 조회

이를 처리하기 위한 함수를 작성하겠다.

- domain/user/user_router.py

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/signin")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user_by_username(db=db, username=username)
        if user is None:
            raise credentials_exception
        return user
```

위 코드를 잠시 설명하고 넘어가겠다. 먼저 `OAuth2PasswordBearer` 를 이용해서 토큰을 가져올 수 있다. 이때 tokenUrl 을 설정해줄 수 있다.

- tokenUrl: Swagger UI 에서 Authentication

이제 질문과 답변에 사용자 정보를 맵핑하기 위해 다음과 같이 함수를 수정하자.

- domain/question/question_router.py

```python
@router.post("/create", status_code=status.HTTP_201_CREATED)
def question_create(_question: QuestionCreateSchema,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
  question_crud.question_create(db=db, question=_question, current_user=user)
```

- domain/question/question_crud.py

```python
@auto_commit
def question_create(db: Session, question: QuestionCreateSchema, user: User):
    question = Question(subject=question.subject,
                        content=question.content,
                        create_date=datetime.now(),
                        user=user)
    db.add(question)
```

이제 질문 작성시 사용자 정보를 맵핑할 수 있다. 답변도 마찬가지로 처리하면 된다.

- domain/answer/answer_router.py

```python
@router.post("/create/{question_id}", status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int,
                  _answer_create: AnswerCreateSchema,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    _question = question_crud.question_detail(db, question_id)
    if not _question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")
    answer_crud.create_answer(db, question=_question, answer=_answer_create, user=user)
```

- domain/answer/answer_crud.py

```python
@auto_commit
def create_answer(db: Session, question: Question,
                  answer: AnswerCreateSchema,
                  user: User):
    db_answer = Answer(question=question,
                       content=answer.content,
                       create_date=datetime.now(),
                       user=user)
    db.add(db_answer)
```

이제 구현이 완료되었으니 Swagger UI 를 통해서 API 테스트를 해보자. 로그인(Swagger UI 에서 Authorize에서 로그인) 후 질문 등록 API 를 호출하면 아래와 같이 요청이 나가는것을 확인할
수 있다.

```http request
POST /api/question/create
content-type: application/json
accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJpbG4xMDI3IiwiZXhwIjoxNzQ5NzQwNzUyfQ.yH0v0QkCBKwkGuVKCo8asKDrvuZB-6D1eqUkWypo4ig

{
  "subject": "string",
  "content": "string"
}
```

Authorization 헤더에 Bearer 토큰이 포함되어 있는 것을 확인할 수 있다. 이 토큰을 통해서 백엔드에서 사용자 정보를 조회하고, 질문 작성시 사용자 정보를 맵핑할 수 있다.

이제 해더에서 인증정보를 제외하고 다시 요청해보자 (Swagger UI 에서 Authorize에서 로그아웃)

아래와 같이 응답 헤더와 응답 바디가 오는것을 확인 가능하다.

- 응답 바디

```http response
401 Unauthorized

{
  "detail": "Not authenticated"
}
```

- 응답 헤더

```
 access-control-allow-credentials: true 
 content-length: 30 
 content-type: application/json 
 date: Wed,11 Jun 2025 06:08:15 GMT 
 server: uvicorn 
 www-authenticate: Bearer 
```

www-authenticate 헤더에 Bearer 가 포함되어있어야 한다고 명시하고 있다.

### 질문/답변 프론트엔드 수정

이제 질문과 답변에 대한 처리를 하기 위해 프론트엔드 코드를 수정하겠다. 먼저 인증 실패에 대하나 처리를 위해 fastapi 함수 먼저 수정해보겠다.

- frontend/src/lib/api.js

```javascript
import {access_token, username, is_signed} from "./store.js";
import {get} from "svelte/store";
import {push} from "svelte-spa-router";
```

먼저 로컬 스토리지에서 access_token, username, is_signed 를 가져와서 사용한다. svelte/store 에서 get 함수를 이용해서 스토어 값을 가져올 수 있다.

- frontend/src/lib/api.js

```javascript
function _is_authentication_error(method, status) {
    return method !== 'signin' && (status === 401 || status === 403);
}

function unauthorized_callback() {
    access_token.set('');
    username.set('');
    is_signed.set(false);
    alert('Authentication error, please sign in again.');
    push('/signin');
}
```

위 두 함수를 추가해서 인증 오류에 대한 체크와 인증 오류에 대한 callback 를 처리하겠다. 다음으로 API 요청시(로그인 API 제외) 토큰을 넘겨줄 수 있도록 `Authorization` 헤더를 추가하겠다.

- frontend/src/lib/api.js

```javascript
function default_options(method, params, content_type = 'application/json') {
...

    const _access_token = get(access_token);
    if (_access_token) {
        options.headers['Authorization'] = `Bearer ${_access_token}`;
    }

...
}
```

위 default_options 에서 토큰이 있는 경우에 `Authorization` 헤더를 추가하도록 했다. 이제 API 요청시 토큰이 있는 경우에만 헤더에 토큰을 포함하게 된다.

다음으로 인증 실패에 대한 callback 처리를 추가하자

- frontend/src/lib/api.js

```javascript
export const fastapi = (operation, url, params, success_callback, failure_callback) => {
    response
        .json()
        .then((json) => {
            if (_is_authentication_error(method, response.status)) { // 인증 오류 체크 추가
                _failure_callback(json, unauthorized_callback)  // 인증 오류 콜백
            } else if (_is_error(response)) {
                _failure_callback(json, failure_callback);
            } else {
                _success_callback(json, success_callback);
            }
        })
        .catch((error) => {
            alert(JSON.stringify(error))
        })
}
)
.
catch((error) => {
    alert(error);
})
}
```

마지막으로 로그아웃 된 경우에는 질문 등록과 답변이 불가능하도록 만들어 보겠다.

- frontend/src/routes/Question.svelte

```sveltehtml

<script>
    import {page, is_signed} from "../lib/store"
</script>
<a use:link href="/question/create/" class="btn btn-primary {$is_signed ? '' : 'disabled'}">질문 등록하기</a>
```

is_signed 를 가져와서 해당 값 여부에 따라서 활성화/비활성화 되도록 a 태그의 class 에 `{$is_signed ? '' : 'disabled'}` 를 추가했다. 답변도 마찬가지로 처리하면 된다.

### 질문/답변 작성자 표시

이제 질문과 답변 작성자를 표시해보자. 먼저 응답에 대한 Schema 를 수정하겠다.

- domain/user/user_schema.py

```python
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
```

먼자 사용자 정보를 표시해 줄 UserSchema 를 정의했다. 이제 질문과 답변에 사용자 정보를 포함시키겠다.

- domain/question/question_schema.py

```python
class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str | None = None
    create_date: datetime.datetime
    answers: list[AnswerSchema] = []
    user: UserSchema | None

```

- domain/answer/answer_schema.py

```python
class AnswerSchema(BaseModel):
    id: int
    content: str
    create_date: datetime
    user: UserSchema | None
```

이제 화면에 글쓴이에 대한 정보를 표시하도록 하자

- frontend/src/routes/Question.svelte

```sveltehtml
    ...

<table class="table">
    <thead>
    <tr class="text-center table-dark">
        <th>번호</th>
        <!-- th style 적용 -->
        <th style="width: 50%">제목</th>
        <!-- 글쓴이 추가 -->
        <th>글쓴이</th>
        <th>작성일시</th>
    </tr>
    </thead>
    <tbody>
    {#each question_list as question, i}
        <!-- tr 클래스에 text-center 추가 -->
        <tr class="text-center">
            <td>{ total - ($page * size) - i }</td>
            <!-- td class="text-start" 추가 -->
            <td class="text-start">
                <a use:link href="/question/{question.id}">{question.subject}</a>
                {#if question.answers.length > 0 }
                    <span class="text-danger small mx-2">{question.answers.length}</span>
                {/if}
            </td>
            <!-- 글쓴이 추가 -->
            <td>{question.user ? question.user.username : ""}</td>
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
    {/each}
    </tbody>
</table>

...
```

주석 부분을 참고하여 코드를 추가하면 된다 다음은 상세 화면에서 글쓴이를 표시하겠다.

- frontend/src/routes/QuestionDetail.svelte

```sveltehtml
    ...

<h2 class="border-bottom py-2">{question_detail.subject}</h2>
<div class="card my-3">
    <div class="card-body">
        <div class="card-text" style="white-space: pre-line;">{question_detail.content}</div>
        <div class="d-flex justify-content-end">
            <!-- 글쓴이 추가 시작 -->
            <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{ question_detail.user ? question_detail.user.username : ""}</div>
                <div>{moment(question_detail.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
            </div>
            <!-- 글쓴이 추가 종료 -->
        </div>
    </div>
</div>

<Error error={error}/>
<form method="post" class="my-3">
    <div class="mb-3">
            <textarea rows="10"
                      bind:value={content}
                      class="form-control"
                      disabled={$is_signed ? '' : 'disabled'}
            ></textarea>
    </div>
    <input type="submit" value="답변 등록" class="btn btn-primary {$is_signed ? '' : 'disabled'}"
           on:click={post_answer}/>
</form>
<button class="btn btn-secondary" on:click="{() => {
        push('/question')
    }}">목록으로
</button>
<h5 class="border-bottom my-3 py-2">{question_detail.answers.length}개의 답변이 있습니다.</h5>
{#each question_detail.answers as answer}
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
            <div class="d-flex justify-content-end">
                <!-- 글쓴이 추가 시작-->
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                    <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
                <!-- 글쓴이 추가 종료-->
            </div>
        </div>
    </div>
{/each}


...

```

주석 부분을 참고하여 코드를 추가하면 된다. 이제 질문과 답변 작성자를 표시할 수 있다.

### 개시물 수정과 삭제

등록/조회에 대해 처리했으니 수정/삭제에 대해 구현해보도록 하겠다. 먼저 수정사항이 발생하게 되면 수정한 날짜가 필요할 것이다. 이것을 위해 Question, Answer 모델에 수정날짜를 추가하겠다.

- models.py

```python
class Question(Base):
    ...

    modify_date = Column(DateTime, nullable=True)

    def is_owner(self, user_id: int) -> bool:
        """질문 작성자 여부 확인"""
        return self.user_id == user_id


class Answer(Base):
    ...

    modify_date = Column(DateTime, nullable=True)

    def is_owner(self, user_id: int) -> bool:
        """답변 작성자 여부 확인"""
        return self.user_id == user_id
```

이제 리비전 파일을 생성하고 적용하자

```shell
alembic revision --autogenerate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'question_id_seq' as owned by integer column 'question(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'answer_id_seq' as owned by integer column 'answer(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected added column 'answer.modify_date'
INFO  [alembic.autogenerate.compare] Detected added column 'question.modify_date'
  Generating /Users/geontae/PycharmProjects/FastAPIProject/example/migrations/versions/2b6ff85702a7_.py ...  done

alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 4347f84829f1 -> 2b6ff85702a7, empty message
```

이제 Question, Answer 에서 수정가능한 데이터를 전달받아 처리하기 위한 Schema 를 정의하겠다.

- domain/question/question_schema.py

```python
class QuestionUpdateSchema(QuestionCreateSchema):
    question_id: int

    @field_validator('question_id')
    def positive_id(cls, question_id: int):
        if not question_id or question_id <= 0:
            raise ValueError("질문 ID는 양수여야 합니다.")
        return question_id
```

- domain/answer/answer_schema.py

```python
class AnswerUpdateSchema(AnswerCreateSchema):
    answer_id: int

    @field_validator('answer_id')
    def positive_id(cls, answer_id: int):
        if not answer_id or answer_id <= 0:
            raise ValueError("답변 ID는 양수여야 합니다.")

        return answer_id
```

데이터를 수정하기 위해서는 식별자가 필요하다. 따라서 질문과 답변에 대한 식별자를 전달 받아 해당 식별자로 데이터를 조회해서 수정할 수 있도록 한다. 이때 식별자는 필수로 전달받아야 하며 양수이어야 하기 때문에
validator 를 이용해 검증을 하였다.

이제 질문과 답변을 수정하기 위한 API 를 작성하겠다. 각각의 API 명세는 아래와 같다.

| 구분    | Method | URL                              | 설명        |
|-------|--------|----------------------------------|-----------|
| 질문 수정 | PUT    | /api/question/update             | 질문 수정 API |
| 답변 수정 | PUT    | /api/answer/update/{question_id} | 답변 수정 API |

스키마는 `QuestionUpdateSchema`, `AnswerUpdateSchema` 를 사용한다. 이제 API 를 작성하겠다.

- domain/question/question_router.py

```python
@router.put("/update", status_code=status.HTTP_200_OK)
def question_update(_question_update: QuestionUpdateSchema,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    question = question_crud.question_detail(question_id=_question_update.question_id, db=db)

    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")

    if not question.is_owner(user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 질문 작성자만 수정할 수 있습니다.")

    question_crud.update_question(question=question, question_update=_question_update, db=db)
```

여기서 주의할 점은 질문에 대한 수정은 수정한 사람 본인만 가능하다는 것이다. 따라서 본인의 여부를 확인하기 위해 Question 모델에 `is_owner` 메소드를 추가해서 사용자 ID와 비교하여 본인인지
확인하도록 하였다.

- 이 부분은 이후에 리팩토링 조금 해보겠다.

이제 질문에 대해 수정하는 crud 함수를 작성하겠다. 위 코드에서는 미리 update_question 함수를 호출하고 있다. 다라서 question_crud.py 에 아래와 같이 함수를 작성하겠다.

- domain/question/question_crud.py

```python
@auto_commit
def update_question(db: Session, question: Question, question_update: QuestionUpdateSchema):
    question.subject = question_update.subject
    question.content = question_update.content
    question.modify_date = datetime.now()  # 수정일시 추가
    db.add(question)
```

이제 답변에 대해서도 동일하게 처리하겠다.

- domain/answer/answer_router.py

```python
@router.put("/update", status_code=status.HTTP_200_OK)
def update_answer(answer_update: AnswerUpdateSchema,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    answer = answer_crud.get_answer_by_id(db, answer_update.answer_id)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="답변을 찾을 수 없습니다.")

    if not answer.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 답변 작성자만 수정할 수 있습니다.")

    answer_crud.update_answer(db=db, answer=answer, answer_update=answer_update)
```

답변에 대해서도 동일하게 처리하되, 답변 작성자 여부를 확인하기 위해 Answer 모델에 `is_owner` 메소드를 추가하여 사용자 ID와 비교하여 본인인지 확인하도록 하였다.

이제 답변에 대한 수정 crud 함수를 작성하겠다. 위 코드에서는 미리 update_answer 함수를 호출하고 있다. 따라서 answer_crud.py 에 아래와 같이 함수를 작성하겠다.

- domain/answer/answer_crud.py

```python
@auto_commit
def update_answer(db: Session, answer: Answer, answer_update: AnswerUpdateSchema):
    answer.content = answer_update.content
    answer.modify_date = datetime.now()
    db.add(answer)
```

이제 FastAPI Swagger UI 를 통해서 API 테스트를 해보고 결과를 확인하자. 정상적으로 동작한다. 

이제 삭제에 대한 API 를 작성하겠다. 삭제는 question_id 또는 answer_id 를 통해서 삭제할 수 있도록 하겠다. API 명세는 아래와 같다.

| 구분    | Method | URL                               | 설명        |
|-------|--------|-----------------------------------|-----------|
| 질문 삭제 | DELETE | /api/question/delete              | 질문 삭제 API |
| 답변 삭제 | DELETE | /api/answer/delete                | 답변 삭제 API |

스키마는 `QuestionIdentifierSchema`, `AnswerIdentifierSchema` 를 사용한다. 이 스키마는 식별자만 포함된 스키마로 아래와 같이 정의한다. (리팩토링도 함께 진행한다)
- domain/question/question_schema.py

```python
class QuestionIdentifierSchema(BaseModel):
    question_id: int

    @field_validator('question_id')
    def positive_id(cls, question_id: int):
        if not question_id or question_id <= 0:
            raise ValueError("질문 ID는 양수여야 합니다.")
        return question_id

class QuestionUpdateSchema(QuestionIdentifierSchema, QuestionCreateSchema):
    pass
```

- domain/answer/answer_schema.py

```python
class AnswerIdentifierSchema(BaseModel):
    answer_id: int

    @field_validator('answer_id')
    def positive_id(cls, answer_id: int):
        if not answer_id or answer_id <= 0:
            raise ValueError("답변 ID는 양수여야 합니다.")
        return answer_id

class AnswerUpdateSchema(AnswerIdentifierSchema, AnswerCreateSchema):
    pass 
```

이제 API와 curd 함수를 작성하겠다.

- domain/question/question_router.py

```python
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(question_id: QuestionIdentifierSchema,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question = question_crud.question_detail(question_id=question_id.question_id, db=db)
    if not question:
        return

    if not question.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 질문 작성자만 삭제할 수 있습니다.")

    question_crud.delete_question(question=question, db=db)
```

- domain/question/question_crud.py

```python
@auto_commit
def delete_question(db: Session, question: Question):
    db.delete(question)
```

이제 답변에 대해서도 동일하게 처리하겠다.

- domain/answer/answer_router.py

```python
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    answer = answer_crud.get_answer_by_id(db, answer_id)
    if not answer:
        return

    if not answer.is_owner(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다. 답변 작성자만 삭제할 수 있습니다.")

    answer_crud.delete_answer(db=db, answer=answer)
```

- domain/answer/answer_crud.py

```python
@auto_commit
def delete_answer(db: Session, answer: Answer):
    db.delete(answer)
```

정상 독작하는것까지 확인하자. 

이제 화면에서 수정과 삭제를 처리할 수 있도록 하겠다. 먼저 질문 목록에서 수정과 삭제를 처리할 수 있도록 하겠다.

> UI는 따로 정리하지 않았으며 아래 링크를 참고해서 작성하면 된다.
> - [질문과 답변 수정 및 삭제](https://wikidocs.net/177112#_5)
>

삭제 API 를 호출하면 최종적으로는 데이터가 없기 때문에 204 No Content 를 호출한다. 이때 fastapi 에서 204 를 처리할 수 없어 해당부분에 대한 방어로직을 추가해 주자. 

- frontend/src/lib/api.js

```javascript
export const fastapi = (operation, url, params, success_callback, failure_callback) => {

    fetch(_url, options)
        .then((response) => {
            ...

            // 204 No Content 응답 처리 추가 
            if (response.status === 204) {
                _success_callback(undefined, success_callback)
                return
            }
            
            ...
}

```