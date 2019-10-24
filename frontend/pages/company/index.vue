<template>
  <div class="pt-5">
    <SearchCompany/>
  </div>
</template>

<script>
    import SearchCompany from "../../components/company/SearchCompany";
    export default {
        name: "index",
        data()  {
          return {

          }
        },
        components: {
            SearchCompany
        },
        mounted() {
          // TODO определяем, админ ли,
        },
        methods : {

        }
    }
</script>

<style scoped>

</style>
