<script>
    import {link, push} from 'svelte-spa-router'
    import moment from "moment/min/moment-with-locales";

    moment.locale('ko')

    import {fastapi} from "../lib/api.js";
    import {is_signed, username} from "../lib/store.js";
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

    function delete_question(_question_id) {
        if (window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/question/delete"
            let params = {
                question_id: _question_id
            }
            fastapi('delete', url, params,
                (json) => {
                    push('/question')
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function delete_answer(answer_id) {
        if (window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params,
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }
</script>

<div class="container my-3">
    <!--    질문 -->
    <h2 class="border-bottom py-2">{question_detail.subject}</h2>
    <div class="card my-3">
        <div class="card-body">
            <div class="card-text" style="white-space: pre-line;">{question_detail.content}</div>
            <div class="d-flex justify-content-end">
                <div class="badge bg-light text-dark p-2 text-start">
                    <div class="mb-2">{ question_detail.user ? question_detail.user.username : ""}</div>
                    <div>{moment(question_detail.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                </div>
            </div>
            <div class="my-3">
                {#if question_detail.user && $username === question_detail.user.username}
                    <a use:link href="/question/{question_id}/modify" class="btn btn-sm btn-outline-secondary">수정</a>
                    <button class="btn btn-sm btn-outline-secondary"
                            on:click={() => delete_question(question_detail.id)}>삭제
                    </button>

                {/if}
            </div>
        </div>
    </div>
    <!--    답변 등록-->
    <Error error={error}/>
    <form method="post" class="my-3">
        <div class="mb-3">
            <textarea rows="10"
                      bind:value={content}
                      class="form-control"
                      disabled={$is_signed ? '' : 'disabled'}
            ></textarea>
        </div>
        <input type="submit" value="답변 등록" class="btn btn-primary {$is_signed ? '' : 'disabled'}"
               on:click={post_answer}/>
    </form>
    <button class="btn btn-secondary" on:click="{() => {
        push('/question')
    }}">목록으로
    </button>
    <!--    답변 목록-->
    <h5 class="border-bottom my-3 py-2">{question_detail.answers.length}개의 답변이 있습니다.</h5>
    {#each question_detail.answers as answer}
        <div class="card my-3">
            <div class="card-body">
                <div class="card-text" style="white-space: pre-line;">{answer.content}</div>
                <div class="d-flex justify-content-end">
                    <div class="badge bg-light text-dark p-2 text-start">
                        <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                        <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
                    </div>
                </div>
                <div class="my-3">
                    {#if answer.user && $username === answer.user.username }
                        <a use:link href="/answer/{answer.id}/modify" class="btn btn-sm btn-outline-secondary">수정</a>
                        <button class="btn btn-sm btn-outline-secondary" on:click={() => delete_answer(answer.id) }>삭제
                        </button>
                    {/if}

                </div>
            </div>
        </div>
    {/each}

</div>