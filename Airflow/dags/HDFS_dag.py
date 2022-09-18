from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

default_args = {
    # 'owner': 'php1301',
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    # 'email': ['test@example.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_execute_hdfs_commands = DAG(
    dag_id='execute_hdfs_commands',
    default_args=default_args,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',
    start_date=days_ago(1),
    dagrun_timeout=timedelta(minutes=60),
    description='executing hdfs commands ',
)

start_task = BashOperator(task_id="start_task",
                          bash_command="/home/phucpham1301/airflow/dags/test.sh ",
                          dag=dag_execute_hdfs_commands,
                          )
print("creating a directory")
create_dir = BashOperator(task_id="create_dir",
                          bash_command="/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -mkdir -p /test_php1301  ",
                          dag=dag_execute_hdfs_commands
                          )

print("giving permissions to a directory")
give_permissions = BashOperator(
    task_id="give_permissions",
    bash_command="/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -chmod -R 777 /test_php1301 ",
    dag=dag_execute_hdfs_commands
    )

list_all_files = BashOperator(task_id="list_files",
                              bash_command="/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -ls /  ",
                              dag=dag_execute_hdfs_commands
                              )

create_empty_file = BashOperator(
    task_id="create_file",
    bash_command="/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -touchz /test_php1301/test.txt  ",
    dag=dag_execute_hdfs_commands
    )

remove_dir = BashOperator(task_id="remove_dir",
                          bash_command="/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -rm -r /test_php1301  ",
                          dag=dag_execute_hdfs_commands,
                          )
copy_from_local = BashOperator(
    task_id="copy_from_local",
    bash_command=
    "/home/phucpham1301/hadoop-3.3.4/bin/hdfs dfs -copyFromLocal /home/phucpham1301/hadoop-3.3.4/weatherHistory.csv /test_php1301  ",
    dag=dag_execute_hdfs_commands
    )
start_task >> create_dir >> give_permissions >> list_all_files >> create_empty_file >> remove_dir >> copy_from_local

if __name__ == '__main__ ':
    dag_execute_hdfs_commands.cli()
