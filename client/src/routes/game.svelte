<script context="module">
  export async function preload(page, session) {
    let validation = await this.fetch("/service/validate", {
      credentials: "include"
    });
    if (validation.status == 401) {
      return this.redirect(302, "/invite");
    }

    ///

    // if (session.id == 0) {
    //   return this.redirect(302, "/game");
    // }

    //

    let gameData = await this.fetch("/service/data.json", {
      credentials: "include"
    }).then(r => r.json());

    return { gameData };
  }
</script>

<script>
  import Slot from "../components/_layout.svelte";
  import QuestionCard from "../components/QuestionCard.svelte";

  export let gameData;
  console.log(gameData);
</script>

<Slot>
  {#each gameData as data}
    <QuestionCard {...data} />
  {/each}
</Slot>
