**Group 1**

* 32\. Heng Hour (Leader)  
* 33\. Heng Pengly  
* 14\. Yos Sak  
* 30.Han KimHeng  
* 26\. Sem VatanakPanha

**Topic: Smart Building Mapping and Navigation System for RUPP Campus 1 Using Graphs, Trees, and Hash Tables**

Understand Problem: 

- **Core Goal:** Build a system that allows users to search for campus buildings/facilities and provides the **shortest path** between any two locations.  
- **New Student Confusion:** RUPP has a huge campus with many spread-out locations like Building A, Building B, Building T, the STEM Building, NICC, CKCC. New students and visitors easily get lost trying to find specific rooms, science labs, or offices.  
- **User Needs:** Quick information lookup (e.g., "Where is the register office?") and navigational guidance.  
- **No Quick Information:** Paper maps on the school walls do not show helpful details like office hours, building descriptions, or room availability.  
    
  Design System:   
- **Graph (Navigation Layer):**  
  * **Model:** Use vertices/nodes to represent buildings/landmarks and edges to represent paths or roads.  
  * **Functionality:** Implement **Dijkstra’s Algorithm** to calculate and display the shortest path from a starting point to a destination vertex. Use an adjacency list for efficient pathfinding on a sparse campus map.

- **Hash Table (Information Layer):**  
  * **Model:** Store campus facility data (like building names).  
  * **Functionality:** Use the **building name as the key** and the building object as the value to provide *O*(1) search time for details.

- **Tree (Categorization Layer):**  
  * **Model:** Use a hierarchical structure (like a BST or AVL Tree) to categorize locations by type (e.g., Academic Buildings → Labs, Lecture Halls; Services → Dining, Admin).  
  * **Functionality:** Allows users to filter their search through a **decision-making logic** tree (e.g., search for all "Library" types).


  


  


  


  


  


  

| \#\# System Overview (Teacher's Diagram)                             ┌─────────┐                             │  RUPP   │                             │ Campus  │                             └────┬────┘                                  │                                  ▼                         ┌─────────────────┐                         │ Data Collection │                         │  (Buildings,    │                         │   Distances,    │                         │   Coords)       │                         └────────┬────────┘                                  │               ┌──────────────────┼──────────────────┐               │                  │                  │               ▼                  ▼                  ▼ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ │  GRAPH (Navigation) │ │  TREE (Filtering)   │ │  HASH (Retrieval)   │ │  ─────────────────  │ │  ─────────────────  │ │  ─────────────────  │ │                     │ │                     │ │                     │ │ PURPOSE:            │ │ PURPOSE:            │ │ PURPOSE:            │ │ Model campus as     │ │ Organize buildings  │ │ Store building info │ │ network of paths    │ │ by category for     │ │ for instant access  │ │ for route finding   │ │ filtered browsing   │ │ by name             │ │                     │ │                     │ │                     │ │ USES:               │ │ USES:               │ │ USES:               │ │ • Dijkstra's algo   │ │ • BST/AVL tree      │ │ • Hash table        │ │   (shortest path)   │ │   (sorted access)   │ │   (chaining)        │ │ • BFS/DFS           │ │ • Category nodes    │ │ • O(1) average      │ │   (exploration)     │ │   (grouping)        │ │   lookup            │ │                     │ │                     │ │                     │ │ EXAMPLES:           │ │ EXAMPLES:           │ │ EXAMPLES:           │ │ → "STEM to Library" │ │ → "Show Academic"   │ │ → "Find CJCC info"  │ │ → finds shortest    │ │ → lists Academic    │ │ → returns coords,   │ │   weighted path     │ │   buildings         │ │   desriptions       │ └─────────┬───────────┘ └─────────┬───────────┘ └─────────┬───────────┘           │                       │                       │           └───────────────────────┼───────────────────────┘                                   │                                   ▼                         ┌───────────────┐                         │   EVALUATOR   │                         │  (Integrate)  │                         │               │                         │ Combines all  │                         │ 3 DSA layers  │                         │ into unified  │                         │    system     │                         └───────┬───────┘                                 │                                 ▼                         ┌───────────────┐                         │  UI \+ Testing │                         │  (Campus Map) │                         │               │                         │ User selects  │                         │ start & end   │                         │ → see route   │                         └───────────────┘ |
| :---- |




Assign Roles

- **Heng Hour (Team Leader):** Responsible for overall project management, **system integration** (merging the Graph, Hash, and Tree modules), and finalizing the presentation slides.  
- **Heng Pengly (Graph Specialist):** Responsible for building the campus map model and implementing **Dijkstra's shortest path algorithm**.  
- **Yos Sak (Hash Table Specialist):** Responsible for building the **directory system**, implementing the hash function, and handling data storage for all building information.  
- **Sem Vatanakpanha (Tree Specialist):** Responsible for the **location categorization logic** using a Tree structure to allow for filtered searches.  
- **Kimheng:(UI/Tester):** Responsible for developing the **User Interface** (CLI or GUI), handling user inputs, and performing functionality testing to ensure all parts work together.

        Code Progression :  15 %

