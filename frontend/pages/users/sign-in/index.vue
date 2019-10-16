<template>
      <div class="d-flex justify-content-center p-5">
          <LoginForm></LoginForm>
      </div>
</template>

<script>
    import LoginForm from '~/components/auth/LoginForm.vue'
    export default {
        name: "index",
        components: {
            LoginForm
        }
    }
</script>

<style scoped>

</style>
