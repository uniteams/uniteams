<template>
  <div class="d-flex justify-content-center p-5">
    <RegistrationForm/>
  </div>
</template>

<script>
    import RegistrationForm from '~/components/auth/RegistrationForm.vue'
    export default {
        name: "registration",
         components: {
             RegistrationForm
         }
    }
</script>

<style scoped>

</style>
