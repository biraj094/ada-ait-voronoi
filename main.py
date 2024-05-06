import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from delaunay_naive import Graph, Point
import matplotlib.tri as tri
import delauney_bowyer as db
import pickle
from scipy.spatial import Voronoi, voronoi_plot_2d


def colorizeEdges(edges):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]
    random.shuffle(colors)
    edge_colors = {}
    for idx, edge in enumerate(edges):
        edge_colors[edge.edgeToStr()] = colors[idx % len(colors)]
    return edge_colors

def colorizeTriangles(triangles):
    colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]
    random.shuffle(colors)
    triangle_colors = {}
    for idx, triangle in enumerate(triangles):
        triangle_colors[str(triangle)] = colors[idx % len(colors)]
    return triangle_colors

def delaunay_triangulation():
    st.title("Exploring Delaunay Triangulation with Naive Implementation")
    st.write("Explore the Delaunay triangulation process through a naive implementation. Unlike the Bowyer-Watson algorithm, this approach exhaustively checks all possible triangles, lacking the efficiency of dynamic updates. Without interactivity due to resource-intensive computations, users observe the complete recalculation of the triangulation for each point insertion. Despite its simplicity, this method demonstrates the computational overhead of brute-force approaches, highlighting the need for more efficient algorithms like Bowyer-Watson. By visualizing the exhaustive process, users gain insight into the challenges of computational geometry and appreciate the performance gains offered by more sophisticated algorithms.")
    graph = Graph()
    random.seed(time.time())

    st.write("Adding 100  points...")
    for x in range(0, 70):
        while graph.addPoint(Point(random.randint(50, 974), random.randint(50, 718))) is False:
            st.write("Couldn't add point")

    st.write("Generating Delaunay Mesh...")
    graph.generateDelaunayMesh()

    # Colorize the edges using the colorizeEdges function
    edge_colors = colorizeEdges(graph._edges)
    # Colorize the triangles using the colorizeTriangles function
    triangle_colors = colorizeTriangles(graph._triangles)

    # Create plot
    fig, ax = plt.subplots()
    for p in graph._points:
        ax.plot(p.pos()[0], p.pos()[1], 'o', color='white', markersize=3)
    for e in graph._edges:
        # Update plotting code to use edge colors
        ax.plot([e._a.pos()[0], e._b.pos()[0]], [e._a.pos()[1], e._b.pos()[1]], color=edge_colors[e.edgeToStr()])
    for t in graph._triangles:
        # Plot triangles and fill with corresponding colors
        ax.fill([t._a.pos()[0], t._b.pos()[0], t._c.pos()[0]], [t._a.pos()[1], t._b.pos()[1], t._c.pos()[1]], color=triangle_colors[str(t)], alpha=0.5)

    # Customize plot
    ax.set_xlim(0, 1024)
    ax.set_ylim(0, 768)
    ax.set_facecolor('black')

    # Display plot in Streamlit
    st.pyplot(fig)

import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import random

def bowyer_watson():
    st.title("Exploring Delaunay Triangulation with Bowyer-Watson Algorithm")
    st.write("Discover the Bowyer-Watson algorithm's efficiency in constructing Delaunay triangulations. This visualization showcases the algorithm's dynamic insertion of points while preserving the Delaunay property. Similar to Voronoi diagram generation, the Python implementation offers efficiency over naive approaches by updating the triangulation dynamically. Users can interactively adjust parameters, like the number of points, witnessing the triangulation's evolution. This hands-on exploration enhances understanding of Delaunay triangulation's geometric intricacies, demonstrating its significance in computational geometry.")
    WIDTH = int(100)
    HEIGHT = int(100)
    # n = 100  # n should be greater than 2
    # n = st.number_input("Number of Points", min_value=50, step=1, value=200) 
    st.write("<span style='color:red'>Number of Points (Interactive)</span>", unsafe_allow_html=True)
    n = st.number_input("", min_value=50, step=1, value=200, format="%d", key="number_input", help="Enter the number of points")

    xs = [random.randint(1, WIDTH - 1) for x in range(n)]
    ys = [random.randint(1, HEIGHT - 1) for y in range(n)]
    zs = [0 for z in range(n)]

    DT = db.Delaunay_Triangulation(WIDTH, HEIGHT)
    for x, y in zip(xs, ys):
        DT.AddPoint(db.Point(x, y))

    # Remove the super triangle on the outside
    DT.Remove_Super_Triangles()
    XS, YS, TS = DT.export()
    triang = tri.Triangulation(xs, ys)

    # Plot the triangulation.
    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.set_aspect('equal')
    
    # Define 10 different colors
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']
    
    # Plot triangles with different colors
    for i, t in enumerate(triang.triangles):
        ax.fill([xs[t[0]], xs[t[1]], xs[t[2]]], [ys[t[0]], ys[t[1]], ys[t[2]]], color=colors[i % len(colors)], alpha=0.5)
    
    # Plot edges with different colors
    for edge in triang.edges:
        ax.plot([xs[edge[0]], xs[edge[1]]], [ys[edge[0]], ys[edge[1]]], color=colors[(edge[0] + edge[1]) % len(colors)])
    
    ax.set_title('Bowyer-Watson implementation of Delaunay triangulation')

    # Convert plot to an image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    # Convert buffer to image array
    img_array = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    # Reshape the image array
    img = plt.imread(io.BytesIO(img_array))
    st.image(img, use_column_width=True)
    plt.close(fig)  

