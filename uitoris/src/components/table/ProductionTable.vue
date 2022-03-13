<template>
  <div>
    <router-link to="/production/add"
      ><b-button variant="outline-primary" size="sm"
        >Add Plant Data</b-button
      ></router-link
    >
    <b-button size="sm" class="float-right" @click="csvExport(csvData)">
      Export to CSV
    </b-button>
    <!-- <router-link to="/Production/add">Add</router-link> -->
    <h2 class="text-center">Production Table</h2>
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
          label="Filter on"
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
              </template>
            </b-form-select>
            <b-input-group-append>
              <b-button :disabled="!filterOn" @click="filterOn = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group></b-form-group
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
      :per-page="0"
      :filter="filter"
      :filter-included-fields="filterOn"
      @filtered="onFiltered"
    >
      <template #cell(date)="data">{{ data.value | formatDate }}</template>

      <template #cell(actions)="row">
        <b-button
          variant="primary"
          class="mr-2"
          size="sm"
          @click="EditProduction(row.item.id)"
          ><i class="far fa-edit text-light"></i
        ></b-button>
        <b-button variant="danger" class="mr-2" size="sm" @click="showModal(row.item.id)"
          ><i class="far fa-trash-alt text-light"></i
        ></b-button>
        <b-button variant="secondary" size="sm" @click="row.toggleDetails">{{
          row.detailsShowing ? "Hide" : "Show"
        }}</b-button>
      </template>

      <template #row-details="row">
        <b-card>
          <b-row class="mb-2" v-for="(value, key) in row.item" :key="key">
            <b-col sm="3" class="text-sm-right">
              <b>{{ key }}: </b>
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
        <b-btn type="submit" variant="outline-danger" @click="DeleteProduction"
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
            :value="pageOptions"
            size="sm-1"
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
// import { mapActions } from "vuex";
import { mapState, mapActions } from "vuex";
export default {
  name: "ProductionTable",
  title: "Plant Production",

  data() {
    return {
      ID: null,
      infoModaltitle: "",
      searchTitle: "",
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 15, 20, { value: 100, text: "Show a lot" }],
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
      filters: {
        date: "",
        plant: "",
        product_code: "",
        shift: "",
        operator_name: "",
        wastage: "",
        end_reading: "",
        start_reading: "",
        no_of_winderman: "",
      },
      fields: [
        {
          key: "id",
          label: "Id",
          thClass: "my-class2",
          sortable: true,
          sortDirection: "desc",
        },
        { key: "date", label: "Date", sortable: true, sortDirection: "desc" },
        {
          key: "plant_name",
          label: "Plant",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class2",
        },
        { key: "shift", label: "Shift", sortable: true, sortDirection: "desc" },
        {
          key: "operator_name_name",
          label: "Operator name",
          sortable: true,
          sortDirection: "desc",
        },
        {
          key: "product_code_code",
          label: "Product Code",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "color_marking_on_bobin",
          label: "Color Marking on Bobin",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "tape_color",
          label: "Tape Color",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "denier",
          label: "Denier",
          sortable: true,
          sortDirection: "desc",
        },
        {
          key: "end_reading",
          label: "end reading",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "start_reading",
          label: "start reading",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "production_in_kg",
          label: "production in kg",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "wastage",
          label: "wastage",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },

        { key: "actions", label: "Actions" },
      ],
    };
  },

  computed: {
    // ...mapGetters("production", { totalRows: "productionListLength" }),
    ...mapState({ items: (state) => state.production.productionall }),
    ...mapState({ totalRows: (state) => state.production.count }),
    filtered() {
      const filtered = this.items.filter((item) => {
        return Object.keys(this.filters).every((key) =>
          String(item[key]).includes(this.filters[key])
        );
      });
      return filtered.length > 0
        ? filtered
        : [
            Object.keys(this.items[0]).reduce(function (obj, value) {
              obj[value] = "";
              return obj;
            }, {}),
          ];
    },
    csvData() {
      return this.items.map((item) => ({
        ...item,
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
  created() {
    // this.getProductions();
    this.retrieveProductions();
  },
  methods: {
    ...mapActions("production", ["deleteProduction", "getProductions"]),

    DeleteProduction() {
      this.deleteProduction(this.ID);
      this.hideModal();
    },

    EditProduction(Id) {
      this.$router.push({ name: "EditPlantProduction", params: { id: Id } });
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
    getRequestParams(searchTitle, currentPage, perPage) {
      let params = {};
      if (searchTitle) {
        params["searchTitle"] = searchTitle;
      }
      if (currentPage) {
        params["page"] = currentPage;
      }
      if (perPage) {
        params["page_size"] = perPage;
      }
      return params;
    },
    retrieveProductions() {
      const params = this.getRequestParams(
        this.searchTitle,
        this.currentPage,
        this.perPage
      );
      this.getProductions(params);
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
      link.setAttribute("download", "plant production.csv");
      link.click();
    },

    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length;
      // this.currentPage = 1;
    },
  },
  watch: {
    currentPage: {
      handler: function (value) {
        this.currentPage = value;
        this.retrieveProductions();
        // console.log(this.currentPage);
      },
    },
    perPage: {
      handler: function (value) {
        this.perPage = value;
        this.currentPage = 1;
        this.retrieveProductions();
      },
    },
  },
};
</script>
<style lang="scss" scoped>
.my-class {
  max-width: 90px;
}
.my-class1 {
  max-width: 70px;
}
.my-class2 {
  max-width: 60px;
}
</style>
