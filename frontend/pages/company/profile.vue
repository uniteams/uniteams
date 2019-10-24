<template>
  <div class="pt-3">

    <div v-if="!isCreated" class="card">
      <h5 class="card-header">Профиль компании</h5>
      <div class="card-body">
        <h5 class="card-title">Реквизиты</h5>


        <div class="row">

          <div class="col-md-2">
            <div class="form-group">
              <label for="country">Страна</label>
              <input
                     type="email"
                     class="form-control"
                     id="country"
                     placeholder="РФ">
            </div>
          </div>

          <div class="col-md-5">
            <div class="form-group">
              <label for="inn">ИНН</label>
              <input v-model="userfio"
                     type="text"
                     class="form-control"
                     id="inn"
                     placeholder="10 или 12 цифр">
            </div>
          </div>

          <div class="col-md-5">
            <div class="form-group">
              <label for="kpp">КПП</label>
              <input v-model="userfio"
                     type="text"
                     class="form-control"
                     id="kpp"
                     placeholder="9 цифр">
            </div>
          </div>

        </div>

        <div class="row">

          <div class="col-md-5">
            <div class="form-group">
              <label for="country">БИК банка</label>
              <input
                     type="text"
                     class="form-control"
                     id="bik"
                     placeholder="youname@domain.org">
            </div>
          </div>


          <div class="col-md-7">
            <div class="form-group">
              <label for="rorder">Расчетный счет</label>
              <input
                     type="text"
                     class="form-control"
                     id="rorder"
                     placeholder="youname@domain.org">
            </div>
          </div>

        </div>

        <h5 class="card-title">Адрес</h5>

        <div class="row">

          <div class="col-md-2">
            <div class="form-group">
              <label for="region">Регион</label>
              <input
                     type="text"
                     class="form-control"
                     id="region"
                     placeholder="02">
            </div>
          </div>

          <div class="col-md-3">
            <div class="form-group">
              <label for="city">Город</label>
              <input
                     type="text"
                     class="form-control"
                     id="city"
                     placeholder="Уфа">
            </div>
          </div>

          <div class="col-md-5">
            <div class="form-group">
              <label for="street">Улица</label>
              <input
                     type="text"
                     class="form-control"
                     id="street"
                     placeholder="Ленина">
            </div>
          </div>

          <div class="col-md-2">
            <div class="form-group">
              <label for="house">Дом</label>
              <input
                type="text"
                class="form-control"
                id="house"
                placeholder="1">
            </div>
          </div>

        </div>


      </div>
      <div class="card-footer ">
        <button @click="saveCompanyProfile()" class="btn btn-primary">Сохранить</button>
      </div>
    </div>

  </div>
</template>

<script>
    export default {
        name: "profile",
        data() {
            return {

            }
        },
        methods: {
            saveCompanyProfile() {

            }
        }
    }
</script>

<style scoped>

</style>
