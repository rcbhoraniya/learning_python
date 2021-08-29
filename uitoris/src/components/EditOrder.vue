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
        </div>
      </b-card>
      <!-- <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card> -->
    </b-container>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],
      formname: "Edit Order Form#",
      showform: false,
      order: null,
    };
  },
  computed: {
    // ...mapGetters("product", { getProductbyPlant: "getProductByPlant" }),
    // ...mapState({ plants: (state) => state.plant.plantall }),
    // ...mapState({ products: (state) => state.product.productall }),
    // ...mapState({ operators: (state) => state.operator.operatorall }),
    ...mapState({ form: (state) => state.order.order }),
  },
  mounted() {
    // this.getPlants();
    this.getOrderById(this.$route.params.id);
    // this.getOperators();
    // this.getProductions();
  },
  methods: {
    // ...mapActions("plant", ["getPlants"]),
    ...mapActions("order", ["getOrderById", "editOrder"]),
    // ...mapActions("operator", ["getOperators"]),
    // ...mapActions("production", ["addProduction", "getProductions"]),

    onSubmitForm() {
      //   event.preventDefault();
      // alert(JSON.stringify(this.form));
      var data = this.form;
      this.editOrder(data);
      this.showform = true;
      this.data = {};
      this.$router.push("/order");
    },
  },
};
</script>
