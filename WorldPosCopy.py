### World Position Copy#
# This plugin aims to copy the world coordinates of selected objects
# from the previous frame, and apply them in the current frame. This
# operates as a psuedo-solution for IK-FK snapping on a specific rig

import bpy
from bge import logic

cScene = logic.getCurrentScene()
cController = logic.getCurrentController()
