<template>
  <div class="clearfix">
    <router-view/>
  </div>
</template>
<style lang="scss">
@mixin clearfix() {
  &::after {
    display: block;
    content: "";
    clear: both;
  }
}

// Usage as a mixin
.element {
  @include clearfix;
}
</style>
