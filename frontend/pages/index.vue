<template>
  <section class="container">
    <div>
      <app-logo/>
      <h1 class="title">
        Welcome to uniteams APP
      </h1>
      <nuxt-link no-prefetch to="/second-page">Next page</nuxt-link>
      <nuxt-link no-prefetch to="/users/sign-in">Sign-in</nuxt-link>
    </div>
  </section>
</template>

<script>
import AppLogo from '~/components/AppLogo.vue'

export default {
  components: {
    AppLogo
  }
}
</script>

<style>
.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}
</style>

