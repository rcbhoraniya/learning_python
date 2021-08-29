<template>
  <div>
    <b-navbar fixed="top" toggleable="lg" type="dark" variant="info">
      <b-navbar-brand to="/production">Toris</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/production">Production</b-nav-item>
          <b-nav-item to="/product">Product</b-nav-item>
          <b-nav-item to="/order">Order</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
        </b-navbar-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-form>
            <b-form-input
              size="sm"
              class="mr-sm-2"
              placeholder="Search "
              v-model="search"
            ></b-form-input>
            <b-button
              size="sm"
              class="my-2 my-sm-0"
              type="submit"
              @click.prevent="getSearch"
              >Search</b-button
            >
          </b-nav-form>
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template slot="button-content"><em>User</em></template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item href="#">Sign Out</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>
<script>
export default {
  name: "Nav",
  data() {
    return {
      search: "",
    };
  },
  methods: {
    getSearch() {},
  },
};
</script>
<style scoped>
.navbar-dark .navbar-nav .nav-link {
  color: #fdfdfe;
}
</style>
