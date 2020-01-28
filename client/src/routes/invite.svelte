<script>
  import BackgroundFuzz from "../components/BackgroundFuzz/BackgroundFuzz.svelte";

  import { Invite, Auth, Login, Register } from "../components/Invite";
  import SVGLoader from "../components/SVGLoader.svelte";

  let currentPage = "";
  import { onMount } from "svelte";
  onMount(() => {
    let anchor = location.hash.substr(1);
    currentPage =
      ["invite", "auth", "login", "register"].indexOf(anchor) > -1
        ? anchor
        : "invite";
  });
</script>

<style>
  main {
    text-align: center;
    padding: 32px 0;
  }

  .logoContainer {
    width: 50%;
    margin: 0 auto;
    transition: margin-top 400ms ease-out;
  }

  .logoContainer.lowered {
    margin-top: 10%;
  }

  .background {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
  }

  .background:after {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    transition: all 1s;
    background-color: rgba(0, 35, 88, 0.7);
  }
</style>

<main class="container is-widescreen">
  <div class="logoContainer" class:lowered={currentPage == 'invite'}>
    <SVGLoader imageURL="/assets/img/compclub.logo.white.svg" />
  </div>
  {#if currentPage == 'invite'}
    <Invite bind:currentPage />
  {:else if currentPage == 'auth'}
    <Auth bind:currentPage />
  {:else if currentPage == 'register'}
    <Register />
  {:else if currentPage == 'login'}
    <Login />
  {/if}
</main>

<div class="background">
  <BackgroundFuzz resource="invite/background.jpg" />
</div>
