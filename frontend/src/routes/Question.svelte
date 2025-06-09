<script>
    import {link} from "svelte-spa-router"
    import moment from "moment/min/moment-with-locales"

    moment.locale('ko')

    import {fastapi} from "../lib/api.js";
    import {page} from "../lib/store"

    import Navigation from "../components/Navigation.svelte";

    let size = 10
    let total = 0
    let question_list = []
    let pages = [];

    $: total_page = Math.ceil(total / size)

    function get_pagination_range(page_number = 0, size = 10, total = 0) {
        if (total === 0) return [];
        let _total_page = Math.ceil(total / size)
        const visiblePages = 10;

        // 0-based page index를 1-based 페이지 번호로 변환
        const currentPage = page_number + 1;

        let start = currentPage - Math.floor(visiblePages / 2);
        let end = currentPage + Math.floor(visiblePages / 2) - 1;

        if (start < 1) {
            start = 1;
            end = Math.min(visiblePages, _total_page);
        }

        if (end > _total_page) {
            end = _total_page;
            start = Math.max(1, _total_page - visiblePages + 1);
        }

        const range = [];
        for (let i = start; i <= end; i++) {
            range.push(i);
        }

        return range;
    }

    function get_question_list(_page) {
        let params = {
            page: _page,
            size: size
        }
        fastapi('GET', '/api/question/list', params, (json) => {
            total = json.total
            question_list = json.questions
            $page = _page
            pages = get_pagination_range($page, size, total)
        })
    }

    $: get_question_list($page)
</script>
<Navigation/>
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
                <td>{ total - ($page * size) - i }</td>
                <td>
                    <a use:link href="/question/{question.id}">{question.subject}</a>
                    {#if question.answers.length > 0 }
                        <span class="text-danger small mx-2">{question.answers.length}</span>
                    {/if}
                </td>
                <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
            </tr>
        {/each}
        </tbody>
    </table>
    <!-- Pagination Start -->
    <ul class="pagination justify-content-center">
        <li class="page-item">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( 0)}">처음</button>
        </li>
        <li class="page-item {$page <= 0 && 'disabled'}">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( $page-1)}">이전</button>
        </li>

        <!-- Page Number Display -->
        {#each pages as p}
            <li class="page-item {p - 1 === $page && 'active'}">
                <button on:click={() => get_question_list(p - 1)} class="page-link">{p}</button>
            </li>
        {/each}
        <!-- Next Button -->
        <li class="page-item {$page >= total_page -1  && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
        </li>
        <li class="page-item">
            <!-- Previous Button -->
            <button class="page-link" on:click="{() => get_question_list( total_page -1)}">마지막</button>
        </li>
    </ul>
    <!-- Pagination End -->
    <a use:link href="/question/create/" class="btn btn-primary">질문 등록하기</a>
</div>