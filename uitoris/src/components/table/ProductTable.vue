<template>
  <div>
    <router-link to="/product/add"
      ><b-button variant="outline-primary" size="sm">Add Product</b-button></router-link
    >

    <b-button size="sm" class="float-right" @click="csvExport(csvData)">
      Export to CSV
    </b-button>
    <h2 class="text-center">Product Table</h2>
    <!-- User Interface controls -->
    <b-row>
      <b-col lg="4" class="my-1">
        <b-form-group
          label="Filter"
          label-for="filter-input"
          label-cols-sm="3"
          label-align-sm="right"
          label-size="sm"
          class="mb-0"
        >
          <b-input-group size="sm">
            <b-form-input
              id="filter-input"
              v-model="filter"
              type="search"
              placeholder="Type to Search"
            ></b-form-input>

            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
      </b-col>

      <b-col lg="3" class="my-1">
        <b-form-group
          label="Sort"
          label-for="sort-by-select"
          label-cols-sm="3"
          label-align-sm="right"
          label-size="sm"
          class="mb-0"
          v-slot="{ ariaDescribedby }"
        >
          <b-input-group size="sm">
            <b-form-select
              id="sort-by-select"
              v-model="filterOn"
              :options="sortOptions"
              :aria-describedby="ariaDescribedby"
              class="w-25"
            >
              <template #first>
                <option value="">-- none --</option>
              </template> </b-form-select
            ><b-input-group-append>
              <b-button :disabled="!filterOn" @click="filterOn = ''">Clear</b-button>
            </b-input-group-append></b-input-group
          ></b-form-group
        >
      </b-col>
    </b-row>

    <!-- Main table element -->
    <b-table
      hover
      responsive="sm"
      bordered
      show-empty
      small
      :items="items"
      :fields="fields"
      :current-page="currentPage"
      :per-page="perPage"
      :filter="filter"
      :filter-included-fields="filterOn"
      @filtered="onFiltered"
    >
      <template #cell(actions)="row">
        <b-button
          variant="primary"
          class="mr-2"
          size="sm"
          @click="EditProduct(row.item.id)"
          ><i class="far fa-edit text-light"></i
        ></b-button>
        <b-button variant="danger" class="mr-2" size="sm" @click="showModal(row.item.id)"
          ><i class="far fa-trash-alt text-light"></i
        ></b-button>
        <b-button variant="primary" size="sm" @click="row.toggleDetails">{{
          row.detailsShowing ? "Hide" : "Show"
        }}</b-button>
      </template>
      <template #row-details="row">
        <b-card>
          <b-row class="mb-2" v-for="(value, key) in row.item" :key="key">
            <b-col sm="3" class="text-sm-right">
              <b>{{ key }}:</b>
            </b-col>
            <b-col>{{ value }}</b-col>
          </b-row>
          <b-button variant="primary" size="sm" @click="row.toggleDetails"
            >Hide Details</b-button
          >
        </b-card>
      </template>
    </b-table>
    <b-modal ref="myModalRef" hide-footer :title="infoModaltitle">
      <div>
        <h5>Do you want to delete this job?</h5>
      </div>
      <div class="float-right pt-4">
        <b-btn type="submit" variant="outline-danger" @click="DeleteProduct"
          >Delete</b-btn
        >
      </div>
      <div class="float-right pr-2 pt-4">
        <b-btn
          type="submit"
          variant="outline-success"
          style="padding-left: 10px"
          @click="hideModal"
          >Cancel</b-btn
        >
      </div>
    </b-modal>

    <b-row>
      <b-col sm="5" md="3" class="my-1">
        <b-form-group
          label="Per page"
          label-for="per-page-select"
          label-cols-sm="6"
          label-cols-md="2"
          label-cols-lg="3"
          label-align-sm="right"
          label-size="sm"
          class="mb-0"
        >
          <b-form-select
            id="per-page-select"
            v-model="perPage"
            :options="pageOptions"
            size="sm"
          ></b-form-select>
        </b-form-group>
      </b-col>

      <b-col>
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="right"
          size="sm"
          class="my-0"
          first-text="First"
          prev-text="Prev"
          next-text="Next"
          last-text="Last"
        ></b-pagination>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from "vuex";
export default {
  name: "EditableTable",
  title: "Product",
  data() {
    return {
      fields: [
        // { key: "id", label: "Id", sortable: true, sortDirection: "desc" },
        {
          key: "product_code",
          label: "Product Code",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "color_marking_on_bobin",
          label: "color Marking on Bobin",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        { key: "tape_color", label: "Tape Color", sortable: true, sortDirection: "desc" },
        {
          key: "denier",
          label: "Denier",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "gramage",
          label: "Gramage",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "tape_width",
          label: "Tape Width",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "cutter_spacing",
          label: "Cutter Spacing",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "streanth_per_tape_in_kg",
          label: "Streanth per tape in kg",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "elongation_percent",
          label: "Elongation %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "tenacity",
          label: "Tenacity",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "pp_percent",
          label: "pp %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "filler_percent",
          label: "filler %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "shiner_percent",
          label: "shiner %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "color_percent",
          label: "color %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "tpt_percent",
          label: "tpt %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "uv_percent",
          label: "uv %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        {
          key: "color_name",
          label: "color name",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },

        { key: "actions", label: "Actions", thClass: "action" },
      ],
      ID: null,
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 15, 20, { value: 100, text: "Show a lot" }],
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
      infoModalshow: false,
      infoModaltitle: "",
    };
  },
  mounted() {
    this.getProducts();
  },
  computed: {
    ...mapGetters("product", { totalRows: "productListLength" }),
    ...mapState({ items: (state) => state.product.productall }),
    csvData() {
      return this.items.map((item) => ({
        ...item,
        // plant: "TPF", //item.address.city,
        // shift: "Day", //item.company.name
      }));
    },
    sortOptions() {
      // Create an options list from our fields
      return this.fields
        .filter((f) => f.sortable)
        .map((f) => {
          return { text: f.label, value: f.key };
        });
    },
  },

  methods: {
    ...mapActions("product", ["getProducts"]),
    DeleteProduct() {
      this.deleteProduct(this.ID);
      this.hideModal();
    },
    EditProduct(Id) {
      this.$router.push({ name: "EditProduct", params: { id: Id } });
    },
    showModal(id) {
      this.infoModaltitle = `Item#${id}`;
      this.ID = id;
      this.$refs.myModalRef.show();
    },
    hideModal() {
      this.$root.$emit("bv::hide::modal", "myModal");
      this.$refs.myModalRef.hide();
    },
    csvExport(arrData) {
      let csvContent = "data:text/csv;charset=utf-8,";
      csvContent += [
        Object.keys(arrData[0]).join(","),
        ...arrData.map((item) => Object.values(item).join(",")),
      ]
        .join("\n")
        .replace(/(^\[)|(\]$)/gm, "");

      const data = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", data);
      link.setAttribute("download", "product.csv");
      link.click();
    },

    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      this.currentPage = 1;
    },
  },
};
</script>
<style lang="css">
.my-class {
  max-width: 80px;
}
.my-class1 {
  max-width: 70px;
}
.my-class2 {
  max-width: 50px;
}
.action {
  max-width: 130px;
}
</style>
