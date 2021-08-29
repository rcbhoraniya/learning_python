<template>
  <div>
    <b-table striped show-empty :items="filtered">
      <template slot="top-row" slot-scope="{ fields }">
        <td v-for="field in fields" :key="field.key">
          <input v-model="filters[field.key]" :placeholder="field.label" />
        </td>
      </template>
    </b-table>
    <!-- <template #cell(date)="data">{{ data.value | formatDate }}</template>

      <template #cell(actions)="row">
        <b-button
          variant="primary"
          class="mr-2"
          size="sm"
          :to="'/production/' + row.item.id"
          ><i class="far fa-edit text-light"></i
        ></b-button>
        <b-button
          variant="danger"
          class="mr-2"
          size="sm"
          @click="deleteAction(row.item.id)"
          ><i class="far fa-trash-alt text-light"></i
        ></b-button>
        <b-button variant="info" size="sm" @click="row.toggleDetails">{{
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
          <b-button variant="info" size="sm" @click="row.toggleDetails"
            >Hide Details</b-button
          >
        </b-card>
      </template> -->
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "DataTable",
  data() {
    return {
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
          thClass: "my-class2",
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
          thClass: "my-class1",
        },
        {
          key: "wastage",
          label: "wastage",
          sortable: true,
          sortDirection: "desc",
          thClass: "my-class1",
        },

        // { key: "actions", label: "Actions" },
      ],
    };
  },

  created() {
    this.getProductions();
  },
  methods: { ...mapActions("production", ["getProductions"]) },
  computed: {
    ...mapState({ items: (state) => state.production.productionall }),
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
  max-width: 60px;
}
</style>
