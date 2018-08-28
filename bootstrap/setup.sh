apt update
apt upgrade

# install specific scrapper dependencies
apt install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
apt install python3 python3-dev

# create dev env
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
