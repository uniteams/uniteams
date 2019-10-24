<template>
  <div class="container">

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Uniteams</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <nuxt-link no-prefetch to="/" active-class="active" class="nav-link" exact>Home</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link no-prefetch to="/users/sign-in" active-class="active"  class="nav-link">Sign-up</nuxt-link>
          </li>
          <li class="nav-item">
            <nuxt-link no-prefetch to="/company/" active-class="active"  class="nav-link">Company</nuxt-link>
          </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>

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