def example():
    with open("./lat_long_list", "rb") as fp:  
        my_list = pickle.load(fp)
    points = [(lng, lat) for lat, lng in my_list[:200]]
    vor = Voronoi(points)
    fig, ax = plt.subplots(figsize=(10, 8))
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='red', line_width=2, line_alpha=0.6, point_size=6)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.spines['bottom'].set_color('gray')
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_color('gray')
    ax.spines['left'].set_linewidth(0.5)
    ax.tick_params(axis='both', colors='gray')
    ax.scatter([lng for lat, lng in points], [lat for lat, lng in points], color='blue', label='Hospitals')
    
    # Add legend for hospitals
    ax.legend(loc='upper right', fontsize=12)
    ax.set_title('Voronoi Diagram of Hospitals in Bangkok', color='black', fontsize=16)
    st.pyplot(fig)

def usecase_example():
    st.title('Optimizing Hospital Placement in Bangkok with Voronoi Diagrams')
    st.write('In the bustling metropolis of Bangkok, ensuring efficient access to healthcare facilities is paramount for public welfare. To address this challenge, advanced spatial analysis techniques like Voronoi diagrams emerge as invaluable tools.')

    st.write('**Contextual Overview:**')
    st.write('Bangkok, Thailand\'s capital, is a sprawling urban landscape teeming with millions of residents and visitors. As with any major city, access to healthcare services is critical for maintaining public health and safety. However, the strategic placement of hospitals is complex, requiring considerations of population density, traffic patterns, and geographic features.')

    st.write('**Voronoi Diagrams in Action:**')
    st.write('To visualize and analyze hospital distribution in Bangkok, we employ Voronoi diagrams. The provided Python code utilizes a sample of hospital coordinates (latitudes and longitudes) to generate a Voronoi diagram, dividing Bangkok into distinct regions based on the proximity to these hospitals.')
    # Generating Voronoi diagram
    example()
    st.write('**Benefits of Voronoi Diagrams:**')
    st.write('1. **Optimized Resource Allocation:** Voronoi diagrams help identify areas with inadequate access to healthcare facilities, enabling policymakers to strategically allocate resources to underserved regions.')
    st.write('2. **Spatial Analysis:** By visually representing spatial relationships, Voronoi diagrams facilitate informed decision-making regarding hospital placement, considering factors like population distribution and travel time.')
    st.write('3. **Efficiency Enhancement:** Through the clear delineation of catchment areas, Voronoi diagrams aid in streamlining emergency response systems and optimizing ambulance dispatch routes.')
    st.write('4. **Cost Reduction:** By minimizing redundancy and ensuring equitable distribution, Voronoi diagrams contribute to cost-effective healthcare delivery, maximizing the impact of limited resources.')

    


def main():
    st.sidebar.title("Menu")
    algorithm = st.sidebar.selectbox("Please choose menu items", ["Home","Naive Delaunay Triangulation", "Bowyer-Watson","Real world usecase"])

    if algorithm == "Home":
        st.title("Voronoi using naive and Bowyer-Watson Implementation")
        st.write("Delaunay triangulation is a method for creating a triangulated representation of a set of points in a plane such that no point lies inside the circumcircle of any triangle in the triangulation.")
        st.write("Naive Delaunay Algorithm")
        st.write("The naive approach to Delaunay triangulation involves checking every possible triangle formed by the given points and verifying if it satisfies the Delaunay condition. This method has a time complexity of O(n^4), where n is the number of input points, making it inefficient for large datasets.")
        st.write("Bowyer-Watson")
        st.write("The Bowyer-Watson algorithm is a more efficient approach to Delaunay triangulation. It starts with a super-triangle that encloses all the input points and iteratively adds points one by one while maintaining the Delaunay condition. The time complexity of the Bowyer-Watson algorithm is O(n^2 log n), where n is the number of input points. This algorithm significantly reduces the time complexity compared to the naive approach, making it more suitable for practical applications, especially with larger datasets.")
        st.write("<u><b>Submitted by:</b> Biraj Koirala (st124371) and Parun Ngamcharoen (st124026)</u>", unsafe_allow_html=True)
        st.write("<u><b>Submitted to:</b> Prof. Chantri Polprasert</u>", unsafe_allow_html=True)
    elif algorithm == "Bowyer-Watson":
        bowyer_watson()
    elif algorithm == "Naive Delaunay Triangulation":
        delaunay_triangulation()
    elif algorithm == "Real world usecase":
        usecase_example()


        

if __name__ == "__main__":
    main()
