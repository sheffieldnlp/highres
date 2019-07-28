<template>
    <div class="container">
        <div class="content">
            <h3>Project {{ this.project_name }} Status</h3>
            <hr />
            <h5>Summary Group Name</h5>
        </div>
        <b-table :data="evaluation_results">
            <template slot-scope="props">
                <b-table-column field="no" label="No." width="40">
                    {{ props.row.no }}
                </b-table-column>
                <b-table-column field="name" label="Summary ID">
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

const axios = require('axios');

export default {
  name: 'EvaluationStatus',
  components: { BTableColumn, BTable },
  data() {
    return {
      evaluation_results: [],
      project_name: '',
      summ_group_name: '',
    };
  },
  methods: {
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
    axios.get(`project/progress/evaluation/${this.$route.params.project_id}`)
      .then((response) => {
        this.evaluation_results = response.data.systems;
        this.project_name = response.data.name;
        this.summ_group_name = response.data.summ_group_name;
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
