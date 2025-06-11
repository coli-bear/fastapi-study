<script>
    import {push} from "svelte-spa-router";
    import {fastapi} from "../lib/api.js";
    import Error from "../components/Error.svelte";
    import {access_token, username, is_signed} from "../lib/store.js";

    let error = {detail: []}
    let signin_username = "";
    let signin_password = "";

    function sign_error(json) {
        error = json;
        console.error("Sign in error:", error);
    }

    function signin_success_callback(json) {
        console.log("Sign in success:", json);
        $access_token = json.access_token;
        $username = json.username;
        $is_signed = true;
        push("/question")
    }

    function signin(event) {
        event.preventDefault()
        let url = "/api/user/signin"
        let params = {
            username: signin_username,
            password: signin_password
        }
        fastapi('signin', url, params, signin_success_callback, sign_error)
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">Sign In</h5>
    <Error error={error}/>
    <form method="post">
        <div class="mb-3">
            <label for="username">username</label>
            <input type="text" class="form-control" id="username" bind:value="{signin_username}">
        </div>
        <div class="mb-3">
            <label for="password">password</label>
            <input type="password" class="form-control" id="password" bind:value="{signin_password}">
        </div>
        <button type="submit" class="btn btn-primary" on:click="{signin}">Sign In</button>
    </form>
</div>