<template>
  <div>
    <b-container fluid>
      <div id="app">
        <navbar-toris></navbar-toris>
        <b-alert
          v-if="alert.message"
          :show="showDismissibleAlert"
          dismissible
          @dismissed="ClearAlert"
          :variant="`${alert.type}`"
        >
          {{ alert.message }}
        </b-alert>
        <router-view />
      </div>
    </b-container>
    <footer-toris></footer-toris>
  </div>
</template>
<script>
// import Navbar from "@/components/Navbar";
// import Footer from "@/components/Footer";
export default {
  name: "app",
  components: {},
  data() {
    return {
      showDismissibleAlert: true,
    };
  },
  computed: {
    alert() {
      return this.$store.state.alert;
    },
  },
  watch: {
    $route() {
      // clear alert on location change
      this.$store.dispatch("alert/clear");
    },
  },
  methods: {
    ClearAlert() {
      this.$store.dispatch("alert/clear");
    },
  },
};
</script>
<style lang="scss">
// #app {
//   font-family: Avenir, Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
//   // text-align: center;
//   color: #16212c;
// }

#nav {
  padding: 2px;

  a {
    // font-weight: bold;
    color: #004992;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
