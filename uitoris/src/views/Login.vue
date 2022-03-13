<template>
  <div>
    <h3 class="text-center">Sign in</h3>
    <div class="d-flex justify-content-center align-items-center container">
      <b-card class="bg-form col-4">
        <!-- <b-alert
          variant="danger"
          dismissible
          fade
          :show="showDismissibleAlert"
          @dismissed="showDismissibleAlert = false"
        >
          {{ message.detail }}
        </b-alert> -->
        <b-form @submit.prevent="handleLogin" class="mb-3">
          <b-form-group id="input-group-1" label="Username:" label-for="username">
            <b-form-input
              id="username"
              v-model="user.username"
              type="text"
              placeholder="Enter username"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-2" label="Password:" label-for="password">
            <b-form-input
              id="password"
              type="password"
              v-model="user.password"
              placeholder="Enter password"
              required
            ></b-form-input>
          </b-form-group>

          <b-button block type="submit" variant="primary" class="mb-3 mt-5"
            >Submit</b-button
          >
        </b-form>
        <div class="text-center">
          <router-link to="/registration">Create an account</router-link>
        </div>
      </b-card>
    </div>
  </div>
</template>

<script>
import { User } from "@/models";
import { mapActions, mapState } from "vuex";
export default {
  name: "Loginform",
  title: "Login",

  data() {
    return {
      user: new User("", ""),
      message: "",
      showDismissibleAlert: false,
    };
  },
  computed: {
    ...mapState({ loggedIn: (state) => state.auth.status.loggedIn }),
  },
  created() {
    // reset login status
    this.Logout();
  },

  methods: {
    ...mapActions("auth", ["Login", "Logout"]),
    handleLogin() {
      this.Login(this.user);
    },
  },
};
</script>

<style lang="css" scoped></style>
