<template>
  <div>
    <div class="d-flex justify-content-center align-items-center container">
      <b-card class="login col-6">
        <h3 class="text-center">User Ragistration</h3>

        <b-form @submit.prevent="handleSubmit">
          <b-row>
            <b-col>
              <b-form-group id="firstname" label="Firstname:" label-for="firstname">
                <b-form-input
                  id="firstname"
                  v-model="user.first_name"
                  type="text"
                  placeholder="Enter firstname"
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group id="lastname" label="Lastname:" label-for="lastname">
                <b-form-input
                  id="lastname"
                  v-model="user.last_name"
                  type="text"
                  placeholder="Enter lastname"
                  required
                ></b-form-input>
              </b-form-group> </b-col
          ></b-row>
          <b-form-group id="input-group-1" label="Username:" label-for="username">
            <b-form-input
              id="username"
              v-model="user.username"
              type="text"
              placeholder="Enter username"
              required
            ></b-form-input>
          </b-form-group>
          <b-row
            ><b-col>
              <b-form-group id="password" label="Password:" label-for="password">
                <b-form-input
                  id="password"
                  type="password"
                  v-model="user.password"
                  placeholder="Enter password"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <!-- <b-form-group
                id="conformpassword"
                label="Conform password:"
                label-for="conformpassword"
              >
                <b-form-input
                  id="conformpassword"
                  type="password"
                  v-model="user.password"
                  placeholder="Enter conformpassword"
                  required
                ></b-form-input>
              </b-form-group> -->
            </b-col></b-row
          >
          <b-form-group id="input-group-2" label="Email:" label-for="email">
            <b-form-input
              id="email"
              type="email"
              v-model="user.email"
              placeholder="Enter email"
              required
            ></b-form-input>
          </b-form-group>

          <b-button block type="submit" variant="primary" class="mb-5 mr-3"
            >Submit</b-button
          >
        </b-form>
      </b-card>
    </div>
  </div>
</template>

<script>
import { User } from "@/models";
import { mapActions } from "vuex";
export default {
  name: "Loginform",
  title: "User registration",

  data() {
    return {
      user: new User("", "", "", "", ""),
      message: "",
    };
  },
  computed: {},

  methods: {
    ...mapActions("auth", ["userRegistration"]),
    handleSubmit() {
      this.userRegistration(this.user)
        .then(() => {
          this.$router.push({ name: "About" });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style lang="css" scoped>
body {
  background-color: #fff;
}
.login {
  background-color: #f8f9fa;
}
</style>
