<template>
  <div>
    <!-- <h1>Employee</h1> -->
    <EmployeeTable />
  </div>
</template>

<script>
import EmployeeTable from "@/components/table/EmployeeTable.vue";
export default {
  name: "EmployeeVue",
  title: "EmployeeVue",
  components: {
    EmployeeTable,
  },
};
</script>

<style lang="scss" scoped></style>
