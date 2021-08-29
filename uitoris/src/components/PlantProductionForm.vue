<template>
  <div>
    <b-button variant="outline-info" size="sm" to="/production">Back</b-button>
    <h4 class="text-center">{{ formName }}</h4>
    <b-container>
      <b-card>
        <b-form @submit.prevent="$emit('on-submit', form)">
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

              <b-form-group label="Plant:" label-for="plant" description="">
                <b-form-select
                  id="plant"
                  v-model="form.plant"
                  :options="plants"
                  value-field="id"
                  text-field="name"
                  @change="lastItem(form.plant)"
                ></b-form-select>
              </b-form-group>

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
              </b-form-group>

              <b-form-group
                label="Operator name:"
                label-for="operator_name"
                description=""
              >
                <b-form-select
                  v-model="form.operator_name"
                  :options="operators"
                  value-field="id"
                  text-field="name"
                ></b-form-select>
              </b-form-group>

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
            ><b-col>
              <b-form-group label="end_reading:" label-for="end_reading" description="">
                <b-form-input
                  id="end_reading"
                  v-model="form.end_reading"
                  type="text"
                  placeholder="Enter end_reading "
                  required
                ></b-form-input>
              </b-form-group>

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
          <b-button type="submit" variant="primary" class="mr-2">Submit</b-button>
        </b-form>
      </b-card>
    </b-container>
  </div>
</template>

<script>
export default {
  props: {
    formName: String,
    plants: Array,
    products: Array,
    operators: Array,
    production: Object,
    // items: Array,
  },
  data() {
    return {
      formname: "Edit Plant Production#",
      // formId: this.form.id,
      form: {
        id: this.production?.id || "",
        date: this.production?.date || "",
        plant: this.production?.plant || "",
        product_code: this.production?.product_code || "",
        shift: this.production?.shift || "",
        operator_name: this.production?.operator_name || "",
        wastage: this.production?.wastage || "",
        end_reading: this.production?.end_reading || "",
        start_reading: this.production?.start_reading || "",
        no_of_winderman: this.production?.no_of_winderman || "",
      },
      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],

      showform: false,
    };
  },
  computed: {},
  mounted() {},
  methods: {},
};
</script>
