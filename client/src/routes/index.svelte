<script context="module">
  export async function preload(page, session) {
    if (!session) {
      return this.redirect(302, "/invite");
    }
    if (session.id == 0) {
      this.redirect(302, "/admin");
    } else {
      this.redirect(302, "/game");
    }
  }
</script>
