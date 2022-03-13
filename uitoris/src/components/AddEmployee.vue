<template>
  <div>
    <router-link to="/employee"
      ><b-button variant="outline-primary" size="sm">Back</b-button></router-link
    >
    <b-container>
      <div class="d-flex justify-content-center align-items-center container">
        <b-card class="bg-form col-12">
          <h3 class="text-center">{{ formname }}{{ form.id }}</h3>
          <b-form @submit.prevent="onSubmitForm" v-if="!showform">
            <b-row>
              <b-col>
                <b-form-group label="First Name:" label-for="name" description="">
                  <b-form-input
                    id="name"
                    v-model="form.name"
                    type="text"
                    placeholder="Enter name "
                    required
                  ></b-form-input>
                </b-form-group> </b-col
              ><b-col>
                <b-form-group label="Middle Name:" label-for="mname" description="">
                  <b-form-input
                    id="mname"
                    v-model="form.mname"
                    type="text"
                    placeholder="Enter middle name "
                    required
                  ></b-form-input>
                </b-form-group> </b-col
              ><b-col>
                <b-form-group label="Last Name:" label-for="lname" description="">
                  <b-form-input
                    id="mname"
                    v-model="form.lname"
                    type="text"
                    placeholder="Enter last name "
                    required
                  ></b-form-input> </b-form-group
              ></b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group label="Address:" label-for="address" description="">
                  <b-form-input
                    id="address"
                    v-model="form.address"
                    type="text"
                    placeholder="Enter address "
                    required
                  ></b-form-input>
                </b-form-group> </b-col
            ></b-row>
            <b-row>
              <b-col>
                <b-form-group label="State:" label-for="state" description="">
                  <b-form-select
                    id="state"
                    v-model="form.state"
                    :options="states"
                    value-field="id"
                    text-field="name"
                    @change="getdistrict(form.state)"
                  ></b-form-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="District:" label-for="district" description="">
                  <b-form-select
                    id="districts"
                    v-model="form.district"
                    :options="districts"
                    value-field="id"
                    text-field="name"
                  ></b-form-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="City:" label-for="city" description="">
                  <b-form-input
                    id="city"
                    v-model="form.city"
                    type="text"
                    placeholder="Enter city "
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Mobile no1:" label-for="mobile1" description="">
                  <b-form-input
                    id="mobile1"
                    v-model="form.mobile1"
                    type="text"
                    placeholder="Enter mobile no 1 "
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <b-form-group label="Mobile no2:" label-for="mobile2" description="">
                  <b-form-input
                    id="mobile2"
                    v-model="form.mobile2"
                    type="text"
                    placeholder="Enter mobile no 2 "
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Designation:" label-for="plant" description="">
                  <b-form-select
                    id="designation"
                    v-model="form.designation"
                    :options="designations"
                    value-field="id"
                    text-field="designation"
                  ></b-form-select>
                </b-form-group>
              </b-col>
              <b-col>
                <b-form-group label="Aadhhar No:" label-for="aadhhar_no" description="">
                  <b-form-input
                    id="aadhhar_no"
                    v-model="form.aadhhar_no"
                    type="text"
                    placeholder="Enter aadhhar no "
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>

              <!-- <b-col class="col-sm-3">
                <b-img thumbnail fluid :src="file" alt="Image 1"></b-img>
              </b-col> -->
            </b-row>
            <b-row>
              <b-col>
                <b-form-group
                  label="Upload Photo:"
                  label-for="photo_file"
                  label-align-sm="left"
                >
                  <b-form-file
                    id="photo_file"
                    v-model="file"
                    accept="image/jpeg, image/png, image/gif"
                    placeholder="Drag&amp;drop or select add Image"
                    @change="onFileChange"
                  ></b-form-file>
                </b-form-group>
              </b-col>
              <b-col>
                <b-img
                  v-bind:src="imagePreview"
                  width="100"
                  height="125"
                  v-show="showPreview"
                />
              </b-col>
            </b-row>
            <div class="text-center">
              <b-button type="submit" variant="primary">Submit</b-button>
            </div>
          </b-form>

          <div v-else>
            <h4>You submitted successfully!</h4>
            <button class="btn btn-success" @click="newEmployee">Add</button>
          </div>
        </b-card>
      </div>
      <b-card class="mt-3" header="Form Data Result">
        <pre class="m-0">{{ form }}</pre>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";

