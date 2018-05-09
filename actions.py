from pymouse import PyMouse
class action:
    left_click = 1
    right_click = 2
    middle = 3
    prev_coordinates = [-1, -1]
    prev_state = ''
    def __init__(self, img_shape):
        """ Initalize actions; set up screen size and senstivity"""
        self.mouse_cntrl = PyMouse()
        shape_y, shape_x, _ = img_shape
        print shape_x, shape_y, self.mouse_cntrl.screen_size()
        screen_x, screen_y = self.mouse_cntrl.screen_size()
        self.x_convert = screen_x * 1.0 / shape_x 
        self.y_convert = screen_y * 1.0 / shape_y
        self.sensitivity = 1.0

    def update_sensitivity(self, sensitivity):
        #update sensitivity
        self.sensitivity = sensitivity / 100.0

    def screen_size(self):
        return self.mouse_cntrl.screen_size()

    def perform_release(self):
        # use in drag and drop to perform drop
        if self.prev_state == 'four':
            x, y = self.mouse_cntrl.position()
            self.mouse_cntrl.release(x, y)

    def zero(self):
        # No fingers
        self.prev_state = 'zero'
        print "Unable to detect"

    def one(self, hull_p):
        # one finger; movement control
        self.perform_release()
        print  "ek. Co-ordinates in image"+ str(hull_p)
        if self.prev_state == 'one':
            x,y = self.mouse_cntrl.position()
            new_x, new_y = x + self.sensitivity * self.x_convert * (-1 * \
                    self.prev_coordinates[0] + hull_p[0]), \
                    y + self.sensitivity * self.y_convert *\
                    (-1 * self.prev_coordinates[1] + hull_p[1])
            self.mouse_cntrl.move(int(new_x), int(new_y))
            self.prev_coordinates[0] = hull_p[0]
            self.prev_coordinates[1] = hull_p[1]
        else:
            self.prev_coordinates[0] = hull_p[0]
            self.prev_coordinates[1] = hull_p[1]
            self.prev_state = 'one'

    def two(self):
        # two fingers; left click
        print "Left Click"
        self.perform_release()
        if self.prev_state == 'two':
            return
        current_x, current_y = self.mouse_cntrl.position()
        self.mouse_cntrl.click(current_x,current_y, self.left_click)
        self.prev_state = 'two'

    def three(self):
        # 3 fingers; performs right click
        print "Right Click"
        self.perform_release()
        if self.prev_state == 'three':
            return
        current_x, current_y = self.mouse_cntrl.position()
        self.mouse_cntrl.click(current_x, current_y, self.right_click)
        self.prev_state = 'three'
