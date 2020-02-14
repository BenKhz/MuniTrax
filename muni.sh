cp /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
export DISPLAY=:0
lxpanelctl exit
python3 XML_app_refactor.py
