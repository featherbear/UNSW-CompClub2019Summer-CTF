<script>
  import { fade } from "svelte/transition";

  let displayName, username, password, password2;

  let currentPage = "name";

  let salutation = "";
  $: {
    var hour = new Date().getHours();

    if (hour < 12) {
      salutation = "morning";
    } else if (hour < 18) {
      salutation = "afternoon";
    } else {
      salutation = "evening";
    }
  }

  function focusInputElement(element) {
    element && element.focus();
  }

  let formElem;
  function nameHandler(evt) {
    if (evt.keyCode == 9 || evt.keyCode == 13) {
      evt.preventDefault();
      if (evt.target.value.trim() == "") return;
      currentPage = "username";
    }
  }

  function usernameHandler(evt) {
    if (evt.keyCode == 9 || evt.keyCode == 13) {
      evt.preventDefault();
      if (evt.target.value.trim() == "") return;
      // TODO: Check if username is available
      currentPage = "password";
    }
  }

  let passwordEntered = false;
  function passwordHandler(evt) {
    if (evt.keyCode == 9 || evt.keyCode == 13) {
      evt.preventDefault();
      // No trim for passwords
      if (evt.target.value == "") return;
      passwordEntered = true;
    }
  }

  function password2Handler(evt) {
    if (evt.keyCode == 13) {
      evt.preventDefault();
      if (password == password2) {
        submit();
      }
    }
  }

  async function submit() {
    let data = {
      name: displayName.trim(),
      username: username.trim(),
      password
    };
    if (!data.name) return;
    if (!data.username) return;

    let result = await fetch("/service/register", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      }
    });

    if (result.status == 200) {
      window.location = "/";
    }
  }
</script>

<section class="section" in:fade={{ delay: 400 }} out:fade>
  <form bind:this={formElem}>
    {#if currentPage == 'name'}
      <div in:fade={{ delay: 400 }} out:fade>
        <h1 class="is-size-1 has-text-light">
          Good {salutation}, Agent
          <input
            type="text"
            name="name"
            class="has-text-light minimal"
            spellcheck="false"
            placeholder="(your display name)"
            maxlength="20"
            on:keydown={nameHandler}
            bind:value={displayName}
            use:focusInputElement />
          .
        </h1>
      </div>
    {:else if currentPage == 'username'}
      <div in:fade={{ delay: 400 }} out:fade>
        <h1 class="is-size-1 has-text-light">
          Username:
          <input
            type="text"
            name="username"
            class="has-text-light minimal"
            spellcheck="false"
            pattern="\w*"
            maxlength="20"
            placeholder="(your username)"
            on:keydown={usernameHandler}
            bind:value={username}
            use:focusInputElement />
        </h1>
      </div>
    {:else if currentPage == 'password'}
      <div in:fade={{ delay: 400 }} out:fade>
        <h1 class="is-size-1 has-text-light">password</h1>
        <input
          class="input blueBox has-text-centered is-size-1 has-text-light"
          name="password"
          type="password"
          on:keydown={passwordHandler}
          bind:value={password}
          use:focusInputElement />

        {#if passwordEntered}
          <div transition:fade>
            <h1 class="is-size-1 has-text-light">confirm</h1>
            <input
              class="input blueBox has-text-centered is-size-1 has-text-light"
              name="password2"
              type="password"
              on:keydown={password2Handler}
              bind:value={password2}
              use:focusInputElement />
          </div>
        {/if}
      </div>
    {/if}
  </form>
</section>
