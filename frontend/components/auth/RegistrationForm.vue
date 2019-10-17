<template>
  <div>
    <h3>Registration</h3>
    <div class="form-group">
      <label for="InputLogin">Login</label>
      <input type="text"
             v-model="login"
             v-bind:class="{ 'is-invalid': isHaveError.login }"
             class="form-control"
             id="InputLogin"
             placeholder="Login">
      <div v-if="isHaveError.login" class="invalid-feedback">{{ isHaveError.login }}</div>
    </div>
    <div class="form-group">
      <label for="InputEmail">Email address</label>
      <input type="email"
             v-model="email"
             v-bind:class="{ 'is-invalid': isHaveError.email }"
             class="form-control"
             id="InputEmail"
             placeholder="Enter email">
      <div v-if="isHaveError.email" class="invalid-feedback">{{ isHaveError.email }}</div>
    </div>
    <div class="form-group">
      <label for="InputPassword">Password</label>
      <input type="password"
             v-model="password"
             v-bind:class="{ 'is-invalid': isHaveError.password }"
             class="form-control"
             id="InputPassword"
             placeholder="Password">
      <div v-if="isHaveError.password" class="invalid-feedback">{{ isHaveError.password }}</div>
    </div>
    <div class="form-group">
      <label for="InputRetryPassword">Retry password</label>
      <input type="password"
             v-model="retrypassword"
             v-bind:class="{ 'is-invalid': isHaveError.retrypassword }"
             class="form-control"
             id="InputRetryPassword"
             placeholder="Retry password">
      <div v-if="isHaveError.retrypassword" class="invalid-feedback">{{ isHaveError.retrypassword }}</div>
    </div>

    <small class="form-text text-muted">More fields you need... </small>

    <button @click="sendForm()" class="btn btn-primary">Registration</button>

    <div class="p-2">
      <nuxt-link no-prefetch to="/users/sign-in/">or sign-up</nuxt-link>
    </div>
  </div>
</template>

<script>
    export default {
        data() {
            return {
                login: '',
                email: '',
                password: '',
                retrypassword: '',
                isHaveError: {
                    login: false,
                    email: false,
                    password: false,
                    retrypassword: false
                },
                lockButton: false
            }
        },
        mounted() {

        },
        methods: {
            sendForm() {
                if (this.lockButton) {
                    return false;
                }

                this.isHaveError = {
                    login: false,
                    email: false,
                    password: false,
                    retrypassword: false
                };



                // Валидация, метод в утилитах /static/js/utilities.js
                if (!validate(this.login, '!empty')) {
                    this.isHaveError.login = 'Введите корректный адрес почты'; // TODO i18n
                }
                if (!validate(this.password, 'password')) {
                    this.isHaveError.password = 'Введите пароль'; // TODO i18n
                }

                // Если нет ошибок отправляем
                if (!this.isHaveError.email && !this.isHaveError.password) {
                    this.lockButton = true; // Блокируем
                    this.doLogin();
                }

            },
            doLogin() {
                this.$axios.$post(API + '/user/registration/', {

                })
                    .then((responses)=>{
                        // TODO Регистрация успешна
                        console.log(responses);
                        this.lockButton = false; // Разблокируем
                    })
                    .catch((error) => {
                        // TODO Регистрация провалена
                        console.log(error);
                        this.lockButton = false; // Разблокируем
                    });
            }
        }
    }
</script>

<style scoped>

</style>
