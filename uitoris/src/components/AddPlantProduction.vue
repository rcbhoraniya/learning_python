<template>
  <div>
    <router-link to="/production"
      ><b-button variant="outline-primary" size="sm" @click="clearstate"
        >Back</b-button
      ></router-link
    >
    <b-container>
      <b-card class="bg-form col-12">
        <h3 class="text-center">{{ formname }}{{ form.id }}</h3>
        <b-form @submit.prevent="onSubmitForm" v-if="!showform">
          <b-row>
            <b-col>
              <b-form-group label="Date:" label-for="date">
                <b-form-datepicker
                  id="date"
                  v-model="form.date"
                  class="mb-2"
                  required
                ></b-form-datepicker>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="Plant:" label-for="plant" description="">
                <b-form-select
                  id="plant"
                  v-model="form.plant"
                  :options="plants"
                  value-field="id"
                  text-field="name"
                  @change="lastItem(form.plant)"
                ></b-form-select>
              </b-form-group> </b-col
            ><b-col>
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
            </b-col></b-row
          >
          <b-row
            ><b-col>
              <b-form-group label="Shift:" label-for="shift" description="">
                <b-form-select
                  id="shift"
                  v-model="form.shift"
                  :options="options"
                  value-field="value"
                  text-field="text"
                  disabled-field="notEnabled"
                ></b-form-select>
              </b-form-group> </b-col
            ><b-col>
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
              </b-form-group> </b-col
            ><b-col>
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
              </b-form-group> </b-col
          ></b-row>
          <b-row
            ><b-col>
              <b-form-group label="end_reading:" label-for="end_reading" description="">
                <b-form-input
                  id="end_reading"
                  v-model="form.end_reading"
                  type="text"
                  placeholder="Enter end_reading "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
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
              </b-form-group> </b-col
            ><b-col>
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
        </b-form>

        <div v-else>
          <h4>You submitted successfully!</h4>
          <button class="btn btn-success" @click="newPlantProduction">Add</button>
        </div>
      </b-card>

      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import { mapActions, mapState, mapGetters } from "vuex";
// import { Production } from "@/models";
export default {
  data() {
    return {
      form: {
        plant: "",
        date: "",
        shift: "",
        operator_name: "",
        no_of_winderman: "",
        product_code: "",
        end_reading: "",
        start_reading: "",
        wastage: "",
      },

      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],
      formname: "Add Plant Production",
      showform: false,
    };
  },
  computed: {
    ...mapGetters("production", { getstartreading: "getStartreading" }),
    ...mapGetters("employee", { employeeOperator: "employeeOperator" }),
    ...mapState({ plants: (state) => state.plant.plantall }),
    ...mapState({ products: (state) => state.product.productall }),
    ...mapState({ startreadingitem: (state) => state.production.startreadingItem }),
  },
  mounted() {
    this.getPlants();
    this.getProducts();
    this.getEmployees();
  },
  watch: {
    getstartreading: {
      handler() {
        this.form.start_reading = this.getstartreading;
      },
      immediate: true,
    },
  },
  methods: {
    ...mapActions("plant", ["getPlants"]),
    ...mapActions("product", ["getProducts"]),
    ...mapActions("employee", ["getEmployees"]),
    ...mapActions("production", [
      "addProduction",
      "getProductions",
      "getStartReading",
      "clearStartReading",
    ]),
    lastItem(plant) {
      this.getStartReading(plant);
      let start = this.getstartreading;
      this.form.start_reading = start;
    },
    onSubmitForm() {
      let data = {
        plant: this.form.plant,
        date: this.form.date,
        shift: this.form.shift,
        operator_name: this.form.operator_name,
        no_of_winderman: this.form.no_of_winderman,
        product_code: this.form.product_code,
        end_reading: this.form.end_reading,
        start_reading: this.form.start_reading,
        wastage: this.form.wastage,
      };

      console.log("data", data);
      this.addProduction(data);
      this.showform = true;
      this.clearStartReading();
    },
    newPlantProduction() {
      this.showform = false;
      this.clearStartReading();
      this.form = {
        plant: "",
        date: "",
        shift: "",
        operator_name: "",
        no_of_winderman: "",
        product_code: "",
        end_reading: "",
        start_reading: "",
        wastage: "",
      };
    },
    clearstate() {
      this.$store.dispatch("production/clearStateStartReading");
    },
  },
};
</script>
<style lang="css" scoped></style>
