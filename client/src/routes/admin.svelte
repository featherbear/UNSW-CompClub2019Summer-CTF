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
  import QuestionRow from "../components/Admin/QuestionRow.svelte";
  export let gameData;
</script>

<style>
  table.table {
    background-color: transparent;
    color: #f5f5f5 !important;
  }

  table th {
    color: #f5f5f5 !important;
  }

  table td {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  table tbody tr:first-child td {
    text-align: center;
    font-size: 1.25rem;
  }

  table tbody tr:first-child:hover {
    background-color: hsla(0, 0%, 100%, 0.3);
  }
</style>

<Slot>
  <div class="container">
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Category</th>
          <th>Flag</th>
          <th>Points</th>
          <th>Solves</th>
          <th />
        </tr>
      </thead>
      <tfoot>
        <tr>
          <th>Title</th>
          <th>Description</th>
          <th>Category</th>
          <th>Flag</th>
          <th>Points</th>
          <th>Solves</th>
          <th />
        </tr>
      </tfoot>
      <tbody>
        <tr onclick="openModalEdit()">
          <td colspan="6">Add new question</td>
          <td />
        </tr>

        {#each gameData as data}
          <QuestionRow {...data} />
        {/each}

      </tbody>
    </table>
  </div>

</Slot>
