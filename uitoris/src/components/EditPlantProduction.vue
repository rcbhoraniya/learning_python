<template>
  <div>
    <router-link to="/production"
      ><b-button variant="outline-primary" size="sm">Back</b-button></router-link
    >
    <b-container>
      <b-card class="bg-form col-12">
        <h3 class="text-center">{{ formname }}{{ form.id }}</h3>
        <b-form @submit="onSubmitForm" v-if="!showform">
          <b-row>
            <b-col>
              <b-form-group label="Date:" label-for="date">
                <b-form-datepicker
                  id="date"
                  v-model="form.date"
                  class="mb-2"
                  required
                ></b-form-datepicker>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Plant:" label-for="plant" description="">
                <b-form-select
                  id="plant"
                  v-model="form.plant"
                  :options="plants"
                  value-field="id"
                  text-field="name"
                ></b-form-select>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Product Code:" label-for="product_code" description="">
                <b-form-select id="product_code" v-model="form.product_code" class="mb-3">
                  <b-form-select-option
                    v-for="product in products"
                    :key="product.id"
                    v-bind:value="product.id"
                  >
                    {{ product.product_code }}-{{ product.color_marking_on_bobin }}-{{
                      product.tape_color
                    }}-{{ product.denier }}
                  </b-form-select-option>
                </b-form-select>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group label="Shift:" label-for="shift" description="">
                <b-form-select
                  id="shift"
                  v-model="form.shift"
                  :options="options"
                  value-field="value"
                  text-field="text"
                  disabled-field="notEnabled"
                ></b-form-select>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Operator name:"
                label-for="operator_name"
                description=""
              >
                <b-form-select
                  v-model="form.operator_name"
                  :options="employeeOperator"
                  value-field="id"
                  text-field="name"
                ></b-form-select>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="No of winderman:"
                label-for="no_of_winderman"
                description=""
              >
                <b-form-input
                  id="no_of_winderman"
                  v-model="form.no_of_winderman"
                  type="text"
                  placeholder="Enter no_of_winderman "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group label="end_reading:" label-for="end_reading" description="">
                <b-form-input
                  id="end_reading"
                  v-model="form.end_reading"
                  type="text"
                  placeholder="Enter end_reading "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="start_reading:"
                label-for="start_reading"
                description=""
              >
                <b-form-input
                  id="start_reading"
                  v-model="form.start_reading"
                  type="text"
                  placeholder="Enter start_reading "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="wastage:" label-for="wastage" description="">
                <b-form-input
                  id="wastage"
                  v-model="form.wastage"
                  type="text"
                  placeholder="Enter wastage "
                  required
                ></b-form-input>
              </b-form-group> </b-col
          ></b-row>
          <div class="text-center">
            <b-button type="submit" variant="primary">Submit</b-button>
          </div>
          <!-- <b-button variant="danger" @click="Reset">Reset</b-button> -->
        </b-form>
        <div v-else>
          <h4>You submitted successfully!</h4>
        </div>
        <!-- <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card> -->
      </b-card>
    </b-container>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex";

export default {
  data() {
    return {
      formname: "Edit Plant Production#",
      production: null,
      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],

      showform: false,
    };
  },
  computed: {
    ...mapGetters("employee", { employeeOperator: "employeeOperator" }),
    ...mapState({ plants: (state) => state.plant.plantall }),
    ...mapState({ products: (state) => state.product.productall }),
    ...mapState({ form: (state) => state.production.production }),
  },
  mounted() {
    this.getPlants();
    this.getProducts();
    this.getEmployees();
    this.getProductionById(this.$route.params.id);
  },
  methods: {
    ...mapActions("plant", ["getPlants"]),
    ...mapActions("product", ["getProducts"]),
    ...mapActions("employee", ["getEmployees"]),
    ...mapActions("production", ["getProductionById", "editProduction"]),

    onSubmitForm() {
      event.preventDefault();
      var data = this.form;
      this.editProduction(data);
      this.showform = true;
      this.$router.push("/production");
    },
  },
};
</script>
<style lang="scss" scoped></style>
