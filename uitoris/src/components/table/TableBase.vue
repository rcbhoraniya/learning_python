<template>
  <div class="mt-3">
    <table class="table table-bordered table-sm table-hover">
      <thead>
        <tr>
          <th scope="col" v-for="th in tableHeader" :key="th.key">
            <div>
              <span>{{ th.text }}</span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="td in tableData" :key="td.key">
          <td scope="row">{{ td.id }}</td>
          <td scope="row">{{ td.plant.name }}</td>
          <td scope="row">{{ td.shift }}</td>
          <td scope="row">{{ td.start_reading }}</td>
          <td scope="row">{{ td.end_reading }}</td>
          <td scope="row">
            <button class="btn btn-danger btn-sm" v-on:click="deleteProduction(td.id)">
              Delete
            </button>
            <button class="btn btn-success btn-sm" v-on:click="editProduction(td.id)">
              Edit
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "TableBase",
  props: { columns: Array, entries: Array },
  computed: {
    tableHeader() {
      return this.columns || [];
    },
    tableData() {
      return this.entries || [];
    },
  },
  methods: {
    ...mapActions("production", ["deleteProduction"]),
  },
};
</script>

<style scoped></style>
