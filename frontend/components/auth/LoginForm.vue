<template>
  <div class="login">
    <form>
      <h3>Sign-up</h3>
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
      <button type="submit" class="btn btn-primary">Sign up</button>
      <div class="p-2">
        <nuxt-link no-prefetch to="/users/sign-in/registration/">or registration</nuxt-link>
      </div>
    </form>
  </div>
</template>

<style>

</style>

