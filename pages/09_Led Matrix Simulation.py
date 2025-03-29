import streamlit as st
import numpy as np
from PIL import Image
import io
import time

class LEDMatrix:
    def __init__(self, width=32, height=8, color=[255, 0, 0]):  # Default red
        self.width = width
        self.height = height
        self.matrix = np.zeros((height, width), dtype=np.uint8)
        self.brightness = 255
        self.color = color  # RGB color list
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
            'A': [[0,1,0],[1,0,1],[1,1,1],[1,0,1],[1,0,1]], 'B': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,1,0]],
            'C': [[0,1,1],[1,0,0],[1,0,0],[1,0,0],[0,1,1]], 'D': [[1,1,0],[1,0,1],[1,0,1],[1,0,1],[1,1,0]],
            'E': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,1,1]], 'F': [[1,1,1],[1,0,0],[1,1,0],[1,0,0],[1,0,0]],
            'G': [[0,1,1],[1,0,0],[1,0,1],[1,0,1],[0,1,1]], 'H': [[1,0,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1]],
            'I': [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]], 'J': [[0,0,1],[0,0,1],[0,0,1],[1,0,1],[0,1,0]],
            'K': [[1,0,1],[1,0,1],[1,1,0],[1,0,1],[1,0,1]], 'L': [[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]],
            'M': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]], 'N': [[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,0,1]],
            'O': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]], 'P': [[1,1,0],[1,0,1],[1,1,0],[1,0,0],[1,0,0]],
            'Q': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,1]], 'R': [[1,1,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]],
            'S': [[0,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0]], 'T': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]],
            'U': [[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0]], 'V': [[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
            'W': [[1,0,1],[1,0,1],[1,0,1],[1,1,1],[1,0,1]], 'X': [[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
            'Y': [[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0]], 'Z': [[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]],
            'a': [[0,0,0],[0,1,1],[1,0,1],[1,0,1],[0,1,1]], 'b': [[1,0,0],[1,0,0],[1,1,0],[1,0,1],[1,1,0]],
            'c': [[0,0,0],[0,1,1],[1,0,0],[1,0,0],[0,1,1]], 'd': [[0,0,1],[0,0,1],[0,1,1],[1,0,1],[0,1,1]],
            'e': [[0,0,0],[0,1,0],[1,1,1],[1,0,0],[0,1,1]], 'f': [[0,0,0],[0,1,1],[1,0,0],[1,1,0],[1,0,0]],
            'g': [[0,0,0],[0,1,1],[1,0,1],[0,1,1],[1,0,0]], 'h': [[1,0,0],[1,0,0],[1,1,0],[1,0,1],[1,0,1]],
            'i': [[0,0,0],[0,1,0],[0,0,0],[0,1,0],[0,1,0]], 'j': [[0,0,0],[0,0,1],[0,0,0],[1,0,1],[0,1,0]],
            'k': [[1,0,0],[1,0,1],[1,1,0],[1,0,1],[1,0,1]], 'l': [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1]],
            'm': [[0,0,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1]], 'n': [[0,0,0],[1,1,0],[1,0,1],[1,0,1],[1,0,1]],
            'o': [[0,0,0],[0,1,0],[1,0,1],[1,0,1],[0,1,0]], 'p': [[0,0,0],[1,1,0],[1,0,1],[1,1,0],[1,0,0]],
            'q': [[0,0,0],[0,1,1],[1,0,1],[0,1,1],[0,0,1]], 'r': [[0,0,0],[0,1,1],[1,0,0],[1,0,0],[1,0,0]],
            's': [[0,0,0],[0,1,1],[0,1,0],[1,0,0],[1,1,0]], 't': [[0,1,0],[1,1,1],[0,1,0],[0,1,0],[0,0,1]],
            'u': [[0,0,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]], 'v': [[0,0,0],[1,0,1],[1,0,1],[0,1,0],[0,1,0]],
            'w': [[0,0,0],[1,0,1],[1,0,1],[1,1,1],[1,0,1]], 'x': [[0,0,0],[1,0,1],[0,1,0],[1,0,1],[1,0,1]],
            'y': [[0,0,0],[1,0,1],[1,0,1],[0,1,1],[1,0,0]], 'z': [[0,0,0],[1,1,1],[0,1,0],[1,0,0],[1,1,1]],
            '0': [[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0]], '1': [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[0,1,0]],
            '2': [[1,1,0],[0,0,1],[0,1,0],[1,0,0],[1,1,1]], '3': [[1,1,0],[0,0,1],[0,1,0],[0,0,1],[1,1,0]],
            '4': [[0,0,1],[0,1,1],[1,0,1],[1,1,1],[0,0,1]], '5': [[1,1,1],[1,0,0],[1,1,0],[0,0,1],[1,1,0]],
            '6': [[0,1,1],[1,0,0],[1,1,0],[1,0,1],[0,1,0]], '7': [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
            '8': [[0,1,0],[1,0,1],[0,1,0],[1,0,1],[0,1,0]], '9': [[0,1,0],[1,0,1],[0,1,1],[0,0,1],[1,1,0]],
            ' ': [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        }
        
        pos_x = x
        for char in message:
            if char in font:
                for row in range(5):
                    for col in range(3):
                        if font[char][row][col]:
                            self.pixel(pos_x + col, y + row, c)
                pos_x += 4
        self.update_needed = True

    def set_color(self, color):
        self.color = color
        self.update_needed = True

    def show(self):
        self.update_needed = False

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
                                    img_array[py, px] = self.color
        return Image.fromarray(img_array)


# Streamlit app
def main():
    st.header("LED Matrix Simulator")

    # Initialize or update display with custom settings
    if 'display' not in st.session_state:
        st.session_state.display = LEDMatrix()
        st.session_state.display.text("Hello", 0, 0, 1)  # Display "Hello World" on load
        st.session_state.display.show()  # Update display immediately

    display = st.session_state.display

    # Display at the top
    display_placeholder = st.empty()
    display_placeholder.image(display.get_image(), caption="LED Matrix Display", use_container_width=True)

    # Customization widgets below the display
    col_custom1, col_custom2 = st.columns(2)
    
    with col_custom1:
        color_options = {
            "Red": [255, 0, 0],
            "Yellow": [255, 255, 0],
            "Blue": [0, 0, 255],
            "Orange": [255, 165, 0],
            "Light Green": [144, 238, 144]
        }
        selected_color = st.selectbox("LED Color", list(color_options.keys()), index=0)
        display.set_color(color_options[selected_color])

    with col_custom2:
        width_options = [8, 16, 24, 32, 40, 48, 56, 64]
        selected_width = st.selectbox("Matrix Width", width_options, index=3)  # Default 32
        if selected_width != display.width:
            display = LEDMatrix(width=selected_width, height=8, color=display.color)
            st.session_state.display = display

    # Two columns below customization
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            """
            <style>
            .stTextArea>div>div>textarea {
                font-family: "Consolas", monospace;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        
        code = st.text_area(
            "Enter Python code to control the display and click run button ",
            value='''display.fill(0)
display.text("Hello", 0, 0, 1)
display.show()''',
            height=200,
            key="code_input",
        )
        
        if st.button("▶ Run"):
            try:
                display.fill(0)
                exec(code, {'display': display, 'time': time})
                if not display.update_needed:
                    st.success("Code executed successfully!")
                    display_placeholder.image(display.get_image(), caption="LED Matrix Display", use_container_width=True)
                else:
                    st.warning("Don't forget to add display.show() at the end!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with col2:
        with st.expander("Help", expanded=False):
            st.markdown("""
            - **display.fill(c)**: Fills all LEDs. `c=0` off, `c=1` on.
              - Example: `display.fill(1)` (turns all LEDs on)
            - **display.pixel(x, y, c)**: Sets a single pixel. `x`, `y` are coordinates, `c=0` off, `c=1` on.
              - Example: `display.pixel(0, 0, 1)` (top-left pixel on)
            - **display.hline(x, y, length, c)**: Draws a horizontal line. `length` is number of pixels.
              - Example: `display.hline(2, 1, 5, 1)` (line from (2,1) to (6,1))
            - **display.vline(x, y, length, c)**: Draws a vertical line.
              - Example: `display.vline(1, 2, 4, 1)` (line from (1,2) to (1,5))
            - **display.rectangle(x, y, width, height, c)**: Draws a rectangle outline.
              - Example: `display.rectangle(4, 1, 5, 4, 1)` (rect at (4,1), 5 wide, 4 high)
            - **display.text(message, x, y, c)**: Displays text. Supports A-Z, a-z, 0-9.
              - Example: `display.text("Hello", 10, 0, 1)` (text at (10,0))
            - **display.show()**: Updates the display. Required at the end.
              - Example: `display.show()`
            """)

if __name__ == "__main__":
    main()