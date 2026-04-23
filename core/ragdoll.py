import pymunk
import pygame
import math
import random

class Ragdoll:
    def __init__(self, space, x, y):
        self.space = space
        self.x = x
        self.y = y
        self.bodies = []
        self.shapes = []
        self.joints = []
        self.skin_color = (210, 180, 150)
        self.head_color = (210, 180, 150)
        
        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        self.hit_timer = 0
        
        self.create()
        
    def create(self):
        scale = 1.0
        torso_width = 25 * scale
        torso_height = 40 * scale
        head_radius = 14 * scale
        arm_width = 6 * scale
        arm_length = 25 * scale
        leg_width = 8 * scale
        leg_length = 30 * scale
        
        torso_x = self.x
        torso_y = self.y
        
        head = pymunk.Body(2, pymunk.moment_for_circle(2, 0, head_radius))
        head.position = (torso_x, torso_y - torso_height // 2 - head_radius - 8)
        head_s = pymunk.Circle(head, head_radius)
        head_s.friction = 0.8
        head_s.elasticity = 0.1
        self.space.add(head, head_s)
        self.bodies.append(head)
        self.shapes.append(head_s)
        self.head = head
        self.head_shape = head_s
        self.head_radius = head_radius
        
        torso = pymunk.Body(8, pymunk.moment_for_box(8, (torso_width, torso_height)))
        torso.position = (torso_x, torso_y)
        torso.angular_damping = 0.8
        torso.linear_damping = 0.1
        torso_s = pymunk.Poly.create_box(torso, (torso_width, torso_height))
        torso_s.friction = 0.8
        torso_s.elasticity = 0.1
        self.space.add(torso, torso_s)
        self.bodies.append(torso)
        self.shapes.append(torso_s)
        
        left_arm = pymunk.Body(2, pymunk.moment_for_box(2, (arm_width, arm_length)))
        left_arm.position = (torso_x - torso_width // 2 - arm_width // 2, torso_y - torso_height // 2 + arm_length // 2)
        left_arm.angular_damping = 0.5
        left_arm_s = pymunk.Poly.create_box(left_arm, (arm_width, arm_length))
        left_arm_s.friction = 0.8
        self.space.add(left_arm, left_arm_s)
        self.bodies.append(left_arm)
        self.shapes.append(left_arm_s)
        
        right_arm = pymunk.Body(2, pymunk.moment_for_box(2, (arm_width, arm_length)))
        right_arm.position = (torso_x + torso_width // 2 + arm_width // 2, torso_y - torso_height // 2 + arm_length // 2)
        right_arm.angular_damping = 0.5
        right_arm_s = pymunk.Poly.create_box(right_arm, (arm_width, arm_length))
        right_arm_s.friction = 0.8
        self.space.add(right_arm, right_arm_s)
        self.bodies.append(right_arm)
        self.shapes.append(right_arm_s)
        
        left_leg = pymunk.Body(3, pymunk.moment_for_box(3, (leg_width, leg_length)))
        left_leg.position = (torso_x - 8, torso_y + torso_height // 2 + leg_length // 2)
        left_leg.angular_damping = 0.5
        left_leg_s = pymunk.Poly.create_box(left_leg, (leg_width, leg_length))
        left_leg_s.friction = 0.8
        self.space.add(left_leg, left_leg_s)
        self.bodies.append(left_leg)
        self.shapes.append(left_leg_s)
        
        right_leg = pymunk.Body(3, pymunk.moment_for_box(3, (leg_width, leg_length)))
        right_leg.position = (torso_x + 8, torso_y + torso_height // 2 + leg_length // 2)
        right_leg.angular_damping = 0.5
        right_leg_s = pymunk.Poly.create_box(right_leg, (leg_width, leg_length))
        right_leg_s.friction = 0.8
        self.space.add(right_leg, right_leg_s)
        self.bodies.append(right_leg)
        self.shapes.append(right_leg_s)
        
        neck_joint = pymunk.PivotJoint(head, torso, (head.position.x, head.position.y + head_radius))
        neck_joint.error_bias = 0.01
        self.space.add(neck_joint)
        self.joints.append(neck_joint)
        
        shoulder_joint = pymunk.PivotJoint(torso, left_arm, (torso_x - torso_width // 2, torso_y - torso_height // 2))
        shoulder_joint.error_bias = 0.01
        self.space.add(shoulder_joint)
        self.joints.append(shoulder_joint)
        
        r_shoulder_joint = pymunk.PivotJoint(torso, right_arm, (torso_x + torso_width // 2, torso_y - torso_height // 2))
        r_shoulder_joint.error_bias = 0.01
        self.space.add(r_shoulder_joint)
        self.joints.append(r_shoulder_joint)
        
        hip_joint = pymunk.PivotJoint(torso, left_leg, (torso_x - 8, torso_y + torso_height // 2))
        hip_joint.error_bias = 0.01
        self.space.add(hip_joint)
        self.joints.append(hip_joint)
        
        r_hip_joint = pymunk.PivotJoint(torso, right_leg, (torso_x + 8, torso_y + torso_height // 2))
        r_hip_joint.error_bias = 0.01
        self.space.add(r_hip_joint)
        self.joints.append(r_hip_joint)
        
    def update(self):
        pass
        
    def render(self, screen, camera_offset):
        for shape in self.shapes:
            try:
                if shape.body is None:
                    continue
                if isinstance(shape, pymunk.Circle):
                    center = shape.body.position + shape.offset
                    pos = (int(center.x - camera_offset[0]), int(center.y - camera_offset[1]))
                    if pos[0] < -100 or pos[0] > 1380 or pos[1] < -100 or pos[1] > 820:
                        continue
                    pygame.draw.circle(screen, self.skin_color, pos, int(shape.radius))
                    pygame.draw.circle(screen, (50, 40, 35), pos, int(shape.radius), 1)
                elif isinstance(shape, pymunk.Poly):
                    verts = [shape.body.position + v.rotated(shape.body.angle) for v in shape.get_vertices()]
                    screen_verts = []
                    for v in verts:
                        screen_verts.append((int(v.x - camera_offset[0]), int(v.y - camera_offset[1])))
                    if len(screen_verts) < 3:
                        continue
                    pygame.draw.polygon(screen, self.skin_color, screen_verts)
                    pygame.draw.polygon(screen, (50, 40, 35), screen_verts, 1)
            except:
                continue

    def destroy(self):
        for shape in self.shapes:
            try:
                self.space.remove(shape)
            except:
                pass
        for body in self.bodies:
            try:
                self.space.remove(body)
            except:
                pass
        for joint in self.joints:
            try:
                self.space.remove(joint)
            except:
                pass
                
    def apply_force(self, force, point=None):
        for body in self.bodies:
            if point:
                body.apply_force_at_world_point(force, point)
            else:
                body.apply_force_at_world_point(force, body.position)
                
    def get_position(self):
        if self.bodies:
            return self.bodies[0].position
        return (self.x, self.y)
        
    def get_velocity(self):
        if self.bodies:
            return self.bodies[0].velocity
        return (0, 0)
    
    def take_damage(self, amount):
        if not self.alive:
            return False
            
        self.health -= amount
        self.hit_timer = 10
        
        if self.health <= 0:
            self.die()
            return True
        return False
    
    def die(self):
        self.alive = False
        self.health = 0
        
    def get_head_position(self):
        if hasattr(self, 'head'):
            return self.head.position
        return self.get_position()