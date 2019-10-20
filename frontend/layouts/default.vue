<template>
  <div class="container">
    <Messages/>
    <nuxt/>
  </div>
</template>

<script>
  import Messages from "~/components/system/messages";

  export  default {
      name : "default",
      components: {
          Messages
      }
  }
</script>

<style>

</style>

