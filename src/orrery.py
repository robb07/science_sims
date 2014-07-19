'''
An Orrery is a model of the solar system that shows the relative motion of the planets and moons.

Created on Jun 16, 2014

@author: Robb
'''

from visual import *

# WIDTH = 500
# HEIGHT = 500
WIDTH = 1000
HEIGHT = 1000

# MODE = 'Inner Planets'
MODE = 'Classical Planets'
# MODE = 'The Nine Planets'

# FRAME_OF_REFERENCE = 'Sun'
# FRAME_OF_REFERENCE = 'Mercury'
# FRAME_OF_REFERENCE = 'Earth'
FRAME_OF_REFERENCE = 'Jupiter'

#from http://en.wikipedia.org/wiki/Orrery
#processed in excel: all relative to Earth 
planet_properties = dict([('Mercury', dict([('avg_orbital_radius', 0.39),('diameter',  0.38),('mass',   0.05 ),('density', 5.5),('n_moons',  0),('orbital_period', 0.24),('inclination', 7   ),('tilt', 0  ),('rotational_period',   '59 days' ),('color',color.gray(0.7)   )])),
                          ('Venus',   dict([('avg_orbital_radius', 0.72),('diameter',  0.95),('mass',   0.82 ),('density', 5.3),('n_moons',  0),('orbital_period', 0.62),('inclination', 3.4 ),('tilt', 177),('rotational_period', '-243 days' ),('color',color.magenta)])),
                          ('Earth',   dict([('avg_orbital_radius', 1   ),('diameter',  1   ),('mass',   1    ),('density', 5.5),('n_moons',  1),('orbital_period', 1   ),('inclination', 0   ),('tilt', 23 ),('rotational_period', '23.9 hours'),('color',color.blue  )])),
                          ('Mars',    dict([('avg_orbital_radius', 1.52),('diameter',  0.53),('mass',   0.11 ),('density', 3.9),('n_moons',  2),('orbital_period', 1.88),('inclination', 1.9 ),('tilt', 25 ),('rotational_period', '24.5 hours'),('color',color.red   )])),
                          ('Jupiter', dict([('avg_orbital_radius', 5.2 ),('diameter', 11.21),('mass', 317.9  ),('density', 1.3),('n_moons', 67),('orbital_period', 11.9),('inclination', 1.3 ),('tilt', 3  ),('rotational_period',   '10 hours'),('color',(1,0.7,0.2))])),
                          ('Saturn',  dict([('avg_orbital_radius', 9.54),('diameter',  9.45),('mass',  95.2  ),('density', 0.7),('n_moons', 62),('orbital_period', 29.5),('inclination', 2.5 ),('tilt', 27 ),('rotational_period',   '11 hours'),('color',color.green )])),
                          ('Uranus',  dict([('avg_orbital_radius', 19.2),('diameter',  4.01),('mass',  14.5  ),('density', 1.3),('n_moons', 27),('orbital_period', 84  ),('inclination', 0.8 ),('tilt', 98 ),('rotational_period',  '-17 hours'),('color',color.cyan )])),
                          ('Neptune', dict([('avg_orbital_radius', 30.1),('diameter',  3.88),('mass',  17.1  ),('density', 1.6),('n_moons', 14),('orbital_period', 165 ),('inclination', 1.8 ),('tilt', 28 ),('rotational_period',   '16 hours'),('color',color.blue )])),
                          ('Pluto',   dict([('avg_orbital_radius', 39.4),('diameter',  0.18),('mass',   0.002),('density', 2  ),('n_moons',  5),('orbital_period', 248 ),('inclination', 17.1),('tilt', 122),('rotational_period', '-6.4 days' ),('color',color.white )]))])

#diameter is in astronomical units for the sun instead of earth diameters
sun_properties = dict([('name','Sun'),('avg_orbital_radius', 0.),('diameter',0.01),('orbital_period', 0.)])

#from http://en.wikipedia.org/wiki/Moon
moon_properties = dict([('name','Moon'),('avg_orbital_radius', 0.00257),('diameter', 0.273),('mass', 0.012),('density', 3.34),('n_moons',  0),('orbital_period',0.07479 ),('inclination',5.1),('tilt', 6.6 ),('rotational_period','27.3 days' ),('color',color.gray(0.7)   )])

ORBITAL_RADIUS_SCALE_FACTORS = dict([('unit',5),('diameter',5),('mass',5),('density',5),('log-diameter',5)])

if MODE == 'Inner Planets':
    DT = 0.001
    show_planets = ['Mercury','Venus','Earth','Mars']
    SIZE_MODE = 'diameter'
elif MODE == 'Classical Planets':
    DT = 0.005
    show_planets = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn']
    SIZE_MODE = 'log-diameter'
