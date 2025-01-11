def draw_triangle(a, b, c, triangle_type):
    plt.figure(figsize=(5, 5))
    if triangle_type == "none":
        st.write("Unable to draw the triangle.")
        return

    if triangle_type == "equilateral":
        points = np.array([[0, 0], [a, 0], [a/2, (np.sqrt(3)/2) * a]])
    elif triangle_type == "isosceles":
        if a == b:
            points = np.array([[0, 0], [c, 0], [c / 2, np.sqrt(a**2 - (c / 2)**2)]])
        elif b == c:
            points = np.array([[0, 0], [a, 0], [a / 2, np.sqrt(b**2 - (a / 2)**2)]])
        else:
            points = np.array([[0, 0], [b, 0], [b / 2, np.sqrt(c**2 - (b / 2)**2)]])
    elif triangle_type == "right-angle":
        points = np.array([[0, 0], [a, 0], [0, b]])
    else:  # scalene
        points = np.array([[0, 0], [a, 0], [b * np.cos(np.arccos((a**2 + b**2 - c**2) / (2 * a * b))), b * np.sin(np.arccos((a**2 + b**2 - c**2) / (2 * a * b)))]])
    
    plt.plot([points[0][0], points[1][0]], [points[0][1], points[1][1]], 'k-')
    plt.plot([points[1][0], points[2][0]], [points[1][1], points[2][1]], 'k-')
    plt.plot([points[2][0], points[0][0]], [points[2][1], points[0][1]], 'k-')
    plt.fill(points[:, 0], points[:, 1], color="skyblue", alpha=0.5)
    plt.axis("equal")
    plt.axis("off")
    plt.show()
    st.pyplot(plt)
