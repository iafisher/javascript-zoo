<script>
  window.fetch("http://localhost:8888/api/project/get?pk=1").then(response => {
    response.json().then(data => {
      console.log(data);
    });
  });
</script>

<main>
</main>
