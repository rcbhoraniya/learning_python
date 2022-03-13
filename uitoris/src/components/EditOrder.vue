<template>
  <div>
    <router-link to="/order"
      ><b-button variant="outline-primary" size="sm">Back</b-button></router-link
    >
    <b-container>
      <b-card class="bg-form col-12">
        <h2 class="text-center">{{ formname }}{{ form.id }}</h2>
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
              <b-form-group label="Customer name:" label-for="customer_name">
                <b-form-input
                  id="customer_name"
                  v-model="form.customer_name"
                  placeholder="Enter  customer name"
                  class="mb-2"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="Order qty:" label-for="order_qty">
                <b-form-input
                  id="order_qty"
                  v-model="form.order_qty"
                  placeholder="Enter order qty "
                  class="mb-2"
                  required
                ></b-form-input> </b-form-group
            ></b-col> </b-row
          ><b-row
            ><b-col>
              <b-form-group label="PI number:" label-for="pi_number">
                <b-form-input
                  id="pi_number"
                  v-model="form.pi_number"
                  class="mb-2"
                  placeholder="Enter pi number "
                  required
                ></b-form-input>
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
              </b-form-group> </b-col
            ><b-col> </b-col
          ></b-row>

          <div class="text-center">
            <b-button type="submit" variant="primary">Submit</b-button>
          </div>
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
      formname: "Edit Order Form#",
      showform: false,
      order: null,
    };
  },
  computed: {
    ...mapState({ products: (state) => state.product.productall }),
    ...mapState({ form: (state) => state.order.order }),
  },
  mounted() {
    this.getProducts();
    this.getOrderById(this.$route.params.id);
  },
  methods: {
    ...mapActions("product", ["getProducts"]),
    ...mapActions("order", ["getOrderById", "editOrder"]),
    onSubmitForm() {
      var data = this.form;
      this.editOrder(data);
      this.showform = true;
      this.$router.push("/order");
    },
  },
};
</script>
<style lang="css" scoped></style>
