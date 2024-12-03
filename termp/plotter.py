from math import sqrt,degrees,atan2

class Plotter:
    def __init__(self, stepper, servo):
        self.stepper = stepper
        self.servo = servo

    def G0(self, X=None, Y=None, Z=None):
        if X is not None or Y is not None:
            self.stepper.move_vec(X - self.stepper.x, Y - self.stepper.y)
        if Z is not None and Z > 0:
            self.servo.move_pen(False)

    def G1(self, X=None, Y=None, Z=None):
        if X is not None or Y is not None:
            self.stepper.move_vec(X - self.stepper.x, Y - self.stepper.y)
        if Z is not None and Z < 0:
            self.servo.move_pen(True)

    def G2(self, X, Y, Z, I, J):
        r = sqrt(I ** 2 + J ** 2)
        m = self.stepper.x + I
        n = self.stepper.y + J
        s_angle = degrees(atan2(-J, -I))
        e_angle = degrees(atan2(Y - n, X - m))
        if s_angle < 0:
            s_angle += 360
        if e_angle < 0:
            e_angle += 360
        if s_angle < e_angle:
            s_angle += 360
        self.stepper.circle(r, s_angle, e_angle, cw=1)

    def G3(self, X, Y, Z, I, J):
        r = sqrt(I ** 2 + J ** 2)
        m = self.stepper.x + I
        n = self.stepper.y + J
        s_angle = degrees(atan2(-J, -I))
        e_angle = degrees(atan2(Y - n, X - m))
        if s_angle < 0:
            s_angle += 360
        if e_angle < 0:
            e_angle += 360
        if s_angle > e_angle:
            s_angle -= 360
        self.stepper.circle(r, s_angle, e_angle, cw=0)