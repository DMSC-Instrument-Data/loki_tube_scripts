import numpy
import math
from sets import *
from itertools import product


class LOKIGenerator(object):
    pixels = Set()
    straws = Set()
    modules = Set()
    tubes = Set()
    panels = {}
    idCount = None  # Chronological detector ID count

    def __init__(self, filename, useIntrinsicResolution=True, useComplexDetectorScheme=True,
                 displayPanels=[1, 2, 3, 4, 5, 6, 7, 8, 9], tubeResolution=0.005):
        '''
        :param filename: File where idf xml file will be output. Filename should contain xml extension.
        :param useIntrinsicResolution: Whether or not to use the intrinsic resolution of the tube otherwise 1000 pixels per straw
        :param displayPanels: list of panels to be display. Only values 1-9 valid.
        '''
        self.useIntrinsicResolution = useIntrinsicResolution
        self.useComplexDetScheme = useComplexDetectorScheme
        self.idfFile = open(filename, "w");
        self.tubeIDConversionFile = open("LOKI_ID_Conversion.csv", "w")
        self.tubeThetaOffset = 13.45  # degrees
        self.tubeDiameter = 0.0254  # metres
        self.tubeRowLength = 4  # tubes
        self.tubeRotation = -8.45  # degrees
        self.tubRowAngleOffset = 103.45  # degrees
        self.tubeResolution = tubeResolution  # metres
        self.detIDText = ""
        self.detIDConsecutiveText = ""
        self.displayPanels = displayPanels
        self.panels[1] = (10, 1200, 1340, 28, True)
        self.panels[2] = (10, 1200, 1340, -28, True)
        self.panels[3] = (16, 1200, 1750, 25.6, False)
        self.panels[4] = (16, 1200, 1750, -25.6, False)
        self.panels[5] = (8, 1000, 2950, 9.7, True)
        self.panels[6] = (8, 1000, 2950, -9.7, True)
        self.panels[7] = (6, 500, 3300, 6.5, False)
        self.panels[8] = (6, 500, 3300, -6.5, False)
        self.panels[9] = (28, 1000, 5000, -0, True, True)
        # self.panels[9] = (2, 1500, 2000, -0, True, True)

    def isNegative(self, num):
        return num < 0

    def toRadians(self, degrees):
        return math.pi * degrees / 180.0

    def getOrientation(self, isHorizontal):
        return "horz" if isHorizontal else "vert"

    def getDirection(self, isHorizontal, theta):
        if isHorizontal:
            return "bottom" if self.isNegative(theta) else "top"
        else:
            return "right" if self.isNegative(theta) else "left"

    def __del__(self):
        self.idfFile.close()
        self.tubeIDConversionFile.close()

    def _writeInstrumentHeader(self):
        self.idfFile.write("<?xml version='1.0' encoding='ASCII'?>\n")
        self.idfFile.write("<!-- For help on the notation used to specify an Instrument ")
        self.idfFile.write("Definition File see http://www.mantidproject.org/IDF -->\n")
        self.idfFile.write("<instrument xmlns=\"http://www.mantidproject.org/IDF/1.0\" ")
        self.idfFile.write("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
        self.idfFile.write("xsi:schemaLocation=\"http://www.mantidproject.org/IDF/1.0 ")
        self.idfFile.write("http://schema.mantidproject.org/IDF/1.0/IDFSchema.xsd\"\n")
        self.idfFile.write("name=\"LOKI\" valid-from   =\"1900-01-31 23:59:59\"\n")
        self.idfFile.write("valid-to     =\"2100-01-31 23:59:59\"\n")
        self.idfFile.write("last-modified=\"2010-11-16 12:02:05\">\n")
        self.idfFile.write("<!---->\n")
        self.idfFile.write("<defaults>\n")
        self.idfFile.write("\t<length unit=\"metre\"/>\n")
        self.idfFile.write("\t<angle unit=\"degree\"/>\n")
        self.idfFile.write("\t<reference-frame>\n")
        self.idfFile.write("\t\t<along-beam axis=\"z\"/>\n")
        self.idfFile.write("\t\t<pointing-up axis=\"y\"/>\n")
        self.idfFile.write("\t\t<handedness val=\"right\"/>\n")
        self.idfFile.write("\t</reference-frame>\n")
        self.idfFile.write("<default-view axis-view=\"z-\"/></defaults>\n\n")

    def _writeInsrumentFooter(self):
        self.idfFile.write("</instrument>\n")

    def _writeSource(self):
        self.idfFile.write("<component type=\"moderator\">\n")
        self.idfFile.write("\t<location z=\"-8.64\"/>\n")
        self.idfFile.write("</component>\n")
        self.idfFile.write("<type is=\"Source\" name=\"moderator\"/>\n\n")

    def _writeSample(self):
        self.idfFile.write("<component type=\"sample-position\">\n")
        self.idfFile.write("\t<location y=\"0.0\" x=\"0.0\" z=\"0.0\"/>\n")
        self.idfFile.write("</component>\n")
        self.idfFile.write("<type is=\"SamplePos\" name=\"sample-position\"/>\n\n")

    def _writeMonitors(self):
        self.idfFile.write("<!--MONITORS-->\n")
        self.idfFile.write("<component type=\"monitors\" idlist=\"monitors\">\n")
        self.idfFile.write("\t<location/>\n")
        self.idfFile.write("</component>\n")
        self.idfFile.write("<type name=\"monitors\">\n")
        self.idfFile.write("\t<component type=\"monitor\">\n")
        self.idfFile.write("\t\t<location z=\"-15.4\" name=\"BM2_FOC\"/>\n")
        self.idfFile.write("\t\t<location z=\"-21.3\" name=\"BM3_haloMon\"/>\n")
        self.idfFile.write("\t\t<location z=\"-23.5\" name=\"BM4_Trans\"/>\n")
        self.idfFile.write("\t</component>\n")
        self.idfFile.write("</type>\n\n")

        self.idfFile.write("<!--MONITOR SHAPE-->")
        self.idfFile.write("<type is=\"monitor\" name=\"monitor\">\n")
        self.idfFile.write("<cuboid id=\"pixel-shape\">\n")
        self.idfFile.write("<left-front-bottom-point y=\"-0.04\" x=\"-0.04\" z=\"0.0\"/>\n")
        self.idfFile.write("<left-front-top-point y=\"0.04\" x=\"-0.04\" z=\"0.0\"/>\n")
        self.idfFile.write("<left-back-bottom-point y=\"-0.04\" x=\"-0.04\" z=\"-0.04\"/>\n")
        self.idfFile.write("<right-front-bottom-point y=\"-0.04\" x=\"0.04\" z=\"0.0\"/>\n")
        self.idfFile.write("</cuboid>\n")
        self.idfFile.write("<algebra val=\"pixel-shape\"/>\n")
        self.idfFile.write("</type>\n\n")

        self.idfFile.write("<!--MONITOR IDs-->\n")
        self.idfFile.write("<idlist idname=\"monitors\">\n")
        self.idfFile.write("\t<id val=\"-1\"/>\n")
        self.idfFile.write("\t<id val=\"-2\"/>\n")
        self.idfFile.write("\t<id val=\"-3\"/>\n")
        self.idfFile.write("</idlist>\n\n")

    def _writePixel(self, type, length, isHorizontal):
        x, y = ("1.0", "0.0") if isHorizontal else ("0.0", "1.0")
        pixelHeight = self.tubeResolution if self.useIntrinsicResolution else length / 1000.0

        pixelText = "<type name=\"" + type + "\" is=\"detector\">\n"
        pixelText += "<cylinder id=\"cyl-approx\">\n"
        pixelText += "\t<centre-of-bottom-base r=\"0.0\" t=\"0.0\" p=\"0.0\" />\n"
        pixelText += "\t<axis x=\"" + x + "\" y=\"" + y + "\" z=\"0.0\" />\n"
        pixelText += "\t<radius val=\"0.00375\" />\n"
        pixelText += "\t<height val=\"" + str(pixelHeight) + "\" />\n"
        pixelText += "</cylinder>\n"
        pixelText += "<algebra val=\"cyl-approx\" />\n"
        pixelText += "</type>\n\n"

        self.pixels.add(pixelText)

    def _writeStraw(self, type, length, isHorizontal):
        lengthInMetres = length / 1000.0
        end = lengthInMetres / 2
        begin = -end
        nPixels = lengthInMetres / self.tubeResolution if self.useIntrinsicResolution else 1000
        nPixels = int(nPixels)

        x1, x2, y1, y2 = (begin, end, 0, 0) if isHorizontal else (0, 0, begin, end)

        pixelType = ("h" if isHorizontal else "v") + "-pixel-" + str(length) + "mm"

        strawText = "<type name=\"" + type + "\" outline=\"yes\">\n"
        strawText += "<component type=\"" + str(pixelType) + "\">\n"
        strawText += "\t<locations x=\"" + str(x1) + "\" x-end=\"" + str(x2) + "\" y=\""
        strawText += str(y1) + "\" y-end=\"" + str(y2) + "\" n-elements=\"" + str(nPixels) + "\" />\n"
        strawText += "</component>\n"
        strawText += "</type>\n\n"

        self.straws.add(strawText)

        self._writePixel(pixelType, length, isHorizontal)

    def _writeTube(self, tubeName, length, isHorizontal):
        strawType = ("horz" if isHorizontal else "vert") + "_straw_" + str(length) + "mm"
        tubeHorzPos = 0.0065
        x1, y1 = (0.0, 0.0)
        x2, y2 = (0.0, tubeHorzPos) if isHorizontal else (tubeHorzPos, 0.0)

        tubeText = "<type name=\"" + tubeName + "\">\n"
        tubeText += "<component type=\"" + strawType + "\">\n"
        tubeText += "\t<location x=\"" + str(x1) + "\" y=\"" + str(y1) + "\" z=\"0.0\" name=\"straw_1\"/>\n"
        tubeText += "\t<location x=\"" + str(x1) + "\" y=\"" + str(y1) + "\" z=\"0.0075\" name=\"straw_2\"/>\n"
        tubeText += "\t<location x=\"" + str(x1) + "\" y=\"" + str(y1) + "\" z=\"-0.0075\" name=\"straw_3\"/>\n"
        tubeText += "\t<location x=\"" + str(x2) + "\" y=\"" + str(y2) + "\" z=\"0.00375\" name=\"straw_4\"/>\n"
        tubeText += "\t<location x=\"" + str(x2) + "\" y=\"" + str(y2) + "\" z=\"-0.00375\" name=\"straw_5\"/>\n"
        tubeText += "\t<location x=\"" + str(-x2) + "\" y=\"" + str(-y2) + "\" z=\"-0.00375\" name=\"straw_6\"/>\n"
        tubeText += "\t<location x=\"" + str(-x2) + "\" y=\"" + str(-y2) + "\" z=\"0.00375\" name=\"straw_7\"/>\n"
        tubeText += "</component>\n"
        tubeText += "</type>\n\n"

        self.tubes.add(tubeText)
        self._writeStraw(strawType, length, isHorizontal)

    def _writeSingleModule(self, moduleType, isHorizontal, strawLength, theta):
        tubeType = self.getDirection(isHorizontal, theta) + "_tube_" + str(strawLength) + "mm"
        axisx, axisy = ('1', '0') if isHorizontal else ('0', '1')
        tubeRadius = self.tubeDiameter / 2
        vstart = -tubeRadius
        shortAngleBetweenTubes = self.toRadians(self.tubRowAngleOffset)
        vend = vstart + (math.sin(shortAngleBetweenTubes) * self.tubeDiameter)

        rowLength = (self.tubeRowLength - 1) * self.tubeDiameter
        z1Start = -rowLength / 2
        z1End = z1Start + rowLength

        hlength = math.cos(shortAngleBetweenTubes) * self.tubeDiameter

        x1, y1 = (0, vstart) if isHorizontal else (vstart, 0)
        x2, y2 = (0, vend) if isHorizontal else (vend, 0)

        direction = self.getDirection(isHorizontal, theta)

        isRightOrBottomBank = (direction is "right") or (direction is "bottom")

        z2Start, z2End = (z1Start - hlength, z1End - hlength) if isRightOrBottomBank else (
            z1Start + hlength, z1End + hlength)

        moduleText = "<type name=\"" + moduleType + "\">\n"
        moduleText += "<component type=\"" + str(tubeType) + "\">\n"
        moduleText += "\t<locations x=\"" + str(x1) + "\" y=\"" + str(y1) + "\" z=\"" + str(z1Start)
        moduleText += "\" z-end=\"" + str(z1End) + "\" n-elements=\"" + str(self.tubeRowLength) + "\""
        moduleText += " name=\"detector_module_layer_1\" rot=\"" + str(self.tubeRotation) + "\" axis-x=\""
        moduleText += axisx + "\" axis-y=\"" + axisy + "\" axis-z=\"0\"/>\n"
        moduleText += "\t<locations x=\"" + str(x2) + "\" y=\"" + str(y2) + "\" z=\""
        moduleText += str(z2Start) + "\" z-end=\"" + str(z2End) + "\" n-elements=\""
        moduleText += str(self.tubeRowLength) + "\" name=\"detector_module_layer_2\" rot=\""
        moduleText += str(self.tubeRotation) + "\" axis-x=\"" + axisx + "\" axis-y=\""
        moduleText += axisy + "\" axis-z=\"0\"/>\n"
        moduleText += "</component>\n</type>\n\n"

        self.modules.add(moduleText)
        self._writeTube(tubeType, strawLength, isHorizontal)

    def _writePacks(self, numPacks, panelType, moduleType, isHorizontal, strawLength, theta):
        packDiameter = self.tubeDiameter * 2.0
        totalLength = packDiameter * (numPacks - 1)
        dir = self.getDirection(isHorizontal, theta)
        mul = -1 if dir is "bottom" or dir is "right" else 1
        startPos = mul * (totalLength / 2)
        self.idfFile.write("<type name=\"" + panelType + "\">\n<component type=\"" + moduleType + "\">\n")

        hChange = packDiameter * math.cos(self.toRadians(self.tubeThetaOffset))
        vChange = packDiameter * math.sin(self.toRadians(self.tubeThetaOffset))

        v = 0;
        h = startPos;
        for i in xrange(numPacks):
            x, y = (0, h) if isHorizontal else (h, 0)
            z = v
            self.idfFile.write(
                "\t<location name=\"Pack_" + str(i + 1) + "\" x=\"" + str(x) + "\" y=\"" + str(y) + "\" z=\"" + str(
                    z) + "\" />\n")

            if dir is "right" or dir is "bottom":
                h += hChange
            else:
                h -= hChange
            v += vChange
        self.idfFile.write("</component>\n</type>\n\n")

        self._writeSingleModule(moduleType, isHorizontal, strawLength, theta)

    def _writeIDs(self, idListName, panelNumber, numPacks, strawLength):
        lengthInMetres = strawLength / 1000.0
        tubesPerPack = self.tubeRowLength * 2
        strawsPerTube = 7
        pixelsPerStraw = lengthInMetres / self.tubeResolution if self.useIntrinsicResolution else 1000
        pixelsPerStraw = int(pixelsPerStraw)

        self.detIDText += "<idlist idname=\"" + idListName + "\">\n"
        self.detIDConsecutiveText += "<idlist idname=\"" + idListName + "\">\n"

        "Straw and tube ordering based on Davide's regime"
        strawOrder = [4, 1, 7, 5, 6, 3, 2]
        tubeOrder = [2, 4, 6, 8, 1, 3, 5, 7]
        for pack, tube, straw in product(range(numPacks), range(tubesPerPack), range(strawsPerTube)):
            id_pre = str(panelNumber) + str(pack + 1).zfill(2) + str(tubeOrder[tube]) + str(strawOrder[straw])
            start = id_pre + str(0).zfill(4)
            end = id_pre + str(pixelsPerStraw - 1).zfill(4)
            startCons = str(self.idCount)
            endCons = str(self.idCount + pixelsPerStraw - 1)
            self.tubeIDConversionFile.write(startCons + "," + endCons + "," + start + "," + end + "\n")
            self.idCount += pixelsPerStraw
            self.detIDText += "\t<id start=\"" + start + "\" end=\"" + end + "\"/>\n"
            self.detIDConsecutiveText += "\t<id start=\"" + startCons + "\" end=\"" + endCons + "\"/>\n"

        self.detIDText += "</idlist>\n\n"
        self.detIDConsecutiveText += "</idlist>\n\n"

    def _writePanel(self, panelNumber, numPacks, strawLength, r, theta, isHorizontal=False, isRearPanel=False):
        r_mm = r / 1000.0
        orientation = self.getOrientation(isHorizontal)
        direction = "back" if isRearPanel else self.getDirection(isHorizontal, theta)
        panelType = "panel_" + str(strawLength) + "_" + orientation + "_" + direction
        x = y = 0
        z = r_mm * math.cos(self.toRadians(theta))

        calc = r_mm * math.sin(self.toRadians(theta))
        x, y = (0, calc) if isHorizontal else (calc, 0)

        name = "Panel_" + str(panelNumber) + "_" + orientation + "_" + str(strawLength) + "_" + direction
        idList = "Panel_" + str(panelNumber) + "_Ids_" + orientation + "_" + direction
        moduleType = "pack_" + orientation + "_" + str(strawLength) + "mm_" + self.getDirection(isHorizontal, theta)

        self.idfFile.write("<component name=\"" + name + "\" type=\"" + panelType + "\" idlist=\"" + idList + "\">\n")
        if isRearPanel:
            self.idfFile.write("\t<location x=\"" + str(x) + "\" y=\"" + str(y) + "\" z=\"" + str(z) + "\"")
            self.idfFile.write(" rot=\"13.45\" axis-x=\"1\" axis-y=\"0\" axis-z=\"0\" />\n")
        else:
            self.idfFile.write("\t<location x=\"" + str(x) + "\" y=\"" + str(y) + "\" z=\"" + str(z) + "\" />\n")

        self.idfFile.write("</component>\n\n")

        self._writeIDs(idList, panelNumber, numPacks, strawLength)
        self._writePacks(numPacks, panelType, moduleType, isHorizontal, strawLength, theta)

    def _completeWrite(self):
        for module in self.modules:
            self.idfFile.write(module)
        for tube in self.tubes:
            self.idfFile.write(tube)
        for straw in self.straws:
            self.idfFile.write(straw)
        for pixel in self.pixels:
            self.idfFile.write(pixel)
        if self.useComplexDetScheme:
            self.idfFile.write(self.detIDText)
        else:
            self.idfFile.write(self.detIDConsecutiveText)

    def generate(self):
        '''
        Generates the LOKI geometry file with filename specified in constructor.
        :return:
        '''
        self.idCount = 1  # reset detector ID counts
        self._writeInstrumentHeader()
        self._writeSource()
        self._writeSample()
        self._writeMonitors()
        for panel in self.displayPanels:
            self._writePanel(panel, *self.panels[panel])
        self._completeWrite()

        self._writeInsrumentFooter()


if __name__ == "__main__":
    lokiWriter = LOKIGenerator("LOKI_Definition_test.xml", True, True)
    lokiWriter.generate()
