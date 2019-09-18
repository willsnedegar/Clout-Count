<template>
  <div>
    <b-navbar toggleable="sm" type="light" variant="light" class="mb-3">
      <b-navbar-toggle target="nav-text-collapse"></b-navbar-toggle>

      <b-navbar-brand>Social Media Rankings</b-navbar-brand>

      <b-collapse id="nav-text-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item style="" href="#">Regular People</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-text>By Will Snedegar</b-nav-text>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div class='container-fluid'>
      <router-view></router-view>
    </div>

  </div>
</template>

<script>

export default {
  name: 'DefaultContainer',
}
</script>
