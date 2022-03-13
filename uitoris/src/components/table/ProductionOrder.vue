<template>
  <div>
    <router-link to="/production"
      ><b-button variant="outline-primary" size="sm">Home</b-button></router-link
    >
    <b-button size="sm" class="float-right" @click="csvExport(csvData)">
      Export to CSV
    </b-button>
    <h2 class="text-center">Production Order Table</h2>
    <!-- User Interface controls -->

    <!-- Main table element -->
    <b-table
      hover
      responsive="sm"
      bordered
      show-empty
      small
      :items="items"
      :fields="fields"
    ></b-table>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "ProductionOrderTable",
  title: "ProductionOrder",
  data() {
    return {
      fields: [
        // { key: "id", label: "Id", sortable: true, sortDirection: "desc" },
        {
          key: "product_code",
          label: "product code",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "req_production",
          label: "req production",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "color_marking_on_bobin",
          label: "color marking on bobin",
          sortable: true,
          sortDirection: "desc",
        },
        {
          key: "tape_color",
          label: "tape color",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "denier",
          label: "denier",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },
        {
          key: "gramage",
          label: "gramage",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "tape_width",
          label: "tape width",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "cutter_spacing",
          label: "cutter spacing",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "streanth_per_tape_in_kg",
          label: "streanth per tape in kg",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "elongation_percent",
          label: "elongation percent",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class100",
        },
        {
          key: "tenacity",
          label: "tenacity",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "pp_percent",
          label: "pp %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "filler_percent",
          label: "filler %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "shiner_percent",
          label: "shiner %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "color_percent",
          label: "color %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "tpt_percent",
          label: "tpt %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "uv_percent",
          label: "uv %",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
        {
          key: "color_name",
          label: "color name",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class",
        },
      ],
    };
  },
  mounted() {
    this.getProductionOrder();
  },
  computed: {
    ...mapState({ items: (state) => state.production_order.production_order }),
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

  methods: {
    ...mapActions("production_order", ["getProductionOrder"]),

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
      link.setAttribute("download", "production_order.csv");
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
.my-class100 {
  max-width: 100px;
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
