"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke
 *             @version:   0.9
 *                @date:   16.04.2021
 ******************************************************************************/
/**        Testerlotzi
 *
 ****
"""


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

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


class Scene:
    """
        OpenGL 2D scene class
    """
    # initialization

    def __init__(self, width, height,
                 polygon_A=np.array([0, 0]), polygon_B=np.array([0, 0]),
                 scenetitle="2D Scene"):
        # time
        self.t = 0
        self.dt = 0.01
        self.scenetitle = scenetitle
        self.pointsize = 7
        self.linewidth = 3
        self.width = width
        self.height = height
        self.polygon_A = polygon_A
        self.polygon_B = polygon_B
        self.rendered_polygon = polygon_A
        self.forward_animation = False
        self.backward_animation = False


    #selbst gefrickel
    def getMorphedPoint(self,points):
        """Nimmt ein Tupel zweier Punkte an und gibt den gemorphten Punkt zur�ck"""
       
        x = (1-self.t)*points[0][0] + self.t*points[1][0]
        y = (1-self.t)*points[0][1] + self.t*points[1][1]
        #print("Time: {} ?????".format(self.t))
        return [x, y]


    def getMorphedPolygon(self):
        """erzeugt das passend zur Zeit gemorphte Polygon"""
        return [self.getMorphedPoint(points) for points in zip(self.polygon_A, self.polygon_B)]

    # set scene dependent OpenGL states

    def setOpenGLStates(self):
        glPointSize(self.pointsize)
        glLineWidth(self.linewidth)

    # step

    def step(self):
        # TODO 4:
        # - interpolate:
        # - rendered_polygon = (1-self.t)*polygon_A + self.t*polygon_B
        #self.rendered_polygon = polygon_A
        self.rendered_polygon = self.getMorphedPolygon()

    # animation

    def animation(self):
        if self.forward_animation:
            self.t += self.dt
            if self.t >= 1:
                self.t = 1
                self.forward_animation = False

        if self.backward_animation:
            self.t -= self.dt
            if self.t <= 0:
                self.t = 0
                self.backward_animation = False

        self.step()

    # render

    def render(self):
        # set color to blue
        glColor(0.0, 0.0, 1.0)

        self.animation()

        # render points
        glBegin(GL_POINTS)
    
        for p in self.rendered_polygon:
            glVertex2fv(p)
        glEnd()

        # render polygon
        glBegin(GL_LINE_LOOP)
        for p in self.rendered_polygon:
            glVertex2fv(p)
        glEnd()

    # set polygon A

    def set_polygon_A(self, polygon):
        self.polygon_A = np.copy(polygon)

    # set polygon B

    def set_polygon_B(self, polygon):
        self.polygon_B = np.copy(polygon)


class RenderWindow:
    """
        GLFW Rendering window class
        YOU SHOULD NOT EDIT THIS CLASS!
    """

    def __init__(self, scene):

        # save current working directory
        cwd = os.getcwd()

        # Initialize the library
        if not glfw.init():
            return

        # restore cwd
        os.chdir(cwd)

        # version hints
        #glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        #glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        #glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        #glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # buffer hints
        glfw.window_hint(glfw.DEPTH_BITS, 32)

        # define desired frame rate
        self.frame_rate = 100

        # make a window
        self.width, self.height = scene.width, scene.height
        self.aspect = self.width/float(self.height)
        self.window = glfw.create_window(
            self.width, self.height, scene.scenetitle, None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # initialize GL
        glViewport(0, 0, self.width, self.height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glOrtho(-self.width/2, self.width/2, -
                self.height/2, self.height/2, -2, 2)
        glMatrixMode(GL_MODELVIEW)

        # set window callbacks
        glfw.set_mouse_button_callback(self.window, self.onMouseButton)
        glfw.set_key_callback(self.window, self.onKeyboard)
        glfw.set_window_size_callback(self.window, self.onSize)

        # create scene
        self.scene = scene  # Scene(self.width, self.height)
        self.scene.setOpenGLStates()

        # exit flag
        self.exitNow = False

        # animation flags
        self.forward_animation = False
        self.backward_animation = False

    def onMouseButton(self, win, button, action, mods):
        print("mouse button: ", win, button, action, mods)

    def onKeyboard(self, win, key, scancode, action, mods):
        print("keyboard: ", win, key, scancode, action, mods)
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exitNow = True
            if key == glfw.KEY_F:
                # Forward animation
                self.scene.forward_animation = True
            if key == glfw.KEY_B:
                # Backward animation
                self.scene.backward_animation = True

    def onSize(self, win, width, height):
        print("onsize: ", win, width, height)
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)

    def run(self):
        # initializer timer
        glfw.set_time(0.0)
        t = 0.0
        while not glfw.window_should_close(self.window) and not self.exitNow:
            # update every x seconds
            currT = glfw.get_time()
            if currT - t > 1.0/self.frame_rate:
                # update time
                t = currT
                # clear viewport
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                # render scene
                self.scene.render()
                # swap front and back buffer
                glfw.swap_buffers(self.window)
                # Poll for and process events
                glfw.poll_events()
        # end
        glfw.terminate()


def transformLocalToGlobal(point):
    """Transformiert die lokalen  in die globalen Koordinaten"""
    width, height = 640, 480
    return np.array([point[0] * (-width / 2.5), point[1]*height / 2.5])


def readInPolygon(file):
    # einlesen der einzelnen Zeilen
    rawpoints = [l.split() for l in open(file).readlines()]
    # tuples aus rawpoints erzeugen bsp. from ['0.277080', '0.086289'] to (0.277080, 0.086289)
    pointTuples = list(
        map(lambda point: (float(point[0]), float(point[1])), rawpoints))
    # tuples nach np.array
    #pointsAsArray = list(map(lambda point: np.array([point[0], point[1]]) , pointTuples))
    pointsAsArray = list(map(transformLocalToGlobal, pointTuples))

    return pointsAsArray


# main
if __name__ == '__main__':
    """
    if len(sys.argv) != 3:
       print("morph.py firstPolygon secondPolygon")
       print("pressing 'F' should start animation morphing from first polygon to second")
       print("pressing 'B' should start animation morphing from second polygon back to first")
       sys.exit(-1)
    """
    # set size of render viewport
    width, height = 640, 480

    # TODO 1:
    # - read in polygons
    polygon_A = [np.array([-width/2.5, 0]), np.array([width/2.5, 0])]
    polygon_B = [np.array([0, -height/2.5, 0]), np.array([0, height/2.5])]

    polygon_A = readInPolygon('polygonA.dat')
    polygon_B = readInPolygon('polygonZ.dat')
   
    print("Polygon_A = {}".format(polygon_A))
    print("Polygon_B = {}".format(polygon_B))

    # TODO 2:
    # - make both polygons contain same number of points

    while len(polygon_A) != len(polygon_B):
        if len(polygon_A) < len(polygon_B):
            polygon_A.append(polygon_A[-1])
        else:
            polygon_B.append(polygon_B[-1])


    # TODO 3:
    # - transform from local into global coordinate system

    # instantiate a scene
    scene = Scene(width, height, polygon_A, polygon_B, "Morphing Template")

    # pass the scene to a render window
    rw = RenderWindow(scene)
    rw.run()
