library(visNetwork)
library(htmlwidgets)

# # Create nodes data with round rectangle shape and light blue background color for both nodes
# nodes <- data.frame(id = 1:2,
#                     label = c("flow", "overland flow"),  # Set node labels
#                     shape = "box",  # Rectangle shape for round appearance
#                     font = list(color = "black"),
#                     stringsAsFactors = FALSE)

# # Set color background separately to ensure both nodes have light blue
# nodes$color <- list(list(background = "lightblue"), list(background = "lightblue"))

# # Create an empty edges data frame (no connections initially)
# edges <- data.frame(from = integer(0), to = integer(0))

# # Create the interactive network
# network <- visNetwork(nodes, edges) %>%
#   visOptions(manipulation = TRUE) %>%  # Enable the manipulation interface for editing
#   visNodes(shape = "box", font = list(size = 20)) %>%  # Set font size
#   visPhysics(enabled = FALSE) %>%  # Disable physics for static positioning
#   visLayout(randomSeed = 1234)  # Ensure a consistent layout

# # Save the network to an HTML file without self-contained resources
# saveWidget(network, file = "dependency.html", selfcontained = FALSE)

# ------------------------------------------------------------------------------
# # Create initial nodes data with light blue background color for both nodes
# nodes <- data.frame(id = 1:2,
#                     label = c("PK::flow", "PK::overland flow"),  # Set node labels
#                     shape = "box",  # Rectangle shape for round appearance
#                     font = list(color = "black"),
#                     stringsAsFactors = FALSE)

# # Set color background separately to ensure both nodes have light blue
# nodes$color <- list(list(background = "lightblue"), list(background = "lightblue"))

# # Create an empty edges data frame (no connections initially)
# edges <- data.frame(from = integer(0), to = integer(0))

# # Create the interactive network with manipulation enabled
# network <- visNetwork(nodes, edges) %>%
#   visOptions(manipulation = TRUE) %>%  # Enable the manipulation interface for editing
#   visNodes(shape = "box", font = list(size = 20)) %>%  # Set font size and node shape
#   visPhysics(enabled = FALSE) %>%  # Disable physics for static positioning
#   visLayout(randomSeed = 1234) %>%  # Ensure a consistent layout
#   visEvents(doubleClick = "function(nodes) {
#     // When a node is double-clicked, prompt the user for a color
#     var nodeId = nodes.nodes[0];
#     var newColor = prompt('Enter a color (e.g., lightblue, red, etc.):', 'lightblue');
#     if (newColor) {
#       var network = this;
#       // Update the selected node's background color
#       network.body.data.nodes.update({id: nodeId, color: {background: newColor}});
#     }
#   }")

# # Save the network to an HTML file
# saveWidget(network, file = "../dependency.html", selfcontained = FALSE)

# ------------------------------------------------------------------------------
library(visNetwork)
library(htmlwidgets)

# Create initial nodes data with specific labels, colors, and hover text
nodes <- data.frame(id = 1:3,
                    label = c("MPC::flow coupler", "PK::flow", "PK::overland flow"),  # Set node labels
                    shape = "box",  # Rectangle shape for round appearance
                    font = list(color = "black"),
                    title = c("Strong coupling (PK Type: coupled water)",  # Hover text for MPC
                              "Richards Equation (PK Type: richards flow)",      # Hover text for PK::flow
                              "Diffusive Wave Equation (PK Type: overland flow, pressure basis)"),  # Hover text for PK::overland flow
                    stringsAsFactors = FALSE)

# Set color background separately to ensure the correct initial color for each node
nodes$color <- list(list(background = "coral"),  # "MPC::flow coupler" in coral
                    list(background = "lightblue"),  # "PK::flow" in lightblue
                    list(background = "lightblue"))  # "PK::overland flow" in lightblue

# Create edges to connect the nodes
edges <- data.frame(from = c(1, 1), to = c(2, 3))  # Connect "MPC::flow coupler" to "PK::flow" and "PK::overland flow"

# Define custom positions for the nodes (flip y-positions so MPC is above)
nodes$x <- c(0, -100, 100)  # Set the x positions (center, left, right)
nodes$y <- c(-100, 0, 0)  # Set the y positions (MPC at the top, PK nodes below)

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
saveWidget(network, file = "../dependency_graph.html", selfcontained = FALSE)
