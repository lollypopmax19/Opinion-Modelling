import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import Global
import pickle
import time


normFac = None

class Dynamics:
    u = 0
    _sumConst = 0
    _uCache = None

    def __init__(self, network, view):
        normFac = (1.0 / Global.num_nodes)
        self._uCache = np.zeros(Global.num_nodes, dtype=np.float32)
        self.network = network
        self.view = view
        
        self.uCostCache = np.zeros(Global.num_iterations)

        self.qArray = np.zeros(Global.num_nodes, dtype=np.float32)
        self.setUpQArray()

        self.neighborMatrix = np.zeros((Global.num_nodes * Global.num_nodes), dtype=np.float32)
        self.setUpNeighborMatrix()

        self.edgeArray = np.zeros((Global.num_nodes), dtype = np.float32)
        self.setUpEdgeArray()

        _meinungen =  self.network.meinungen.astype(np.float32);

        if sum(self.qArray) == 0:
            raise ValueError("c_star too high!")

        for i in range(Global.num_nodes):
            self._sumConst += self.qArray[i] ** 2
        self._sumConst *= Global.dT

        if not glfw.init():
            raise Exception("GLFW konnte nicht initialisiert werden.")

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(640, 480, "Compute Shader", None, None)
        if not window:
            glfw.terminate()
            raise Exception("Fenster konnte nicht erstellt werden.")

        glfw.make_context_current(window)

        print("OpenGL Version:", glGetString(GL_VERSION).decode("utf-8"))
        print("GLSL Version:", glGetString(GL_SHADING_LANGUAGE_VERSION).decode("utf-8"))

        shader = compileShader(self.compute_shader_code, GL_COMPUTE_SHADER)
        program = compileProgram(shader)

        buffer1 = glGenBuffers(1)
        buffer2 = glGenBuffers(1)
        buffer3 = glGenBuffers(1)
        buffer4 = glGenBuffers(1)

        glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer1)
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.qArray.nbytes, self.qArray, GL_DYNAMIC_COPY)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer2)
        glBufferData(GL_SHADER_STORAGE_BUFFER, _meinungen.nbytes, _meinungen, GL_DYNAMIC_COPY)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer3)
        glBufferData(GL_SHADER_STORAGE_BUFFER, self._uCache.nbytes, self._uCache, GL_DYNAMIC_COPY)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer4)
        glBufferData(GL_SHADER_STORAGE_BUFFER, self.neighborMatrix.nbytes, self.neighborMatrix, GL_DYNAMIC_COPY)

        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, buffer1)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, buffer2)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, buffer3)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, buffer4)

        glUseProgram(program)

        #sei facNu sei average edge count der beeinflussten agents
        _maskArray = np.zeros(Global.num_nodes)
        for i in range(Global.num_nodes):
            if self.qArray[i] == 1:
                _maskArray[i] = self.edgeArray[i]
        _facNu = sum(_maskArray)  / sum(self.qArray)

        u_location = glGetUniformLocation(program, "u")
        dT_location = glGetUniformLocation(program, "dT")
        nu_location = glGetUniformLocation(program, "nu")
        wd_location = glGetUniformLocation(program, "W_D")
        n_location = glGetUniformLocation(program, "n")
        norm_location = glGetUniformLocation(program, "norm")
        sumConst_location = glGetUniformLocation(program, "sumCost")
        facNu_location = glGetUniformLocation(program, "facNu")

        glUniform1f(u_location, self.u)
        glUniform1f(dT_location, Global.dT)
        glUniform1f(nu_location, Global.nu)
        glUniform1f(wd_location, Global.W_D)
        glUniform1i(n_location, Global.num_nodes)
        glUniform1f(norm_location, normFac)
        glUniform1f(sumConst_location, self._sumConst)
        glUniform1f(facNu_location, _facNu)


        _stepCount = 0
        for i in range(Global.num_iterations):
            if self.calcEpsilon() > Global.epsilon:
                glDispatchCompute((Global.num_nodes + 255) // 256, 1, 1)
                glMemoryBarrier(GL_SHADER_STORAGE_BARRIER_BIT)

                #fetch results from buffer
                glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer2)
                _wArray = np.frombuffer(glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, _meinungen.nbytes), dtype=np.float32)

                glBindBuffer(GL_SHADER_STORAGE_BUFFER, buffer3)
                self._uCache = np.frombuffer(glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, self._uCache.nbytes), dtype=np.float32)

                self.u = sum(self._uCache)
                glUniform1f(u_location, self.u) 
                self.network.set_meinungen(_wArray)

                self.uCostCache[i] = Global.dT * abs(self.u) * sum(self.qArray)

                
                if i % Global.renderRate == 0:
                    print("average: " + str(normFac * sum(_wArray)) + " --u is:  " + str(Global.dT * abs(self.u) * sum(self.qArray)) + " -- Frame: " + str(i));
                    self.view.plot_graph(i, Global.c_star, self.uCostCache, Global.W_D)
                    time.sleep(Global.fPeriod)
            else:
                _stepCount = i;
                break

        print("-------Result-------")
        print("Cost: " + str(sum(self.uCostCache)) + " -- c_star: " + str(Global.c_star) + " --steps: " + str(_stepCount))

    def calcEpsilon(self):
        _diff_array = abs(self.network.meinungen - Global.W_D)
        _max = np.max(_diff_array) 
        return _max
        
    compute_shader_code = """
    #version 430
    layout (local_size_x = 256) in;  // Setze 256 Threads pro Block

    layout (std430, binding = 0) buffer qArray {
        float qarray[];
    };
    layout (std430, binding = 1) buffer wArray {
        float warray[];
    };
    layout (std430, binding = 2) buffer uCache {
        float ucache[];
    };
    layout (std430, binding = 3) buffer nMatrix {
        float nmatrix[];
    };

    uniform float u; 
    uniform float dT; 
    uniform float nu;
    uniform float W_D;
    uniform int n;
    uniform float norm;
    uniform float sumConst;     
    uniform float facNu;

    void main() {
        uint index = gl_GlobalInvocationID.x;  // Globale Indexberechnung

        if (index < n){
            //berechne next_w_j
        float correction = u * qarray[index];

        //rk_step1
        float w0 = warray[index];
        float f0 = 0.0;
        for(int i=0;i<n;++i){
            f0 += (warray[i] - w0) * nmatrix[n * index + i];
        }
        f0 = f0*norm;
        float k1 = dT * (f0 + correction);

        //rk_step2
        float w1 = warray[index] + 0.5*k1;
        float f1 = 0.0;
        for(int i=0;i<n;++i){
            f1 += (warray[i] - w1) * nmatrix[n * index + i];
        }
        f1 = f1*norm;
        float k2 = dT * (f1 + correction);

        //rk_step3
        float w2 = warray[index] + 0.5*k2;
         float f2 = 0.0;
        for(int i=0;i<n;++i){
            f2 += (warray[i] - w2) * nmatrix[n * index + i];
        }
        f2 = f2*norm;
        float k3 = dT * (f2 + correction);

        //rk_step4
        float w3 = warray[index] + k3;
        float f3 = 0.0;
        for(int i=0;i<n;++i){
            f3 += (warray[i] - w3) * nmatrix[n * index + i];
        }
        f3 = f3*norm;
        float k4 = dT * (f3 + correction);

        float rk_result = w0 + (1./6.) * (k1 + 2.0*k2 + 2.0* k3 + k4);

        warray[index] = clamp(rk_result, -1.0, 1.0);

        float fac1 = - ( (qarray[index]) / (n * (nu * facNu) + dT * qarray[index] * qarray[index]) );
        float newF = 0.0;
        for(int i=0;i<n;++i){
            newF += warray[i] - warray[index];
        }
        newF = newF*norm;
        float fac2 = warray[index] - W_D + dT * newF;
        ucache[index] = fac1 * fac2;
        }
    }

    """

    def setUpNeighborMatrix(self):
        for indexI in range(Global.num_nodes): #row
            for indexJ in range(Global.num_nodes): #col
                self.neighborMatrix[Global.num_nodes * indexI + indexJ] = self.network.is_neighbor(indexI, indexJ)

    def setUpQArray(self):
        for index in range(len(self.qArray)):
            if self.network.get_num_edges(index) >= Global.c_star:
                self.qArray[index] = 1
            else:
                self.qArray[index] = 0

    def setUpEdgeArray(self):
        for i in range(Global.num_nodes):
            self.edgeArray[i] = self.network.get_num_edges(i)


