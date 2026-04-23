import pymunk
import pymunk.pygame_util

def create_space():
    space = pymunk.Space()
    space.gravity = (0, 900)
    return space

def create_static_segment(space, p1, p2, radius=2):
    body = space.static_body
    shape = pymunk.Segment(body, p1, p2, radius)
    shape.friction = 0.8
    shape.elasticity = 0.3
    space.add(shape)
    return shape

def create_dynamic_body(space, x, y, mass, radius):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = (x, y)
    space.add(body)
    return body

def create_circle_shape(space, body, radius, friction=0.6, elasticity=0.3):
    shape = pymunk.Circle(body, radius)
    shape.friction = friction
    shape.elasticity = elasticity
    space.add(shape)
    return shape

def create_box_shape(space, body, width, height, friction=0.6, elasticity=0.3):
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.friction = friction
    shape.elasticity = elasticity
    space.add(shape)
    return shape

def create_pin_joint(space, body_a, body_b, anchor_a, anchor_b):
    joint = pymunk.PinJoint(body_a, body_b, anchor_a, anchor_b)
    space.add(joint)
    return joint

def create_pivot_joint(space, body_a, body_b, pivot):
    joint = pymunk.PivotJoint(body_a, body_b, pivot)
    space.add(joint)
    return joint

def create_damped_spring(space, body_a, body_b, anchor_a, anchor_b, rest_length, stiffness, damping):
    spring = pymunk.DampedSpring(body_a, body_b, anchor_a, anchor_b, rest_length, stiffness, damping)
    space.add(spring)
    return spring

def create_rotary_limit_joint(space, body_a, body_b, min_angle, max_angle):
    joint = pymunk.RotaryLimitJoint(body_a, body_b, min_angle, max_angle)
    space.add(joint)
    return joint

def space_draw_options(space, surface):
    return pymunk.pygame_util.DrawOptions(surface)