$(document).ready(function() {
	
	$.getJSON("/neighborsinfo",function(data) {
		var users = data['user_list']
		var neighbors = data['neighbors_list']
		for (user_index in users) {
			$("#neighbors").append(users[user_index] +"<ol>")
			for (neighbor in neighbors[user_index]) {
				$("#neighbors").append("<li>"+neighbors[user_index][neighbor] + "</li>")
			}
			$("#neighbors").append("</ol>")
		}

	})

})