<template>
  <div class="pt-3">
    <div v-if="!isCreated"  class="card">
      <h5 class="card-header">Создать компанию</h5>
      <div class="card-body">
        <h5 class="card-title">Введите адрес рабочей почты</h5>
        <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label for="workEmail">Рабочий e-mail</label>
                <input v-model="email" type="email" class="form-control" id="workEmail" placeholder="youname@domain.org">
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label for="workFIO">ФИО</label>
                <input v-model="userfio" type="text" class="form-control" id="workFIO"  placeholder="Иванов Каспарас Оринтасович">
              </div>
            </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="workCopmanyName">Название компании</label>
              <input v-model="companyName" type="text" class="form-control" id="workCopmanyName" placeholder="ИП Абек Альбертович Акопян">
            </div>
          </div>
        </div>
      </div>
      <div class="card-footer ">
        <button @click="createCompany()" class="btn btn-primary">Создать компанию</button>
      </div>
    </div>

    <div v-if="isCreated" class="card">
      <h5 class="card-header">Компания создана !</h5>
      <div class="card-body">
        <p>Подтвердите почту перейдя по ссылки отправленной вам по указанному адресу.</p>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "create",
        data() {
            return {
                email: '',
                userfio: '',
                companyName: '',
                isCreated: false
            }
        },
        methods: {
            createCompany() {
              // TODO company AJAX to sen Vertification
                this.isCreated = true;
            }
        }
    }
</script>

<style scoped>

</style>
