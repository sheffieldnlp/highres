#%%
'''
Calculate the length of evaluation samples
'''

import pandas as pd
from flask_sqlalchemy import SQLAlchemy

from backend.models import Dataset, Document, Summary, SummaryGroup, EvaluationResult, SummaryStatus, EvaluationProject
from backend.app import create_app

#%%
# Loading data from database
summary_name = 'BBC_Sample_system_ptgen'
project_name = 'Inf Doc T_Convs2s Highlight Sample '
# summary_name = 'BBC_system_tconvs2s'
# summary_name = 'BBC_ref_gold'
app = create_app()
db = SQLAlchemy(app)
results_dir = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/results'
q_results = db.session\
    .query(EvaluationResult, SummaryStatus, EvaluationProject)\
    .join(SummaryStatus)\
    .join(EvaluationProject)\
    .all()
#%%
# Create dataframe
summaries = {}
elapsed_times = []
projects = []
for result, _, project in q_results:
    finished_at = result.finished_at
    opened_at = result.opened_at
    elapsed_times.append(finished_at-opened_at)
    projects.append(project.name)
df_result = pd.DataFrame({
    'elapsed_time': pd.Series(elapsed_times),
    'project': pd.Series(projects)
})
#%%
# Grouping dataframe and analysis
import os
df_result_group = df_result.groupby('project')
save_path = os.path.join(results_dir, 'evaluation_result')
if not os.path.exists(save_path):
    os.mkdir(save_path)
for project, data in df_result_group:
    data.describe().to_csv(os.path.join(save_path, '%s_result.csv' % project))
