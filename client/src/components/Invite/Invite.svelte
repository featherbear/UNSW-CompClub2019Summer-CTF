<script>
  import { fade } from "svelte/transition";
  export let currentPage;
</script>

<section class="section" in:fade={{delay: 400}} out:fade>
  <h1 class="is-size-3 has-text-light">
    Your mission, should you choose to accept ...
  </h1>
  <div class="field is-grouped is-grouped-centered">
    <p class="control">
      <span
        on:click={() => (currentPage = 'auth')}
        class="button is-success is-outlined is-large">
        YEET
      </span>
    </p>
    <p class="control">
      <a
        class="button is-danger is-outlined is-large"
        href="//www.youtube.com/watch?v=dQw4w9WgXcQ">
        NOPE
      </a>
    </p>
  </div>
</section>
