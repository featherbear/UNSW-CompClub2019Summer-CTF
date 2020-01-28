<script>
  import { fade } from "svelte/transition";
  export let currentPage;
</script>

<section class="section" in:fade={{delay: 400}} out:fade>
  <h1 class="is-size-3 has-text-light">Are you new here?</h1>
  <div class="field is-grouped is-grouped-centered">
    <p class="control">
      <span
        on:click={() => (currentPage = 'register')}
        class="button is-warning is-outlined is-large">
        REGISTER
      </span>
    </p>
    <p class="control">
      <span
        on:click={() => (currentPage = 'login')}
        class="button is-warning is-outlined is-large">
        LOGIN
      </span>
    </p>
  </div>
</section>
