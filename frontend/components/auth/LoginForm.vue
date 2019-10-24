<template>
  <div class="login">
    <h3>Sign-up</h3>
    <div class="form-group">
      <label for="exampleInputEmail1">Login</label>
      <input v-model="login"
             type="text"
             v-bind:class="{ 'is-invalid': isHaveError.login }"
             class="form-control"
             id="exampleInputEmail1"
             aria-describedby="emailHelp"
             placeholder="Enter login">
      <div v-if="isHaveError.login" class="invalid-feedback">{{ isHaveError.login }}</div>
    </div>
    <div class="form-group">
      <label for="exampleInputPassword1">Password</label>
      <input v-model="password"
             type="password"
             v-bind:class="{ 'is-invalid': isHaveError.password }"
             class="form-control"
             id="exampleInputPassword1"
             placeholder="Password">
      <div v-if="isHaveError.password" class="invalid-feedback">{{ isHaveError.password }}</div>
    </div>
    <button @click="sendForm()" type="submit" class="btn btn-primary">Sign up</button>
    <div class="p-2">
      <nuxt-link no-prefetch to="/users/sign-in/registration/">or registration</nuxt-link>
    </div>

  </div>
</template>

<script>
    export default {
        // Содаём модль данных
        data() {
            return {
                login: '',   // Модель
                password: '',
                isHaveError: {
                    login: false,
                    password: false
                },
                lockButton: false // Блокировка повторного нажатия
            }
        },
        // Как только компонент загрузился см. жизненый цикл компонента nuxt.js
        mounted() {

        },
        // Методы, которые мы моржем вызывать Пример:  @click="sendForm()"
        methods: {
            // Обрабатываем данные формы
            sendForm() {
                // Блокировка повторного нажатия
                if (this.lockButton) {
                    return false;
                }

                this.isHaveError = {
                    login: false,
                    password: false
                };

                // Валидация, метод в утилитах /static/js/utilities.js
                if (!validate(this.login, '!empty')) {
                    this.isHaveError.login = 'Введите логин'; // TODO i18n
                }

                if (!validate(this.password, 'password')) {
                    this.isHaveError.password = 'Введите пароль'; // TODO i18n
                }


                // Если нет ошибок отправляем
                if (!this.isHaveError.email && !this.isHaveError.password ) {
                    this.lockButton = true; // Блокируем
                    this.doLogin();
                }
            },
            async doLogin() {
                try {
                    await this.$store.dispatch('login', {
                        username: this.login,
                        password: this.password
                    });

                    this.$root.$emit('setMessage', 'Вход выполнен', 'alert-success'); // TODO i18n
                    this.lockButton = false; // Разблокируем

                } catch (error) {

                    this.lockButton = false; // Разблокируе
                    console.log(error.response);
                    if(error.response) {
                        this.$root.$emit('setMessage', error.response.data.response.detail, 'alert-danger'); // TODO i18n
                    } else {
                        this.$root.$emit('setMessage', error, 'alert-danger'); // TODO i18n
                    }

                }


                /*
                this.$axios.post('/auth/login', {
                    username: this.login,
                    password: this.password
                })
                    .then((responses) => {
                        // TODO Сделать редирект на страницу профиля при успешной авторизаци
                        this.$root.$emit('setMessage', 'Вход выполнен', 'alert-success'); // TODO i18n
                        this.lockButton = false; // Разблокируем
                    })
                    .catch((error) => {

                        // TODO Отработать ошибку
                        this.lockButton = false; // Разблокируе
                        console.log(error.response);
                        if(error.response) {
                            this.$root.$emit('setMessage', error.response.data.response.detail, 'alert-danger'); // TODO i18n
                        } else {
                            this.$root.$emit('setMessage', error, 'alert-danger'); // TODO i18n
                        }
                    });
                  */
            }
        }
    }
</script>

<style>

</style>

