This project has been created as part of the 42 curriculum by <Mezahir>

1- *Description*:

    This project is a drone routing simulation system built in Python. The goal is to move aLL drones from a  start zone to a 
    target end zone as efficiently as possible, minimizing the total number of simulation turns.
    the system reads a map file describing a network of interconnected zones, each with specific properties such as capacity constraints,color of zone  and zone type.
    drones navigate this network simultaneously, following computed paths while respecting all traffic rules.



    - **A map parser** : that reads and validates custom map files — it catches every formatting error, invalid zone type, duplicate connection, or missing .

    - **A pathfinding engine** : that uses a Dijkstra-style algorithm with a min-heap priority queue to find the N shortest paths from start to end. At each step,
        the lowest-cost node is expanded first. Blocked zones and already-visited nodes in the current path are skipped to avoid cycles. Each neighbor's cost depends on its zone type,
        the algorithm keeps exploring until it finds the requested number of paths or empty heap , then drones are distributed across them in round-robin to maximize parallel movement and minimize total turns.

    - **A simulation engine** : that runs the fleet turn by turn. Each turn, the engine collects all intended moves first without modifying any state, then applies them all at once.
        this ensures that drones leaving a zone free up space for incoming drones in the same turn.conflicts are prevented using two sreservation dictionaries — zone_reserved and con_reserved 
        that track how many drones have already claimed in this turn. before any move is committed, available capacity is computed as max - current - reserved. if zero, the drone waits until next turn.

    - **A visual interface** :  built with PyGame that renders the zone network as a graph — each zone is displayed as a colored circle, connections are drawn as lines between them
        and drones are represented as small loaded images positioned on their current zone.


2- *Instructions*:

    **installation** :
        - Clone the repository and install all dependencies:
            cd fly-in
            make install
    **Execution** :
        -To run the program directly, navigate to the project root and execute:
            python3 main.py maps/map.txt
        Or using the Makefile:
            make run FILE=maps/your_map.txt
    Other commands
        make debug FILE=maps/your_map.txt : to run in debug mode
        make lint                          : to run flake8 and mypy
        make clean                           : to remove cache files
        make re FILE=maps/your_map.txt      : to clean and re-run

3- *Resources*:

    - https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
    - https://major-prepa.com/python/algorithme-dijkstra/
    - https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle
    - https://www.geeksforgeeks.org/python/introduction-to-pygame/
    - https://www.w3schools.com/python/ref_module_heapq.asp
    - https://www.geeksforgeeks.org/python/heap-queue-or-heapq-in-python/
    - AI was used to better understand the project requirements and how Dijkstra's algorithm works, and guide the overall organization of the project

4- *Additional sections*:

    **Algorithm explanation** :
        The project uses a Dijkstra-style algorithm with a priority queue (heapq) to find multiple shortest paths from the start zone to the goal.
            The heap stores:
            tuple of : (the current cost,the current zone, the path followed so far)
            it starts with: (0, start, [start])
            the algorithm always takes the path with the lowest cost from the heap.
            if the current zone is the goal, the path is saved.
            otherwise, all neighbors are explored

            For each neighbor:
            the  cost is added,a new path is created,and the result is pushed in the heap.
            The process repeats until enough paths are found or heap became empty.

    **Visual representation** :
        The simulation is displayed using PyGame.

        - Zones are represented as colored circles.
        - Connections between zones are displayed as lines.
        - Drones are shown as moving drones on the map.

        The user can:

        - press A to advance the simulation turn by turn,
        - use the arrow keys to move around the map,
        - and close the window to exit the simulation.

    **Example input/output** :
        example Map
            nb_drones: 2

            start_hub: start 0 0 [color=green]
            hub: A 1 0 [color=yellow]
            end_hub: goal 2 0 [color=red]

            connection: start-A
            connection: A-goal
        Example Output
            D1-A
            D1-goal D2-A
            D2-goal
