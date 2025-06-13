<script>
    import Router from 'svelte-spa-router'
    import Question from "./routes/Question.svelte"
    import QuestionDetail from "./routes/QuestionDetail.svelte"
    import Home from "./routes/Home.svelte";
    import QuestionCreate from "./routes/QuestionCreate.svelte";
    import UserCreate from "./routes/UserCreate.svelte";
    import UserSignIn from "./routes/UserSignIn.svelte";
    import QuestionModify from "./routes/QuestionModify.svelte";
    import AnswerModify from "./routes/AnswerModify.svelte";

    const routes = {
        "/": Home,
        '/question': Question,
        '/question/create': QuestionCreate,
        '/question/:question_id': QuestionDetail, // 동적 라우팅
        '/question/:question_id/modify': QuestionModify,
        '/answer/:answer_id/modify': AnswerModify,
        '/signup': UserCreate,
        '/signin': UserSignIn
    };
    const useHash = false; // true로 설정하면 해시 모드 사용
</script>

<Router {routes} {useHash}/>