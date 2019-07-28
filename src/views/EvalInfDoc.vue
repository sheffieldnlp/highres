<template>
    <div class="container is-fluid home">
        <div class="columns" :style="{ display: display.landing }">
            <div class="column is-8 is-offset-2 box content">
                <component :is="dynamicLanding"></component>
                <div align="center">
                    <button class="button is-primary is-large"
                            style="margin-bottom: 2rem;margin-top: 2rem;"
                            v-on:click="closeLanding()">I consent
                    </button>
                </div>
            </div>
        </div>
        <div class="columns" :style="{ display: display.content }">
            <div class="column is-3">
                <div class="box instruction" :style="{ display: highlightDisplay }">
                    <div class="content">
                        <h1>
                            Instructions & Controls
                        </h1>
                        <!-- eslint-disable -->
                        <p class="my-text">
                            Your task is <strong>to assess the quality of the summary based on the document and its higlights</strong>. <br/> Hover the mouse on top of
                            <b-tooltip
                                    label="Nice!">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip> to see more information.
                        </p>
                        <hr>
                        <p class="my-text">Words that are important in the document have been highlighted using heatmap
                            coloring (<strong>Darker color signifies higher importance</strong>). You have to decide which importance level that signifies the informativeness of words.</p>
                        <p class="my-text">Use the slider to remove light color (less important highlights) by sliding it to the right. The number tells you how many color you can remove until there is only one color (the most important words) left.</p>
                    </div>
                    <div style="margin-bottom: 1.8rem; margin-top: 1.8rem; flex: 1;">
                        <vue-slider ref="slider" v-model="intensitySlider.value"
                                    v-bind="intensitySlider.options" v-if="show"
                                    v-on:input="onSliderInput"></vue-slider>
                    </div>
                </div>
                <div class="box instruction" :style="{ display: nonHighlightDisplay }">
                    <div class="content">
                        <h1>
                            Instructions & Controls
                        </h1>
                        <!-- eslint-disable -->
                        <p class="my-text">
                            Your task is <strong>to assess the quality of the summary based on the document</strong>.
                        </p>
                    </div>


                </div>
            </div>
            <div class="column">
                <div class="content" align="center">
                    <h2>Please don't refresh the page.</h2>
                </div>
                <div class="box document">
                    <div ref="document">
                    </div>
                </div>
            </div>
            <div class="column is-3">
                <div class="box summary">
                    <div class="content">
                        <h1>Assessment</h1>
                        <h5 class="my-header">Assess the following summary.</h5>
                        <p class="my-summary">{{ system_text }}</p>
                        <hr>
                        <h5 class="my-header">
                            <strong>How strongly agree are you on the following statements?</strong>
                        </h5>
                        <p class="my-text">
                            <b-tooltip
                                    label="Do the summary has all the important
                                     information of the document?">
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
                            <vue-slider v-model="recall"
                                        v-if="show" width="100%"></vue-slider>
                            </span>
                            <span class="level-right">
                                <label class="label is-small">Strongly <br/> agree</label>
                            </span>
                        </div>
                        <p class="my-text">
                            <b-tooltip
                                    label="Do the summary only has important
                                     information?">
                                <b-icon
                                    pack="fas"
                                    icon="info-circle"
                                    size="is-small">
                                </b-icon>
                            </b-tooltip>
                            <strong>Only important</strong> information is in the summary.
                        </p>
                        <div class="level" align="center" style="margin-bottom: 1.8rem; margin-top: 1.8rem;">
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
import Word from '@/components/Component/Word.vue';
import Char from '@/components/Component/Char.vue';
import LineBreaker from '@/components/Component/LineBreaker.vue';
import LandingInfDoc from '@/components/Landing/LandingInfDoc.vue';
import LandingInfDocMTurk from '@/components/LandingMTurk/LandingInfDoc.vue';
import LandingInfDocNoMTurk from '@/components/LandingMTurk/LandingInfDocNo.vue';
import Vue from 'vue';
import vueSlider from 'vue-slider-component';
import BRadio from 'buefy/src/components/radio/Radio.vue';
import BTooltip from 'buefy/src/components/tooltip/Tooltip.vue';
import BIcon from 'buefy/src/components/icon/Icon.vue';
// const randomColor = require('randomcolor');
const axios = require('axios');

const waitTimeForButton = 30;

window.onbeforeunload = () => 'Are you sure you want leave?';

