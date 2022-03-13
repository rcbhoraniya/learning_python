<template>
  <div>
    <b-navbar fixed="top" toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand to="/production">TorisERP</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="loggedIn">
          <b-nav-item to="/production">Production</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <b-nav-item to="/order">Order</b-nav-item>
          <b-nav-item to="/production_order">productionOrder</b-nav-item>
          <b-nav-item to="/employee">Employee</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item v-if="!loggedIn" right to="/registration">Registration</b-nav-item>
          <b-nav-item v-if="!loggedIn" right to="/login">Sign in</b-nav-item>
          <b-nav-item v-if="loggedIn" right>User>>{{ user.user }}</b-nav-item>
          <b-nav-item v-if="loggedIn" :to="{ name: 'Login' }" right>Sign out</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>
<script>
import { mapActions, mapState } from "vuex";
export default {
  name: "navbar-toris",
  data() {
    return {
      search: "",
      // loggedIn: false,
    };
  },
  computed: {
    ...mapState({ loggedIn: (state) => state.auth.status.loggedIn }),
    ...mapState({ user: (state) => state.auth.user }),
  },

  methods: {
    getSearch() {},
    ...mapActions("auth", ["Logout"]),
    LogOut() {
      this.Logout();
    },
  },
};
</script>
<style scoped>
.navbar-dark .navbar-nav .nav-link {
  /* font-weight: bold; */
  color: #fdfdfe;
}
</style>
