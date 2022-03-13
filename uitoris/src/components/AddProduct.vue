<template>
  <div>
    <router-link to="/product"
      ><b-button variant="outline-primary" size="sm">Back</b-button></router-link
    >

    <b-container>
      <b-card class="bg-form col-12">
        <h2 class="text-center">{{ formname }}{{ form.id }}</h2>
        <b-form @submit.prevent="onSubmitForm" v-if="!showform">
          <b-row>
            <b-col>
              <b-form-group label="Product code:" label-for="product_code">
                <b-form-input
                  id="product_code"
                  v-model="form.product_code"
                  placeholder="Enter  product code"
                  class="mb-2"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group
                label="Color marking on bobin:"
                label-for="color_marking_on_bobin"
              >
                <b-form-input
                  id="color_marking_on_bobin"
                  v-model="form.color_marking_on_bobin"
                  placeholder="Enter  color marking on bobin"
                  class="mb-2"
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Tape color:" label-for="tape_color">
                <b-form-input
                  id="tape_color"
                  v-model="form.tape_color"
                  placeholder="Enter  tape_color"
                  class="mb-2"
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="Denier:" label-for="denier">
                <b-form-input
                  id="denier"
                  v-model="form.denier"
                  placeholder="Enter denier "
                  class="mb-2"
                  required
                ></b-form-input> </b-form-group
            ></b-col> </b-row
          ><b-row
            ><b-col>
              <b-form-group label="Gramage:" label-for="gramage">
                <b-form-input
                  id="gramage"
                  v-model="form.gramage"
                  class="mb-2"
                  placeholder="Enter gramagen "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="Tape width:" label-for="tape_width">
                <b-form-input
                  id="tape_width"
                  v-model="form.tape_width"
                  class="mb-2"
                  placeholder="Enter Tape Width"
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group
                label="Cutter spacing:"
                label-for="cutter_spacing"
                description=""
              >
                <b-form-input
                  id="cutter_spacing"
                  v-model="form.cutter_spacing"
                  type="text"
                  placeholder="Enter cutter spacing "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Streanth per tape in kg:"
                label-for="streanth_per_tape_in_kg"
                description=""
              >
                <b-form-input
                  id="streanth_per_tape_in_kg"
                  v-model="form.streanth_per_tape_in_kg"
                  type="text"
                  placeholder="Enter streanth per tape in kg "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Elongation percent:"
                label-for="elongation_percent"
                description=""
              >
                <b-form-input
                  id="elongation_percent"
                  v-model="form.elongation_percent"
                  type="text"
                  placeholder="Enter Elongation percent "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="Tenacity:" label-for="tenacity" description="">
                <b-form-input
                  id="tenacity"
                  v-model="form.tenacity"
                  type="text"
                  placeholder="Enter tenacity "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group label="PP percent:" label-for="pp_percent" description="">
                <b-form-input
                  id="pp_percent"
                  v-model="form.pp_percent"
                  type="text"
                  placeholder="Enter pp percent "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group
                label="Filler percent:"
                label-for="filler_percent"
                description=""
              >
                <b-form-input
                  id="filler_percent"
                  v-model="form.filler_percent"
                  type="text"
                  placeholder="Enter filler percent "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-group
                label="Shiner percent:"
                label-for="shiner_percent"
                description=""
              >
                <b-form-input
                  id="shiner_percent"
                  v-model="form.shiner_percent"
                  type="text"
                  placeholder="Enter shiner percent "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col>
              <b-form-group
                label="Color percent:"
                label-for="color_percent"
                description=""
              >
                <b-form-input
                  id="color_percent"
                  v-model="form.color_percent"
                  type="text"
                  placeholder="Enter color percent "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="TPT percent:" label-for="tpt_percent" description="">
                <b-form-input
                  id="tpt_percent"
                  v-model="form.tpt_percent"
                  type="text"
                  placeholder="Enter tpt percent "
                  required
                ></b-form-input>
              </b-form-group> </b-col
            ><b-col>
              <b-form-group label="UV percent:" label-for="uv_percent" description="">
                <b-form-input
                  id="uv_percent"
                  v-model="form.uv_percent"
                  type="text"
                  placeholder="Enter uv percent "
                  required
                ></b-form-input>
              </b-form-group>
            </b-col> </b-row
          ><b-row>
            <b-col>
              <b-form-group label="Color name:" label-for="color_name" description="">
                <b-form-input
                  id="color_name"
                  v-model="form.color_name"
                  type="text"
                  placeholder="Enter color name "
                  required
                ></b-form-input> </b-form-group></b-col
            ><b-col> </b-col>
            <b-col> </b-col>
            <b-col> </b-col>
          </b-row>

          <div class="text-center">
            <b-button type="submit" variant="primary">Submit</b-button>
          </div>
        </b-form>

        <div v-else>
          <h4>You submitted successfully!</h4>
          <button class="btn btn-success" @click="AddnewProduct">Add</button>
        </div>
      </b-card>
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import { Product } from "@/models";
export default {
  data() {
    return {
      form: new Product(),
      options: [
        { value: "Day", text: "DAY" },
        { value: "Night", text: "NIGHT" },
      ],
      formname: "Add Product Form",
      showform: false,
    };
  },
  computed: {},
  mounted() {},
  methods: {
    ...mapActions("product", ["getProducts", "addProduct"]),
    onSubmitForm() {
      this.addProduct(this.form);
      this.showform = true;
    },
    AddnewProduct() {
      this.showform = false;
      this.form = new Product();
    },
  },
};
</script>
<style lang="css" scoped></style>
