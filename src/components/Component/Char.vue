<template>
    <span :style="charStyle" v-bind:data-type="type"
          v-bind:data-index="index"><slot></slot></span>
</template>

<script>
export default {
  name: 'Char',
  props: ['index', 'fgColor', 'bgColor', 'type', 'fontWeight', 'cursor', 'compIndex'],
  data() {
    return {
      charStyle: {
        'background-color': this.bgColor,
        color: this.fgColor,
        'font-weight': this.fontWeight,
        cursor: this.cursor,
      },
    };
  },
  methods: {
    highlight(color, opacity = 1.0) {
      this.charStyle['background-color'] = color;
      this.charStyle.opacity = opacity;
    },
    rmHighlight() {
      this.charStyle['background-color'] = '#ffffff';
      this.charStyle.opacity = 1.0;
    },
  },

};
</script>

<style scoped>

</style>
