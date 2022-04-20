# Microservice Pattern Identification From Recovered Architectures of Orchestrated Systems
Artifacts from the software engineering paper.
* anal.py -- Analysis tool for finding dependencies between microservices
* use_cases -- Python scripts to stimulate network traffic in the [TrainTicket](https://github.com/FudanSELab/train-ticket) and [eShopOnContainer](https://github.com/dotnet-architecture/eShopOnContainers) benchmark systems.
* recovered -- Recovered artifacts from benchmark systems TrainTicket, eShopOnContainer and SocksShop.

## Recovered artifacts

In each folder there are files such as
* prescriptive.png -- Prescriptive architecture from the respective project documentation.
* recovered.gv -- GraphViz file representing the recovered architecture
* recovered.pdf -- PDF render of GraphViz file
* vertices.csv -- CSV of the components and their type
* edges.csv -- CSV of dependencies between the components
