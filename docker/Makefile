.PHONY: all wwtin tpls amanzi ats

all: wwtin tpls amanzi ats

wwtin:
	docker build -t metsi/workshop21:wwtin-latest -f Dockerfile-Ubuntu-WW+TIN ./

tpls:
	docker build -t metsi/workshop21:TPLs-latest -f Dockerfile-Workshop-TPLs ./

amanzi:
	docker build -t metsi/workshop21:Amanzi-latest -f Dockerfile-Workshop-Amanzi ./

ats:
	docker build -t metsi/workshop21:latest -f Dockerfile-Workshop-ATS ./