<script>
    import Router from 'svelte-spa-router'
    import Question from "./routes/Question.svelte"
    import QuestionDetail from "./routes/QuestionDetail.svelte"
    import Home from "./routes/Home.svelte";

    const routes = {
        "/": Home,
        '/question': Question,
        '/question/': Question, // 명시적으로도 허용 (선택사항)
        '/question/:question_id': QuestionDetail, // 동적 라우팅
    };
    const useHash = false; // true로 설정하면 해시 모드 사용
</script>

<Router {routes} {useHash}/>