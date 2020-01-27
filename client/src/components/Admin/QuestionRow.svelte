<script>
  export let id;
  export let title;
  export let description;
  export let points;
  export let solves;
  export let categoryID;
  export let categoryName;

  let showFlag = false;
  let flag = "";

  async function revealFlag() {
    fetch("/service/getFlag", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question: id })
    })
      .then(r => r.text())
      .then(value => {
        flag = value;
        showFlag = true;
      });
  }
</script>

<style>
  /* tr td:nth-child(2) {
  max-width: 20vw;
} */
</style>

<tr>
  <td>{title}</td>
  <td>{description}</td>
  <td>{categoryName}</td>
  <td>
    {#if !showFlag}
      <button class="button is-outlined is-info" on:click|once={revealFlag}>
        reveal flag
      </button>
    {:else}{flag}{/if}
  </td>
  <td>{points}</td>
  <td>{solves}</td>
  <td>
    <button class="button is-outlined is-info" on:click={() => {}}>edit</button>
  </td>
</tr>
