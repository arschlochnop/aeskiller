#!/usr/bin/env python
# encoding: utf-8

"""
@time: 17-2-10 下午7:15
@author: Darkmelody(xx@nop.pw)
@version: 1.0.7
"""

import json, subprocess, time,base64

from burp import IBurpExtender
from burp import IMessageEditorTabFactory
from burp import IMessageEditorTab
from burp import IContextMenuFactory
from burp import ITab

# Java imports
from javax import swing
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import JMenuItem
from java.awt import GridBagLayout
from java import awt
from java.util import List, ArrayList

# Menu items
menuItems = {
    False: "Turn on AES Killer",
    True:  "Turn off AES Killer"
}

# Global Switch
_forceAES = False

class BurpExtender(IBurpExtender, IMessageEditorTabFactory, IContextMenuFactory,ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName('AES Killer')
        print 'AES Killer - 1.0.7\nBurp AES Auto en/decrypt\nmail:xx@nop.pw\n\n'
        self._jPanel = swing.JPanel()
        self._jPanel.setLayout(awt.GridBagLayout())
        self._jPanelConstraints = awt.GridBagConstraints()

        # Create panel for KEY info
        self._jLabelKEY = swing.JLabel("AES KEY:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 0
        self._jPanel.add(self._jLabelKEY, self._jPanelConstraints)

        self._jTextFieldKEY = swing.JTextField("3W7a5n4n5a7Sg.53", 35)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 0
        self._jPanel.add(self._jTextFieldKEY, self._jPanelConstraints)

        # Create panel for IV info
        self._jLabelIV = swing.JLabel("AES IV:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 1
        self._jPanel.add(self._jLabelIV, self._jPanelConstraints)

        self._jTextFieldIV = swing.JTextField("Must Decode By HEX!", 3)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 1
        self._jPanel.add(self._jTextFieldIV, self._jPanelConstraints)

        # Create panel for Mode info
        self._jLabelMODE = swing.JLabel("AES MODE:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 2
        self._jPanel.add(self._jLabelMODE, self._jPanelConstraints)

        self._jTextFieldMODE = swing.JTextField("padding7", 3)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 2
        self._jPanel.add(self._jTextFieldMODE, self._jPanelConstraints)

        # Create panel for par info
        self._jLabelPar = swing.JLabel("Parameters:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 3
        self._jPanel.add(self._jLabelPar, self._jPanelConstraints)

        self._jTextFieldPar = swing.JTextField("Target Parameters .e.q data|cryptdata|ret", 3)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 3
        self._jPanel.add(self._jTextFieldPar, self._jPanelConstraints)

        # Create panel for py path info
        self._jLabelPythonPath = swing.JLabel("Python Path:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 4
        self._jPanel.add(self._jLabelPythonPath, self._jPanelConstraints)

        self._jTextFieldPythonPath = swing.JTextField("/usr/bin/python2.7", 3)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 4
        self._jPanel.add(self._jTextFieldPythonPath, self._jPanelConstraints)

        # Create panel for script path info
        self._jLabelScriptPath = swing.JLabel("Script Path:")
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 0
        self._jPanelConstraints.gridy = 5
        self._jPanel.add(self._jLabelScriptPath, self._jPanelConstraints)

        self._jTextFieldScriptPath = swing.JTextField("/home/dark/tool/Burp/json-decoder/AESKiller.py", 3)
        self._jPanelConstraints.fill = awt.GridBagConstraints.HORIZONTAL
        self._jPanelConstraints.gridx = 1
        self._jPanelConstraints.gridy = 5
        self._jPanel.add(self._jTextFieldScriptPath, self._jPanelConstraints)

        callbacks.customizeUiComponent(self._jPanel)
        callbacks.addSuiteTab(self)

        callbacks.registerMessageEditorTabFactory(self)
        callbacks.registerContextMenuFactory(self)
        return

    def getTabCaption(self):
        return "AES Killer"
    def getUiComponent(self):
        return self._jPanel
    def setPython(self):
        pass

    def createNewInstance(self, controller, editable):
        return AES_KillerTab(self, controller, editable)

    def createMenuItems(self, IContextMenuInvocation):
        global _forceAES
        menuItemList = ArrayList()
        menuItemList.add(JMenuItem(menuItems[_forceAES], actionPerformed=self.onClick))

        return menuItemList

    def onClick(self, event):
        global _forceAES
        _forceAES = not _forceAES


class AES_KillerTab(IMessageEditorTab):
    def __init__(self, extender, controller, editable):
        self._extender = extender
        self._helpers = extender._helpers
        self._editable = editable
        self._txtInput = extender._callbacks.createTextEditor()
        self._txtInput.setEditable(editable)

    def printalert(self,alert):
        self._extender._callbacks.issueAlert(alert)
    def getTabCaption(self):
        return "AES Killer"

    def getUiComponent(self):
        return self._txtInput.getComponent()

    def isEnabled(self, content, isRequest):
        global _forceAES

        if isRequest:
            r = self._helpers.analyzeRequest(content)
        else:
            r = self._helpers.analyzeResponse(content)

        msg = content[r.getBodyOffset():].tostring()
        return True
        # for header in r.getHeaders():
        #     if header.lower().startswith("host:"):
        #         host = header.split(":")[1].lower()
        #         for allowedHost in self.setting['supportedHost']:
        #             if allowedHost == host.strip():
        #                 print "load " + host
        #                 return True
        # return False

    def evalshell(self, crypttype, hashstr):
        key = base64.b64encode(self._extender._jTextFieldKEY.getText().strip())
        if crypttype == 1:
            hashstr = base64.b64encode(hashstr)
        shell_str = "%s %s %s %s %s %s" % (self._extender._jTextFieldPythonPath.getText().strip(),
                                           self._extender._jTextFieldScriptPath.getText().strip(),str(key),
                                           self._extender._jTextFieldIV.getText().strip(),str(crypttype),hashstr)
        p = subprocess.Popen(shell_str,  stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE,shell = True)
        while p.poll() == None:
            time.sleep(0.01)
        result = p.stdout.read().strip()
        self.printalert(p.stderr.read().strip())
        return result

    def setMessage(self, content, isRequest):
        if content is None:
            self._txtInput.setText(None)
            self._txtInput.setEditable(False)
        else:
            if isRequest:
                r = self._helpers.analyzeRequest(content)
            else:
                r = self._helpers.analyzeResponse(content)

            msg = content[r.getBodyOffset():].tostring()
            #print "start decrypt"
            """
            Test json type
            """
            sign = 0
            try:
                msg = json.loads(msg)
                sign = 1
                for i in self._extender._jTextFieldPar.getText().strip().split('|'):
                    msg[i] = self.evalshell(2, msg[i])
                pretty_msg = json.dumps(msg, indent=4,ensure_ascii=False)
            except Exception,e:
                self.printalert(e.message)
            """
            Split POST Parameters
            """
            if sign == 0:
                try:
                    pretty_msg = ""
                    msg_tmp = msg.split("&")
                    for i in msg_tmp:
                        if i.strip() == "":
                            continue
                        par = i[:i.index("=")]
                        value = i[i.index("=")+1:]
                        if par in self._extender._jTextFieldPar.getText().strip().split('|'):
                            value = self.evalshell(2, value)
                        pretty_msg = pretty_msg + par +"="+ value +"&"

                except Exception,e:
                    self.printalert(e.message)
                    #print "problem parsing data in setMessage"
                    return

            self._txtInput.setText(pretty_msg)
            self._txtInput.setEditable(self._editable)

        self._currentMessage = content
        return

    def getMessage(self):
        if self._txtInput.isTextModified():
            
            pre_data = self._txtInput.getText().tostring()
            #print "start en"
            sign = 0
            try:
                pre_data = json.loads(pre_data)
                sign = 1
                for i in self._extender._jTextFieldPar.getText().strip().split('|'):
                    pre_data[i] = self.evalshell(1, pre_data[i])
                data = json.dumps(pre_data)
            except Exception,e:
                self.printalert(e.message)
            if sign == 0:
                try:
                    par_tmp = pre_data.split("&")
                    for i in par_tmp:
                        if i.strip() == "":
                            continue
                        par = i[:i.index("=")]
                        value = i[i.index("=")+1:]
                        if par in self._extender._jTextFieldPar.getText().strip().split('|'):
                            value = self.evalshell(1, value)
                        data = data + par +"="+ value +"&"
                except Exception,e:
                    self.printalert(e.message)
                    data = self._helpers.bytesToString(self._txtInput.getText())

            # Reconstruct request/response
            r = self._helpers.analyzeRequest(self._currentMessage)
            return self._helpers.buildHttpMessage(r.getHeaders(), self._helpers.stringToBytes(data))
        else:
            return self._currentMessage

    def isModified(self):
        return self._txtInput.isTextModified()

    def getSelectedData(self):
        return self._txtInput.getSelectedText()
