from PIL import Image, ImageDraw
from collections import deque

# Function to convert image to maze represented as a 2D array
def image_to_maze(image_path):
    # Open the image
    img = Image.open(image_path)
    # Convert the image to grayscale
    img = img.convert('L')
    # Convert the image to a binary array (0 for paths, 1 for walls)
    maze = [[1 if img.getpixel((j, i)) > 128 else 0 for j in range(img.width)] for i in range(img.height)]
    return maze

# Function to solve the maze using BFS
def solve_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    # Define possible moves: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Visited array to keep track of visited cells
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    visited[start[0]][start[1]] = True

    # Queue for BFS
    queue = deque([(start, [])])

    while queue:
        (row, col), path = queue.popleft()
        if (row, col) == end:
            return path + [(row, col)]
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 0 and not visited[new_row][new_col]:
                visited[new_row][new_col] = True
                queue.append(((new_row, new_col), path + [(row, col)]))
    return None

# Function to draw the maze and solution path
def draw_maze(maze, solution):
    cell_size = 20
    maze_image = Image.new('RGB', (len(maze[0]) * cell_size, len(maze) * cell_size), color='white')
    draw = ImageDraw.Draw(maze_image)
    
    # Draw maze walls
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 1:
                draw.rectangle([col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size], fill='black')

    # Draw solution path
    if solution:
        for i in range(len(solution) - 1):
            draw.line([(solution[i][1] * cell_size + cell_size // 2, solution[i][0] * cell_size + cell_size // 2),
                       (solution[i + 1][1] * cell_size + cell_size // 2, solution[i + 1][0] * cell_size + cell_size // 2)],
                      fill='green', width=2)
    
    maze_image.show()

# Main function
def main():
    # Input image representing the maze
    maze_image_path = input("Enter the path to the maze image: ")
    # Convert image to maze
    maze = image_to_maze(maze_image_path)
    
    # Find start and end points
    start = tuple(map(int, input("Enter the start point (row col): ").split()))
    end = tuple(map(int, input("Enter the end point (row col): ").split()))

    # Solve the maze
    solution = solve_maze(maze, start, end)
    if solution:
        print("Solution path:", solution)
        # Visualize the maze and solution path
        draw_maze(maze, solution)
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()