export default {
  data() {
    return {
      form: {
        name: "",
        mname: "",
        lname: "",
        address: "",
        mobile1: "",
        mobile2: "",
        designation: "",
        aadhhar_no: "",
        city: "",
        state: "",
        photo_image: "",
      },
      file: null,
      imagePreview: null,
      showPreview: false,
      formname: "Add Employee",
      showform: false,
    };
  },
  computed: {
    ...mapState({ designations: (state) => state.designation.designationall }),
    ...mapState({ states: (state) => state.employee.statesall }),
    ...mapState({ districts: (state) => state.employee.districtsall }),
  },
  mounted() {
    this.getDesignations();
    this.getStates();
    // this.getDistricts();
  },
  // watch: {
  //   file(val) {
  //     if (!val) return;
  //     if (this.previewImg) {
  //       this.previewImg.remove();
  //     }
  //     const img = document.createElement("img");
  //     img.classList.add("obj");
  //     img.file = this.file;
  //     this.previewImg = img;
  //     this.$refs.preview.appendChild(img);

  //     const fileReader = new FileReader();
  //     fileReader.onload = (e) => {
  //       this.previewImg.src = e.target.result;
  //     };
  //     fileReader.readAsDataURL(this.file);
  //   },
  // },
  methods: {
    ...mapActions("designation", ["getDesignations"]),
    ...mapActions("employee", [
      "getEmployees",
      "addEmployee",
      "getStates",
      "getDistricts",
    ]),

    getdistrict(state) {
      this.getDistricts(state);
      let start = this.getstartreading;
      this.form.start_reading = start;
    },
    onFileChange(event) {
      /*
    Set the local file variable to what the user has selected.
    */
      this.form.photo_image = event.target.files[0];

      /*
    Initialize a File Reader object
    */
      let reader = new FileReader();

      /*
    Add an event listener to the reader that when the file
    has been loaded, we flag the show preview as true and set the
    image to be what was read from the reader.
    */
      reader.addEventListener(
        "load",
        function () {
          this.showPreview = true;
          this.imagePreview = reader.result;
        }.bind(this),
        false
      );

      /*
    Check to see if the file is not empty.
    */
      if (this.form.photo_image) {
        /*
            Ensure the file is an image file.
        */
        if (/\.(jpe?g|png|gif)$/i.test(this.form.photo_image.name)) {
          console.log("here");
          /*
            Fire the readAsDataURL method which will read the file in and
            upon completion fire a 'load' event which we will listen to and
            display the image in the preview.
            */
          reader.readAsDataURL(this.form.photo_image);
        }
      }
    },

    onSubmitForm() {
      let data = {
        name: this.form.name,
        mname: this.form.mname,
        lname: this.form.lname,
        address: this.form.address,
        city: this.form.city,
        mobile1: this.form.mobile1,
        mobile2: this.form.mobile2,
        designation: this.form.designation,
        aadhhar_no: this.form.aadhhar_no,
        state: this.form.state,
        photo_image: this.form.photo_image,
      };
      this.addEmployee(data);
      this.showform = true;
    },
    newEmployee() {
      this.showform = false;

      this.form = {
        name: "",
        mname: "",
        lname: "",
        address: "",
        mobile1: "",
        mobile2: "",
        designation: "",
        aadhhar_no: "",
        city: "",
        state: "",
        photo_image: "",
      };
    },
  },
};
</script>
<style lang="css" scoped></style>
