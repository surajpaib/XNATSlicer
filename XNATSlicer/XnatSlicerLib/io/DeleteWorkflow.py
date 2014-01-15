# python
import os
import sys
import shutil
import zipfile

# application
from __main__ import qt


    
class DeleteWorkflow(object):
    """ 
    XnatDeletedWorkflow conducts the necessary steps to delete
    a folder or a file from a given XNAT host.  The ability to delete
    either depends on the user's priveleges determined both by the 
    projects and the XNAT host.


    TODO: Consider setting the current item to the deleted 
    sibling above or below it.  If no siblings, then go to parent.
    """
    
    def __init__(self, MODULE, uriName):
        """ Init function.
        """

        #--------------------
        # The MODULE
        #--------------------
        self.MODULE = MODULE


        
        #--------------------
        # The Dialog box.  If the user 'OK's the delete
        # it calls on 'DeleteWorkflow.beginWorkflow'
        #--------------------
        self.deleteDialog = qt.QMessageBox()
        self.deleteDialog.setIcon(qt.QMessageBox.Warning)
        self.deleteDialog.setText("Are you sure you want to delete the '%s' from Xnat?"%(uriName))   
        self.deleteDialog.connect('buttonClicked(QAbstractButton*)', self.beginWorkflow)
        self.deleteDialog.addButton(qt.QMessageBox.Ok)
        self.deleteDialog.addButton(qt.QMessageBox.Cancel)  


        
        
    def beginWorkflow(self, button = None):
        """ Main function for the class.
        """

        #--------------------
        # If there's no button argument, then exit out of function
        # by showing the deleteDialog.
        #--------------------
        if not button:
            self.deleteDialog.show()

            
        #--------------------
        # If 'ok' pressed in the deleteDialog...
        #--------------------
        elif button and 'ok' in button.text.lower(): 
            
            #
            # Construct the full delete string based on type of tree item deleted
            #
            delStr = self.MODULE.View.getXnatUri()
            #print "delStr", delStr

            if not '/files/' in delStr:
                delStr = os.path.dirname(delStr)
                
            #
            # Call delete XnatIo's 'delete' function.
            #
            self.MODULE.XnatIo.delete(delStr)

            
            #
            # Set currItem to parent of deleted item and expand it. 
            #
            self.MODULE.View.removeCurrItem()



        #--------------------
        # Cancel workflow if 'Cancel' button was pressed.
        #--------------------
        elif button and button.text.lower().find('cancel') > -1:
             return
