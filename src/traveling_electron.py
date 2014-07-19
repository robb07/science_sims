'''
A simulation of an electron moving through electric and magnetic fields.

Created on Jul 17, 2014

@author: Robb
'''

from visual import *

print("""
      Right button drag to rotate "camera" to view scene.
      On a one-button mouse, right is Command + mouse.
      Middle button to drag up or down to zoom in or out.
      On a two-button mouse, middle is left + right.
      On a one-button mouse, middle is Option + mouse.
      """)

WIDTH = 1000
HEIGHT = 1000

DT = 0.05

SIZE = 0.1

# # Circle YZ
# starting_point = (0,0,1.0)
# field_point = (0,0,0)
# particle_vel = vector(0.1,0,0)
# E_field = dict([('mag',0.0),('axis',vector(0,1,0))])
# B_field = dict([('mag',1.0),('axis',vector(0,1,0))])

# # Circle XY
# starting_point = (0,-1,0)
# field_point = (0,0,0)
# particle_vel = vector(0.1,0,0)
# E_field = dict([('mag',0.0),('axis',vector(0,1,0))])
# B_field = dict([('mag',1.0),('axis',vector(0,0,1))])

# # Helix
# starting_point = (0,0,1)
# field_point = (0,0,0)
# particle_vel = vector(0.1,0.01,0)
# E_field = dict([('mag',0.0),('axis',vector(0,-1,0))])
# B_field = dict([('mag',1.0),('axis',vector(0,1,0))])

# # Expanding Helix
# starting_point = (0,0,1)
# field_point = (0,0,0)
# particle_vel = vector(0.1,0,0)
# E_field = dict([('mag',0.001),('axis',vector(0,-1,0))])
# B_field = dict([('mag',1.0),('axis',vector(0,1,0))])

# Expanding Helix
starting_point = (0,0,1)
field_point = (0,0,0)
particle_vel = vector(0.1,0.01,0)
E_field = dict([('mag',0.05),('axis',vector(1,0,0))])
B_field = dict([('mag',1.0),('axis',vector(0,1,0))])

def electron(pos=vector(0,0,0),vel=vector(1,0,0)):
    '''Makes an electron'''
    p = sphere(color=color.blue, radius=SIZE, make_trail=True)
    p.pos = pos
    p.mass = 10.0
    p.vel = vel
    p.charge = -1
    return p

def field(pos=vector(0,0,0),axis=vector(1,0,0),mag=1,color=color.white):
    '''creates an arrow to mark a field'''
    f = arrow(pos=pos, axis=axis, color=color)
    f.mag = mag
    if mag == 0:
        f.visible = False
    return f

def describe(field_properties):
    '''Turns the field into a string notation'''
    return str(field_properties['mag']*field_properties['axis'])
def setup():
    '''setup the electron and field'''
    global scene, particle, magnetic_field, electric_field, pause
    scene = display(title='Traveling Electron -- E = '+describe(E_field)+', B = ' + describe(B_field),x=0,y=0,width=WIDTH,height=HEIGHT)
    
    particle = electron(vector(starting_point),particle_vel)
    electric_field = field(vector(field_point),E_field['axis'],E_field['mag'],color=color.blue)
    magnetic_field = field(vector(field_point),B_field['axis'],B_field['mag'],color=color.yellow)
    
    scene.range = (10,2,10)
    scene.autocenter = False
    scene.autoscale = False
    
    pause = False

def run():
    '''Run the electron simulation'''
    global scene, pause
    t = 0.0
    
    while True:
        rate(100)
        if scene.kb.keys:
            key = scene.kb.getkey()
            print 'key:', key, ord(key)
            if key == ' ':
                pause = not pause
            #elif ord(key) == 10:
            #    scene.delete()
            #    setup()
        
        if not pause:
            t += DT
            F = particle.charge*(electric_field.mag*electric_field.axis + particle.vel.cross(magnetic_field.mag*magnetic_field.axis))
            accel = F/particle.mass
            particle.vel = particle.vel + accel*DT
            particle.pos = particle.pos + particle.vel*DT
            
            #print 'pos:',particle.pos, 'v:', mag(particle.vel), 'a:', mag(accel)
        

if __name__ == '__main__':
    setup()
    run()