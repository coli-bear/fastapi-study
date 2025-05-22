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
</div>