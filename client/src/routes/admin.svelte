<script context="module">
  export async function preload(page, session) {
    if (!session) {
      return this.redirect(302, "/");
    }

    let validation = await this.fetch("/service/validate", {
      credentials: "include"
    });
    if (validation.status == 401) {
      return this.redirect(302, "/invite");
    }

    if (session.id != 0) {
      return this.error(403, "Not admin!");
    }

    //

    let gameData = await this.fetch("/service/data.json", {
      credentials: "include"
    }).then(r => r.json());

    return { gameData };
  }
</script>

<script>
  import Slot from "../components/_layout.svelte";
  export let gameData;
</script>

<Slot>
  <!--
  {#each gameData as data}
  {/each} 
  -->
</Slot>
