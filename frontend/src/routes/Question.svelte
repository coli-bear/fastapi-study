<script>
    import {fastapi} from "../lib/api.js";

    let question_list = []

    function get_question_list() {
        fastapi('GET', '/question/', {}, (json) => {
            question_list = json
        })
    }

    get_question_list()
</script>

<ul>
    {#each question_list as question}
        <li>{question.subject}</li>
    {/each}
</ul>