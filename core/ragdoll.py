import pymunk
import pygame
import math

class Ragdoll:
    def __init__(self, space, x, y):
        self.space = space
        self.x = x
        self.y = y
        self.bodies = []
        self.shapes = []
        self.joints = []
        self.color = (200, 180, 160)
        
        self.create()
        
    def create(self):
        scale = 1.0
        
        head_radius = 15 * scale
        torso_width = 25 * scale
        torso_height = 50 * scale
        arm_width = 8 * scale
        arm_length = 30 * scale
        leg_width = 10 * scale
        leg_length = 35 * scale
        
        head = self.create_body(head_radius, 3, (self.x, self.y - torso_height - head_radius - 5))
        self.bodies.append(head)
        
        torso = self.create_box(torso_width, torso_height, 10, (self.x, self.y))
        self.bodies.append(torso)
        
        left_upper_arm = self.create_box(arm_width, arm_length, 3, (self.x - torso_width, self.y - torso_height//2))
        right_upper_arm = self.create_box(arm_width, arm_length, 3, (self.x + torso_width, self.y - torso_height//2))
        left_lower_arm = self.create_box(arm_width, arm_length, 3, (self.x - torso_width - arm_length//2, self.y - torso_height//2 + arm_length))
        right_lower_arm = self.create_box(arm_width, arm_length, 3, (self.x + torso_width + arm_length//2, self.y - torso_height//2 + arm_length))
        
        self.bodies.extend([left_upper_arm, right_upper_arm, left_lower_arm, right_lower_arm])
        
        left_upper_leg = self.create_box(leg_width, leg_length, 4, (self.x - 10, self.y + torso_height//2))
        right_upper_leg = self.create_box(leg_width, leg_length, 4, (self.x + 10, self.y + torso_height//2))
        left_lower_leg = self.create_box(leg_width, leg_length, 3, (self.x - 10, self.y + torso_height//2 + leg_length))
        right_lower_leg = self.create_box(leg_width, leg_length, 3, (self.x + 10, self.y + torso_height//2 + leg_length))
        
        self.bodies.extend([left_upper_leg, right_upper_leg, left_lower_leg, right_lower_leg])
        
        self.create_joints(head, torso, (0, head_radius + 5), (0, -torso_height//2))
        
        self.create_joints(torso, left_upper_arm, (-torso_width//2, -torso_height//2), (0, -arm_length//2))
        self.create_joints(torso, right_upper_arm, (torso_width//2, -torso_height//2), (0, -arm_length//2))
        self.create_joints(left_upper_arm, left_lower_arm, (0, arm_length//2), (0, -arm_length//2))
        self.create_joints(right_upper_arm, right_lower_arm, (0, arm_length//2), (0, -arm_length//2))
        
        self.create_joints(torso, left_upper_leg, (-10, torso_height//2), (0, -leg_length//2))
        self.create_joints(torso, right_upper_leg, (10, torso_height//2), (0, -leg_length//2))
        self.create_joints(left_upper_leg, left_lower_leg, (0, leg_length//2), (0, -leg_length//2))
        self.create_joints(right_upper_leg, right_lower_leg, (0, leg_length//2), (0, -leg_length//2))
        
    def create_body(self, radius, mass, position):
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = position
        
        shape = pymunk.Circle(body, radius)
        shape.friction = 0.6
        shape.elasticity = 0.3
        shape.color = self.color
        
        self.space.add(body)
        self.space.add(shape)
        
        self.shapes.append(shape)
        return body
        
    def create_box(self, width, height, mass, position):
        moment = pymunk.moment_for_box(mass, (width, height))
        body = pymunk.Body(mass, moment)
        body.position = position
        
        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 0.6
        shape.elasticity = 0.3
        shape.color = self.color
        
        self.space.add(body)
        self.space.add(shape)
        
        self.shapes.append(shape)
        return body
        
    def create_joints(self, body_a, body_b, anchor_a, anchor_b):
        joint = pymunk.PinJoint(body_a, body_b, anchor_a, anchor_b)
        self.space.add(joint)
        self.joints.append(joint)
        return joint
    
    def update(self):
        pass
        
    def render(self, screen, camera_offset):
        for shape in self.shapes:
            if isinstance(shape, pymunk.Circle):
                center = shape.body.position + (shape.offset).rotated(shape.body.angle)
                pos = (int(center.x - camera_offset[0]), int(center.y - camera_offset[1]))
                radius = int(shape.radius)
                pygame.draw.circle(screen, shape.color, pos, radius)
                pygame.draw.circle(screen, (0, 0, 0), pos, radius, 1)
                
            elif isinstance(shape, pymunk.Poly):
                verts = [shape.body.position + v.rotated(shape.body.angle) for v in shape.get_vertices()]
                screen_verts = [(int(v.x - camera_offset[0]), int(v.y - camera_offset[1])) for v in verts]
                pygame.draw.polygon(screen, shape.color, screen_verts)
                pygame.draw.polygon(screen, (0, 0, 0), screen_verts, 1)
                
    def destroy(self):
        for shape in self.shapes:
            self.space.remove(shape)
        for body in self.bodies:
            self.space.remove(body)
        for joint in self.joints:
            self.space.remove(joint)
            
    def apply_force(self, force, point=None):
        for body in self.bodies:
            if point:
                body.apply_force_at_local_point(force, point)
            else:
                body.apply_force_at_center(force)
                
    def get_position(self):
        if self.bodies:
            return self.bodies[0].position
        return (self.x, self.y)