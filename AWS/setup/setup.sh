#!/bin/bash

MATERIALS=/home/ec2-user/environment/WeatherForecastDataPipeline/AWS
GIT_USERNAME=php1301

# create the cluster
eksctl create cluster -f $MATERIALS/EKS/cluster.yml

SCRIPT_SETUP_FLUX=$MATERIALS/scripts/setup-flux.sh
chmod a+x $SCRIPT_SETUP_FLUX
$SCRIPT_SETUP_FLUX $GIT_USERNAME

fluxctl sync --k8s-fwd-ns flux

# if fail recreate the deploy key airflow-workstation-deploy-flux in the repo
# airflow-eks-config with the key generated below
fluxctl identity --k8s-fwd-ns flux

# and execute fluxctl sync --k8s-fwd-ns flux again

