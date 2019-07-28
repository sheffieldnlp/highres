<template>
  <div class="container home">
        <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <LandingFluency></LandingFluency>
                <div align="center">
                    <button class="button is-primary is-large" style="margin-bottom: 2rem"
                    v-on:click="closeLanding()">I consent</button>
                </div>
            </div>
        </div>
        <div class="columns" :style="{ display: display.content }">
            <div class="column is-5 is-offset-3">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Assess the following summary</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                        <strong>How strongly agree are you on the following statements?</strong>
                        </h5>
                        <p class="my-text">
                            The summary is <strong>fluent</strong>.
                            <b-tooltip
                                    label="E.g. are there any grammatical mistakes?
                                    are the sentence sounds natural?">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip>
                        </p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                            <vue-slider min="1" max="100" v-model="fluency"
                                        v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <p class="my-text">
                            The summary is <strong>clear</strong>.
                            <b-tooltip
                                    label="E.g. are nouns, pronouns or personal
                                    names well-specified?">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip>
                        </p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                            <vue-slider min="1" max="100" v-model="clarity"
                                        v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <button class="button is-primary" :disabled="timer.isRunning"
                    v-on:click="saveEvaluation()">{{ timenow }}</button>
                    </div>
                </div>
            </div>
            <!-- eslint-enable -->
        </div>
        <div class="columns" :style="{ display: display.message }">
            <div class="column is-8 is-offset-2 box content">
                <div align="center">
                    <h1>{{ message }}</h1>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import LandingFluency from '@/components/Landing/LandingFluency.vue';
import vueSlider from 'vue-slider-component';

const axios = require('axios');

const waitTimeForButton = 5;

function getFile() {
  axios.get(`project/evaluation/fluency/${this.project_id}/single_doc`)
    .then((response) => {
      this.system_text = response.data.system_text;
      this.ref_text = response.data.ref_text;
      this.summ_status_id = response.data.summ_status_id;
    })
    .catch(() => {
      this.showMessage('There are no more documents available!');
    });
}

function sendResult(resultJSON) {
  axios.post('project/save_result/evaluation', resultJSON)
    .then(() => {
      this.$toast.open({
        message: 'Submission successful.',
        type: 'is-success',
      });
      this.showMessage('Thank you for submitting!');
    })
    .catch((error) => {
      this.$toast.open({
        message: `${error}`,
        type: 'is-danger',
      });
    });
}

export default {
  components: {
    LandingFluency,
    vueSlider,
  },
  data() {
    return {
      show: false,
      system_text: '',
      ref_text: '',
      fluency: 50,
      clarity: 50,
      project_id: this.$route.params.project_id,
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
      is_landing: true,
      display: {
        content: 'none',
        landing: 'flex',
        message: 'none',
      },
      message: '',
    };
  },
  methods: {
    showMessage(message) {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'flex';
      this.message = message;
    },
    closeLanding() {
      this.display.content = 'flex';
      this.display.landing = 'none';
      window.scrollTo(0, 0);
      this.show = true;
    },
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        fluency: this.fluency,
        clarity: this.clarity,
        category: 'fluency',
      };
      sendResult.call(this, resultJSON);
    },
  },
  computed: {
    timenow() {
      if (this.timer.isRunning === true) {
        if ((this.timer.now - this.timer.date) < waitTimeForButton) {
          return `Wait ${waitTimeForButton - (this.timer.now - this.timer.date)} seconds`;
        }
        // eslint-disable-next-line
        this.timer.isRunning = false;
        window.clearInterval(this.timer.timer);
      }
      return 'Click to submit';
    },
  },
  mounted: function onMounted() {
    getFile.call(this);
    this.timer.timer = window.setInterval(() => {
      this.timer.now = Math.trunc((new Date()).getTime() / 1000);
    }, 1000);
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
