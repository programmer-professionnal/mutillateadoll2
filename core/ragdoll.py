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
        self.color = (200, 180, 160)
        self.skin_color = (210, 180, 150)
        
        self.balance_force = 15
        self.created = False
        
        self.create()
        
    def create(self):
        scale = 1.0
        
        head_radius = 12 * scale
        neck_width = 6 * scale
        neck_height = 8 * scale
        torso_width = 22 * scale
        torso_height = 45 * scale
        shoulder_width = 30 * scale
        arm_width = 5 * scale
        arm_length = 25 * scale
        hand_radius = 5 * scale
        hip_width = 20 * scale
        leg_width = 7 * scale
        leg_length = 30 * scale
        foot_width = 10 * scale
        foot_height = 5 * scale
        
        head = self.create_circle(head_radius, 2, (self.x, self.y - torso_height - neck_height - head_radius - 15))
        self.head = head
        
        neck = self.create_box(neck_width, neck_height, 2, (self.x, self.y - torso_height - neck_height - 10))
        self.neck = neck
        
        torso = self.create_box(torso_width, torso_height, 8, (self.x, self.y - torso_height // 2 - 5))
        self.torso = torso
        
        left_shoulder = self.create_circle(5, 1, (self.x - shoulder_width // 2, self.y - torso_height - 5))
        right_shoulder = self.create_circle(5, 1, (self.x + shoulder_width // 2, self.y - torso_height - 5))
        
        left_upper_arm = self.create_box(arm_width, arm_length, 2, (self.x - shoulder_width // 2 - arm_length // 2, self.y - torso_height // 2))
        right_upper_arm = self.create_box(arm_width, arm_length, 2, (self.x + shoulder_width // 2 + arm_length // 2, self.y - torso_height // 2))
        
        left_lower_arm = self.create_box(arm_width - 1, arm_length, 2, (self.x - shoulder_width // 2 - arm_length - arm_length // 2, self.y - torso_height // 2 + arm_length))
        right_lower_arm = self.create_box(arm_width - 1, arm_length, 2, (self.x + shoulder_width // 2 + arm_length + arm_length // 2, self.y - torso_height // 2 + arm_length))
        
        left_hand = self.create_circle(hand_radius, 1, (self.x - shoulder_width // 2 - arm_length * 2, self.y - torso_height // 2 + arm_length * 2))
        right_hand = self.create_circle(hand_radius, 1, (self.x + shoulder_width // 2 + arm_length * 2, self.y - torso_height // 2 + arm_length * 2))
        
        left_hip = self.create_circle(5, 2, (self.x - hip_width // 2, self.y))
        right_hip = self.create_circle(5, 2, (self.x + hip_width // 2, self.y))
        
        left_upper_leg = self.create_box(leg_width, leg_length, 3, (self.x - hip_width // 2, self.y + leg_length // 2 + 5))
        right_upper_leg = self.create_box(leg_width, leg_length, 3, (self.x + hip_width // 2, self.y + leg_length // 2 + 5))
        
        left_lower_leg = self.create_box(leg_width - 1, leg_length, 2, (self.x - hip_width // 2, self.y + leg_length + leg_length // 2 + 5))
        right_lower_leg = self.create_box(leg_width - 1, leg_length, 2, (self.x + hip_width // 2, self.y + leg_length + leg_length // 2 + 5))
        
        left_foot = self.create_box(foot_width, foot_height, 1, (self.x - hip_width // 2, self.y + leg_length * 2 + 10))
        right_foot = self.create_box(foot_width, foot_height, 1, (self.x + hip_width // 2, self.y + leg_length * 2 + 10))
        
        self.bodies = [head, neck, torso, left_shoulder, right_shoulder, 
                      left_upper_arm, right_upper_arm, left_lower_arm, right_lower_arm,
                      left_hand, right_hand, left_hip, right_hip,
                      left_upper_leg, right_upper_leg, left_lower_leg, right_lower_leg,
                      left_foot, right_foot]
        
        self.create_joint(head, neck, (0, head_radius + 2), (0, -neck_height // 2), -45, 45)
        self.create_joint(neck, torso, (0, neck_height // 2), (0, -torso_height // 2), -30, 30)
        
        self.create_joint(torso, left_shoulder, (-torso_width // 2, -torso_height // 2 + 5), (0, 0), -150, 30)
        self.create_joint(torso, right_shoulder, (torso_width // 2, -torso_height // 2 + 5), (0, 0), -30, 150)
        
        self.create_joint(left_shoulder, left_upper_arm, (0, 0), (0, -arm_length // 2), -120, 60)
        self.create_joint(right_shoulder, right_upper_arm, (0, 0), (0, -arm_length // 2), -60, 120)
        
        self.create_joint(left_upper_arm, left_lower_arm, (0, arm_length // 2), (0, -arm_length // 2), -120, 10)
        self.create_joint(right_upper_arm, right_lower_arm, (0, arm_length // 2), (0, -arm_length // 2), -10, 120)
        
        self.create_joint(left_lower_arm, left_hand, (0, arm_length // 2), (0, 0), -30, 30)
        self.create_joint(right_lower_arm, right_hand, (0, arm_length // 2), (0, 0), -30, 30)
        
        self.create_joint(torso, left_hip, (-torso_width // 2 + 3, torso_height // 2), (0, 0), -30, 80)
        self.create_joint(torso, right_hip, (torso_width // 2 - 3, torso_height // 2), (0, 0), -80, 30)
        
        self.create_joint(left_hip, left_upper_leg, (0, 0), (0, -leg_length // 2), -90, 15)
        self.create_joint(right_hip, right_upper_leg, (0, 0), (0, -leg_length // 2), -15, 90)
        
        self.create_joint(left_upper_leg, left_lower_leg, (0, leg_length // 2), (0, -leg_length // 2), -120, 10)
        self.create_joint(right_upper_leg, right_lower_leg, (0, leg_length // 2), (0, -leg_length // 2), -10, 120)
        
        self.create_joint(left_lower_leg, left_foot, (0, leg_length // 2), (0, 0), -45, 20)
        self.create_joint(right_lower_leg, right_foot, (0, leg_length // 2), (0, 0), -20, 45)
        
        self.created = True
        
    def create_circle(self, radius, mass, position):
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment)
        body.position = position
        
        shape = pymunk.Circle(body, radius)
        shape.friction = 0.8
        shape.elasticity = 0.1
        shape.color = self.skin_color
        
        self.space.add(body)
        self.space.add(shape)
        
        self.shapes.append(shape)
        return body
        
    def create_box(self, width, height, mass, position):
        moment = pymunk.moment_for_box(mass, (width, height))
        body = pymunk.Body(mass, moment)
        body.position = position
        body.angular_damping = 0.5
        body.linear_damping = 0.1
        
        shape = pymunk.Poly.create_box(body, (width, height))
        shape.friction = 0.8
        shape.elasticity = 0.1
        shape.color = self.skin_color
        
        self.space.add(body)
        self.space.add(shape)
        
        self.shapes.append(shape)
        return body
        
    def create_joint(self, body_a, body_b, anchor_a, anchor_b, min_angle=-90, max_angle=90):
        pivot = pymunk.PivotJoint(body_a, body_b, anchor_a)
        self.space.add(pivot)
        self.joints.append(pivot)
        
        limit = pymunk.RotaryLimitJoint(body_a, body_b, math.radians(min_angle), math.radians(max_angle))
        self.space.add(limit)
        self.joints.append(limit)
        
    def update(self):
        if not self.created:
            return
            
        target_angle = 0
        for body in self.bodies:
            angle_diff = target_angle - body.angle
            if abs(angle_diff) > 0.05:
                body.angular_velocity += angle_diff * self.balance_force * 0.1
                
        torso_body = self.torso
        if torso_body:
            target_x = self.x
            current_x = torso_body.position.x
            if abs(current_x - target_x) > 2:
                force = (target_x - current_x) * 0.5
                for body in self.bodies:
                    body.apply_force_at_world_point((force * 0.1, 0), body.position)
                    
    def render(self, screen, camera_offset):
        for shape in self.shapes:
            try:
                if shape.body is None:
                    continue
                if isinstance(shape, pymunk.Circle):
                    center = shape.body.position + shape.offset
                    pos = (int(center.x - camera_offset[0]), int(center.y - camera_offset[1]))
                    if pos[0] < -100 or pos[0] > SCREEN_WIDTH + 100 or pos[1] < -100 or pos[1] > SCREEN_HEIGHT + 100:
                        continue
                    radius = int(shape.radius)
                    color = shape.color if hasattr(shape, 'color') else self.skin_color
                    pygame.draw.circle(screen, color, pos, radius)
                    pygame.draw.circle(screen, (50, 40, 35), pos, radius, 1)
                    
                elif isinstance(shape, pymunk.Poly):
                    verts = [shape.body.position + v.rotated(shape.body.angle) for v in shape.get_vertices()]
                    screen_verts = []
                    for v in verts:
                        sv = (int(v.x - camera_offset[0]), int(v.y - camera_offset[1]))
                        screen_verts.append(sv)
                    color = shape.color if hasattr(shape, 'color') else self.skin_color
                    pygame.draw.polygon(screen, color, screen_verts)
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
        if self.torso:
            return self.torso.position
        return (self.x, self.y)
        
    def get_velocity(self):
        if self.torso:
            return self.torso.velocity
        return (0, 0)
        
    def get_velocity(self):
        if self.torso:
            return self.torso.velocity
        return (0, 0)