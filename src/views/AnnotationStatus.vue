<template>
    <div class="container">
        <div class="content">
            <h3>Project {{ $route.params.project_id }} Status
                <button v-on:click="update" class="button is-primary is-small">
                    <b-icon
                    pack="fas"
                    icon="sync-alt">
                    </b-icon>
                </button>
            </h3>
        </div>
        <b-table :data="annotation_results">
            <template slot-scope="props">
                <b-table-column field="no" label="No." width="40">
                    {{ props.row.no }}
                </b-table-column>
                <b-table-column field="name" label="Document Name">
                    {{ props.row.name }}
                </b-table-column>
                <b-table-column field="progress" label="Progress">
                    <div class="columns level">
                        <div class="column is-10 level-item">
                            <progress
                                class="progress is-success"
                                :value="props.row.progress" max="1">
                            </progress>
                        </div>
                        <div class="column is-2 level-item">
                            {{
                              props.row.progress
                              .toLocaleString(
                                "en",
                                {style: "percent", maximumSignificantDigits: 2},
                              )
                            }}
                        </div>
                    </div>
                </b-table-column>
                <template slot="empty">
                    <section class="section">
                        <div class="content has-text-grey has-text-centered">
                            <p>
                                <b-icon
                                    icon="frown"
                                    pack="fas"
                                    size="is-large">
                                </b-icon>
                            </p>
                            <p>There is no result.</p>
                        </div>
                    </section>
                </template>
            </template>
        </b-table>
    </div>
</template>

<script>
import BTable from 'buefy/src/components/table/Table.vue';
import BTableColumn from 'buefy/src/components/table/TableColumn.vue';
import BIcon from 'buefy/src/components/icon/Icon.vue';

const axios = require('axios');

export default {
  name: 'AnnotatingStatus',
  components: { BIcon, BTableColumn, BTable },
  data() {
    return {
      annotation_results: [],
    };
  },
  methods: {
    update() {
      axios.get(`project/progress/annotation/${this.$route.params.project_id}`)
        .then((response) => {
          this.annotation_results = response.data.documents;
        })
        .catch((error) => {
          this.$toast.open({
            message: `${error}`,
            type: 'is-danger',
          });
        });
    },
    export_result(id) {
      axios.post(`project/${id}/close`)
        .then(() => {
          this.$toast.open({
            message: `Project ${id} has been closed`,
            type: 'is-success',
          });
          this.$router.push({ name: 'manage' });
        })
        .catch((error) => {
          this.$toast.open({
            message: `${error}`,
            type: 'is-danger',
          });
        });
    },
  },
  beforeCreate() {
    axios.get(`project/progress/annotation/${this.$route.params.project_id}`)
      .then((response) => {
        this.annotation_results = response.data.documents;
      })
      .catch((error) => {
        this.$toast.open({
          message: `${error}`,
          type: 'is-danger',
        });
      });
  },
};
</script>

<style scoped>

</style>
