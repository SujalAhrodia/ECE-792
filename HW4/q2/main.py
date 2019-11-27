import os
import sys
import csv

file_name = sys.argv[1]

def deploy_cont(cont):
    os.system("ansible-playbook create_container.yml --extra-vars cname="+cont)


with open(file_name) as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        con1, con2, net = row[0], row[1], row[2]
        deploy_cont(con1)
        deploy_cont(con2)