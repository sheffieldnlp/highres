<template>
    <div class="container">
        <div class="content">
            <h3>Annotation Projects</h3>
        </div>
        <div>
            <b-table :data="annotation_projects">
                <template slot-scope="props">
                    <b-table-column field="no" label="No." width="40">
                        {{ props.row.no }}
                    </b-table-column>
                    <b-table-column field="id" label="ID" width="40">
                        {{ props.row.id }}
                    </b-table-column>
                    <b-table-column field="name" label="Name">
                        <a :href="'/#/admin/annotation_status/' + props.row.id">
                            {{ props.row.name }}
                        </a>
                    </b-table-column>
                    <b-table-column field="category" label="Category">
                        {{ props.row.category }}
                    </b-table-column>
                    <b-table-column field="dataset_name" label="Dataset">
                        {{ props.row.dataset_name }}
                    </b-table-column>
                    <b-table-column field="created_at"
                                    label="Created at" centered>
                        {{ new Date(props.row.created_at).toLocaleDateString() }}
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
                    <b-table-column label="Link for Participants">
                        <b-field>
                            <b-input icon-pack="fas" icon="link"
                                :value="props.row.link"
                                readonly size="is-small">
                            </b-input>
                            <!--<p class="control">-->
                                <!--<button size="icon is-small is-primary">-->
                                    <!--<i class="fas fa-clipboard"></i>-->
                                <!--</button>-->
                            <!--</p>-->
                        </b-field>
                    </b-table-column>
                    <b-table-column field="id" label="Close Project">
                        <a class="button is-danger is-outlined is-small"
                           v-on:click="close_project(props.row.id)">
                            <span>Close And Save</span>
                            <span class="icon is-small">
                                <i class="fas fa-times"></i>
                            </span>
                        </a>
                    </b-table-column>
                </template>
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
                            <p>There is no active annotation project in database.</p>
                        </div>
                    </section>
                </template>
            </b-table>
        </div>
        <hr>
        <div class="content">
            <h3>Evaluation Projects</h3>
        </div>
        <div>
            <b-table :data="evaluation_projects" striped="true">
                <template slot-scope="props">
                    <b-table-column field="no" label="No." width="40">
                        {{ props.row.no }}
                    </b-table-column>
                    <b-table-column field="id" label="ID" width="40">
                        {{ props.row.id }}
                    </b-table-column>
                    <b-table-column field="name" label="Name" width="100">
                        <a :href="'/#/admin/evaluation_status/' + props.row.id">
                        {{ props.row.name }}
                        </a>
                    </b-table-column>
                    <b-table-column field="category" label="Category">
                        {{ props.row.category }}
                    </b-table-column>
                    <b-table-column field="dataset_name" label="Dataset">
                        {{ props.row.dataset_name }}
                    </b-table-column>
                    <b-table-column field="summ_group_name" label="Summary Group" width="100">
                        {{ props.row.summ_group_name }}
                    </b-table-column>
                    <b-table-column field="created_at"
                                    label="Created at" centered>
                        {{ new Date(props.row.created_at).toLocaleDateString() }}
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
                    <b-table-column label="Link for Participants">
                        <b-field>
                            <b-input icon-pack="fas" icon="link"
                                :value="props.row.link"
                                readonly size="is-small">
                            </b-input>
                            <!--<p class="control">-->
                                <!--<button size="icon is-small is-primary">-->
                                    <!--<i class="fas fa-clipboard"></i>-->
                                <!--</button>-->
                            <!--</p>-->
                        </b-field>
                    </b-table-column>
                    <b-table-column field="id" label="Close Project">
                        <a class="button is-danger is-outlined is-small"
                           v-on:click="close_project(props.row.id)">
                            <span>Close</span>
                            <span class="icon is-small">
                                <i class="fas fa-times"></i>
                            </span>
                        </a>
                    </b-table-column>
                </template>
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
                            <p>There is no active evaluation project in database.</p>
                        </div>
                    </section>
            </template>
            </b-table>
        </div>
    </div>
</template>

<script>
import BTable from 'buefy/src/components/table/Table.vue';
import BTableColumn from 'buefy/src/components/table/TableColumn.vue';

const axios = require('axios');

export default {
  name: 'ManageProject',
  components: { BTableColumn, BTable },
  data() {
    return {
      annotation_projects: [],
      evaluation_projects: [],
    };
  },
  methods: {
    get_progress() {
      axios.get('project/all_progress/annotation')
        .then((response) => {
          this.annotation_projects = response.data.projects;
        });
      axios.get('project/all_progress/evaluation')
        .then((response) => {
          this.evaluation_projects = response.data.projects;
        });
    },
    close_project(id) {
      this.$dialog.confirm({
        message: `Do you want to close project ${id}?`,
        onConfirm: () => {
          axios.post(`project/${id}/close`)
            .then(() => {
              this.$toast.open({
                message: `Project ${id} has been closed`,
                type: 'is-success',
              });
              this.get_progress();
            })
            .catch((error) => {
              this.$toast.open({
                message: `${error}`,
                type: 'is-danger',
              });
            });
        },
      });
    },
  },
  beforeMount() {
    this.get_progress();
  },
};
</script>

<style scoped>
progress {
    display: inline;
    width: 80%;
}
</style>
