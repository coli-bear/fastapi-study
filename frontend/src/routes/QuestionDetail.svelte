<script>
    import {fastapi} from "../lib/api.js";
    export let params = {};
    let question_id =   params.question_id;
    let question_detail = {}

    fastapi('GET', `/api/question/detail/${question_id}`, undefined, json => {
        question_detail = json
    })

    console.log(question_detail)

</script>

<h1>{question_detail.subject}</h1>
<div>
    {question_detail.content}
</div>