# Frontend with Svelte

> 참고1 : [Wikidocs FastAPI - Svelte 환경 준비](https://wikidocs.net/175833)<br/>
> 참고2 : [Wikidocs FastAPI - Svelte로 프론트엔드 만들기](https://wikidocs.net/176328)<br/>
> 참고3 : [nvm 설치 참고](https://sukvvon.tistory.com/69)

이제 전체 애플리케이션을 구현하기 위해 svlete 를 사용해서 프론트엔드를 구현해보자. 이것을 기반으로 질문과 답변을 할 수 있는 애플리케이션을 만들 것이다.

- 사전에 nodejs와 npm이 설치되어 있어야 한다. nvm을 사용하여 설치하는 것을 추천한다.

> - 여기서는 화면에 대한 구현을 먼저 작성하였다. 실제 개발에서는 API 명세를 정의하고 백엔드 개발과 프론트 개발을 진행해야 한다는 것을 명심하자.
> - 개발 완료된 프론트를 기반으로 처리를 위한 백엔드 API 를 마지막에 작성하겠다.

## Svelte 설치하기

아래 명령어를 이용히 `svlete` 애플리케이션을 구성하겠다.

```shell
npm create vite@latest frontend -- --template svelte 
```

해당 명령어를 실행하게 되면 Svlete 애플리케이션을 선택가능하고 해당 위치에서 SvelteKit 을 선택해서 원하는 프로젝트 환경을 구성할 수 있다.

- 여기서는 SvelteKit 을 사용하지 않고 기본 Javascript 을 선택해서 하겠다.

```shell
npm create vite@latest frontend -- --template svelte 

> npx
> create-vite frontend --template svelte

│
◇  Scaffolding project in /Users/geontae/PycharmProjects/FastAPIProject/example/frontend...
│
└  Done. Now run:

  cd frontend
  npm install
  npm run dev
```

실행된 명령어의 결과는 위와 같다. 다음으로 패키지를 설치하기 위해 다음 명령어를 실행하자.

```shell
cd frontend
npm install
```

아래 명령어를 이용해서 애플리케이션이 정상적으로 동작하는지 확인해보자.

```shell
npm run dev

> frontend@0.0.0 dev
> vite

3:42:45 PM [vite] (client) Forced re-optimization of dependencies

  VITE v6.3.5  ready in 667 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help


```

위와같은 결과가 나온다면 정상적으로 동작된 것이다.

## 질문 목록 화면 구현

이제 앞서 만든 백엔드 애플리케이션의 목록을 보여주기 위한 프론트엔드를 구현해보자.

- `frontend/src/App.svelte` 파일을 다음과 같이 수정하자.

```sveltehtml

<script>
    let question_list = []

    function get_question_list() {
        fetch("http://localhost:8000/question/list").then(((response) => {
            response.json().then((json_data) => {
                question_list = json_data
            })
        })).catch((error => {
            alert("Error: " + error.message)
        }))
    }

    get_question_list()
</script>

<ul>
    {#each question_list as question}
        <li>> {question.subject}</li>
    {/each}
</ul>
```

### Svelte 필수 문법

정리를 하지 않으려 했지만... 프로젝트를 완전히 구현하기 위해서는 필수 내용을 정리했다.

#### 분기분

```sveltehtml

{#if 조건문1}
    <p>조건문 1 실행</p>
{:else if 조건문2}
    <p>조건문 2 실행</p>
{:else}
    <p>그 외 실행</p>
{/if}
```

#### 반복문

```sveltehtml

{#each item_list as item}
    <p>{item}</p>
{/each}
```

#### 객체 접근

```sveltehtml
{obj}
{obj.subject}
{obj.content.id}
```

### Svelte Router

Svelte Router 는 화면 이동을 위해서 필요하다. 여기 프로젝트에서는 다음과 같은 화면들이 필요하다.

- 홈 : /
- 질문 목록 : /#/question
- 질문 상세 : /#/question/:id
- 질문 작성 : /#/question/create
- 질문 수정 : /#/question/update/:id
- 답변 수정 : /#/answer/update/:answer_id
- 사용자 로그인 : /#/signin
- 사용자 회원가입 : /#/signup

책에서 제시하는 방법에서 몇가지 수정을 하였다 먼저 uri의 prefix 를 question 으로 통일 하였다.

> 홈 에서는 네비게이션을 제공하고, 나중에 토이 프로젝트로 해당 화면 아래 프론트 애플리케이션을 추가하겠다.

위 경로로 요청하면 해당 페이지가 렌더링 되도록 router 를 등록해보자.

먼저 `routes` 디렉토리를 생성하겠다.

```shell 
mkdir src/routes
```

다음으로 라우팅을 위한 `svelte-spa-router` 패키지를 설치하겠다.

```shell
npm install svelte-spa-router
```

CSS 적용을 위해서 `bootstrap` 패키지를 설치하겠다.

```shell
npm install bootstrap
```

#### 라우터 등록하기

먼저 기존에 App.svelte 파일을 다음과 같이 수정하겠다.

```sveltehtml

<script>
    import Router from 'svelte-spa-router'
    import Question from "./routes/Question.svelte"
    import QuestionDetail from "./routes/QuestionDetail.svelte"
    import Home from "./routes/Home.svelte";
    import QuestionCreate from "./routes/QuestionCreate.svelte";

    const routes = {
        "/": Home,
        '/question': Question,
        '/question/': Question, // 명시적으로도 허용 (선택사항)
        '/question/create': QuestionCreate,
        '/question/:question_id': QuestionDetail, // 동적 라우팅
    };
    const useHash = false; // true로 설정하면 해시 모드 사용
</script>

<Router {routes} {useHash}/>
```

Home.svelte 는 메인화면을 구현하기 위해 잠시 분리해 놨다. 그 다음으로 질문을 관리하기 위한 Question.svelte 파일을 작성하겠다

> 참고1 : wikidocs 에서는 bootstrap 을 나중에 적용하지만 여기서는 2장 까지 완성본을 기준으로 문서를 정리하기 때문에 미리 설치하고, 디자인 요소를 접목시켜놨다.<br/>
> 참고2 : 여기서 `useHash` 를 true 로 설정하면 해시 모드로 동작한다. 해시 모드는 URL 에 # 을 붙여서 페이지를 구분하는 방식이다. 예를 들어,
`http://localhost:5173/#/question` 과 같이 사용한다. 자세한 내용은 아래 링크를 참고하자.
> - [Hash Router와 Browser Router 의 차이점](https://noodabee.tistory.com/entry/Hash-Router%EC%99%80-Browser-Router%EC%9D%98-%EC%B0%A8%EC%9D%B4%EC%A0%90)

#### Home.svelte

```sveltehtml
<h1>Home</h1>
<h2>Welcome Svelte Application</h2>
<ul>
    <li><a href="#/question/">Go To Question</a></li>

</ul>
```

Home 화면에는 간단하게 메인화면을 구현하였으며, 질문 도메인을 이동하기 위한 링크를 추가하였다.

### API 호출을 위한 lib 파일 작성하기

이제 API 를 호출하기 위한 lib 파일을 작성하겠다. `src/lib/api.js` 파일을 생성하고 다음과 같이 작성하자.

```javascript
function _generate_url(method, url, params) {
    let _url = `${import.meta.env.VITE_SERVER_URL}${url.startsWith('/') ? url : '/' + url}`;
    if (method.toLowerCase() === 'get' && params && Object.keys(params).length > 0) {
        const queryString = new URLSearchParams(params).toString();
        _url += '?' + queryString;
    }
    return _url;
}

const _is_error = (response) => {
    if (!!response) {
        return !(response.status >= 200 && response.status < 300);
    }

    return true;
}

function _failure_callback(json, failure_callback) {
    if (failure_callback) {
        failure_callback(json)

    } else {
        alert(JSON.stringify(json))
    }
}

function _success_callback(json, success_callback) {
    if (!success_callback) {
        return
    }
    if (json) {
        success_callback(json)
    } else {
        success_callback()
    }
}

export const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation.toLowerCase();
    let content_type = 'application/json';
    let _url = _generate_url(method, url, params);
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

    fetch(_url, options)
        .then((response) => {
            if (response.status === 201) {
                _success_callback(undefined, success_callback)
            }

            response
                .json()
                .then((json) => {
                    if (_is_error(response)) {
                        _failure_callback(json, failure_callback);
                    } else {
                        _success_callback(json, success_callback);
                    }
                })
                .catch((error) => {
                    alert(JSON.stringify(error))
                })
        })
        .catch((error) => {
            alert(error);
        })
}
```

코드를 분석해 보면, `fastapi` 함수를 통해 FastAPI 로 구현된 API 에 `fetch` 를 이용해 API 를 호출하고 있다. 이 때 method, url, params, 성공/실패에 대한
callback 을 인자로 전달 받고 처리하고 있다. 각 함수의 설명은 아래와 같다.

- `_generate_url` : url 을 생성하는 함수로, `VITE_SERVER_URL` 환경변수를 통해 FastAPI 서버의 주소를 가져온다.
- `_is_error` : 응답이 성공인지 실패인지 판단하는 함수로, 200~300 사이의 상태코드가 아니면 실패로 간주한다.
- `_failure_callback` : 실패했을 때 호출되는 콜백 함수로, 실패 시 alert 창을 띄운다. fastapi 함수 호출시 전달받은 failure_callback 함수를 전달하면 해당 함수를
  호출한다.
- `_success_callback` : 성공했을 때 호출되는 콜백 함수로, 성공 시 json 데이터를 전달한다. fastapi 함수 호출시 전달받은 success_callback 함수를 전달하면 해당 함수를
  호출한다.
- `fastapi` : 실제 API 를 호출하는 함수로, method, url, params, 성공/실패 콜백을 인자로 받아서 fetch 를 통해 API 를 호출한다. 이 때 응답이 성공이면
  `_success_callback` 함수를 호출하고, 실패면 `_failure_callback` 함수를 호출한다.

#### Error.svelte

API 요청시 입력값에 대한 Validation 을 진행할 예정이다. 이 때 vaidation에 실패하면 출력해 줄 Error.svelte 파일을 작성하겠다.

```sveltehtml

<script>
    export let error
</script>

{#if typeof error.detail === 'string'}
    <div class="alert alert-danger" role="alert">
        <div>
            {error.detail}
        </div>
    </div>
{:else if typeof error.detail === 'object' && error.detail.length > 0}
    <div class="alert alert-danger" role="alert">
        {#each error.detail as err, i}
            <div><strong>{err.loc[1]}</strong> : {err.msg}</div>
        {/each}
    </div>
{/if}
```

export let error 을 통해 부모 컴포넌트에서 전달받은 error 를 출력해준다. error.detail 이 string 인 경우와 object 인 경우에 따라 다르게 처리한다.

이후 API 에서 제공되는 에러는 아래와 같다.

#### Question.svelte

```sveltehtml

<script>
    import {fastapi} from "../lib/api.js";
    import {link} from "svelte-spa-router"

    let question_list = []

    function get_question_list() {
        fastapi('GET', '/api/question/list', {}, (json) => {
            question_list = json
        })
    }

    get_question_list()
</script>
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
                <td>{i + 1}</td>
                <td>
                    <a use:link href="/question/{question.id}">{question.subject}</a>
                </td>
                <td>{question.create_date}</td>
            </tr>
        {/each}
        </tbody>
    </table>
    <a use:link href="/question/create/" class="btn btn-primary">질문 등록하기</a>
</div>
```

#### QuestionCreate.svelte

질문 등록을 위한 화면을 작성하겠다. 질문 등록 화면은 질문 제목과 내용을 입력받고, 등록 버튼을 클릭하면 질문이 등록된다. 질문 등록 후에는 질문 목록으로 이동한다.

```sveltehtml

<script>
    import {push} from "svelte-spa-router";
    import {fastapi} from "../lib/api.js";
    import Error from "../components/Error.svelte";

    let error = {"detail": []};
    let subject = "";
    let content = "";

    function post_question(event) {
        event.preventDefault()
        let url = "/api/question/create"
        let params = {
            "subject": subject,
            "content": content
        }
        fastapi('POST', url, params,
            (json) => {
                push("/question/")
            }, (error_json) => {
                error = error_json
            })
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 등록하기</h5>
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" bind:value={subject}>
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value={content}></textarea>
        </div>
        <button class="btn btn-primary" on:click={post_question}>등록하기</button>
    </form>
</div>
```

여기서는 `svelte-spa-router` 의 `push` 함수를 사용하여 질문 등록 후 질문 목록으로 이동한다. 질문 등록 시 에러가 발생하면 `Error.svelte` 를 통해 에러를 출력한다.

#### QuestionDetail.svelte

질문 상세 화면을 작성해보자. 여기서는 등록한 질문의 제목, 내용, 작성일시를 보여주며, 답변을 작성하고, 답변을 보여주는 화면을 작성하겠다.

```sveltehtml

<script>
    import {fastapi} from "../lib/api.js";
    import Error from "../components/Error.svelte";

    export let params = {};
    let question_id = params.question_id;
    let question_detail = {answers: []}
    let content = ''
    let error = {detail: []}

    function get_question() {
        fastapi('GET', `/api/question/detail/${question_id}`, undefined, json => {
            question_detail = json
        })
    }

    get_question()

    function post_answer(event) {
        event.preventDefault()
        let url = `/api/answer/create/${question_id}`
        let params = {
            content: content
        }

        fastapi('POST', url, params,
            (json) => {
                content = ''
                error = {detail: []}
                get_question()
            }, (err_json) => {
                error = err_json
            })

    }
</script>

<div class="container my-3">
    <!--    질문 -->
    <h2 class="border-bottom py-2">{question_detail.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question_detail.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2">
                    {question_detail.create_date}
                </div>
            </div>
        </div>
    </div>
    <!--    답변 등록-->
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10" bind:value={content} class="form-control"></textarea>
        </div>
        <input type="submit" value="답변 등록" class="btn btn-primary" on:click={post_answer}/>
    </form>
    <!--    답변 목록-->
    <h5 class="border-bottom my-3 py-2">{question_detail.answers.length}개의 답변이 있습니다.</h5>
    {#each question_detail.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
                <div class="d-flex justify-content-end">
                    <div class="badge bg-light text-dark p-2">{answer.create_date}</div>
                </div>
            </div>
        </div>
    {/each}
</div>
```

### 백엔드 API 구현

이제 프론트엔드에서 호출하는 API 를 구현하겠다. 여기서는 질문 등록, 질문 상세, 답변 등록 API 를 구현하겠다. 질문 목록은 앞장에 작성했으므로 작성하지 않겠다.

먼저 API 명세를 정리하자.

| Method | URL                               | 설명       |
|--------|-----------------------------------|----------|
| POST   | /api/question/create              | 질문 등록    |
| GET    | /api/question/detail/:question_id | 질문 상세 조회 |
| POST   | /api/answer/create/:question_id   | 답변 등록    |

#### 질문 등록 API 구현

먼저 질문을 등록하기 위해 요청 본문을 정의하겠다.

- domain/question/question_schema.py

```python
from pydantic import BaseModel, field_validator


class QuestionCreateSchema(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    @classmethod
    def not_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("빈 값은 허용되지 않습니다..")
        return value

```

여기서 `field_validator` 를 사용하였다. 여기서 주의해야 할점은 파이썬에서 메서드의 첫 인자로는 `self` 를 입력하지만 여기서는 `cls` 를 사용해야 한다는 점이다.

> not_empty 메서드가 클래스 메서드인지에 대해서 ChatGPT 에게 질문했다. <br/>
> 먼저 pydantic v1 에서는 pydantic 에서 내부 로직에 의해 동작되는 특수한 함수로 pydantic 에서 cls 에 직접 접근할수 있도록 객체를 전달하는 반면 v2 에서는 클래스 메서드로 정의되어야
> 한다. 이때 @classmethod 는 생략이 가능하며, 명시적으로 cls 를 인자로 전달받아 클래스메서드임을 나타낸다. 만약 @classmethod 를 작성하여 명시적으로 알려주려 한다면 아래와 같이 작성해야
> 동작한다.
> ```python
>    @field_validator('subject', 'content')
>    @classmethod
>    def not_empty(cls, value: str):
>        pass
> ```
> 만약 @classmethod 가 field_validator 위에 작성되었다면 해당 메서드가 정상 동작되지 않는것을 확인할 수 있다.

요청 본문을 정의했다면 이제 질문 등록 API 를 작성하겠다.

- domain/question/question_router.py

```python
from starlette import status


@router.post("/create", status_code=status.HTTP_201_CREATED)
def question_create(_question: QuestionCreateSchema, db: Session = Depends(get_db)):
    question_crud.question_create(db=db, question=_question)
```

wikidocs 에서는 응답 본문이 없으므로 204 No Content 를 사용했지만 HTTP 명세를 따라 201 Created 를 사용하였다.

> 참고 : 완전한 Restful API 개발을 위해서는 몇가지 사항이 추가되어야 한다.
> - API Version, 응답에 대한 이후 처리가 가능한 URL 제공 등 자세한 사항은 아래 링크를 통해 확인해보자 잘 정리되어 있다.
> - [Gabia - RESTful API 설계 가이드](https://library.gabia.com/contents/8339/)

이제 router 구현을 완료 하였으니 실제 database 에 저장하기 위한 함수를 작성 하겠다.

- domain/question/question_crud.py

```python
from database import auto_commit
from domain.question.question_schema import QuestionCreateSchema


@auto_commit
def question_create(db: Session, question: QuestionCreateSchema):
    question = Question(subject=question.subject, content=question.content, create_date=datetime.now())
    db.add(question)
```

이 부분에서는 1장에서 작성한 `auto_commit` 데코레이터를 사용하여 DB 에 저장하는 함수를 작성하였다.

#### 답변 등록 API 구현

> 질문 상세에서 답변 스키마를 사용하기 위해 먼저 구현 내용을 정리했다.

- domain/answer/answer_schema.py

```python
from datetime import datetime
from pydantic import BaseModel, field_validator


class AnswerCreateSchema(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, content: str):
        print(content)
        if not content or not content.strip():
            raise ValueError("컨텐츠가 비어있거나 공백일 수 없습니다.")
        return content


class AnswerSchema(BaseModel):
    id: int
    content: str
    create_date: datetime
```

먼저 답변 등록을 위한 `AnswerCreateSchema`와 답변 조회를 위한 `AnswerSchema` 를 작성하였다.

- domain/answer/answer_router.py

```python
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import get_db
from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreateSchema
from domain.question import question_crud
from domain.answer import answer_crud

router = APIRouter(prefix="/api/answer")


@router.post("/create/{question_id}", status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int, _answer_create: AnswerCreateSchema, db: Session = Depends(get_db)):
    _question = question_crud.question_detail(db, question_id)
    if not _question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="질문을 찾을 수 없습니다.")
    answer_crud.create_answer(db, question=_question, answer=_answer_create)
```

질문 등록을 위한 API 를 작성하였다. 이때 먼저 질문을 조회해서 질문이 있는 경우에만 답변을 등록하도록 구현 되어있다. 이제 답변을 저장하기 위한 코드를 작성하자.

- domain/answer/answer_crud.py

```python
from database import auto_commit
from domain.answer.answer_schema import AnswerCreateSchema
from models import Answer, Question
from sqlalchemy.orm import Session
from datetime import datetime


@auto_commit
def create_answer(db: Session, question: Question, answer: AnswerCreateSchema):
    db_answer = Answer(question=question, content=answer.content, create_date=datetime.now())
    db.add(db_answer)
```

이제 답변을 등록하기 위한 API 가 작성되었다. 질문 상세 화면에서 답변을 등록하면 해당 API 가 호출되어 답변이 등록된다.

#### 질문 상세 API 구현

질문 상세 API 를 작성하겠다. 질문 상세 API 는 질문과 답변을 함께 조회하는 API 이다. 먼저 이전에 구현했던 목록 API 에서 응답 본문을 처리하기 위한 `QuestionSchema` 를 약간 수정하겠다.

- domain/question/question_schema.py

```python
from domain.answer.answer_schema import AnswerSchema


class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str | None = None
    create_date: datetime.datetime
    answers: list[AnswerSchema] = []  ## 추가 
```

> 참고 : 실제 API 설계를 어떻게 하느냐에 따라 다르긴 하지만 일반적으로 목록과 상세에 대한 응답 본문은 분리하는것이 좋다. 구현하는 프로젝트마다 다르겠지만 목록에서 보여지는 필드보다 상세에 보여지는 필드가 더
> 방대하기 떄문이다.

이제 질문 상세 API 를 작성하겠다.

- domain/question/question_router.py

```python
@router.get("/detail/{question_id}", response_model=QuestionSchema)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    return question_crud.question_detail(question_id=question_id, db=db)
```

path valiable 을 사용하여 질문 ID 를 전달받고, 해당 질문을 조회하여 응답한다. 이때 응답 본문은 `QuestionSchema` 를 사용한다.

> 참고 : path valiable 은 URL 에서 변수 부분을 지정하는 방법으로, FastAPI 에서는 `/{variable_name}` 형태로 사용한다. 예를 들어,
`/question/{question_id}` 는 question_id 라는 변수를 URL 에서 전달받는다는 의미이다.

이제 조회를 위한 함수를 작성하겠다.

- domain/question/question_crud.py

```python
def question_detail(db: Session, question_id: int):
    return db.query(Question).get(question_id)
```

이렇게 상세 조회까지 구현하여 질문 등록, 질문 상세, 답변 등록 API 를 모두 구현하였다. 이제 프론트엔드에서 해당 API 를 호출하여 질문과 답변을 등록하고 조회할 수 있다.

