<template>
  <div>
    <router-link to="/order/add"
      ><b-button variant="outline-primary" size="sm">Add Order</b-button></router-link
    >
    <b-button size="sm" class="float-right" @click="csvExport(csvData)">
      Export to CSV
    </b-button>
    <h2 class="text-center">Order Table</h2>
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
          label="Filter On"
          label-for="filter-by-select"
          label-cols-sm="3"
          label-align-sm="right"
          label-size="sm"
          class="mb-0"
          v-slot="{ ariaDescribedby }"
        >
          <b-input-group size="sm">
            <b-form-select
              id="filter-by-select"
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
      <template #cell(order_date)="data">{{ data.value | formatDate }}</template>
      <template #cell(actions)="row">
        <b-button variant="primary" class="mr-2" size="sm" @click="EditOrder(row.item.id)"
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
        <b-btn type="submit" variant="outline-danger" @click="DeleteOrder">Delete</b-btn>
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
  name: "OrderTable",
  title: "Order",
  data() {
    return {
      fields: [
        // { key: "id", label: "Id", sortable: true, sortDirection: "desc" },
        {
          key: "id",
          label: "id",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "order_date",
          label: "order_date",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "customer_name.name",
          label: "customer_name",
          sortable: true,
          sortDirection: "desc",
        },
        {
          key: "order_qty",
          label: "order_qty",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "pi_number",
          label: "pi_number",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "product_code",
          label: "product_code",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },

        { key: "actions", label: "Actions", thClass: "action" },
      ],
      currentPage: 1,
      perPage: 10,
      pageOptions: [10, 15, 20, { value: 100, text: "Show a lot" }],
      sortBy: "",
      sortDesc: false,
      sortDirection: "asc",
      filter: null,
      filterOn: [],
      ID: null,
      infoModaltitle: "",
    };
  },
  mounted() {
    this.getOrders();
  },
  computed: {
    ...mapGetters("order", { totalRows: "orderListLength" }),
    ...mapState({ items: (state) => state.order.orderall }),
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
    ...mapActions("order", ["getOrders", "deleteOrder"]),
    showModal(id) {
      this.infoModaltitle = `Item#${id}`;
      this.ID = id;
      this.$refs.myModalRef.show();
    },
    hideModal() {
      this.$root.$emit("bv::hide::modal", "myModal");
      this.$refs.myModalRef.hide();
    },

    DeleteOrder() {
      this.deleteOrder(this.ID);
      this.hideModal();
    },
    EditOrder(id) {
      this.$router.push("/order/" + id);
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
      link.setAttribute("download", "order.csv");
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
