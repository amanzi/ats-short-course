library(visNetwork)
library(htmlwidgets)

# Create initial nodes data with specific labels, colors, and hover text
nodes <- data.frame(id = 1:11,
                    label = c("MPC::flow coupler", "PK::flow", "PK::overland flow", 
                    "MPC::flow and transport", "MPC::transport coupler", "PK::subsurface transport",
                     "PK::surface transport", "MPC::reactive transport coupler", "MPC::chemistry coupler",
                     "PK::chemistry surface", "PK::chemistry subsurface"),  # Set node labels
                    shape = "box",  # Rectangle shape for round appearance
                    font = list(color = "black"),
                    title = c("Strong coupling (PK Type: coupled water)",
                              "Richards Equation (PK Type: richards flow)",    
                              "Diffusive Wave Equation (PK Type: overland flow, pressure basis)",
                              "Weak coupling (PK Type: subcycling MPC)",
                              "Weak coupling (PK Type: surface subsurface transport)",
                              "Advection Diffusion Equation (PK Type: transport ATS)",    
                              "Advection Diffusion Equation (PK Type: transport ATS)",
                              "Weak coupling (PK Type: subcycling MPC)",
                              "Weak coupling (PK Type: weak MPC)",
                              "Chemistry Alquimia (PK Type: chemistry alquimia)",
                              "Chemistry Alquimia (PK Type: chemistry alquimia)"
                    ),
                    stringsAsFactors = FALSE)

# Set color background separately to ensure the correct initial color for each node
nodes$color <- list(list(background = "coral"),  
                    list(background = "lightblue"),  
                    list(background = "lightblue"),
                    list(background = "white"),
                    list(background = "coral"),  
                    list(background = "lightblue"),  
                    list(background = "lightblue"),
                    list(background = "white"),
                    list(background = "coral"),
                    list(background = "lightblue"),
                    list(background = "lightblue")                    
                    )  

# Create edges to connect the nodes
edges <- data.frame(from = c(1, 1, 5, 5, 9, 9, 8, 8, 4, 4), to = c(2, 3, 6, 7, 10, 11, 5, 9, 1, 8))  # Connect "MPC::flow coupler" to "PK::flow" and "PK::overland flow"

# Define custom positions for the nodes (flip y-positions so MPC is above)
nodes$x <- c(0, -100, 100, 225, 360, 240, 500, 600, 850, 750, 1000)  # Set the x positions (center, left, right)
nodes$y <- c(-100, 0, 0, -200, 0, 100, 100, -100, 0, 100, 100)  # Set the y positions (MPC at the top, PK nodes below)

# Create the interactive network with manipulation enabled
network <- visNetwork(nodes, edges) %>%
  visOptions(manipulation = TRUE) %>%  # Enable the manipulation interface for editing
  visNodes(shape = "box", font = list(size = 20)) %>%  # Set font size and node shape
  visPhysics(enabled = FALSE) %>%  # Disable physics for static positioning
  visLayout(randomSeed = 1234) %>%  # Ensure a consistent layout
  visEvents(doubleClick = "function(nodes) {
    // When a node is double-clicked, prompt the user for a color
    var nodeId = nodes.nodes[0];
    var newColor = prompt('Enter a color (e.g., lightblue, red, etc.):', 'lightblue');
    if (newColor) {
      var network = this;
      // Update the selected node's background color
      network.body.data.nodes.update({id: nodeId, color: {background: newColor}});
    }
  }")

# Save the network to an HTML file
saveWidget(network, file = "../dependency_transport_reactive.html", selfcontained = FALSE)
