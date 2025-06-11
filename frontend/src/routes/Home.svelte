<script>
    import {is_signed} from "../lib/store.js";
</script>
<h1>Home</h1>
<h2>Welcome Svelte Application</h2>
<ul>
<li><a href="{$is_signed ?'#/question' : '#/signin'}">Go To Question</a></li>

</ul>
