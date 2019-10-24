<template>
  <div>

    <div class="card">
      <h5 class="card-header">Найти компанию</h5>
      <div class="card-body">
        <h5 class="card-title">Введите адрес рабочей почты</h5>

        <div class="input-group mb-3">
          <input type="text" class="form-control"
                 v-model="searchCompanyAddress"
                 placeholder="Адрес почты"
                 aria-label="Recipient's username"
                 aria-describedby="button-addon2">
          <div class="input-group-append">
            <button @click="searchCompany()" class="btn btn-outline-secondary" type="button" id="button-addon2">Найти
            </button>
          </div>
        </div>

        <div class="result ">
          <div class="list-group">
            <nuxt-link no-prefetch :to="'/company/join/:'+copmany.id" v-for="copmany of findedCompany" v-bind:key="copmany.id"
                       class="list-group-item list-group-item-action">
              {{ copmany.name }}
            </nuxt-link>
          </div>
        </div>

      </div>
    </div>

    <nuxt-link no-prefetch to="/company/create" class="btn btn-primary mt-3">Новая компания</nuxt-link>

  </div>
</template>

<script>
    export default {
        name: "SearchCompany",
        data() {
            return {
                searchCompanyAddress: "",
                findedCompany: []
            }
        },
        mounted() {
            // TODO определяем, админ ли,
        },
        methods: {
            searchCompany() {
                // TODO AJAX request
                this.findedCompany = [
                    {name: 'Компания', id: '1'},
                    {name: 'Компания 2', id: '2'},
                    {name: 'Компания 3', id: '3'},
                    {name: 'Компания 4', id: '4'},
                ]
            }
        }
    }
</script>

<style scoped>

</style>
