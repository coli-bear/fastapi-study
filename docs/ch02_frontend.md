# Frontend with Svelte

> 참고1 : [Wikidocs FastAPI - Svelte 환경 준비](https://wikidocs.net/175833)<br/>
> 참고2 : [Wikidocs FastAPI - Svelte로 프론트엔드 만들기](https://wikidocs.net/176328)<br/>
> 참고3 : [nvm 설치 참고](https://sukvvon.tistory.com/69)

이제 전체 애플리케이션을 구현하기 위해 svlete 를 사용해서 프론트엔드를 구현해보자. 이것을 기반으로 질문과 답변을 할 수 있는 애플리케이션을 만들 것이다.

- 사전에 nodejs와 npm이 설치되어 있어야 한다. nvm을 사용하여 설치하는 것을 추천한다.

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

{#if 조건문 1}
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
- 질문 목록 : /#/question/
- 질문 상세 : /#/question/:id
- 질문 작성 : /#/question/create
- 질문 수정 : /#/question/update/:id
- 답변 작성 : /#/question/:id/answer
- 답변 수정 : /#/question/:id/answer/update/:id
- 사용자 로그인 : /#/login
- 사용자 회원가입 : /#/register

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

