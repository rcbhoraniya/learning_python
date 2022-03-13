<template>
  <production-table />
</template>

<script>
import ProductionTable from "../components/table/ProductionTable";
export default {
  name: "Production",
  title: "Production",
  components: {
    "production-table": ProductionTable,
  },
  data() {
    return {};
  },
  computed: {},

  methods: {},
};
</script>

<style lang="css" scoped></style>