function createAndMountWord(sent, token, wordIndex) {
  const WordClass = Vue.extend(Word);
  let aWord = token.word;
  if (aWord === '-LRB-') {
    aWord = '(';
  } else if (aWord === '-RRB-') {
    aWord = ')';
  } else if (aWord === '``') {
    aWord = '"';
  } else if (aWord === '\'\'') {
    aWord = '"';
  }
  const word = new WordClass({
    propsData: {
      sentIndex: sent.index,
      tokenIndex: token.index,
      word: aWord,
      index: wordIndex,
      compIndex: this.components.length,
      type: 'word',
    },
  });
  word.$mount();
  this.components.push(word);
  this.words[wordIndex] = word;
  this.words2Groups[wordIndex] = [];
  this.$refs.document.appendChild(word.$el);
}

function createAndMountWhitespace(whitespace, whitespaceIndex) {
  const CharClass = Vue.extend(Char);
  const char = new CharClass({
    propsData: {
      bgColor: '#ffffff',
      type: 'whitespace',
      index: whitespaceIndex,
      compIndex: this.components.length,
    },
  });
  char.$slots.default = [whitespace];
  char.$mount();
  this.components.push(char);
  this.whitespaces[whitespaceIndex] = char;
  this.whitespaces2Groups[whitespaceIndex] = [];
  this.$refs.document.appendChild(char.$el);
}

function createAndMountLineBreaker() {
  const LineBreakerClass = Vue.extend(LineBreaker);
  const lineBreaker = new LineBreakerClass();
  lineBreaker.$mount();
  this.$refs.document.appendChild(lineBreaker.$el);
}

function redrawHighlight() {
  this.slidersValue.push(this.intensitySlider.value);
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    const index = parseInt(Object.keys(this.highlight.intensities)[i], 10);
    const intensity = this.highlight.intensities[Object.keys(this.highlight.intensities)[i]];
    let low = 0;
    if (this.highlight.max !== this.highlight.min) {
      low = 1 - ((this.intensitySlider.value - this.highlight.min) /
        (this.highlight.max - this.highlight.min));
    }
    if (intensity >= low) {
      this.components[index].highlight(`rgba(255, ${255 - (intensity * 255)}, 0)`);
    } else {
      this.components[index].rmHighlight();
    }
  }
}

function getIntensities(results) {
  for (let i = 0; i < Object.keys(results).length; i += 1) {
    const result = results[Object.keys(results)[i]];
    for (let j = 0; j < Object.keys(result.highlights).length; j += 1) {
      const highlight = result.highlights[Object.keys(result.highlights)[j]];
      for (let k = 0; k < highlight.indexes.length; k += 1) {
        if ((highlight.indexes[k] in this.highlight.intensities)) {
          this.highlight.intensities[highlight.indexes[k]] += 1;
        } else {
          this.highlight.intensities[highlight.indexes[k]] = 1;
        }
        if (this.highlight.intensities[highlight.indexes[k]] > this.highlight.max) {
          this.highlight.max = this.highlight.intensities[highlight.indexes[k]];
        }
        if (this.highlight.intensities[highlight.indexes[k]] < this.highlight.min) {
          this.highlight.min = this.highlight.intensities[highlight.indexes[k]];
        }
      }
    }
  }
  for (let i = 0; i < Object.keys(this.highlight.intensities).length; i += 1) {
    const intensity = this.highlight.intensities[Object.keys(this.highlight.intensities)[i]];
    let normIntensity = 0;
    if (this.highlight.max !== this.highlight.min) {
      normIntensity = (intensity - this.highlight.min) /
        (this.highlight.max - this.highlight.min);
    }
    this.highlight.intensities[Object.keys(this.highlight.intensities)[i]] = normIntensity;
  }
  // Slider setting
  for (let i = this.highlight.min; i <= this.highlight.max; i += 1) {
    this.intensitySlider.options.data.push(i);
  }
  this.intensitySlider.max = this.highlight.max;
  this.intensitySlider.min = this.highlight.min;
  this.intensitySlider.value = this.highlight.max;
}

function parseDoc(textJSON) {
  if (this.is_highlight === '1') {
    getIntensities.call(this, textJSON.results);
  }
  let wordIndex = 0;
  let whitespaceIndex = 0;
  const { endSentIndex } = textJSON.paragraph;
  for (let i = 0; i < textJSON.sentences.length; i += 1) {
    const sent = textJSON.sentences[i];
    for (let j = 0; j < sent.tokens.length; j += 1) {
      const token = sent.tokens[j];
      createAndMountWord.call(this, sent, token, wordIndex);
      // check is last element
      if (j !== sent.tokens.length - 2) {
        createAndMountWhitespace.call(this, ' ', whitespaceIndex);
        whitespaceIndex += 1;
      }
      wordIndex += 1;
    }
    if (endSentIndex.includes(sent.index + 1)) {
      createAndMountLineBreaker.call(this);
    }
  }
}

