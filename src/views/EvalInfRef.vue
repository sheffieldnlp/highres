<template>
  <div class="container home">
        <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <component :is="dynamicLanding"></component>
                <div align="center">
                    <button class="button is-primary is-large" style="margin-bottom: 2rem"
                    v-on:click="closeLanding()">I consent</button>
                </div>
            </div>
        </div>
        <div class="columns" :style="{ display: display.content }">
            <div class="column is-5 is-offset-1">
                <div class="content" align="center">
                    <h2>Please don't refresh the page.</h2>
                </div>
                <div class="box document">
                    <div class="content">
                        <h1>Reference Sentence</h1>
                        <p class="my-summary">{{ ref_text }}</p>
                    </div>
                </div>
            </div>
            <div class="column is-5">

                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Assess the following summary.</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                        <strong>How strongly agree are you on the following statements?</strong>
                        </h5>
                        <p>
                            Hover the mouse on top of the
                            <b-tooltip
                                    label="You should treat that all words
                                    in the reference sentence as important,
                                    and words that don't appear in reference as not important.">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip> to see more information.
                        </p>
                        <p class="my-text">
                            <b-tooltip
                                    label="Do the summary has all the important
                                     information of the reference sentence?">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip>
                            <strong>All important</strong> information is present in the summary
                        </p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                            <vue-slider min="1" max="100" v-model="recall"
                                        v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <p class="my-text">
                            <b-tooltip
                                    label="Do the summary only has important
                                     information (in accordance to reference)?">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip>
                            <strong>Only important</strong> information is in the summary.</p>
                        <div class="level" align="center"
                             style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
                            <span class="level-left">
                                <label class="label is-small">Strongly <br/> disagree</label>
                            </span>
                            <span class="level-item">
                           <vue-slider min="1" max="100" v-model="precision"
                                       v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <div align="center">
                            <button class="button is-primary" :disabled="timer.isRunning"
                                    v-on:click="showTest">{{ timenow }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- eslint-enable -->
        </div>
        <div class="columns" :style="{ display: display.message }">
            <div class="column is-8 is-offset-2 box content">
                <div align="center" v-html="message">
                </div>
            </div>
        </div>
      <div class="columns" :style="{ display: display.test }">
            <div class="column is-8 is-offset-2 box content">
                <div align="center">
                    <h3>Please Answer the Following Question</h3>
                    <div v-html="testPrompt">
                    </div>
                    <div class="block">
                        <b-radio v-model="radio"
                                 native-value="True">
                            True
                        </b-radio>
                        <b-radio v-model="radio"
                                 native-value="False">
                            False
                        </b-radio>
                    </div>
                    <hr/>
                    <div :style="{ display: mTurkDisplay }">
                        <p>
                            Please enter an email to be included in a lucky draw
                            or leave it blank to opt out:
                        </p>
                        <b-field>
                            <b-input v-model="email"
                                     placeholder="Your email"
                                     icon-pack="fas"
                                     icon="envelope" style="width: 250px;"></b-input>
                        </b-field>
                    </div>
                    <div style="margin-top: 5px;">
                        <button class="button is-primary"
                                v-on:click="saveEvaluation">
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
// @ is an alias to /src
import LandingInfRef from '@/components/Landing/LandingInfRef.vue';
import LandingInfRefMTurk from '@/components/LandingMTurk/LandingInfRef.vue';
import vueSlider from 'vue-slider-component';
import BRadio from 'buefy/src/components/radio/Radio.vue';
import BTooltip from 'buefy/src/components/tooltip/Tooltip.vue';
import BIcon from 'buefy/src/components/icon/Icon.vue';

const axios = require('axios');

const waitTimeForButton = 30;

window.onbeforeunload = () => 'Are you sure you want leave?';

function getFile() {
  axios.get(`project/evaluation/informativeness_ref/${this.project_id}/single_doc`)
    .then((response) => {
      this.system_text = response.data.system_text;
      this.ref_text = response.data.ref_text;
      this.summ_status_id = response.data.summ_status_id;
      this.turkCode = response.data.turk_code;
      this.sanity_statement = response.data.sanity_statement;
      this.sanity_answer = response.data.sanity_answer;
    })
    .catch(() => {
      this.showMessage('Server is busy! Please wait 3 minutes and refresh!');
    });
}

function sendResult(resultJSON) {
  axios.post('project/save_result/evaluation', resultJSON)
    .then(() => {
      this.$toast.open({
        message: 'Submission successful.',
        type: 'is-success',
      });
      let text = '';
      if (this.is_mturk === '1') {
        text = '<p>Please enter this code:</p>' +
              `<blockquote>${this.turkCode}</blockquote>`;
      } else {
        text = '<p>Please refresh the page to do another highlighting. ' +
          'You need to do at least twice to be eligible for the lucky draw.</p>';
      }
      this.showMessage(`<h3>Thank you for submitting!</h3><br/> ${text}`);
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
    BIcon,
    BTooltip,
    BRadio,
    LandingInfRef,
    LandingInfRefMTurk,
    vueSlider,
  },
  data() {
    return {
      is_mturk: this.$route.params.mturk,
      show: false,
      system_text: '',
      ref_text: '',
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
      precision: 50,
      recall: 50,
      project_id: this.$route.params.project_id,
      summ_status_id: '',
      display: {
        content: 'none',
        landing: 'block',
        message: 'none',
        test: 'none',
      },
      message: '',
      email: '',
      turkCode: '',
      radio: '',
      sanity_statement: '',
      sanity_answer: '',
    };
  },
  methods: {
    showTest() {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'none';
      this.display.test = 'flex';
    },
    showMessage(message) {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'flex';
      this.display.test = 'none';
      this.message = message;
    },
    closeLanding() {
      this.display.content = 'flex';
      this.display.landing = 'none';
      window.scrollTo(0, 0);
      this.show = true;
      axios.get(`result/evaluation/${this.summ_status_id}`)
        .then((response) => {
          this.result_id = response.data.result_id;
        });
    },
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        precision: this.precision,
        recall: this.recall,
        category: 'Informativeness_Ref',
        mturk_code: '',
        email: this.email,
        result_id: this.result_id,
      };
      if (this.is_mturk === '1') {
        resultJSON.mturk_code = this.turkCode;
      } else {
        resultJSON.mturk_code = null;
      }
      if (this.radio === '') {
        resultJSON.validity = false;
      } else if ((this.radio === 'True') === this.sanity_answer) {
        resultJSON.validity = true;
      } else {
        resultJSON.validity = false;
      }
      sendResult.call(this, resultJSON);
    },
  },
  computed: {
    testPrompt() {
      const prompt = 'Is the statement below is True or False?';
      return `${prompt}<blockquote>${this.sanity_statement}</blockquote>`;
    },
    dynamicLanding() {
      if (this.is_mturk === '0') {
        return 'LandingInfRef';
      }
      return 'LandingInfRefMTurk';
    },
    mTurkDisplay() {
      if (this.is_mturk === '0') {
        return 'block';
      }
      return 'none';
    },
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
