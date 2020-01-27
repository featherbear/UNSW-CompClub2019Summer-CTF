<script>
  import { fade } from "svelte/transition";
</script>

<section class="section" transition:fade={{ delay: 400 }}>
  <form>
    <div class="page" name="name">
      <h1 class="is-size-1 has-text-light">
        Good
        <span class="salutation" />
        , Agent
        <input
          type="text"
          name="name"
          class="has-text-light minimal"
          spellcheck="false"
          required
          placeholder="(your display name)"
          maxlength="20" />
        .
      </h1>
    </div>
    <div class="page" name="username">
      <h1 class="is-size-1 has-text-light">
        Username:
        <input
          type="text"
          name="username"
          class="has-text-light minimal"
          spellcheck="false"
          pattern="\w."
          maxlength="20"
          placeholder="(your username)" />
      </h1>
    </div>

    <div class="page" name="password">
      <h1 class="is-size-1 has-text-light">password</h1>
      <input
        class="input blueBox has-text-centered is-size-1 has-text-light"
        name="password"
        type="password" />
    </div>

    <div class="page" name="password2">
      <h1 class="is-size-1 has-text-light">confirm</h1>
      <input
        class="input blueBox has-text-centered is-size-1 has-text-light"
        name="password2"
        type="password" />
    </div>
  </form>
</section>
