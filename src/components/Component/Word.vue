<template>
    <span ref="word" v-bind:data-type="type" v-bind:data-index="index"></span>
</template>
<script>
import Char from '@/components/Component/Char.vue';
import Vue from 'vue';

const CharClass = Vue.extend(Char);

export default {
  name: 'Word',
  props: ['index', 'sentIndex', 'tokenIndex', 'word', 'type', 'isSource', 'compIndex'],
  data() {
    return {
      chars: [],
    };
  },
  methods: {
    getTokensLength() {
      return this.chars.length;
    },
    annotate() {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle.color = '#ff00ff';
        this.chars[idx].$data.charStyle['font-weight'] = 'bold';
      });
    },
    resetAnnotation() {
      if (this.isSource) {
        this.chars.forEach((char, idx) => {
          this.chars[idx].$data.charStyle.color = '#3878E5';
          this.chars[idx].$data.charStyle.cursor = 'pointer';
          this.chars[idx].$data.charStyle['font-weight'] = 'bold';
        });
      } else {
        this.chars.forEach((char, idx) => {
          this.chars[idx].$data.charStyle.color = '#000000';
          this.chars[idx].$data.charStyle.cursor = 'text';
          this.chars[idx].$data.charStyle['font-weight'] = 'normal';
        });
      }
    },
    highlight(color, opacity = 1.0) {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle['background-color'] = color;
        this.chars[idx].$data.charStyle.opacity = opacity;
      });
    },
    rmHighlight() {
      this.chars.forEach((char, idx) => {
        this.chars[idx].$data.charStyle['background-color'] = '#ffffff';
        this.chars[idx].$data.charStyle.opacity = 1.0;
      });
    },
  },
  mounted: function onMounted() {
    for (let i = 0; i < this.word.length; i += 1) {
      let fgColor = '#000000';
      let fontWeight = 'normal';
      let cursor = 'text';
      if (this.isSource === true) {
        fgColor = '#3878E5';
        fontWeight = 'bold';
        cursor = 'pointer';
      }
      const char = new CharClass({
        propsData: {
          index: this.index,
          bgColor: '#ffffff',
          fgColor,
          fontWeight,
          type: 'char',
          cursor,
        },
      });
      char.$slots.default = [this.word[i]];
      this.chars.push(char);
      char.$mount();
      this.$refs.word.appendChild(char.$el);
    }
  },
};
</script>

<style scoped>

</style>