function getFile() {
  axios.get(`project/evaluation/informativeness_doc/${this.project_id}/single_doc`)
    .then((response) => {
      parseDoc.call(this, response.data.doc_json);
      this.system_text = response.data.system_text;
      this.summ_status_id = response.data.summ_status_id;
      this.turkCode = response.data.turk_code;
      this.sanity_statement = response.data.sanity_statement;
      this.sanity_answer = response.data.sanity_answer;
      redrawHighlight.call(this);
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
  name: 'EvalInfDoc',
  components: {
    BIcon,
    BTooltip,
    BRadio,
    vueSlider,
    LandingInfDoc,
    LandingInfDocMTurk,
    LandingInfDocNoMTurk,
  },
  computed: {
    nonHighlightDisplay() {
      if (this.is_highlight === '0') {
        return 'block';
      }
      return 'none';
    },
    highlightDisplay() {
      if (this.is_highlight === '1') {
        return 'block';
      }
      return 'none';
    },
    mTurkDisplay() {
      if (this.is_mturk === '0') {
        return 'block';
      }
      return 'none';
    },
    testPrompt() {
      const prompt = 'Is the statement below is True or False?';
      return `${prompt}<blockquote>${this.sanity_statement}</blockquote>`;
    },
    dynamicLanding() {
      if (this.is_mturk === '0') {
        return 'LandingInfDoc';
      }
      if (this.is_highlight === '1') {
        return 'LandingInfDocMTurk';
      }
      return 'LandingInfDocNoMTurk';
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
  methods: {
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
      this.start_time = new Date().getTime();
    },
    onSliderInput() {
      redrawHighlight.call(this);
    },
    showTest() {
      this.display.landing = 'none';
      this.display.content = 'none';
      this.display.message = 'none';
      this.display.test = 'flex';
    },
    saveEvaluation() {
      const resultJSON = {
        project_id: this.project_id,
        status_id: this.summ_status_id,
        precision: this.precision,
        recall: this.recall,
        category: 'Informativeness_Doc',
        sliderMax: this.intensitySlider.max,
        sliderMin: this.intensitySlider.min,
        sliderValues: this.slidersValue.join(),
        email: this.email,
        result_id: this.result_id,
        opening_time: this.start_time,
        finished_time: new Date().getTime(),
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
  data() {
    return {
      start_time: 0,
      highlight: {
        intensities: {},
        max: -1,
        min: 999,
      },
      is_mturk: this.$route.params.mturk,
      is_highlight: this.$route.params.highlight,
      show: false,
      timer: {
        now: Math.trunc(new Date().getTime() / 1000),
        date: Math.trunc(new Date().getTime() / 1000),
        isRunning: true,
        timer: null,
      },
      intensitySlider: {
        value: 0,
        options: {
          tooltip: 'always',
          data: [],
          speed: 0.3,
          min: 1,
          max: 0,
          piecewiseLabel: true,
          piecewise: true,
          reverse: true,
        },
      },
      display: {
        content: 'none',
        landing: 'flex',
        message: 'none',
        test: 'none',
      },
      components: [],
      // A collection of Word components
      words: {},
      // A collection of Char components
      whitespaces: {},
      // A mapping of whitespace index to group index
      whitespaces2Groups: {},
      // A mapping of word index to group index
      words2Groups: {},
      precision: 50,
      recall: 50,
      project_id: this.$route.params.project_id,
      summ_status_id: '',
      system_text: '',
      message: '',
      slidersValue: [],
      sanity_statement: '',
      radio: '',
      sanity_answer: '',
      email: '',
    };
  },
  mounted: function onMounted() {
    getFile.call(this);
    this.timer.timer = window.setInterval(() => {
      this.timer.now = Math.trunc((new Date()).getTime() / 1000);
    }, 1000);
  },
};
</script>

<style scoped>
.content li + li {
  margin: 0;
}
.document {
  font-family: 'Lora', serif;
  font-size: 1.2rem;
  line-height: 1.5rem;
}
.summary {
  position: sticky;
  position: -webkit-sticky;
  top: 70px;
}
.instruction {
  position: sticky;
  position: -webkit-sticky;
  top: 70px;
}
.my-header {
  font-size: 1.1rem;
}
.my-text {
    font-size: 0.9rem;
}
.my-summary{
    font-size: 1.1rem;
}
.home {
    padding-top: 25px;
}
</style>
