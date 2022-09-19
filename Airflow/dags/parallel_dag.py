# from airflow import DAG
# from airflow.operators.bash import BashOperator
 
# from datetime import datetime
 
# with DAG('parallel_dag', start_date=datetime(2022, 1, 1), 
#     schedule_interval='@daily', catchup=False) as dag:
 
#     extract_a = BashOperator(
#         task_id='extract_a',
#         bash_command='sleep 10'
#     )
 
#     extract_b = BashOperator(
#         task_id='extract_b',
#         bash_command='sleep 10'
#     )
 
#     load_a = BashOperator(
#         task_id='load_a',
#         bash_command='sleep 10'
#     )
 
#     load_b = BashOperator(
#         task_id='load_b',
#         bash_command='sleep 10'
#     )
 
#     transform = BashOperator(
#         task_id='transform',
#         queue = 'high_cpu',
#         bash_command='sleep 30'
#     )
 
#     extract_a >> load_a
#     extract_b >> load_b
#     [load_a, load_b] >> transform

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2022, 1, 1),
    'owner': 'Airflow',
}

def process(p1):
    print(p1)
    return 'done'

with DAG(dag_id='parallel_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # Tasks dynamically generated 
    # Test tasls git-sync
    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 60'.format(t)) for t in range(1, 4)]

    task_4 = PythonOperator(task_id='task_4', python_callable=process, op_args=['my super parameter'])

    task_5 = BashOperator(task_id='task_5', bash_command='echo "pipeline done"')

    task_6 = BashOperator(task_id='task_6', bash_command='sleep 60')

    tasks >> task_4 >> task_5 >> task_6
        