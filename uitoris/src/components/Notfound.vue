<template>
  <div class="bg-form">
    <div class="container text-center">
      <h1 class="head"><span>404</span></h1>
      <p>Oops! The Page you requested was not found!</p>
      <router-link to="/"
        ><b-button variant="primary"> Back to Home</b-button></router-link
      >
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
h1.head {
  font-size: 250px;
  font-weight: 900;

  letter-spacing: 25px;
  margin: 10px 0 0 0;
  color: rgb(136, 3, 3);
}
</style>
