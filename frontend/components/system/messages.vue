<template>
  <div class="messages">
    <Message v-for="message of messages" v-bind:key="message.id" :message="message"/>
  </div>
</template>

<script>
    import Message from "~/components/system/message";

    export default {
        name: "messages",
        data: () => {
            return {
                messages: []
            }
        },
        components: {
            Message
        },
        mounted() {
            let self = this;
            this.$root.$on('setMessage', function (message, className, header = false) {
                if(!className || !message) {
                    return false;
                }
                const dt = new Date();
                self.messages.push({
                    id: dt.getTime(),
                    messageClass : className,
                    messageText: message,
                    messageHeader: header
                });

                return true;
            })
        }
    }
</script>

<style lang="css">
  .messages {
    position: absolute;
    top: 20px;
    left: 20px;
    max-width: 400px;
  }
</style>
