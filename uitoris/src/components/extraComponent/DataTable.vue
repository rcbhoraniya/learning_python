<template>
  <div>
    <b-form-select id="pageselect" v-model="currentEntries" class="w-25 mt-2">
      <b-form-select-option v-for="se in showEntries" :key="se" v-bind:value="se">
        {{ se }}
      </b-form-select-option>
    </b-form-select>
    <TableBase :columns="columns" :entries="entries" />
  </div>
</template>

<script>
import TableBase from "../components/table/TableBase.vue";
import { mapState, mapActions } from "vuex";

export default {
  name: "DataTable",
  data() {
    return {
      columns: [
        { name: "id", text: "ID" },
        { name: "plant", text: "Plant" },
        { name: "shift", text: "Shift" },
        { name: "end_reading", text: "End Reading" },
        { name: "start_reading", text: "Start Reading" },
      ],
      //   entries: [],
      showEntries: [10, 15, 25, 50, 100],
      currentEntries: 10,
      filteredEntries: [],
    };
  },
  components: {
    TableBase,
  },
  computed: {
    ...mapState({ entries: (state) => state.production.productionall }),
  },
  created() {
    this.getProductions();
  },
  methods: { ...mapActions("production", ["getProductions"]) },
};
</script>

<style scoped></style>
