import re
import smbus2
import time

class FileReader:
    I2C_ADDR = 0x27
    LCD_WIDTH = 16   
    LCD_CHR = 1  #
    LCD_CMD = 0  
    LCD_LINE_1 = 0x80  # LCD first line
    LCD_LINE_2 = 0xC0  # LCD seconde line
    LCD_BACKLIGHT = 0x08  # back light ON
    ENABLE = 0b00000100   # Enable
    
    def __init__(self, plotter, client_socket=None, i2c_address=0x27):
        self.plotter = plotter
        self.client_socket = client_socket
        self.bus = smbus2.SMBus(1)
        self.i2c_address = i2c_address
        self.lcd_init()
        self.progress = 0

    def lcd_init(self):
        self.lcd_byte(0x33, self.LCD_CMD)  
        self.lcd_byte(0x32, self.LCD_CMD)  
        self.lcd_byte(0x06, self.LCD_CMD)  
        self.lcd_byte(0x0C, self.LCD_CMD)  
        self.lcd_byte(0x28, self.LCD_CMD)  
        self.lcd_byte(0x01, self.LCD_CMD)  
        self.lcd_display_string("Edge Scketcher", self.LCD_LINE_1,"center")
        self.lcd_display_string("made by es1", self.LCD_LINE_2,"center")

    def lcd_byte(self,bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)
        
    def lcd_toggle_enable(self,bits):
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))

    def lcd_display_string(self,message, line, align = "left"):
        if align == "right":
            message = message.rjust(self.LCD_WIDTH, " ") 
        elif align == "center":
            message = message.center(self.LCD_WIDTH, " ")
        else:
            message = message.ljust(self.LCD_WIDTH, " ")

        self.lcd_byte(line, self.LCD_CMD)
        for char in message:
            self.lcd_byte(ord(char), self.LCD_CHR)

    def draw_plotter(self, file_path, scale=10):
        with open(file_path, "r") as file:
            lines = file.readlines()
            total_lines = len(lines)

            self.lcd_display_string("Printing...", self.LCD_LINE_1,"center")
            self.progress = 1
            for idx, line in enumerate(lines):
                line = line.strip()
                if self.progress != int((idx + 1) / total_lines * 100):
                    self.lcd_display_string(f"Progress: {self.progress}%", self.LCD_LINE_2,"left")
                    self.progress = int((idx + 1) / total_lines * 100) + 1
                
                # G00 Command
                if re.match(r"^G00\b", line):
                    x = re.search(r"X([-+]?[0-9]*\.?[0-9]+)", line)
                    y = re.search(r"Y([-+]?[0-9]*\.?[0-9]+)", line)
                    z = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", line)
                    
                    x = float(x.group(1)) * scale if x else None
                    y = float(y.group(1)) * scale if y else None
                    z = float(z.group(1)) if z else None
                    self.plotter.G0(X=x, Y=y, Z=z)
                
                # G01 Command
                elif re.match(r"^G01\b", line):
                    x = re.search(r"X([-+]?[0-9]*\.?[0-9]+)", line)
                    y = re.search(r"Y([-+]?[0-9]*\.?[0-9]+)", line)
                    z = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", line)
                    f = re.search(r"F([-+]?[0-9]*\.?[0-9]+)", line)
                    
                    x = float(x.group(1)) * scale if x else None
                    y = float(y.group(1)) * scale if y else None
                    z = float(z.group(1)) if z else None
                    self.plotter.G1(X=x, Y=y, Z=z)
                
                # G02 Command
                elif re.match(r"^G02\b", line):
                    x = re.search(r"X([-+]?[0-9]*\.?[0-9]+)", line)
                    y = re.search(r"Y([-+]?[0-9]*\.?[0-9]+)", line)
                    z = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", line)
                    i = re.search(r"I([-+]?[0-9]*\.?[0-9]+)", line)
                    j = re.search(r"J([-+]?[0-9]*\.?[0-9]+)", line)
                    f = re.search(r"F([-+]?[0-9]*\.?[0-9]+)", line)
                    
                    x = float(x.group(1)) * scale if x else None
                    y = float(y.group(1)) * scale if y else None
                    z = float(z.group(1)) if z else None
                    i = float(i.group(1)) * scale if i else None
                    j = float(j.group(1)) * scale if j else None
                    if x is not None and y is not None and i is not None and j is not None:
                        self.plotter.G2(X=x, Y=y, Z=z, I=i, J=j)
                
                # G03 Command
                elif re.match(r"^G03\b", line):
                    x = re.search(r"X([-+]?[0-9]*\.?[0-9]+)", line)
                    y = re.search(r"Y([-+]?[0-9]*\.?[0-9]+)", line)
                    z = re.search(r"Z([-+]?[0-9]*\.?[0-9]+)", line)
                    i = re.search(r"I([-+]?[0-9]*\.?[0-9]+)", line)
                    j = re.search(r"J([-+]?[0-9]*\.?[0-9]+)", line)
                    f = re.search(r"F([-+]?[0-9]*\.?[0-9]+)", line)
                    
                    x = float(x.group(1)) * scale if x else None
                    y = float(y.group(1)) * scale if y else None
                    z = float(z.group(1)) if z else None
                    i = float(i.group(1)) * scale if i else None
                    j = float(j.group(1)) * scale if j else None
                    if x is not None and y is not None and i is not None and j is not None:
                        self.plotter.G3(X=x, Y=y, Z=z, I=i, J=j)
                        
            self.lcd_display_string("Print Done!", self.LCD_LINE_1,"center")

    def file_info(self, file_path):
        self.lcd_display_string(file_path.split('/')[-1],self.LCD_LINE_1,"center")
        with open(file_path, "r") as file:
            lines = file.readlines()
            total_lines = len(lines)
        expect_time = total_lines / 8.1
        expect_min = int(expect_time // 60)
        expect_sec = int(expect_time % 60)
        display_time = "expect : " + str(expect_min) + "m " + str(expect_sec) + "s"
        self.lcd_display_string(display_time,self.LCD_LINE_2,"center")
        return total_lines, expect_min, expect_sec
        
    def draw(self, file_path):
        self.file_info(file_path)
        time.sleep(1.5)
        self.draw_plotter(file_path)
        time.sleep(1.5)
        self.lcd_init()
        self.progress = 0
        
    def send_progress(self, progress):
        if self.client_socket:
            try:
                self.client_socket.sendall(f"Progress: {progress}%\n".encode('utf-8'))
            except Exception as e:
                print(f"Error sending progress: {e}")



