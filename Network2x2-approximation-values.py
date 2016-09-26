from Config import Input as inputConfig
from Config import Mappings as mappingConfig
from Config.Mappings import charOutToHumanReadableAnnotation
from LogSamplePlot import Filter as fltr
from LogSamplePlot import Plotter as pltr

if __name__ == "__main__":
    dataFilter = fltr.Filter(inputConfig.logFile, mappingConfig.wireToFloatValueMapping)
    dataPlotter = pltr.Plotter()

    numRows, numColumns = 2, 2
    nodesTotal = numRows * numColumns

    # wires plots
    for id in range(0, nodesTotal):
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

    # interrupt plots
    for id in range(0, nodesTotal):
        interruptName = "LOCAL_TIME_TIMER_INTERRUPT"
        dataFilter.setValueMapping(mappingConfig.interruptToFloatValueMapping)
        pltr.addInterruptPlot(dataFilter, dataPlotter, title=("[%s] invoke" % id), nodeId=id,
                              interruptToNumberMapping=mappingConfig.interruptToNumberMapping,
                              facet="invoke",
                              interruptName=interruptName)

        interruptName = "TX_RX_TIMER_OVERVLOW"
        dataFilter.setValueMapping(mappingConfig.interruptToFloatValueMapping)
        pltr.addInterruptPlot(dataFilter, dataPlotter, title=("[%s] post" % id), nodeId=id,
                              interruptToNumberMapping=mappingConfig.interruptToNumberMapping,
                              facet="post",
                              interruptName=interruptName)

    # char out plots
    for id in range(0, nodesTotal):
        filter = fltr.SampleFilter(domain="SRAM", name="char-out", nodeId=id)
        dataFilter.removeSamples(filter)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        annotations = pltr.reMapAnnotation(annotations, charOutToHumanReadableAnnotation)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

    # int16 out plots
    for id in range(0, nodesTotal):
        filter = fltr.SampleFilter(domain="SRAM", name="int16-out", nodeId=id)
        dataFilter.removeSamples(filter)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

    # node state plots
    for id in range(0, nodesTotal):
        filter = fltr.SampleFilter(domain="SRAM", name="Particle.node.state", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

    # approximation values plots
    for id in range(0, nodesTotal):
        filter = fltr.SampleFilter(domain="SRAM", name="Particle.timeSynchronization.progressiveMean[3]", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

        filter = fltr.SampleFilter(domain="SRAM", name="Particle.timeSynchronization.mean[3]", nodeId=id)
        dataFilter.filter(filter)
        xData, yData, annotations = dataFilter.getData(filter)
        dataPlotter.addPlot(xData, yData, annotations, "[%s] %s" % (filter.nodeId, filter.name))

    dataPlotter.setWindowTitle("Network %sx%s Simulation" % (numRows, numColumns))
    dataFilter.printValues()
    dataPlotter.plot()
