<template>
    <div class="container">
        <div class="tile is-ancestor">
            <div class="tile is-parent">
                <div class="tile is-child tabs">
                    <ul>
                        <li v-bind:class="{ 'is-active': isActive.annotation }"
                            v-on:click="toggleActive('annotation')">
                            <router-link :to="{name: 'newAnnotation'}">Annotation</router-link>
                        </li>
                        <li v-bind:class="{ 'is-active': isActive.evaluation }"
                            v-on:click="toggleActive('evaluation')">
                            <router-link :to="{name: 'newEvaluation'}">Evaluation</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="tile is-ancestor">
            <div class="tile is-parent is-5">
                <div class="tile is-child">
                    <router-view></router-view>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'NewProject',
  data() {
    return {
      isActive: {
        annotation: true,
        evaluation: false,
      },
    };
  },
  methods: {
    toggleActive(name) {
      if (name === 'annotation') {
        this.isActive.annotation = true;
        this.isActive.evaluation = false;
      } else if (name === 'evaluation') {
        this.isActive.evaluation = true;
        this.isActive.annotation = false;
      }
    },
  },
};
</script>

<style scoped>
</style>
