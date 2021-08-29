<template>
  <div>
    <b-button variant="outline-info" size="sm" to="/order">Back</b-button>
    <h4 class="text-center">{{ formname }}{{ form.id }}</h4>
    <b-container>
      <b-card>
        <b-form @submit.prevent="onSubmitForm" v-if="!showform">
          <b-row>
            <b-col>
              <b-form-group label="Order Date:" label-for="order_date">
                <b-form-datepicker
                  id="order_date"
                  v-model="form.order_date"
                  class="mb-2"
                  required
                ></b-form-datepicker>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="customer_name:" label-for="customer_name">
                <b-form-input
                  id="customer_name"
                  v-model="form.customer_name"
                  placeholder="Enter  customer_name"
                  class="mb-2"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="order_qty:" label-for="order_qty">
                <b-form-input
                  id="order_qty"
                  v-model="form.order_qty"
                  placeholder="Enter order_qty "
                  class="mb-2"
                  required
                ></b-form-input> </b-form-group
            ></b-col> </b-row
          ><b-row
            ><b-col>
              <b-form-group label="pi_number:" label-for="pi_number">
                <b-form-input
                  id="pi_number"
                  v-model="form.pi_number"
                  class="mb-2"
                  placeholder="Enter pi_number "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="product_code:" label-for="product_code">
                <b-form-input
                  id="product_code"
                  v-model="form.product_code"
                  class="mb-2"
                  placeholder="Enter product_code"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col> </b-col
          ></b-row>

          <b-button type="submit" variant="primary" class="mr-2">Submit</b-button>
        </b-form>

        <div v-else>
          <h4>You submitted successfully!</h4>
          <button class="btn btn-success" @click="AddnewOrder">Add</button>
        </div>
      </b-card>
      <!-- <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card> -->
    </b-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      form: {
        // id: null,
        order_date: "",
        customer_name: "",
        order_qty: "",
        pi_number: "",
        product_code: "",
      },
      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],
      formname: "Add Order Form",
      showform: false,
    };
  },
  computed: {
    // ...mapGetters("product", { getProductbyPlant: "getProductByPlant" }),
    // ...mapState({ plants: (state) => state.plant.plantall }),
    // ...mapState({ products: (state) => state.product.productall }),
    // ...mapState({ operators: (state) => state.operator.operatorall }),
    // ...mapState({ items: (state) => state.order.orderall }),
  },
  mounted() {
    // this.getPlants();
    // this.getOrders();
    // this.getOperators();
    // this.getProductions();
  },
  methods: {
    // ...mapActions("plant", ["getPlants"]),
    ...mapActions("order", ["getOrders", "addOrder"]),
    // ...mapActions("operator", ["getOperators"]),
    // ...mapActions("production", ["addProduction", "getProductions"]),

    onSubmitForm() {
      //   event.preventDefault();
      // alert(JSON.stringify(this.form));
      var data = {
        // id: null,
        order_date: this.form.order_date,
        customer_name: this.form.customer_name,
        order_qty: this.form.order_qty,
        pi_number: this.form.pi_number,
        product_code: this.form.product_code,
      };
      this.addOrder(data);
      this.showform = true;
    },
    AddnewOrder() {
      this.showform = false;
      this.form = {
        // id: null,
        order_date: "",
        customer_name: "",
        order_qty: "",
        pi_number: "",
        product_code: "",
      };
      // this.$router.go();
    },
  },
};
</script>
