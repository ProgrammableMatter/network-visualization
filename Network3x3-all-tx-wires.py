from collections import OrderedDict
from LogSamplePlot import Plotter as pltr
from LogSamplePlot import Filter as fltr
from Config import Mappings as mappingConfig
from Config import Input as inputConfig

if __name__ == "__main__":
    dataFilter = fltr.Filter(inputConfig.logFile, mappingConfig.wireToFloatValueMapping)
    dataPlotter = pltr.Plotter()

    numRows = 3
    numColumns = 3
    nodesTotal = numRows * numColumns

    # column 1

    for id in range(0, numRows * numColumns):
        filter = fltr.SampleFilter(domain="WIRE", name="tx-north", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

        filter = fltr.SampleFilter(domain="WIRE", name="tx-east", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

        filter = fltr.SampleFilter(domain="WIRE", name="tx-south", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

    dataPlotter.setWindowTitle("Network %sx%s Simulation - tx wires" % (numRows, numColumns))
    dataFilter.printValues()
    dataPlotter.plot()
