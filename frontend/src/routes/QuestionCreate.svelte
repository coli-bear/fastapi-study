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