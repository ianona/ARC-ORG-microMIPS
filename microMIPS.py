import wx

class CodeTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.SetSize(500,500)
        self.SetBackgroundColour("WHITE")

        # INITIALIZE  CODE EDITOR
        self.codeEditor = wx.TextCtrl(self, style = wx.TE_MULTILINE, pos=(10,10), size=(400,400))

        # INITIALIZE TEST BUTTON
        self.sendFileBtn = wx.Button(self, label="test", pos=(10,415), size=(100,25))
        self.sendFileBtn.Bind(wx.EVT_BUTTON, self.test)

    def test(self, e):
        code = self.codeEditor.GetValue()
        lines = code.split("\n")

        while "" in lines:
            lines.remove("")

        for i in range(len(lines) - 1, -1, -1):
            if ";" in lines[i]:
                del lines[i]
            
        lines = [line.lower() for line in lines]

        print("----------")
        for i in range(0,len(lines)):
            print("Line " + str(i + 1)  + ": " + lines[i])
        print("----------")

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        style = wx.DEFAULT_FRAME_STYLE
        super(MainFrame, self).__init__(*args, **kwargs, style = style)
        self.initialize()

    def initialize(self):
        # ~AESTHETICS~
        self.SetSize(525,525)
        self.mainPanel = wx.Panel(self)
        self.SetBackgroundColour("WHITE")
        
        self.nb = wx.Notebook(self.mainPanel, pos=(0,0), size=(525,500))
        self.CTab = CodeTab(self.nb)
        self.nb.AddPage(self.CTab, "Code Tab")

        self.SetPosition((300,200))
        self.Show()

def main():
	app = wx.App()
	MainFrame(None)
	app.MainLoop()

main()