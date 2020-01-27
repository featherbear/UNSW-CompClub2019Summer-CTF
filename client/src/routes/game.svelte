<script context="module">
  export async function preload(page, session) {
    const questionsFn = () =>
      this.fetch("/service/questions.json", {
        credentials: "include"
      })
        .then(r => r.json())
        .then(json => json.data);

    const categoriesFn = () =>
      this.fetch("/service/categories.json", {
        credentials: "include"
      })
        .then(r => r.json())
        .then(json => json.data);

    const solvesFn = () =>
      this.fetch("/service/solves.json", {
        credentials: "include"
      })
        .then(r => r.json())
        .then(json => json.data);

    let [questions, categories, solves] = await Promise.all([
      questionsFn(),
      categoriesFn(),
      solvesFn()
    ]);

    return { questions, categories, solves };
  }
</script>

<script>
  import Slot from "../components/_layout.svelte";
  import QuestionCard from "../components/QuestionCard.svelte";

  export let questions;
  export let categories;
  export let solves;

  let mergeData = [];
  $: {
    mergeData = questions.map(question => {
      let [id, title, description, points, categoryID] = question;
      return {
        id,
        title,
        description,
        points,
        categoryID,
        categoryName: categories[categoryID] || "",
        solves: solves[id]
      };
    });
  }
</script>

<Slot>
  {#each mergeData as data}
    <QuestionCard {...data} />
  {/each}
</Slot>
