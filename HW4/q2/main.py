#LOGIC LAYER
import os
import sys
import csv

file_name = sys.argv[1]

with open(file_name) as f:
    csv_reader = csv.reader(f, delimiter=',')
    line_count = 0
    for row in csv_reader:
        con1, con2, net = row[0], row[1], row[2]
        os.system("ansible-playbook create_container.yml --extra-vars cname="+con1)
        os.system("ansible-playbook create_container.yml --extra-vars cname="+con2)
        if net.lower()=="bridge":
            os.system("ansible-playbook create_L2.yml --extra-vars \"nname="+net+" c1name="+con1+" c2name="+con2+"\"")
        elif net.lower()=="vxlan":
             os.system("ansible-playbook create_VXLAN.yml --extra-vars \"c1name="+con1+" c2name="+con2+"\"")
        elif net.lower()=="l3":
             os.system("ansible-playbook create_L3.yml --extra-vars \"c1name="+con1+" c2name="+con2+"\"")
        elif net.lower()=="gre":
             os.system("ansible-playbook create_GRE.yml --extra-vars \"c1name="+con1+" c2name="+con2+"\"")
        else:
            print("NOT A VALID NETWORK OPTION!")
