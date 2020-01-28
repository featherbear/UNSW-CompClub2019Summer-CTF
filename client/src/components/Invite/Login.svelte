<script>
  import { fade } from "svelte/transition";

  let usernameElement;
  let passwordElement;

  function focusInputElement(element) {
    element && element.focus();
  }

  let loginUsernameEntered = false;
  function loginUsernameHandler(evt) {
    if (evt.keyCode == 9 || evt.keyCode == 13) {
      if (evt.target.value.trim() == "") {
        evt.preventDefault();
        return;
      }
      
      if (evt.keyCode != 9) focusInputElement(passwordElement);
      loginUsernameEntered = true;
    }
  }

  function loginPasswordHandler(evt) {
    if (evt.keyCode == 13) {
      evt.preventDefault();
      submit();
    }
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

<section class="section" in:fade={{ delay: 400 }} out:fade>
  <form autocomplete="off">
    <input
      bind:this={usernameElement}
      type="text"
      name="username"
      class="is-size-1 has-text-light minimal has-text-centered"
      spellcheck="false"
      pattern="\w*"
      maxlength="20"
      placeholder="username"
      on:keydown={loginUsernameHandler}
      use:focusInputElement />

    {#if loginUsernameEntered}
      <input
        bind:this={passwordElement}
        on:keydown={loginPasswordHandler}
        on:introstart={evt => evt.target.focus()}
        class="blueBox has-text-centered is-size-1 has-text-light"
        name="password"
        type="password"
        placeholder="password"
        transition:fade
        use:focusInputElement />
    {/if}
  </form>
</section>
