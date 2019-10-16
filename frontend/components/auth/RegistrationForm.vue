<template>
  <form>
    <h3>Registration</h3>
    <div class="form-group">
      <label for="exampleInputEmail1">Email address</label>
      <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"
             placeholder="Enter email">
      <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
    </div>
    <div class="form-group">
      <label for="exampleInputPassword1">Password</label>
      <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">
    </div>
    <div class="form-group">
      <label for="exampleInputPassword2">Retry password</label>
      <input type="password" class="form-control" id="exampleInputPassword2" placeholder="Retry password">
    </div>

    <small class="form-text text-muted">More fields you need... </small>

    <button type="submit" class="btn btn-primary">Registration</button>

    <div class="p-2">
      <nuxt-link no-prefetch to="/users/sign-in/">or sign-up</nuxt-link>
    </div>
  </form>
</template>

<script>

    export default {
        name: "RegistrationForm",

    }
</script>

<style scoped>

</style>
