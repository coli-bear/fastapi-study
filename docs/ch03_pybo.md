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

> 아래 코드에 moment.js 를 사용하여 날짜 형식을 처리한다. moment.js 는 날짜와 시간을 다루는 라이브러리로, 다양한 형식으로 날짜를 출력할 수 있다. 여기서는 한국어 로케일을 설정하여 날짜를 한국어로 출력한다. 

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

이제 사용자 로그인과 로그아웃을 위한 UI 를 구현하겠다. 이때 주의해야할 점이 있는데 로그인요청시 헤더는 `application/x-www-form-urlencoded` 로 요청해야 한다. 이는 OAuth2의 규칙이다. 이에 필요한 패키지를 설치하자.

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

질문과 답변 작성한 사람을 저장하기 위해서는 질문과 답변에 사용자 정보를 맵핑해야 할 것이다. 그러면 API 요청시 사용자 정보는 어떻게 가져올까? 기본적으로 RestAPI 에서는 세션에 데이터를 저장하는것이 아닌 별도의 방법으로 관리하게 된다. 여기서는 JWT 토큰의 payload 에서 username 을 가져와 처리할 것이다. 

> 스케일 아웃에 의한 서버간 세션 공유가 불가능 한 경우에는 JWT 토큰을 이용해서 사용자 정보를 관리한다. 더 나아가 보안상의 이유로 주요정보는 별도의 DBMS 또는 Redis 와 같은 인메모리 DBMS 에 저장하고 JWT 토큰에는 사용자 ID 만 저장하는 방법도 있다.