#     SIZE_MODE = 'diameter'
elif MODE == 'The Nine Planets':
    DT = 0.05
    show_planets = planet_properties.keys()
    SIZE_MODE = 'diameter'

class CelestialBody(object):
    '''A celestial body'''
    
    def __init__(self, name, avg_orbital_radius, orbital_period, color=color.yellow, diameter=1, mass=1, density=1, pos=vector(0,0,0), ang=0, **kwargs):
        '''Constructor for CelestialBody'''
        self.name = name
        
        #orbital parameters
        self.avg_orbital_radius = avg_orbital_radius
        self.orbital_period = orbital_period
        
        #CelestialBody size options
        self.size_options = dict([('unit',1),('diameter',diameter),('mass',mass),('density',density),('log-diameter',log(10*diameter))])
        self.color = color
        
        #absolute position
        self.pos = pos
        self.ang = ang
        
        #relative bodies
        self.focus_body = None
        self.orbiters = dict([])
        
        self.set_sphere()
        
    def set_sphere(self):
        '''Make a new sphere'''
        #the visual object
        self.sphere = sphere(color=self.color, radius=self.size_options[SIZE_MODE]/2., make_trail=True, intervals=10, retain=1+int(self.orbital_period / DT))
    
    def del_sphere(self):
        '''Make the old sphere invisible'''
        self.sphere.visible = False
            
    def update(self,t):
        '''Updates the body's position'''
        if self.focus_body:
            self.ang = 2*pi*(t % self.orbital_period) / self.orbital_period 
            offset = vector(self.avg_orbital_radius*ORBITAL_RADIUS_SCALE_FACTORS[SIZE_MODE]*cos(self.ang),
                            self.avg_orbital_radius*ORBITAL_RADIUS_SCALE_FACTORS[SIZE_MODE]*sin(self.ang),
                            0)
            self.pos = self.focus_body.pos + offset
        
        self.sphere.pos = self.pos
        
        for orbiter in self.orbiters.values():
            orbiter.update(t)
    
    def add_orbiter(self, orbiter):
        '''Add an orbiter to the body'''
        if not self.orbiters.has_key(orbiter.name) or orbiter not in self.orbiters.values():
            self.orbiters[orbiter.name] = orbiter
            orbiter.focus_body = self
            
    def pop_orbiter(self, orbiter_name):
        '''Remove an orbiter from the body'''
        if self.orbiters.has_key(orbiter_name):
            orbiter = self.orbiters.pop(orbiter_name)
            orbiter.focus_body = None
            return orbiter
        else:
            return None
    
    def swap_reference_frame(self,orbiter_name):
        '''Switches the reference frame with the orbiter'''
        if self.orbiters.has_key(orbiter_name):
            orbiter = self.pop_orbiter(orbiter_name)
            
            self.avg_orbital_radius, orbiter.avg_orbital_radius = orbiter.avg_orbital_radius, self.avg_orbital_radius 
            self.orbital_period, orbiter.orbital_period = orbiter.orbital_period, self.orbital_period
            
            self.del_sphere()
            self.set_sphere()
            
            orbiter.add_orbiter(self)
            return orbiter
        else:
            return None
        
    def __str__(self):
        '''String of the Celestial Body'''
        orbiters_str = ',\n\t'.join([str(orbiter) for orbiter in self.orbiters.values()])
        if len(orbiters_str) > 0:
            orbiters_str = ', orbiters: \n\t' + orbiters_str 
        return self.name +  \
                ': [pos: (' + ','.join([str(p) for p in self.pos]) + ')' + \
                ', ang: ' + str(self.ang) + \
                orbiters_str + ']'
        
def setup():
    '''Build the solar systems'''
    global sun, ref_body
    display(title='Orrery -- ' + MODE + ' -- ' + FRAME_OF_REFERENCE + ' Centric',width=WIDTH,height=HEIGHT)
    #sun = CelestialBody('Sun', 0, 0, diameter=2)
    sun = CelestialBody(**sun_properties)
    for planet in show_planets:
        sun.add_orbiter(CelestialBody(planet,**planet_properties[planet]))
    
    earth = sun.orbiters['Earth']
    #earth.add_orbiter(CelestialBody(**moon_properties))
    
    if FRAME_OF_REFERENCE != 'Sun':
        ref_body = sun.swap_reference_frame(FRAME_OF_REFERENCE)
    else:
        ref_body = sun
    
    ref_body.update(0)
    
    print sun
    print ref_body
    print earth

def run():
    '''Run the solar system'''
    t = 0.0
    
    while True:
        rate(100)
        t += DT
        ref_body.update(t)
        #print sun

if __name__ == '__main__':
    setup()
    run()