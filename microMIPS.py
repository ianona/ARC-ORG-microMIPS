import wx
import wx.grid as grid
import time

class UtilitiesTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.SetSize(700,500)
        self.SetBackgroundColour("WHITE")

        registers=[]
        for i in range(1,32):
            registers.append("R"+str(i))
        self.regCmb = wx.ComboBox(self, choices=registers,style=wx.CB_READONLY | wx.CB_DROPDOWN,pos=(10,20))
        self.regBox = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER, pos=(100,20), size=(190,25))
        self.regBox.Bind(wx.EVT_TEXT_ENTER, self.addReg)
        wx.StaticText(self, label="Inputted Register Values:", pos=(10,50))
        self.regLog = wx.TextCtrl(self, style = wx.TE_READONLY | wx.TE_MULTILINE, pos=(10,80), size=(280,150))

        dataAddr=[]
        start="0000"
        while start != "0100":
            dataAddr.append(start)
            start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()
        self.dataCmb = wx.ComboBox(self, choices=dataAddr,style=wx.CB_READONLY | wx.CB_DROPDOWN,pos=(320,20))

        self.dataBox = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER, pos=(420,20), size=(180,25))
        self.dataBox.Bind(wx.EVT_TEXT_ENTER, self.addData)
        wx.StaticText(self, label="Inputted Data Values:", pos=(320,50))
        self.dataLog = wx.TextCtrl(self, style = wx.TE_READONLY | wx.TE_MULTILINE, pos=(320,80), size=(280,150))

        self.loadBtn = wx.Button(self, label="Load", pos=(250,250), size=(120,25))
        self.loadBtn.Bind(wx.EVT_BUTTON, self.load)
        self.resetBtn = wx.Button(self, label="Reset", pos=(250,280), size=(120,25))
        self.resetBtn.Bind(wx.EVT_BUTTON, self.reset)

    def load(self, e):
        r = self.regLog.GetValue().split("\n")
        while "" in r:
            r.remove("")

        registers={}
        for reg in r:
            register = reg.split(": ")[0]
            val = reg.split(": ")[1]
            registers[register] = val

        d = self.dataLog.GetValue().split("\n")
        while "" in d:
            d.remove("")

        data={}
        for entry in d:
            addr = entry.split(": ")[0]
            val = entry.split(": ")[1]
            data[addr] = val

        self.regBox.SetValue("")
        self.regLog.SetValue("")
        self.dataBox.SetValue("")
        self.dataLog.SetValue("")
        self.dataCmb.SetSelection(0)
        self.regCmb.SetSelection(0)
        self.parent.GetParent().GetParent().setUtility(data, registers)

    def reset(self,e):
        self.regBox.SetValue("")
        self.regLog.SetValue("")
        self.dataBox.SetValue("")
        self.dataLog.SetValue("")
        self.dataCmb.SetSelection(0)
        self.regCmb.SetSelection(0)
        self.parent.GetParent().GetParent().reset()

    def addReg(self,e):
        reg = self.regCmb.GetStringSelection()
        val = self.regBox.GetValue()
        if val != "" and len(val) < 17 and self.isHex(val):
            while len(val) < 16:
                val = "0"+val

            val = val.upper()
            self.regLog.AppendText(reg+": "+val+"\n")
            self.regBox.SetValue("")
        else:
            wx.MessageBox('Value cannot be empty and must be composed of 16 or less hex values', 'ERROR: Invalid Value', wx.OK | wx.ICON_INFORMATION)

    def addData(self,e):
        addr = self.dataCmb.GetStringSelection()
        val = self.dataBox.GetValue()

        if len(val) < 3 and self.isHex(val) and val != "":
            while len(val) < 2:
                val = "0"+val
            val=val.upper()
            self.dataLog.AppendText(addr+": "+val+"\n")
            self.dataBox.SetValue("")
        else:
            wx.MessageBox('Value cannot be empty and must be composed of 2 or less hex values', 'ERROR: Invalid Value', wx.OK | wx.ICON_INFORMATION)

    def isHex(self,value):
        try:
            int(value,16)
            return True
        except:
            return False

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
        self.codeGrid = grid.Grid(self, pos = (0,20), size=(320,200))
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
        

        # INITIALIZE TABLE FOR OUTPUT
        wx.StaticText(self, label="Output", pos=(470,0))
        self.outGrid = grid.Grid(self, pos = (470,20), size=(220,450))
        self.outGrid.CreateGrid(0, 2)
        self.outGrid.SetColLabelValue(0, "Cycle")
        self.outGrid.SetColLabelValue(1, "Value")
        self.outGrid.SetRowLabelSize(0)

        self.resetRegisters()

        # INITIALIZE RUN BUTTON
        self.runBtn = wx.Button(self, label="Run Cycle", pos=(460,390), size=(120,25))
        self.runBtn.Bind(wx.EVT_BUTTON, self.run)
        self.runBtn.Hide()

        # INITIALIZE RUN ALL BUTTON
        self.runAllBtn = wx.Button(self, label="Run All Cycles", pos=(460,415), size=(120,25))
        self.runAllBtn.Bind(wx.EVT_BUTTON, self.runAll)
        self.runAllBtn.Hide()

    def displayOutput(self):
        if self.outGrid.GetNumberRows() > 0:
            self.outGrid.DeleteRows(0, self.outGrid.GetNumberRows())

        headers = ["IF","IR","NPC","ID","A","B","IMM","EX","ALUOutput","CONDITION","MEM","PC","LMD","MemoryAffected","WB","Rn"]
        self.outGrid.AppendRows(16)
        for i in range(0,len(headers)):
            self.outGrid.SetCellValue(i, 0, headers[i])

        self.output = [str(x) for x in self.output]

        self.outGrid.SetCellValue(1, 1, self.output[0])
        self.outGrid.SetCellValue(2, 1, self.output[1])

        self.outGrid.SetCellValue(4, 1, self.output[2])
        self.outGrid.SetCellValue(5, 1, self.output[3])
        self.outGrid.SetCellValue(6, 1, self.output[4])

        self.outGrid.SetCellValue(8, 1, self.output[5])
        self.outGrid.SetCellValue(9, 1, self.output[6])

        self.outGrid.SetCellValue(11, 1, self.output[7])
        self.outGrid.SetCellValue(12, 1, self.output[8])
        self.outGrid.SetCellValue(13, 1, self.output[9])

        self.outGrid.SetCellValue(15, 1, self.output[10])
        self.outGrid.AutoSizeColumns(True)

    def resetRegisters(self):
        for i in range(0,32):
            self.regGrid.AppendRows(1)
            self.regGrid.SetCellValue(i, 0, str(i))
            self.regGrid.SetCellValue(i, 1, "0000000000000000")
            self.regGrid.SetReadOnly(i, 0, True)
            self.regGrid.SetReadOnly(i, 1, True)
            self.regGrid.AutoSizeColumns(True)

        if self.dataGrid.GetNumberRows() > 0:
            self.dataGrid.DeleteRows(0, self.dataGrid.GetNumberRows())
        # SET EMPTY DATA ROWS
        start = "0000"     
        while start != "0100":
            self.dataGrid.AppendRows(1)
            cur = self.dataGrid.GetNumberRows() - 1
            self.dataGrid.SetCellValue(cur, 0, start)
            self.dataGrid.AutoSizeColumns(True)
            start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()

        if self.codeGrid.GetNumberRows() > 0:
            self.codeGrid.DeleteRows(0, self.codeGrid.GetNumberRows())

        if self.outGrid.GetNumberRows() > 0:
            self.outGrid.DeleteRows(0, self.outGrid.GetNumberRows())

        self.outGrid.AppendRows(16)
        headers = ["IF","IR","NPC","ID","A","B","IMM","EX","ALUOutput","CONDITION","MEM","PC","LMD","MemoryAffected","WB","Rn"]
        for i in range(0,len(headers)):
            self.outGrid.SetCellValue(i, 0, headers[i])
        self.outGrid.AutoSizeColumns(True)

    def run(self, e):
        self.output = []
        line = self.MEMORY[self.PC]
        print("now cycling " + line + " : " + self.PC)

        # CYCLE 1: IF (instruction fetch cycle)
        self.IR = self.OPCODES[self.PC]
        self.opcodeBin = bin(int(self.IR,16)).split("b")[1].zfill(32)
        self.NPC = hex(int(self.PC,16) + 4).split("x")[1].zfill(4)

        self.output.append(self.IR)
        self.output.append(self.NPC)

        # CYCLE 2: ID (instruction decode cycle)
        # NUMBER OF REGISTER
        self.regA = int(self.opcodeBin[6:11],2)
        self.regB = int(self.opcodeBin[11:16],2)
        # GETS ACTUAL VALUE INSIDE REGISTER
        self.A = self.regGrid.GetCellValue(self.regA, 1)
        self.B = self.regGrid.GetCellValue(self.regB, 1)
        self.IMM = hex(int(self.opcodeBin[16:32],2)).split("x")[1].zfill(16)

        self.output.append(self.A)
        self.output.append(self.B)
        self.output.append(self.IMM)

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
        self.PC=self.PC.upper()

        self.output.append(self.ALUOutput)
        self.output.append(self.COND)

        self.output.append(self.PC)
        self.output.append(self.LMD)
        self.output.append(self.MemoryAffected)

        self.output.append(self.Rn)
        self.displayOutput()

        # R0 IS ALWAYS 0
        self.regGrid.SetCellValue(0, 1, "0000000000000000")
        # IF DONE RUNNING INSTRUCTIONS
        if self.PC not in self.MEMORY:
            self.runBtn.Hide()
            self.runAllBtn.Hide()

    def runAll(self, e):
        while self.PC in self.MEMORY:
            self.output = []
            line = self.MEMORY[self.PC]
            print("now cycling " + line + " : " + self.PC)

            # CYCLE 1: IF (instruction fetch cycle)
            self.IR = self.OPCODES[self.PC]
            self.opcodeBin = bin(int(self.IR,16)).split("b")[1].zfill(32)
            self.NPC = hex(int(self.PC,16) + 4).split("x")[1].zfill(4)

            self.output.append(self.IR)
            self.output.append(self.NPC)

            # CYCLE 2: ID (instruction decode cycle)
            # NUMBER OF REGISTER
            self.regA = int(self.opcodeBin[6:11],2)
            self.regB = int(self.opcodeBin[11:16],2)
            # GETS ACTUAL VALUE INSIDE REGISTER
            self.A = self.regGrid.GetCellValue(self.regA, 1)
            self.B = self.regGrid.GetCellValue(self.regB, 1)
            self.IMM = hex(int(self.opcodeBin[16:32],2)).split("x")[1].zfill(16)

            self.output.append(self.A)
            self.output.append(self.B)
            self.output.append(self.IMM)

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
            self.PC=self.PC.upper()

            self.output.append(self.ALUOutput)
            self.output.append(self.COND)

            self.output.append(self.PC)
            self.output.append(self.LMD)
            self.output.append(self.MemoryAffected)

            self.output.append(self.Rn)
            self.displayOutput()

            # R0 IS ALWAYS 0
            self.regGrid.SetCellValue(0, 1, "0000000000000000")

            
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
        self.LMD = "N/A"
        self.MemoryAffected = "N/A"
        self.Rn = self.ALUOutput

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

        # GIVE ME VALUES
        self.LMD = "N/A"
        self.MemoryAffected = "N/A"
        self.Rn = self.ALUOutput

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
        print("B = " + self.B)
        tempB = self.B
        addressRow = 0
        self.MemoryAffected = []
        if int(dataToStore, 16) is not 0:
            addressRow = 1000 % int(dataToStore, 16)
        for i in range(8):
            self.MemoryAffected.append(dataToStore)
            tempByte = tempB[-2:]
            print("Storing " + tempByte)
            self.dataRepresentation[dataToStore] = tempByte
            dataToStore = hex(int(dataToStore, 16) + 1).split("x")[1].zfill(4)
            tempB = tempB[:-2]
            self.dataGrid.SetCellValue(int(dataToStore, 16) - 1, 1, tempByte)
            addressRow = addressRow + 1

        # GIVE ME VALUES
        self.LMD = "N/A"
        #self.MemoryAffected = "ZACH/KYLE GIVE ME A VALUE"
        self.Rn = "N/A"
        

        print("DATA REPRESENTATION")
        print(self.dataRepresentation)
        # CYCLE 5: WB (write-back cycle)
        
        
    def ld(self, line):
        self.ALUOutput = bin(int(self.A,16) + int(self.IMM,16)).split("b")[1]
        print("ALUOutput: " + self.ALUOutput)
        self.COND = 0
        
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC
        print("DATA REPRESENTATION")
        print(self.dataRepresentation)
        dataToLoad = (self.IMM)[-4:].upper()
        
        self.LMD = ""
        for i in range(8):
            print("Data to Load: " + dataToLoad)
            self.LMD = self.dataRepresentation[dataToLoad] + self.LMD
            dataToLoad = hex(int(dataToLoad, 16) + 1).split("x")[1].zfill(4).upper()
        print("LMD")
        print(self.LMD)

        # GIVE ME VALUES
        #self.LMD = "ZACH/KYLE GIVE ME A VALUE"
        self.MemoryAffected = "N/A"
        self.Rn = self.LMD
        
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

        # GIVE ME VALUES
        self.LMD = "N/A"
        self.MemoryAffected = "N/A"
        self.Rn = "N/A"

        # CYCLE 5: WB (write-back cycle)

    def s64(self, value):
        return -(value & 0x8000) | (value & 0x7fff)

    def bgec(self, line):
        print(self.NPC)
        self.ALUOutput = hex(self.s64(int(self.NPC,16)) + (self.s64(int(self.IMM,16))* 4)).split("x")[1].zfill(4)
        print(self.ALUOutput)
        if(self.s64(int(self.A,16)) >= self.s64(int(self.B,16))):
           self.COND = 1
           self.PC = self.ALUOutput
        # CYCLE 4: MEM (memory access/branch completion cycle)
        else:
            self.COND = 0
            self.PC = self.NPC

        # GIVE ME VALUES
        self.LMD = "N/A"
        self.MemoryAffected = "N/A"
        self.Rn = "N/A"

        # CYCLE 5: WB (write-back cycle)

    def slti(self, line):
        if int(self.A, 16) < int(self.IMM, 16):
            self.ALUOutput = 1
        else:
            self.ALUOutput = 0
        # print("ALUOutput: " + self.ALUOutput)
        self.COND = 0
        # CYCLE 4: MEM (memory access/branch completion cycle)
        self.PC = self.NPC

        # GIVE ME VALUES
        self.LMD = "N/A"
        self.MemoryAffected = "N/A"
        self.Rn = str(self.ALUOutput).zfill(16)

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

        start = list(dataRepresentation.keys())[-1]
        start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()
        while start != "0100":
            self.dataGrid.AppendRows(1)
            cur = self.dataGrid.GetNumberRows() - 1
            self.dataGrid.SetCellValue(cur, 0, start)
            self.dataGrid.AutoSizeColumns(True)
            start = hex(int(start,16) + 1).split("x")[1].zfill(4).upper()

    def updateFromUtility(self, data, registers):
        for d in data:
            row = int(d,16)
            self.dataGrid.SetCellValue(row, 1, data[d])
        for r in registers:
            row = int(r.replace("R",""))
            self.regGrid.SetCellValue(row, 1, registers[r])

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
        self.resetBtn = wx.Button(self, label="Reset", pos=(120,415), size=(100,25))
        self.resetBtn.Bind(wx.EVT_BUTTON, self.reset)

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
            if self.code is not None:
                self.getOpcodes()
                for i in range(0,len(self.code)):
                    line = self.code[i]
                    print("Line " + str(i + 1)  + ": " + line + " : " + self.opcodes[line])
                self.updateOpcodes(self.opcodes,self.code)

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

            # TELLS MAINFRAME TO UPDATE THE MAIN TAB
            self.parent.GetParent().GetParent().updateMain(self.opcodes, self.code, self.codeMemory, self.dataMemory, self.data, self.dataRepresentation)
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

    def reset(self,e):
        self.parent.GetParent().GetParent().reset()
        self.clearOpcodes()

    def getOpcodes(self):
        for line in self.code:
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

    def clearOpcodes(self):
        # EMPTY GRID
        if self.opcodeGrid.GetNumberRows() > 0:
            self.opcodeGrid.DeleteRows(0, self.opcodeGrid.GetNumberRows())


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
        self.UTab = UtilitiesTab(self.nb)
        self.nb.AddPage(self.CTab, "Load/View")
        self.nb.AddPage(self.MTab, "Main")
        self.nb.AddPage(self.UTab, "Utilities")

        self.SetPosition((300,200))
        self.Show()

    # CALLS UPDATE METHODS IN MAIN WITH THE UPDATED INFO
    def updateMain(self, opcodes, codes, codeMemory, dataMemory, data, dataRepresentation):
        if codes is not None:
            self.MTab.updateCode(opcodes, codes, codeMemory, dataRepresentation)
        if data is not None:
            self.MTab.updateData(dataMemory, data, dataRepresentation)
        self.MTab.prepareCycles(codeMemory, dataMemory, opcodes)
        self.nb.SetSelection(1)

    def reset(self):
        self.MTab.resetRegisters()

    def setUtility(self,data,registers):
        self.MTab.updateFromUtility(data,registers)
        self.nb.SetSelection(1)

def main():
	app = wx.App()
	MainFrame(None)
	app.MainLoop()

main()
