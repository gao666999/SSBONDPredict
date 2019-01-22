import numpy as np

class AminoAcid:
    def __init__(self,name,idnumber,chainID):
        self.center = np.zeros([3,])
        self.AminoAcidAmount = 0
        self.name = name
        self.xAxis = None
        self.yAxis = None
        self.zAxis = None
        self.CA = None
        self.N = None
        self.idnumber = idnumber
        self.chainID = chainID

    #Sum all atom coordinate
    def SumCenters(self,x,y,z):
        self.center[0] += x
        self.center[1] += y
        self.center[2] += z
        self.AminoAcidAmount += 1

    #Calculate the center of the amino acid
    def CalculateCenter(self):
        if(self.AminoAcidAmount == 0):
            #print("Amount Error")
            #print self.name
            return False
        #print self.center,self.AminoAcidAmount
        else:
            self.center = self.center / self.AminoAcidAmount
            return True

    #Calculate distance between two amino acid
    def DistanceBetweenAA(self,center):
        dis = np.sqrt(np.sum((center - self.center)**2))
        return dis
    #Input the CA and N
    def InputCAN(self,N,CA):
        self.N = N
        self.CA = CA
    #Establish the 3-dimension coordinate
    def EstablishCoordinate(self):
        #self.xAxis = (Nitrogen - self.center) / np.sqrt(np.sum((Nitrogen - self.center)**2))
        self.xAxis = (self.N - self.center) / np.sqrt(np.dot((self.N - self.center),(self.N - self.center)))
        #print 'hhhhhhhhhhhh'
        #print self.xAxis
        self.yAxis = (self.CA - self.center) - (np.dot((self.CA - self.center), self.xAxis))*self.xAxis
        self.yAxis = self.yAxis / np.sqrt((np.dot(self.yAxis,self.yAxis)))
        self.zAxis = np.cross(self.xAxis, self.yAxis)


        """
        self.xAxis = Nitrogen - self.center
        self.yAxis = (AlphaCarbon - self.center)
        """


    #Return the rho, theta, phi
    def ChangeCoordinate(self,center):
        #print 'hhhhhhhhhhh'
        #print self.center
        #print self.xAxis
        x = np.dot((center - self.center), self.xAxis)
        y = np.dot((center - self.center), self.yAxis)
        z = np.dot((center - self.center), self.zAxis)
        rho = np.sqrt(x**2+y**2+z**2)
        theta = np.arccos(z/rho)
        phi = np.arctan2(y,x)
        return rho,theta,phi
'''
    def get_name(self):
        return self.name

    def get_chainID(self):
        return self.chainID

    def get_idnumber(self):
        return self.idnumber
        '''

