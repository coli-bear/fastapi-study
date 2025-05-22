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

<ul>
    {#each question_list as question}
        <li><a use:link href="/question/{question.id}">{question.subject}</a></li>
    {/each}
</ul>