<script>
  import { fade } from "svelte/transition";

  let usernameElement;
  let passwordElement;

  let loginUsernameEntered = false;
  function loginUsernameHandler(evt) {
    if (evt.keyCode == 9 || evt.keyCode == 13) {
      evt.preventDefault();
      loginUsernameEntered = true;
      focusOnInputElement(passwordElement);
    }
  }

  function loginPasswordHandler(evt) {
    if (evt.keyCode == 13) {
      evt.preventDefault();
      submit();
    }
  }

  function focusOnInputElement(reference) {
    if (!reference) return;
    reference.focus();
  }

  async function submit() {
    let credentials = {
      username: usernameElement.value.trim(),
      password: passwordElement.value
    };

    // Lock form

    let result = await fetch("/service/login", {
      method: "POST",
      body: JSON.stringify(credentials),
      headers: {
        "Content-Type": "application/json"
      }
    });

    // Unlock form

    if (result.status == 200) {
      window.location = "/";
    }

    // Error message
  }
</script>

<section class="section" transition:fade={{ delay: 400 }}>
  <form autocomplete="off">
    <input
      bind:this={usernameElement}
      type="text"
      name="username"
      class="is-size-1 has-text-light minimal has-text-centered"
      spellcheck="false"
      pattern="\w."
      maxlength="20"
      placeholder="username"
      on:keydown={loginUsernameHandler} />

    {#if loginUsernameEntered}
      <input
        bind:this={passwordElement}
        on:keydown={loginPasswordHandler}
        use:focusOnInputElement
        class="input blueBox has-text-centered is-size-1 has-text-light"
        name="password"
        type="password"
        placeholder="password"
        transition:fade />
    {/if}
  </form>
</section>
