<template>
  <div class="alert" v-bind:class="message.messageClass" role="alert">
    <h4 v-if="message.messageHeader" class="alert-heading">{{ message.messageHeader }}</h4>
    {{ message.messageText }}
  </div>
</template>

<script>
    export default {
        name: "message",
        data: () => {
            return {
                lifeTime: 5000
            }
        },
        props: [
            'message'
        ],
        mounted() {
          setTimeout(() => {
              this.close();
          }, this.lifeTime)
        },
        methods: {
            close () {
                this.$destroy();
                this.$el.parentNode.removeChild(this.$el);
            }
        }
    }
</script>

<style scoped>

</style>
