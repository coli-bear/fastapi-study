<script>
    import {push} from 'svelte-spa-router'
    import moment from "moment/min/moment-with-locales";
    moment.locale('ko')

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
                    {moment(question_detail.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
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
    <button class="btn btn-secondary" on:click="{() => {
        push('/question')
    }}">목록으로</button>
    <!--    답변 목록-->
    <h5 class="border-bottom my-3 py-2">{question_detail.answers.length}개의 답변이 있습니다.</h5>
    {#each question_detail.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
                <div class="d-flex justify-content-end">
                    <div class="badge bg-light text-dark p-2">
                        {moment(question_detail.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
                    </div>
                </div>
            </div>
        </div>
    {/each}

</div>