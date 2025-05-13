# Fast API 학습 일지 

Fast API에 대한 기초부터 심화까지 학습예정이다. 여기서는 wikidocs 에서 제공하는 `점프 투 FastAPI` 내용을 정리 했다.  

## 환경 구성 

- python 3.13 venv
- FastAPI
- uvicorn

아래 명령어로 가상환경을 구성한다.

```shell
python3 -m venv venv          # Python 가상환경 생성
source venv/bin/activate      
pip install fastapi uvicorn   
```
> 참고 : Python 가상환경 생성
> - 가상환경을 생성할 때 파이썬의 버전을 지정하고 싶을 수 있다. 이때 `python3.8`과 같이 버전을 명시해주면 된다.
> - 여기서는 python3 이 python3.13 을 심볼릭 링크로 설정해두었기 때문에 python3 만으로도 3.13 버전의 가상환경을 생성할 수 있다.

## FastAPI 시작하기

FastAPI는 Python으로 작성된 웹 프레임워크로 uvicorn 을 이용해서 서버를 실행할 수 있다. 

> uvicorn은 ASGI 서버로, FastAPI와 같은 비동기 웹 프레임워크를 실행하기 위해 사용된다.<br/>
> gunicorn 또한 존재하는데 이 부분은 아래 블로그를 읽고 uvicorn 과 gunicorn의 차이를 이해하고 사용하면 좋을 것 같다.
> 
> [uvicorn vs gunicorn](https://velog.io/@jomminii/fastapi-gunicorn-uvicorn-workers)

FastAPI 간단한 애플리케이션을 구성하고 실행해보자 

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
```

위 코드를 `main.py`라는 이름으로 저장하고 아래 명령어로 서버를 실행한다.

```shell
uvicorn main:app --reload
```

이제 제대로 애플리케이션이 동작하는지 간단하게 확인해보자 

```shell
curl -X GET http://localhost:8000/
{"message":"Hello World"}

curl -X GET http://localhost:8000/hello/fastapi
{"message":"Hello fastapi"}
```

정상 동작하는 것을 확인했다. 간단한 정리는 여기까지만 하고 FastAPI 에 대해서 좀 더 깊게 정리해 보겠다.  

## FastAPI 학습 목차 

- [ch01. FastAPI 시작하기](docs/ch01_fastapi_basic.md)



## 참고
> - [Wiki Docs - FastAPI](https://wikidocs.net/book/8531)
