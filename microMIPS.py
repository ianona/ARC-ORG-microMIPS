import wx
import wx.grid as grid

class MainTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.SetSize(700,500)
        self.SetBackgroundColour("WHITE")

        # INITIALIZE TABLE FOR CODE INFO
        wx.StaticText(self, label="Code", pos=(0,0))
        self.codeGrid = grid.Grid(self, pos = (0,20), size=(220,200))
        self.codeGrid.CreateGrid(0, 4)
        self.codeGrid.SetColLabelValue(0, "Address")
        self.codeGrid.SetColLabelValue(1, "Rep")
        self.codeGrid.SetColLabelValue(2, "Label")
        self.codeGrid.SetColLabelValue(3, "Instruction")
        self.codeGrid.SetRowLabelSize(0)

        # INITIALIZE TABLE FOR DATA INFO
        wx.StaticText(self, label="Data", pos=(0,220))
        self.dataGrid = grid.Grid(self, pos = (0,240), size=(220,200))
        self.dataGrid.CreateGrid(0, 4)
        self.dataGrid.SetColLabelValue(0, "Address")
        self.dataGrid.SetColLabelValue(1, "Rep")
        self.dataGrid.SetColLabelValue(2, "Label")
        self.dataGrid.SetColLabelValue(3, "Code")
        self.dataGrid.SetRowLabelSize(0)

        # INITIALIZE TABLE FOR REGISTERS
        wx.StaticText(self, label="Registers", pos=(230,220))
        self.regGrid = grid.Grid(self, pos = (230,240), size=(220,200))
        self.regGrid.CreateGrid(0, 2)
        self.regGrid.SetColLabelValue(0, "Register")
        self.regGrid.SetColLabelValue(1, "Value")
        self.regGrid.SetRowLabelSize(0)
        self.resetRegisters()

        # INITIALIZE RUN BUTTON
        self.runBtn = wx.Button(self, label="Run Cycle", pos=(460,390), size=(120,25))
        self.runBtn.Bind(wx.EVT_BUTTON, self.run)
        self.runBtn.Hide()

        # INITIALIZE RUN ALL BUTTON
        self.runAllBtn = wx.Button(self, label="Run All Cycles", pos=(460,415), size=(120,25))
        self.runAllBtn.Bind(wx.EVT_BUTTON, self.runAll)
        self.runAllBtn.Hide()

    def resetRegisters(self):
        for i in range(0,32):
            self.regGrid.AppendRows(1)
            self.regGrid.SetCellValue(i, 0, str(i))
            self.regGrid.SetCellValue(i, 1, "0000000000000000")
            self.regGrid.SetReadOnly(i, 0, True)
            self.regGrid.SetReadOnly(i, 1, True)
            self.regGrid.AutoSizeColumns(True)

        # MANUALLY INITIALIZE REGISTERS ACCDG. TO PROBLEM SET 3
        self.regGrid.SetCellValue(3, 1, "0000000000000004")
        self.regGrid.SetCellValue(2, 1, "0000000000000008")
        self.regGrid.SetCellValue(1, 1, "0000000000000002")

    def run(self, e):
        line = self.MEMORY[self.PC]
        print("now cycling " + line + " : " + self.PC)

        # CYCLE 1: IF (instruction fetch cycle)
        self.IR = self.OPCODES[self.PC]
        self.opcodeBin = bin(int(self.IR,16)).split("b")[1].zfill(32)
        self.NPC = hex(int(self.PC,16) + 4).split("x")[1].zfill(4)

        # CYCLE 2: ID (instruction decode cycle)
        # NUMBER OF REGISTER
        self.regA = int(self.opcodeBin[6:11],2)
        self.regB = int(self.opcodeBin[11:16],2)
        # GETS ACTUAL VALUE INSIDE REGISTER
        self.A = self.regGrid.GetCellValue(self.regA, 1)
        self.B = self.regGrid.GetCellValue(self.regB, 1)
        self.IMM = hex(int(self.opcodeBin[16:32],2)).split("x")[1].zfill(16)

        # CYCLE 3: EX (execution cycle)
        if "DADDIU" in line:
            self.daddiu(line)
        elif "DADDU" in line:
            self.daddu(line)
        elif "SD" in line:
            self.sd(line)
        elif "LD" in current:
            self.ld(line)
        elif "BC" in current:
            self.bgec(line)
        elif "BGEC" in current:
            self.bgec(line)
        elif "SLTI" in current:
            self.slti(line)

        # IF DONE RUNNING INSTRUCTIONS
        if self.PC not in self.MEMORY:
            self.runBtn.Hide()
            self.runAllBtn.Hide()

    def runAll(self, e):
        while self.PC in self.MEMORY:
            line = self.MEMORY[self.PC]
            print("now cycling " + line + " : " + self.PC)

            # CYCLE 1: IF (instruction fetch cycle)
            self.IR = self.OPCODES[self.PC]
            self.opcodeBin = bin(int(self.IR,16)).split("b")[1].zfill(32)
            self.NPC = hex(int(self.PC,16) + 4).split("x")[1].zfill(4)

            # CYCLE 2: ID (instruction decode cycle)
            # NUMBER OF REGISTER
            self.regA = int(self.opcodeBin[6:11],2)
            self.regB = int(self.opcodeBin[11:16],2)
            # GETS ACTUAL VALUE INSIDE REGISTER
            self.A = self.regGrid.GetCellValue(self.regA, 1)
            self.B = self.regGrid.GetCellValue(self.regB, 1)
            self.IMM = hex(int(self.opcodeBin[16:32],2)).split("x")[1].zfill(16)

            # CYCLE 3: EX (execution cycle)
            if "DADDIU" in line:
                self.daddiu(line)
            elif "DADDU" in line:
                self.daddu(line)
            elif "SD" in line:
                self.sd(line)
            elif "LD" in line:
                self.ld(line)
            elif "BC" in line:
                self.bc(line)
            elif "BGEC" in line:
                self.bgec(line)
            elif "SLTI" in line:
                self.slti(line)

        self.runBtn.Hide()  
        self.runAllBtn.Hide()

    def prepareCycles(self, codeMemory, dataMemory, opcodes):
        self.PC = "0100"
        # dictionary to map PC to corresponding line 
        self.MEMORY = {}
        self.OPCODES = {}
        for line in codeMemory:
            self.MEMORY[codeMemory[line]] = line
            self.OPCODES[codeMemory[line]] = opcodes[line]
        print(self.OPCODES)

        print("---------------------------")
        self.runBtn.Show()
        self.runAllBtn.Show()

    def daddiu(self, line):
        # REMOVE "DADDIU"
        line = line[line.index("DADDIU")+7:]
        
        args = line.split(",")
        args = [arg.strip() for arg in args]

        self.ALUOutput = bin(int(self.A,16) + int(self.IMM,16)).split("b")[1]
        while len(self.ALUOutput) % 4 != 0:
            self.ALUOutput = "0" + self.ALUOutput
        sign = self.ALUOutput[0]
        # sign extend
        while len(self.ALUOutput) < 64:
            self.ALUOutput = sign + self.ALUOutput

        self.ALUOutput = hex(int(self.ALUOutput, 2)).split("x")[1].zfill(16).upper()
        self.COND = 0

        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC

        # CYCLE 5: WB (write-back cycle)
        self.regGrid.SetCellValue(self.regB, 1, self.ALUOutput)

    def daddu(self, line):
        self.ALUOutput = bin(int(self.A,16) + int(self.B,16)).split("b")[1]
        while len(self.ALUOutput) % 4 != 0:
            self.ALUOutput = "0" + self.ALUOutput
        sign = self.ALUOutput[0]

        self.ALUOutput = hex(int(self.ALUOutput, 2)).split("x")[1].zfill(16).upper()
        self.COND = 0
        
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC

        # CYCLE 5: WB (write-back cycle)
        self.regGrid.SetCellValue(int(self.opcodeBin[16:21],2), 1, self.ALUOutput)


    def sd(self, line):
        print("Sammie")
        self.ALUOutput = bin(int(self.A,16) + int(self.IMM,16)).split("b")[1]
        print("ALUOutput: " + self.ALUOutput)
        self.COND = 0
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC
        dataToStore = (self.IMM)[-4:]
        self.dataRepresentation[dataToStore] = self.B
        print("DATA REPRESENTATION")
        print(self.dataRepresentation)
        # CYCLE 5: WB (write-back cycle)
        
        
    def ld(self, line):
        print("Sammie")
        self.ALUOutput = bin(int(self.A,16) + int(self.IMM,16)).split("b")[1]
        print("ALUOutput: " + self.ALUOutput)
        self.COND = 0
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC
        print("DATA REPRESENTATION")
        print(self.dataRepresentation)
        dataToLoad = (self.IMM)[-4:]
        self.LMD = self.dataRepresentation[dataToLoad]
        print("LMD")
        print(self.LMD)
        
        # CYCLE 5: WB (write-back cycle)
        print("Reg B")
        print(self.regB)
        self.regGrid.SetCellValue(self.regB, 1, self.LMD)
        print("Register: ")
        print(self.regGrid.GetCellValue(self.regB, 1))
        
    def bc(self, line):
        print(self.NPC)
        
        self.ALUOutput = hex(self.s64(int(self.NPC,16)) + (self.s64(int(self.IMM,16))* 4)).split("x")[1].zfill(4)
        print(self.ALUOutput)
        self.COND = 1
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.ALUOutput

        # CYCLE 5: WB (write-back cycle)

    def s64(self, value):
        return -(value & 0x8000) | (value & 0x7fff)

    def bgec(self, line):
        print(self.NPC)
        self.ALUOutput = hex(self.s64(int(self.NPC,16)) + (self.s64(int(self.IMM,16))* 4)).split("x")[1].zfill(4)
        print(self.ALUOutput)
        if(self.s64(int(self.A)) >= self.s64(int(self.B))):
           self.COND = 1
           self.PC = self.ALUOutput
        # CYCLE 4: MEM (memory access/branch completion cycle)
        else:
            self.COND = 0
            self.PC = self.NPC

        # CYCLE 5: WB (write-back cycle)

    def slti(self, line):
        if int(self.A, 16) < int(self.IMM, 16):
            self.ALUOutput = 0
        else:
            self.ALUOutput = 1
        # print("ALUOutput: " + self.ALUOutput)
        self.COND = 0
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC

        # CYCLE 5: WB (write-back cycle)
        outputStr = str(self.ALUOutput).zfill(16)
        self.regGrid.SetCellValue(self.regB, 1, outputStr)
        
    def updateCode(self, opcodes, codes, codeMemory, dataRepresentation):
        # EMPTY GRID
        self.dataRepresentation = dataRepresentation
        if self.codeGrid.GetNumberRows() > 0:
            self.codeGrid.DeleteRows(0, self.codeGrid.GetNumberRows())

        # DELETE ".code"
        del codes[0]

        # ADDS NEW ROW FOR EACH LINE OF INSTRUCTION
        for line in codes:
            self.codeGrid.AppendRows(1)
            cur = self.codeGrid.GetNumberRows() - 1
            self.codeGrid.SetCellValue(cur, 0, codeMemory[line])
            self.codeGrid.SetCellValue(cur, 1, opcodes[line])
            if ":" in line:
                self.codeGrid.SetCellValue(cur, 2, line.split(":")[0])
            self.codeGrid.SetCellValue(cur, 3, line)
            self.codeGrid.SetReadOnly(cur, 0, True)
            self.codeGrid.SetReadOnly(cur, 1, True)
            self.codeGrid.SetReadOnly(cur, 2, True)
            self.codeGrid.SetReadOnly(cur, 3, True)
            self.codeGrid.AutoSizeColumns(True)

    def updateData(self, dataMemory, data, dataRepresentation):
        # EMPTY GRID
        self.dataRepresentation = dataRepresentation
        if self.dataGrid.GetNumberRows() > 0:
            self.dataGrid.DeleteRows(0, self.dataGrid.GetNumberRows())

        # DELETE ".data"
        del data[0]

        # ADDS NEW ROW FOR EACH LINE OF DATA
        for line in dataRepresentation:
            self.dataGrid.AppendRows(1)
            cur = self.dataGrid.GetNumberRows() - 1
            self.dataGrid.SetCellValue(cur, 0, line)
            self.dataGrid.SetCellValue(cur, 1, dataRepresentation[line])

            if line in list(dataMemory.values()):
                for x in dataMemory:
                    if dataMemory[x] == line:
                        found = x
                self.dataGrid.SetCellValue(cur, 2, found.split(":")[0])
                self.dataGrid.SetCellValue(cur, 3, found.split(":")[1])
            self.dataGrid.SetReadOnly(cur, 0, True)
            self.dataGrid.SetReadOnly(cur, 1, True)
            self.dataGrid.SetReadOnly(cur, 2, True)
            self.dataGrid.SetReadOnly(cur, 3, True)
            self.dataGrid.AutoSizeColumns(True)

        # SET EMPTY DATA ROWS
        start = list(dataRepresentation.keys())[-1]
        start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()
               
        while start != "0100":
            print(start)
            self.dataGrid.AppendRows(1)
            cur = self.dataGrid.GetNumberRows() - 1
            self.dataGrid.SetCellValue(cur, 0, start)
            start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()

class CodeTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.SetSize(700,500)
        self.SetBackgroundColour("WHITE")

        # INITIALIZE  CODE EDITOR
        self.codeEditor = wx.TextCtrl(self, style = wx.TE_MULTILINE, pos=(10,10), size=(390,400))

        # INITIALIZE TABLE FOR OPCODES
        wx.StaticText(self, label="OpCodes", pos=(410,10))
        self.opcodeGrid = grid.Grid(self, pos = (410,30), size=(290,150))
        self.opcodeGrid.CreateGrid(0, 2)
        self.opcodeGrid.SetColLabelValue(0, "Instruction")
        self.opcodeGrid.SetColLabelValue(1, "Opcode")

        # INITIALIZE LOAD BUTTON
        self.loadBtn = wx.Button(self, label="Load", pos=(10,415), size=(100,25))
        self.loadBtn.Bind(wx.EVT_BUTTON, self.test)

        self.instructions = ["ld","sd","daddiu","daddu","bc","bgec","slti",".code",".data",":"]
        self.instructions = [word.upper() for word in self.instructions]

    def test(self, e):
        self.lines = self.codeEditor.GetValue().split("\n")

        # REMOVE EMPTY LINES AND COMMENTS
        while "" in self.lines:
            self.lines.remove("")
        for i in range(len(self.lines) - 1, -1, -1):
            if ";" in self.lines[i]:
                del self.lines[i]

        self.lines = [word.upper() for word in self.lines]

        # SEGREGATES DATA PORTION FROM CODE PORTION
        if ".DATA" not in self.lines:
            self.code = self.lines
            self.data = None
        elif ".CODE" not in self.lines:
            self.code = None
            self.data = self.lines
        else:
            self.code = self.lines[self.lines.index(".CODE"):]
            self.data = self.lines[:self.lines.index(".CODE")]
        
        # FUNCTION TO DETERMINE MEMORY ADDRESSES
        self.dataMemory = {}
        self.dataRepresentation = {}
        self.codeMemory = {}
        self.getMemory()

        # CHECKS SYNTAX
        if (self.checkSyntax() and len(self.lines) > 0):

            # FUNCTION TO DETERMINE OPCODES
            self.opcodes = {}
            self.getOpcodes()

            # OUTPUT RESULTS TO CONSOLE
            
            
            print("----------")
            print("CODE MEMORY")
            print(self.codeMemory)
            print("----------")
            print("DATA MEMORY")
            print(self.dataMemory)
            print("----------")
            print("DATA Representation")
            print(self.dataRepresentation)
            print("----------")
            for i in range(0,len(self.lines)):
                line = self.lines[i]
                print("Line " + str(i + 1)  + ": " + line + " : " + self.opcodes[line])
            print("----------")
            
            

            # TELLS MAINFRAME TO UPDATE THE MAIN TAB
            self.parent.GetParent().GetParent().updateMain(self.opcodes, self.code, self.codeMemory, self.dataMemory, self.data, self.dataRepresentation)
            self.updateOpcodes(self.opcodes,self.code)
        else:
            wx.MessageBox('Please recheck your code', 'ERROR: Invalid Syntax', wx.OK | wx.ICON_INFORMATION)

    def checkSyntax(self):
        for line in self.lines:
            valid = False
            for instruction in self.instructions:
                if instruction in line:
                    valid = True
            if not valid:
                return False
        return True

    def getOpcodes(self):
        for line in self.lines:
            if "DADDIU" in line or "SD" in line or "LD" in line or "BGEC" in line or "SLTI" in line:
                self.opcodes[line] = self.IType(line)
            elif "DADDU" in line:
                self.opcodes[line] = self.RType(line)
            elif "BC" in line:
                self.opcodes[line] = self.JType(line)
            else:
                self.opcodes[line] = "NO OPCODE"

    # RETURNS OPCODE FOR I-TYPE
    def IType(self, line):
        opcode = ""

        if "DADDIU" in line:
            args = line.split("DADDIU ")[1].split(",")
            opcode += "011001"
        elif "SD" in line:
            args = line.split("SD ")[1].split(",")
            opcode += "111111"
        elif "LD" in line:
            args = line.split("LD ")[1].split(",")
            opcode += "110111"
        elif "BGEC" in line:
            args = line.split("BGEC ")[1].split(",")
            opcode += "010110"
        elif "SLTI" in line:
            args = line.split("SLTI ")[1].split(",")
            opcode += "001010"

        if "DADDIU" in line or "SLTI" in line:
            rs = args[1].strip()
            rs = ''.join(filter(lambda x: x.isdigit(), rs))
            opcode += '{0:05b}'.format(int(rs))

            rt = args[0].strip()
            rt = ''.join(filter(lambda x: x.isdigit(), rt))
            opcode += '{0:05b}'.format(int(rt))

            imm = args[2].strip()
            imm = imm.replace("#","")
            opcode += bin(int(imm, 16))[2:].zfill(16)
        elif "SD" in line or "LD" in line:
            base = args[1].strip().split("(")[1].replace(")","")
            base = ''.join(filter(lambda x: x.isdigit(), base))
            opcode += '{0:05b}'.format(int(base))

            rt = args[0].strip()
            rt = ''.join(filter(lambda x: x.isdigit(), rt))
            opcode += '{0:05b}'.format(int(rt))

            offset = args[1].strip().split("(")[0]
            for line in self.dataMemory:
                if offset in line:
                    offset = self.dataMemory[line]
                    break

            offset = bin(int(offset,16)).split("b")[1].zfill(16)
            opcode += offset
        elif "BGEC" in line:
            rs = args[0].strip()
            rs = ''.join(filter(lambda x: x.isdigit(), rs))
            opcode += '{0:05b}'.format(int(rs))

            rt = args[1].strip()
            rt = ''.join(filter(lambda x: x.isdigit(), rt))
            opcode += '{0:05b}'.format(int(rt))

            start = self.lines.index(line)
            for l in self.lines:
                if args[2].strip() + ":" in l:
                    end = self.lines.index(l)
            offset = end - start - 1

            # CONSIDER 2's COMPLEMENT WHEN OFFSET IS NEGATIVE
            if offset >= 0:
                opcode += '{0:016b}'.format(int(offset))
            else:
                opcode += bin(((1 << 16) - 1) & offset).split("b")[1]

        opcode = hex(int(opcode,2)).split("x")[1].zfill(8).upper()
        return opcode

    # RETURNS OPCODE FOR R-TYPE
    def RType(self, line):
        opcode = ""

        if "DADDU" in line:
            args = line.split("DADDU ")[1].split(",")
            opcode += "000000"

            rs = args[1].strip()
            rs = ''.join(filter(lambda x: x.isdigit(), rs))
            opcode += '{0:05b}'.format(int(rs))

            rt = args[2].strip()
            rt = ''.join(filter(lambda x: x.isdigit(), rt))
            opcode += '{0:05b}'.format(int(rt))

            rd = args[0].strip()
            rd = ''.join(filter(lambda x: x.isdigit(), rd))
            opcode += '{0:05b}'.format(int(rd))

            opcode += "00000"
            opcode += "101101"

        opcode = hex(int(opcode,2)).split("x")[1].zfill(8).upper()
        return opcode

    # RETURNS OPCODE FOR J-TYPE
    def JType(self, line):
        opcode = ""

        if "BC" in line:
            args = line.split("BC ")[1]
            opcode += "110010"

            start = self.lines.index(line)
            for l in self.lines:
                if args[1].strip() + ":" in l:
                    end = self.lines.index(l)
            offset = end - start - 1

            # CONSIDER 2's COMPLEMENT WHEN OFFSET IS NEGATIVE
            if offset >= 0:
                opcode += '{0:016b}'.format(int(offset))
            else:
                opcode += bin(((1 << 16) - 1) & offset).split("b")[1]

        opcode = hex(int(opcode,2)).split("x")[1].zfill(8).upper()
        return opcode

    def getMemory(self):
        # STARTING FROM 0000, INCREASES BY 8 BYTES PER DATA SEGMENT
        if self.data is not None:
            start = "0000"
            for i in range(1,len(self.data)):
                self.dataMemory[self.data[i]] = start

                args = self.data[i].split(" ")
                data = args[2]
                if args[1] == ".WORD64":
                    data = data.replace("#","")
                    data = data.zfill(16)

                    print(data)
                elif args[1] == ".ASCIIZ":
                    data = data.replace('"','')
                    temp = ""
                    for letter in data:
                        temp = hex(ord(letter)).split("x")[1] + temp
                    data = temp.zfill(16).upper()
                    print(data)
                
                while len(data) > 0:
                    toStore = data[-2:]
                    self.dataRepresentation[start] = toStore
                    start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()
                    data = data[:-2]


        # STARTING FROM 0100, INCREASES BY 4 BYTES PER CODE SEGMENT
        if self.code is not None:
            start = "0100"
            for i in range(1,len(self.code)):
                self.codeMemory[self.code[i]] = start
                start = hex(int(start,16) + 4).split("x")[1].zfill(4).upper()

    def updateOpcodes(self, opcodes, codes):
        # EMPTY GRID
        if self.opcodeGrid.GetNumberRows() > 0:
            self.opcodeGrid.DeleteRows(0, self.opcodeGrid.GetNumberRows())

        # ADDS NEW ROW FOR EACH LINE OF INSTRUCTION
        for line in codes:
            self.opcodeGrid.AppendRows(1)
            cur = self.opcodeGrid.GetNumberRows() - 1
            self.opcodeGrid.SetCellValue(cur, 0, line)
            self.opcodeGrid.SetCellValue(cur, 1, opcodes[line])
            self.opcodeGrid.SetReadOnly(cur, 0, True)
            self.opcodeGrid.SetReadOnly(cur, 1, True)
            self.opcodeGrid.AutoSizeColumns(True)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        style = wx.DEFAULT_FRAME_STYLE
        super(MainFrame, self).__init__(*args, **kwargs, style = style)
        self.initialize()

    def initialize(self):
        # ~AESTHETICS~
        self.SetSize(725,575)
        self.mainPanel = wx.Panel(self)
        self.SetTitle("microMIPS")
        self.SetBackgroundColour("WHITE")
        
        # ADD HEADER PHOTO
        imgHeader = wx.Image("header.jpg", wx.BITMAP_TYPE_ANY).Scale(525,50)
        imgHeader = wx.Bitmap(imgHeader)
        self.header = wx.StaticBitmap(self.mainPanel, -1, imgHeader, (0,5), (500,40))
        
        self.nb = wx.Notebook(self.mainPanel, pos=(0,50), size=(725,500))
        self.CTab = CodeTab(self.nb)
        self.MTab = MainTab(self.nb)
        self.nb.AddPage(self.CTab, "Load/View")
        self.nb.AddPage(self.MTab, "Main")

        self.SetPosition((300,200))
        self.Show()

    # CALLS UPDATE METHODS IN MAIN WITH THE UPDATED INFO
    def updateMain(self, opcodes, codes, codeMemory, dataMemory, data, dataRepresentation):
        self.MTab.resetRegisters()
        if codes is not None:
            self.MTab.updateCode(opcodes, codes, codeMemory, dataRepresentation)
        if data is not None:
            self.MTab.updateData(dataMemory, data, dataRepresentation)
        self.MTab.prepareCycles(codeMemory, dataMemory, opcodes)
        self.nb.SetSelection(1)

def main():
	app = wx.App()
	MainFrame(None)
	app.MainLoop()

main()