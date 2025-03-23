import streamlit as st
import numpy as np
from PIL import Image
import io

class LEDMatrix:
    def __init__(self, width=32, height=8):
        self.width = width
        self.height = height
        self.matrix = np.zeros((height, width), dtype=np.uint8)
        self.brightness = 255
        self.update_needed = False

    def fill(self, c):
        self.matrix.fill(1 if c else 0)
        self.update_needed = True

    def pixel(self, x, y, c):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.matrix[y, x] = 1 if c else 0
            self.update_needed = True

    def hline(self, x, y, length, c=1):
        for i in range(length):
            if x + i < self.width:
                self.pixel(x + i, y, c)
        self.update_needed = True

    def vline(self, x, y, length, c=1):
        for i in range(length):
            if y + i < self.height:
                self.pixel(x, y + i, c)
        self.update_needed = True

    def rectangle(self, x, y, width, height, c=1):
        self.hline(x, y, width, c)
        self.hline(x, y + height - 1, width, c)
        self.vline(x, y, height, c)
        self.vline(x + width - 1, y, height, c)
        self.update_needed = True

    def text(self, message, x=0, y=0, c=1):
        font = {
            # Uppercase A-Z
            'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
            'B': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
            'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[0,1,1]],
            'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
            'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]],
            'F': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,0,0]],
            'G': [[0,1,1],[1,0,0],[1,0,1],[1,0,1],[0,1,1]],
            'H': [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
            'I': [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
            'J': [[0,0,1],[0,0,1],[0,0,1],[1,0,1],[0,1,0]],
            'K': [[1,0,1],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
            'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
            'M': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
            'N': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
            'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
            'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
            'Q': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,1]],
            'R': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
            'S': [[0,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0]],
            'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
            'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
            'V': [[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
            'W': [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1]],
            'X': [[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
            'Y': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]],
            'Z': [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
            # Lowercase a-z
            'a': [[0,0,0],[0,1,1],[1,0,1],[1,0,1],[0,1,1]],
            'b': [[1,0,0],[1,0,0],[1,1,0],[1,0,1],[1,1,0]],
            'c': [[0,0,0],[0,1,1],[1,0,0],[1,0,0],[0,1,1]],
            'd': [[0,0,1],[0,0,1],[0,1,1],[1,0,1],[0,1,1]],
            'e': [[0,0,0],[0,1,0],[1,1,1],[1,0,0],[0,1,1]],
            'f': [[0,0,0],[0,1,1],[1,0,0],[1,1,0],[1,0,0]],
            'g': [[0,0,0],[0,1,1],[1,0,1],[0,1,1],[1,0,0]],
            'h': [[1,0,0],[1,0,0],[1,1,0],[1,0,1],[1,0,1]],
            'i': [[0,0,0],[0,1,0],[0,0,0],[0,1,0],[0,1,0]],
            'j': [[0,0,0],[0,0,1],[0,0,0],[1,0,1],[0,1,0]],
            'k': [[1,0,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
            'l': [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1]],
            'm': [[0,0,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1]],
            'n': [[0,0,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1]],
            'o': [[0,0,0],[0,1,0],[1,0,1],[1,0,1],[0,1,0]],
            'p': [[0,0,0],[1,1,0],[1,0,1],[1,1,0],[1,0,0]],
            'q': [[0,0,0],[0,1,1],[1,0,1],[0,1,1],[0,0,1]],
            'r': [[0,0,0],[0,1,1],[1,0,0],[1,0,0],[1,0,0]],
            's': [[0,0,0],[0,1,1],[0,1,0],[1,0,0],[1,1,0]],
            't': [[0,1,0],[1,1,1],[0,1,0],[0,1,0],[0,0,1]],
            'u': [[0,0,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
            'v': [[0,0,0],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
            'w': [[0,0,0],[1,0,1],[1,0,1],[1,1,1],[1,0,1]],
            'x': [[0,0,0],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
            'y': [[0,0,0],[1,0,1],[1,0,1],[0,1,1],[1,0,0]],
            'z': [[0,0,0],[1,1,1],[0,1,0],[1,0,0],[1,1,1]],
            # Numbers 0-9
            '0': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]],
            '1': [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[0,1,0]],
            '2': [[1,1,0],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
            '3': [[1,1,0],[0,0,1],[0,1,0],[0,0,1],[1,1,0]],
            '4': [[0,0,1],[0,1,1],[1,0,1],[1,1,1],[0,0,1]],
            '5': [[1,1,1],[1,0,0],[1,1,0],[0,0,1],[1,1,0]],
            '6': [[0,1,1],[1,0,0],[1,1,0],[1,0,1],[0,1,0]],
            '7': [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
            '8': [[0,1,0],[1,0,1],[0,1,0],[1,0,1],[0,1,0]],
            '9': [[0,1,0],[1,0,1],[0,1,1],[0,0,1],[1,1,0]],
            # Space
            ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        }
        
        pos_x = x
        for char in message:
            if char in font:
                for row in range(5):
                    for col in range(3):
                        if font[char][row][col]:
                            self.pixel(pos_x + col, y + row, c)
                pos_x += 4  # 3 pixels width + 1 pixel spacing
        self.update_needed = True

    def show(self):
        self.update_needed = False  # Reset flag after showing

    def get_image(self):
        scale = 20
        img_array = np.full((self.height * scale, self.width * scale, 3), 25, dtype=np.uint8)
        
        for y in range(self.height + 1):
            img_array[y * scale - 1:y * scale + 1, :] = [100, 100, 100]
        for x in range(self.width + 1):
            img_array[:, x * scale - 1:x * scale + 1] = [100, 100, 100]

        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y, x]:
                    center_x = x * scale + scale // 2
                    center_y = y * scale + scale // 2
                    radius = scale // 2 - 2
                    
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            if dx*dx + dy*dy <= radius*radius:
                                py = center_y + dy
                                px = center_x + dx
                                if 0 <= py < img_array.shape[0] and 0 <= px < img_array.shape[1]:
                                    img_array[py, px] = [self.brightness, 0, 0]

        return Image.fromarray(img_array)

# Streamlit app
def main():
    st.set_page_config(layout="wide")
    
    st.title("32x8 LED Matrix Simulator")
    
    if 'display' not in st.session_state:
        st.session_state.display = LEDMatrix()
    
    display = st.session_state.display
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Control the Display")
        code = st.text_area(
            "Enter Python code to control the display",
            value='''# Examples with loops and full font (end with display.show()):
display.fill(0)  # Turn all LEDs off

# For loop to draw diagonal
for i in range(8):
    display.pixel(i, i, 1)

# While loop to draw vertical line
x = 10
while x < 15:
    display.vline(x, 3, 1, 1)  # c=1 to turn on
    x += 1

# If-else to draw conditional pattern
for y in range(8):
    if y % 2 == 0:
        display.hline(20, y, 2, 1)  # c=1 to turn on
    else:
        display.hline(21, y, 2, 0)  # c=0 to turn off

display.rectangle(25, 1, 5, 4, 1)  # c=1 to turn on
display.text("Hello123", 0, 0, 1)  # Full font test
# Try display.fill(1) to turn all LEDs on
display.show()''',
            height=400,
            key="code_input",
        )
        
        if st.button("Execute Code"):
            try:
                display.fill(0)  # Reset to all off
                exec(code, {'display': display})
                if not display.update_needed:
                    st.success("Code executed successfully!")
                else:
                    st.warning("Don't forget to add display.show() at the end!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with col2:
        display_placeholder = st.empty()
        display_placeholder.image(display.get_image(), caption="LED Matrix Display", use_container_width=True)
        if not display.update_needed:
            display_placeholder.image(display.get_image(), caption="LED Matrix Display", use_container_width=True)

    st.markdown(
        """
        <style>
        textarea#code_input {
            font-family: 'Courier New', Courier, monospace;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()