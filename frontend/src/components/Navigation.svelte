<script>
    import {link} from "svelte-spa-router";
    import {access_token, is_signed, page, username} from "../lib/store.js";
</script>

<!-- Navigation bar -->
<nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/question" on:click="{() => {$page = 0}}">Pybo</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"/>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <!-- Navigation Bar Sign In 처리 시작 -->
                {#if $is_signed}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signin" on:click={()=>{
                            $access_token = "";
                            $username = "";
                            $is_signed = false;
                        }}>로그아웃 ({$username})</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signup">회원가입</a>
                    </li>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="#/signin">로그인</a>
                    </li>
                {/if}
                <!-- Navigation Bar Sign In 처리 끝 -->
            </ul>
        </div>
    </div>
</nav>